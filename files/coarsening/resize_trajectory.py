import os
from pathlib import Path
import sys

from xbout import open_boutdataset

import restart

ID_TRAJ    = sys.argv[1]
INPUT_PATH = f'/scratch/space1/d175/data/training/ground-truth/trajectory_{ID_TRAJ}'
BASE_PATH  = Path(sys.argv[2])
num_timesteps = 1001

myg = 0
mxg = 2 # guard cells on each end
new_nx = 256 + 2*mxg
new_ny = 1
new_nz = 256

print(f'Opening dataset at {INPUT_PATH}', flush=True)
ds = open_boutdataset(
        datapath=os.path.join(INPUT_PATH, "BOUT.dmp.*.nc"),
        keep_xboundaries=True) # include guard cells

# save the first timestep as the template file
TEMPLATE_PATH = BASE_PATH / '0' / 'fine'
TEMPLATE_FILE = TEMPLATE_PATH / 'BOUT.restart.0.nc'

os.makedirs(TEMPLATE_PATH, exist_ok=True)
ds.bout.to_restart(
        savepath=TEMPLATE_PATH,
        tind=0, # first trajectory timepoint
        nxpe=1, # one restart file/one rank
        prefix="BOUT.restart",
        overwrite=False)

for i in range(num_timesteps):
    OUTPUT_FILE = BASE_PATH / str(i) / 'coarse' / 'BOUT.restart.0.nc'
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # print(f'resizing timestep {i}, template {TEMPLATE_FILE}, output {OUTPUT_FILE}')
    restart.write_resize(
        i, ds,
        new_nx, new_ny, new_nz,
        mxg=mxg,
        input_file=str(TEMPLATE_FILE),
        output_file=str(OUTPUT_FILE),
        mute=True,
    )

ds.close()
