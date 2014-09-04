#!/usr/bin/env python

from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt

try:
    short = sys.argv[1]
except IndexError:
    print('Commit not specified!')
    exit()


NEX = [96, 144, 192, 240]
DISTS = [101, 101, 45, 90]


for i, (nex, dist) in enumerate(zip(NEX, DISTS)):
    for comp in 'ZEN':
        try:
            ifort = np.genfromtxt('../test_ifort%d_%s/OUTPUT_FILES/S%03d.SY.MX%s.sem.ascii' % (i+1, short, dist, comp))
        except IOError:
            ifort = np.empty((0, 2))
        try:
            gfortran = np.genfromtxt('../test_gfortran%d_%s/OUTPUT_FILES/S%03d.SY.MX%s.sem.ascii' % (i+1, short, dist, comp))
        except IOError:
            gfortran = np.empty((0, 2))
        try:
            xlf = np.genfromtxt('../test_xlf%d_%s/OUTPUT_FILES/S%03d.SY.MX%s.sem.ascii' % (i+1, short, dist, comp))
        except IOError:
            xlf = np.empty((0, 2))
        try:
            xlf_strict = np.genfromtxt('../test_xlf_strict%d_%s/OUTPUT_FILES/S%03d.SY.MX%s.sem.ascii' % (i+1, short, dist, comp))
        except IOError:
            xlf_strict = np.empty((0, 2))

        if not (ifort.size + gfortran.size + xlf.size + xlf_strict.size):
            print('NEX=%d, comp=%s is empty!' % (nex, comp))
            continue

        fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)

        for ax, result, name in zip(axes, [gfortran, xlf, xlf_strict], ['gfortran', 'xlf -qnostrict', 'xlf -qstrict']):
            ax.plot(ifort[:,0], ifort[:,1], marker='x', markevery=15, label='ifort')
            ax.plot(result[:,0], result[:,1], marker='o', markevery=20, label=name)
            ax.set_ylabel(comp)
            ax.legend(loc='best')

        result = ifort if ifort.size else gfortran if gfortran.size else xlf if xlf.size else xlf_strict
        if dist < 30:
            axes[2].set_xlim(result[0,0], 1000)
        elif 30 <= dist < 60:
            axes[2].set_xlim(1000, 2000)
        elif 60 <= dist < 90:
            axes[2].set_xlim(2000, 3000)
        elif 90 <= dist:
            axes[2].set_xlim(3000, result[-1,0])
        axes[2].set_xlabel('Time')
        fig.suptitle('%s, %d deg, NEX=%d' % (short, dist, nex))

        fig.savefig('plots/%s-%03d-%03d%s.png' % (short, nex, dist, comp))

