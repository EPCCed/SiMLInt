#include <bout/derivs.hxx>
#include <bout/invert_laplace.hxx>
#include <bout/physicsmodel.hxx>
#include <bout/smoothing.hxx>

#include <client.h>

class HW : public PhysicsModel {
private:
  Field3D n, vort; // Evolving density and vorticity
  Field3D phi;     // Electrostatic potential

  // Model parameters
  BoutReal alpha;     // Adiabaticity (~conductivity)
  BoutReal kappa;     // Density gradient drive
  BoutReal Dvort, Dn; // Diffusion
  bool modified;      // Modified H-W equations?
  bool addCorrection;

  // Poisson brackets: b0 x Grad(f) dot Grad(g) / B = [f, g]
  // Method to use: BRACKET_ARAKAWA, BRACKET_STD or BRACKET_SIMPLE
  BRACKET_METHOD bm; // Bracket method for advection terms

  std::unique_ptr<Laplacian> phiSolver; // Laplacian solver for vort -> phi

  SmartRedis::Client *client;

protected:
  int init(bool UNUSED(restart)) {

    auto& options = Options::root()["hw"];
    alpha = options["alpha"].withDefault(1.0);
    kappa = options["kappa"].withDefault(0.1);
    Dvort = options["Dvort"].withDefault(1e-2);
    Dn = options["Dn"].withDefault(1e-2);

    modified = options["modified"].withDefault(false);

    SOLVE_FOR(n, vort);
    SAVE_REPEAT(phi);

    // Split into convective and diffusive parts
    setSplitOperator();

    phiSolver = Laplacian::create();
    phi = 0.; // Starting phi

    // Use default flags

    // Choose method to use for Poisson bracket advection terms
    switch (options["bracket"].withDefault(0)) {
    case 0: {
      bm = BRACKET_STD;
      output << "\tBrackets: default differencing\n";
      break;
    }
    case 1: {
      bm = BRACKET_SIMPLE;
      output << "\tBrackets: simplified operator\n";
      break;
    }
    case 2: {
      bm = BRACKET_ARAKAWA;
      output << "\tBrackets: Arakawa scheme\n";
      break;
    }
    case 3: {
      bm = BRACKET_CTU;
      output << "\tBrackets: Corner Transport Upwind method\n";
      break;
    }
    default:
      output << "ERROR: Invalid choice of bracket method. Must be 0 - 3\n";
      return 1;
    }

    // initialise smartredis client
    bool cluster_mode = false; // Set to false if not using a clustered database
    client = new SmartRedis::Client(cluster_mode, __FILE__);

    // no correction in the initialisation phase
    addCorrection = false;

    return 0;
  }

  int outputMonitor(BoutReal simtime, int iter, int nout) {
    // output << "iteration  =     " << iter << std::endl;
    if (iter >= 0) {
      // output << "setting correction to true" << std::endl;
      addCorrection = true;
    }
    return 0;
  }

  int convective(BoutReal UNUSED(time)) {
    // Non-stiff, convective part of the problem

    if (addCorrection) {

      size_t nx = mesh->xend - mesh->xstart + 1;
      size_t LocalNz = mesh->LocalNz;
      size_t n_values = 1 * nx * LocalNz * 1;
      std::vector<size_t> dims = {1, nx, LocalNz, 1};
      std::vector<float> input_vort(n_values, 0);
      std::vector<float> input_n(n_values, 0);

      for (int i = mesh->xstart, c=0; i <= mesh->xend; ++i) {
        for (int j = mesh->ystart; j <= mesh->yend; ++j) {
          for (int k = 0; k < LocalNz; ++k) {
            input_vort[c] = (float) vort(i,j,k);
            input_n[c] = (float) n(i,j,k);
            c++;
          }
        }
      }

      std::string inKeyVort = "input_vort";
      std::string outKeyVort = "output_vort";
      std::string inKeyN = "input_n";
      std::string outKeyN = "output_n";

      // put input tensor
      client->put_tensor(inKeyVort, input_vort.data(), dims,
                         SRTensorTypeFloat, SRMemLayoutContiguous);
      client->put_tensor(inKeyN, input_n.data(), dims,
                         SRTensorTypeFloat, SRMemLayoutContiguous);

      // run model
      client->run_model("hw_model_vort", {inKeyVort}, {outKeyVort});
      client->run_model("hw_model_n", {inKeyN}, {outKeyN});

      // unpack output tensor
      std::vector<double> correctionVort(n_values, 0);
      std::vector<double> correctionN(n_values, 0);
      client->unpack_tensor(outKeyVort, correctionVort.data(), {n_values},
                            SRTensorTypeFloat, SRMemLayoutContiguous);
      client->unpack_tensor(outKeyN, correctionN.data(), {n_values},
                            SRTensorTypeFloat, SRMemLayoutContiguous);


      for (int i = mesh->xstart, c=0; i <= mesh->xend; ++i) {
        for (int j = mesh->ystart; j <= mesh->yend; ++j) {
          for (int k = 0; k < LocalNz; ++k) {
            vort(i,j,k) = vort(i,j,k) + (double) correctionVort[c];
            n(i,j,k) = n(i,j,k) + (double) correctionN[c];
            c++;
          }
        }
      }

      addCorrection = false;
      // output << "setting correction to false" << std::endl;
    }

    // Solve for potential
    phi = phiSolver->solve(vort, phi);

    // Communicate variables
    mesh->communicate(n, vort, phi);

    // Modified H-W equations, with zonal component subtracted from resistive coupling term
    Field3D nonzonal_n = n;
    Field3D nonzonal_phi = phi;
    if (modified) {
      // Subtract average in Y and Z
      nonzonal_n -= averageY(DC(n));
      nonzonal_phi -= averageY(DC(phi));
    }

    ddt(n) =
        -bracket(phi, n, bm) + alpha * (nonzonal_phi - nonzonal_n) - kappa * DDZ(phi);

    ddt(vort) = -bracket(phi, vort, bm) + alpha * (nonzonal_phi - nonzonal_n);

    return 0;
  }

  int diffusive(BoutReal UNUSED(time)) {
    // Diffusive terms
    mesh->communicate(n, vort);
    ddt(n) = +Dn * Delp2(n);
    ddt(vort) = +Dvort * Delp2(vort);
    return 0;
  }
};

// Define a main() function
BOUTMAIN(HW);
