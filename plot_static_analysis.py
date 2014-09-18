#!/usr/bin/env python

from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt

# Commits tested on all compilers
ALL_COMMITS = {
    '6994fe6': 'devel',
    'a87d120': 'static-analysis'
}

NEX = [96, 144, 192, 240]
DISTS = [101, 101, 45, 90]
COMPILERS = ['ifort', 'gfortran', 'xlf', 'xlf_strict']
MARKER_SPACING = [13, 17, 23, 29, 31, 37]


# Compare all compilers for static analysis fixes
for i, (nex, dist) in enumerate(zip(NEX, DISTS)):
    for comp in 'ZEN':
        fig, axes = plt.subplots(len(COMPILERS), 1, figsize=(16, 12), sharex=True)
        for ax, compiler in zip(axes, COMPILERS):
            for j, (short, name) in enumerate(ALL_COMMITS.items()):
                filename = '../test_%s%d_%s/OUTPUT_FILES/S%03d.SY.MX%s.sem.ascii' % (
                    compiler, i+1, short, dist, comp)
                data = np.genfromtxt(filename)
                ax.plot(data[:,0], data[:,1], markevery=MARKER_SPACING[j], marker='x', label=name)
            ax.set_ylabel(compiler)

        if dist < 30:
            axes[2].set_xlim(data[0,0], 1000)
        elif 30 <= dist < 60:
            axes[2].set_xlim(1000, 2000)
        elif 60 <= dist < 90:
            axes[2].set_xlim(2000, 3000)
        elif 90 <= dist:
            axes[2].set_xlim(3000, data[-1,0])
        axes[2].set_xlabel('Time')
        axes[0].legend(loc='best')
        fig.suptitle('Static analysis check, %d deg, NEX=%d' % (dist, nex))

        print('plots/static-analysis-%03d-%03d%s.png' % (nex, dist, comp))
        fig.savefig('plots/static-analysis-%03d-%03d%s.png' % (nex, dist, comp))

