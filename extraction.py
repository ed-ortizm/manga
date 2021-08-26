#!/usr/bin/env python3

import glob
import os

import astropy.io.fits as pyfits
import numpy as np
import scipy.constants as cst

from constants import data, data_proc, all_data, all_data_proc
from constants import n_wl, m_wl

if not os.path.exists(all_data_proc):
    os.mkdir(all_data_proc)

## Listing the files in the directory

dapall = pyfits.open('dapall-v2_7_1-2.4.1.fits')

for fname in glob.glob(f'{all_data}/*LOGCUBE*.fits'):

    print(f'Processing {fname.split("/")[-1]}...', end='\r')

    plate_ifu = '{}-{}'.format(*fname.split('-')[1:3])
    cubes = pyfits.open(fname)
    maps = pyfits.open(fname.replace('LOGCUBE','MAPS'))

    ## Skipping data with quality concerns
    if maps['PRIMARY'].header['DAPQUAL'] > 0:
         cubes.close()
         maps.close()
         continue

    ## Stellar velocities
    bin_id = np.ravel(maps['BINID'].data[1, :, :]) 
    bin_snr = np.ravel(maps['BIN_SNR'].data)
    stellar_vel = np.ravel(maps['STELLAR_VEL'].data)
    stellar_vel_mask = np.ravel(maps['STELLAR_VEL_MASK'].data)
    bin_m_flux_mask = np.ravel(maps['BIN_MFLUX_MASK'].data)

    flx = cubes['FLUX'].data
    flx = flx.reshape((flx.shape[0], -1))
    wl = cubes['WAVE'].data
    mask_cube = cubes['MASK'].data

    bins, indices = tuple(map(lambda x : x[1:], np.unique(bin_id, return_index=True)))

    bin_id = bin_id[indices]
    bin_snr = bin_snr[indices]
    stellar_vel = stellar_vel[indices]
    stellar_vel_mask = stellar_vel_mask[indices]
    bin_m_flux_mask = bin_m_flux_mask[indices]

    flx = flx[:, indices]

    ## De-redshifting
    ind = np.where(dapall['DAPALL'].data['plateifu'] == plate_ifu)
    z = dapall['DAPALL'].data['nsa_z'][ind][0]

    wl *= 1. / (1.+z)

    # Correcting for the stellar velocity redshift & interpolating

    all_flx = np.empty((n_wl, indices.size))

    for idx in range(indices.size):
        all_flx[:, idx] = np.interp(m_wl, wl*cst.c / (cst.c + stellar_vel[idx]*1_000.),
                                    flx[:, idx], left=np.nan, right=np.nan)

    all_flx *= 1. / np.nanmedian(all_flx, axis=0)

    np.save(f'{all_data_proc}/{plate_ifu}.npy', all_flx.astype(np.float32))
    np.save(f'{all_data_proc}/{plate_ifu}-id.npy', bin_id.astype(np.int32))
    np.save(f'{all_data_proc}/{plate_ifu}-SNR.npy', bin_snr.astype(np.float32))

    cubes.close()
    maps.close()

dapall.close()
