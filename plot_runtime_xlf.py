#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, AutoDateLocator


RES = (96, 144, 192, 240)
MARKERS = ('o', 'v', 'x', '^')


data = np.genfromtxt('xlf_runtimes',
                     dtype=[('commit', 'S7'), ('res', 'I2'),
                            ('nostrict', 'f8'), ('strict', 'f8')])
indices = np.arange(len(data))

f, ax1 = plt.subplots(1, 1, figsize=(12, 8))
ax2 = ax1.twinx()

ax1.plot(indices, data['nostrict'] / 60, c='b', label='-qnostrict')
ax1.plot(indices, data['strict'] / 60, c='g', label='-qstrict')

ax2.plot(indices, data['strict'] / data['nostrict'], c='r')

for i in range(4):
    mask = data['res'] == (i + 1)
    ax1.scatter(indices[mask], data['nostrict'][mask] / 60,
                c='b', edgecolor='b', marker=MARKERS[i])
    ax1.scatter(indices[mask], data['strict'][mask] / 60,
                c='g', edgecolor='g', marker=MARKERS[i])

    ax2.scatter(indices[mask], data['strict'][mask] / data['nostrict'][mask],
                c='r', edgecolor='r', marker=MARKERS[i],
                label='NEX=%d' % (RES[i], ))

ax1.set_xticks(indices)
ax1.set_xticklabels([x.decode('ascii') for x in data['commit']],
                    rotation='vertical')
ax1.set_xlim(-1, len(indices))
ax1.set_xlabel('Commit')
ax1.set_ylim(0, 200)
ax1.set_ylabel('Runtime (min)')
ax1.legend(loc='upper left')

ax2.set_ylim(1.0, 1.3)
ax2.set_ylabel('Runtime Ratio')
ax2.tick_params(axis='y', colors='r')
ax2.legend(loc='lower right')

f.savefig('xlf-runtime.png')

plt.show()
