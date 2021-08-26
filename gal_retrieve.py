#! /usr/bin/env python3

import sys
import os
import glob

import numpy as np

from myRF_lib import get_metadata, Logger, sp_plot
from constants import data_proc, all_data_proc, n_wl


## Retrieve the name of the spectra




sys.stdout = Logger()

fnames = glob.glob(f'{all_data_proc}/*-*[0-9].npy')

print('Retrieving metadata!')
ids, snrs, plate_ifus = get_metadata(fnames)

## Spaxels with high S/N (>10)

w10 = np.where(snrs > 10.)
ids = ids[w10]
snrs = snrs[w10]
plate_ifus = plate_ifus[w10]
srt_idx = np.argsort(snrs)
split = np.array_split(srt_idx, 10)
print(f'Size of split: {len(split)}. size of the bin: {split[9].size}')

print('Loading outlier scores!')
rhos = np.load('rhos.npy', mmap_mode='r')

ids_prospecs = np.argpartition(rhos, -20)[-20:]

print('Outlier scores for the weirdest spectra')

for n, idx in enumerate(ids_prospecs):
    print(f'{n+1:02} --> {rhos[idx]}')

print('Extracting fluxes for the most outlying spectera')

bin9 = np.load('/home/edgar/zorro/MaNGAdata/spectra_bin_9.npy', mmap_mode = 'r')

prospecs = bin9[:, ids_prospecs]

## Indices for unproceced data

idxs = split[9][ids_prospecs]

## Plotting the spectra
for n, idx in enumerate(idxs):
    plate_ifu = plate_ifus[idx]
    ID = ids[idx]
    xy_pos = sp_plot(plate_ifu, ID, prospecs[:, n])
    print(f'{n+1:02} --> Plate IFU: {plate_ifus[idx]} with bin ID {ids[idx]} and spatial position: {xy_pos}')


#id_prospec = np.argmax(rhos)
#prospec = np.load('/home/edgar/zorro/MaNGAdata/spectra_bin_9.npy', mmap_mode = 'r')[:, id_prospec]
#idx = split[9][id_prospec]
#print(f'Plate IFU: {plate_ifus[idx]} with bin ID {ids[idx]}')
#print(f'Outlier score: {rhos[id_prospec]}')
#plate_ifu = plate_ifus[idx]
#ID = ids[idx]
#sp_plot(plate_ifu, ID, prospec)
