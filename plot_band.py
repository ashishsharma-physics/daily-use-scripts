#!/usr/bin/env python
# -*- coding: utf-8 -*-

# * Comparison of VASP band and Wannier band
# * by En Wang, SF10, IOP, CAS (enwang@iphy.ac.cn)

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Agg')

efermi = 7.32865399
nkp1, nkp2 = 450, 1166
#emin, emax = -2.5, 2.5
emin, emax = -1, 1

# Input data
vasp_data = np.loadtxt("./bnd_ori_soc.dat")
w90_data = np.loadtxt("./wannier90_band.dat")

kk1, vee = vasp_data[:, 0], vasp_data[:, 1]
kk1 = kk1.reshape((-1, nkp1))
vee = vee.reshape((-1, nkp1))

kk2, wee = w90_data[:, 0], w90_data[:, 1]
kk2 = kk2.reshape((-1, nkp2))/(2*np.pi)
wee = wee.reshape((-1, nkp2)) - efermi

fig, ax = plt.subplots()

for kk, ee in zip(kk1, vee):
    ax.plot(kk, ee, 'k-')

for kk, ee in zip(kk2, wee):
    ax.plot(kk, ee, 'r--', linewidth=1)

ax.set_xlim(kk1[0, 0], kk1[0, nkp1-1])
ax.set_ylim(emin, emax)
ax.tick_params(axis='both', which='minor', length=4, width=1, labelsize=12)
ax.tick_params(axis='both', which='major', length=7, width=1, labelsize=12)
ax.set_xlabel('K-Path', fontsize=14)
ax.set_ylabel('Energy', fontsize=14)
ax.set_title(r'WTe$_2$', fontsize=18)
fig.savefig('band_structure_comp_s_narrow_2.png', dpi=300, bbox_inches='tight')
plt.close(fig)
