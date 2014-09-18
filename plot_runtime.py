#!/usr/bin/env python

from __future__ import (division, print_function)

from datetime import datetime
import glob
import os
import platform
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

COMPILERS = ['ifort', 'gfortran', 'xlf', 'xlf_strict']
NEX = [96, 144, 192, 240]
COLOURS = 'bgrc'
if 'scinet' in platform.node() or 'gpc' in platform.node():
    BASE = os.path.expanduser('~/specfem3d_globe')
else:
    BASE = os.path.expanduser('~/code/specfem3d_globe')

runtimes = {}
dtype = np.dtype([('date', 'f4'),
                  ('runtime', 'f4'),
                  ('steps', 'i4'),
                  ('total', 'i4'),
                  ('rev', 'S7')])

for compiler in COMPILERS:
    print(compiler)

    for i in range(4):
        data = []
        for dir in glob.glob('log/test_%s%d_*' % (compiler, i + 1)):
            rev = dir.split('_')[-1]
            print(rev)
            try:
                date = subprocess.check_output(['git', 'log', '-1',
                                                '--pretty=format:%ai',
                                                '%s' % (rev, )],
                                               cwd=BASE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print('WARNING: %s has no git revision!' % (dir, ))
                continue
            split_date = date.split()
            date = ' '.join(split_date[:-1])
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            timestamps = sorted(glob.glob(dir + '/OUTPUT_FILES/timestamp*'))
            if not timestamps:
                print('WARNING: %s has no timestamps!' % (dir, ))
                continue

            time = None
            complete = None
            total = None
            with open(timestamps[-1], 'r') as f:
                for line in f:
                    if 'Elapsed time in seconds' in line:
                        time = float(line.split()[-1])
                    elif 'Time steps done' in line:
                        words = line.split()
                        complete = int(words[4])
                        total = int(words[7])

            if time is None or complete is None or total is None:
                print('WARNING: %s is unparseable!' % (dir, ))
                continue

            if complete != total:
                print('WARNING: %s is incomplete!' % (dir, ))

            if complete <= 5:
                print('WARNING: %s has too few time steps to be useful!' % (dir, ))
                continue

            data += [(mdates.date2num(date), time, complete, total, rev)]

        runtimes['%s%d' % (compiler, i + 1)] = np.array(sorted(data),
                                                        dtype=dtype)

for res in range(4):
    fig, ax = plt.subplots(1, 1, figsize=(12,8))
    for j, compiler in enumerate(COMPILERS):
        runtime = runtimes['%s%d' % (compiler, res + 1)]
        x = runtime['date']
        y = runtime['runtime'] / runtime['steps']
        ok = runtime['steps'] == runtime['total']
        ax.plot(x, y, c=COLOURS[j], label=compiler)
        ax.scatter(x[ok], y[ok], c=COLOURS[j], marker='o')
        ax.scatter(x[~ok], y[~ok], c=COLOURS[j], marker='x')

    locator = mdates.AutoDateLocator()
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlabel('Author Date')
    ax.set_ylabel('Runtime (s/step)')
    ax.legend(loc='best')
    ax.set_title('NEX=%d' % (NEX[res], ))

    fig.savefig('plots/runtime-%d.png' % (NEX[res], ))

plt.show()

