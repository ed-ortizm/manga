#! /usr/bin/env python3

import glob

import numpy as np

from constants import data_proc, all_data_proc, n_wl

def get_metadata(fnames):
    ids = []
    snrs = []
    plate_ifus = []
    for fname in fnames:
        bname = fname[:-4]
        ids.append(np.load(f'{bname}-id.npy'))
        snrs.append(np.load(f'{bname}-SNR.npy'))
        plate_ifus.append([bname.split('/')[-1]]*ids[-1].size)

    return np.hstack(ids), np.hstack(snrs), np.hstack(plate_ifus)

fnames = glob.glob(f'{all_data_proc}/*-*[0-9].npy')

ids, snrs, plate_ifus = get_metadata(fnames)

## Spaxels with high S/N (>10)

w10 = np.where(snrs > 10.)
ids = ids[w10]
snrs = snrs[w10]
plate_ifus = plate_ifus[w10]


## Gruping spaxels with similar snr

n = 10
srt_idx = np.argsort(snrs)

for cnt_bin, bin in enumerate(np.array_split(srt_idx, n)):
    spectra = np.empty((n_wl, bin.size))

    for cnt, idx in enumerate(bin):
       print(f'Processing bin N. {cnt_bin} for spectrum {cnt} of {bin.size}! The SNR is {snrs[idx]}', end='\r')
       # mmap_mode = 'r', reads only the part I'm interested in.
       ifu_spectra = np.load(f'{all_data_proc}/{plate_ifus[idx]}.npy', mmap_mode='r')
       ifu_ids = np.load(f'{all_data_proc}/{plate_ifus[idx]}-id.npy')
       ID = np.where(ifu_ids == ids[idx])[0][0]
       spectra[:, cnt] = ifu_spectra[:, ID]
    ## Keeping spectra where at a given wl more than 90% of values are finite
    wkeep = np.where(np.count_nonzero(~np.isfinite(spectra), axis=1) < bin.size // 10)
    spectra = np.squeeze(spectra[wkeep, :])
    for flx in spectra:
        ## Replacing indefinite values by the nanmedian
        flx[np.where(~np.isfinite(flx))] = np.nanmedian(flx)
    np.save(f'spectra_bin_{cnt_bin}.npy', spectra)
