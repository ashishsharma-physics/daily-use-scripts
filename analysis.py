#!/usr/bin/env python
# -*- coding: utf-8 -*-

# * Get Gap Distribution
# * by En Wang, SF10, IOP, CAS (enwang@iphy.ac.cn)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

def plot_gap_hist(data):
    # data = pd.read_csv('gap2d.dat', sep='\s+', skiprows=1, header=None)
    gap = data.hist(column=3, bins=20)
    plt.savefig('gap_distribution.png')

def plot_gap_k_range(data):
    kk = ['kx', 'ky', 'kz']
    ii = [12, 13, 14]
    for k, i in zip(kk, ii):
        krange = data.hist(column=i, bins=20)
        plt.savefig(f'k_range_{k}.png')

if __name__ == '__main__':
    data = pd.read_csv('gap2d.dat', sep='\s+', skiprows=1, header=None)
    # data = data[data[3] < 0.0002]
    plot_gap_hist(data)
    plot_gap_k_range(data)
