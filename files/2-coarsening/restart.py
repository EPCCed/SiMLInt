"""

Downsample a restart file.

"""

import os
import glob

from boututils.datafile import DataFile
from boututils.boutarray import BoutArray

import numpy as np

def samplePeriodic3DField(var, data, newNx, newNy, newNz, mxg, ratex, ratez, mute):

    if not (mute):
        print(
            "    Resizing "
            + var
            + " to (nx,ny,nz) = ({},{},{})".format(newNx, newNy, newNz)
        )
    newData = np.zeros((newNx, newNy, newNz))
    # sample the data without ghost points
    newData[mxg:-mxg,:,:] = data[mxg+int(ratex/2)-1:-mxg:ratex,:,int(ratez/2)-1::ratez]
    # add the periodic boundary at the start ghost points
    newData[:mxg,:,:] = newData[-2*mxg:-mxg,:,:]
    # add the periodic boundary at the end ghost points
    newData[-mxg:,:,:] = newData[mxg:2*mxg,:,:]

    return var, newData

def resize(
    newNx,
    newNy,
    newNz,
    mxg=2,
    myg=2,
    path="data",
    output="./",
    informat="nc",
    outformat=None,
    mute=False,
):
    """Increase/decrease the number of points in restart files.

    NOTE: Can't overwrite
    WARNING: Currently only implemented with uniform BOUT++ grid

    Parameters
    ----------
    newNx, newNy, newNz : int
        nx, ny, nz for the new file (including ghost points)
    mxg, myg : int, optional
        Number of ghost points in x, y (default: 2)
    path : str, optional
        Input path to data files
    output : str, optional
        Path to write new files
    informat : str, optional
        File extension of input
    outformat : {None, str}, optional
        File extension of output (default: use the same as `informat`)
    mute : bool, optional
        Whether or not output should be printed from this function

    Returns
    -------
    return : bool
        True on success, else False

    """

    if method is None:
        # Make sure the method is set
        method = "linear"

    if outformat is None:
        outformat = informat

    if path == output:
        print("ERROR: Can't overwrite restart files when expanding")
        return False

    def is_pow2(x):
        """Returns true if x is a power of 2"""
        return (x > 0) and ((x & (x - 1)) == 0)

    if not is_pow2(newNz):
        print("ERROR: New Z size {} must be a power of 2".format(newNz))
        return False

    file_list = glob.glob(os.path.join(path, "BOUT.restart.*." + informat))
    file_list.sort()
    nfiles = len(file_list)

    if nfiles == 0:
        print("ERROR: No data found in {}".format(path))
        return False

    if not (mute):
        print("Number of files found: " + str(nfiles))

    for f in file_list:
        new_f = os.path.join(output, f.split("/")[-1])
        if not (mute):
            print("Changing {} => {}".format(f, new_f))

        # Open the restart file in read mode and create the new file
        with DataFile(f) as old, DataFile(new_f, write=True, create=True) as new:

            # Find the dimension
            for var in old.list():
                # Read the data
                data = old.read(var)
                # Find 3D variables
                if old.ndims(var) == 3:
                    break

            nx, ny, nz = data.shape
            
            # Loop over the variables in the old file
            for var in old.list():
                # Read the data
                data = old.read(var)
                attributes = old.attributes(var)

                # Find 3D variables
                if old.ndims(var) == 3:

                    var, newData = samplePeriodic3DField(
                        var, data,
                        newNx, newNy, newNz, mxg,
                        int((nx-2*mxg)/(newNx-2*mxg)),
                        int(nz/newNz),
                        mute)

                else:
                    if not (mute):
                        print("    Copying " + var)
                    newData = data.copy()
                    if not (mute):
                        print("Writing " + var)
                    new.write(var, newData)

                newData = BoutArray(newData, attributes=attributes)

                if not (mute):
                    print("Writing " + var)
                new.write(var, newData)

    return True

def write_resize(
    step,
    dataset,
    new_nx,
    newNy,
    newNz,
    input_file,
    output_file,
    mxg=2,
    myg=2,
    mute=False,
):

    orig_data = dataset.isel(t=step)
    time_value = dataset['t'].values[step]

    # Open the restart file in read mode and create the new file
    with DataFile(input_file) as old, DataFile(output_file, write=True, create=True) as new:

        initial_step = old.read('hist_hi').item()
        # Loop over the variables in the old file
        for var in old.list():
            attributes = old.attributes(var)

            # Find 3D variables
            if old.ndims(var) == 3:

                data = orig_data[var].to_numpy()
                nx, ny, nz = data.shape

                var, newData = samplePeriodic3DField(
                    var, data,
                    new_nx, newNy, newNz, mxg,
                    int((nx-2*mxg)/(new_nx-2*mxg)),
                    int(nz/newNz),
                    mute)

            else:
                # Read the data
                data = old.read(var)
                if not (mute):
                    print("    Copying " + var)
                newData = data.copy()
                if not (mute):
                    print("Writing " + var)
                # new.write(var, newData)

            if attributes['bout_type'] is None and data.dtype == 'S1':
                newData.attributes['bout_type'] = 'string'
            newData = BoutArray(newData, attributes=attributes)

            if not (mute):
                print("Writing " + var)
            new.write(var, newData)

        # write the correct timestep for this data
        new.write('t_array', BoutArray(time_value))
        new.write('tt', BoutArray(time_value))
        new.write('hist_hi', BoutArray(initial_step+step))
