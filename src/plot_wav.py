#!/usr/bin/env python3
#
# receives a list of audio files and plots their waveform.
# NOTE: might only work for *.wav file format.
#
# author: jul 2023
# Cassio Batista - https://cassiotbatista.github.io

import argparse
import fileinput
import os

import matplotlib.pyplot as plt
from scipy.io import wavfile


parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=10, help="number of subplots")
#parser.add_argument("--adjust", action="store_true", help="norm plot bounds")
parser.add_argument("files", nargs="*")
args = parser.parse_args()

filelist = list(
    fileinput.input(files=args.files if len(args.files) > 0 else ('-', ))
)
n = len(filelist) if len(filelist) < args.n else args.n
assert n <= args.n, f"viz is quite terrible for #files > {args.n}"

fig, ax = plt.subplots(n, 1)
xmax, ymax = 0, 0
for i, wavpath in enumerate(sorted(filelist)):
    wavpath = wavpath.strip()
    fs, wav = wavfile.read(wavpath)
    ax[i].plot(wav, label=os.path.basename(wavpath), zorder=3)
    ax[i].legend()
    ax[i].grid()
    if len(wav) > xmax:
        xmax = len(wav)
    if max(wav) > ymax:
        ymax = max(wav)
    if i >= args.n:
        break

norm_factor = 2 ** 15
for i in range(n):
    ax[i].set_xlim([0, xmax])
    ax[i].set_ylim([-norm_factor, norm_factor-1] if ymax > 1 else [-1.1, +1.1])

plt.show()
