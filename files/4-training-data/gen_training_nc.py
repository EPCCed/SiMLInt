#!/usr/env/python
# Script to generate training .nc files from BOUT coarse sim files
# Based on traj_netcdf.ipynb
import sys
import numpy as np
import xarray as xr
from xbout import open_boutdataset
from tqdm import tqdm, trange

basedir = '//scratch/space1/x01/data/my-scratch-data'
outdir = '/scratch/space1/x01/data/my-scratch-data/training/training_nc'

def read_traj(traj):
    dvort0 = []
    dvort1 = []
    dn0 = []
    dn1 = []
    for i in trange(0, 1001):
        ds = open_boutdataset(
                f'{basedir}/trajectory_{traj}/{i}/coarse_sim/BOUT.dmp.*.nc', 
                info=False)
        dvort0.append(ds['vort'][0,:,:,:])
        dvort1.append(ds['vort'][1,:,:,:])
        dn0.append(ds['n'][0,:,:,:])
        dn1.append(ds['n'][1,:,:,:])
    tvort0 = xr.concat(dvort0[1:], 't')
    tn0 = xr.concat(dn0[1:], 't')
    tvort1 = xr.concat(dvort1[:1001], 't')
    tn1 = xr.concat(dn1[:1001], 't')
    d0 = xr.merge([tvort0,tn0])
    d1 = xr.merge([tvort1,tn1])
    return d0, d1

def clean(ds):
    if 'metadata' in ds.attrs:
        del ds.attrs['metadata']
    if 'options' in ds.attrs:
        del ds.attrs['options']
    for variable in ds.variables.values():
        if 'metadata' in variable.attrs:
            del variable.attrs['metadata']
        if 'options' in variable.attrs:
            del variable.attrs['options']
            
traj = sys.argv[1]
d0, d1 = read_traj(traj)
clean(d0)
clean(d1)
d0.to_netcdf(f'{outdir}/gt_traj_{traj}.nc')
d1.to_netcdf(f'{outdir}/sim_traj_{traj}.nc')
#err=d0-d1
#err.to_netcdf(f'{outdir}/err_traj_{traj}.nc')
