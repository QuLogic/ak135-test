#!/usr/bin/env python

from __future__ import print_function

import os
import platform
import numpy as np
import matplotlib.pyplot as plt

def get_file(run, seismo):
    if 'scinet' in platform.node() or 'gpc' in platform.node():
        return os.path.join('..', run, 'OUTPUT_FILES', seismo)
    else:
        return os.path.join(run, seismo)

# Commits tested on all compilers
ALL_COMMITS = [
    ('6994fe6', 'devel'),
    ('a87d120', 'static-analysis')
]

# Commits test on ifort only
IFORT_COMMITS = [
    ('a87d120', 'static-analysis'),
    ('d778d2c', 'fp-model=strict'),
    ('2aaca03', 'fp-model=source'),
    ('cdd5c9d', 'standard-semantics'),
    ('eaa440b', 'standard-semantics without realloc-lhs')
]


NEX = [96, 144, 192, 240]
DISTS = [101, 101, 45, 90]
COMPILERS = ['ifort', 'gfortran', 'xlf', 'xlf_strict']
MARKER_SPACING = [13, 17, 23, 29, 31, 37]


# Compare ifort only for its fixes
for i, (nex, dist) in enumerate(zip(NEX, DISTS)):
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    for ax, comp in zip(axes, 'ZEN'):
        for j, (short, name) in enumerate(IFORT_COMMITS):
            filename = get_file('test_ifort%d_%s' % (i + 1, short),
                                'S%03d.SY.MX%s.sem.ascii' % (dist, comp))
            data = np.genfromtxt(filename)
            ax.plot(data[:,0], data[:,1], markevery=MARKER_SPACING[j], marker='x', label=name)
        ax.set_ylabel(comp)

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
    fig.suptitle('ifort check, %d deg, NEX=%d' % (dist, nex))

    print('plots/ifort-%03d-%03d.png' % (nex, dist))
    fig.savefig('plots/ifort-%03d-%03d.png' % (nex, dist))

plt.show()

