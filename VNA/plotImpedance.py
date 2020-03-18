#!/usr/bin/env python3
from itertools import islice
import sys, re
import numpy as np
import skrf as rf
#rf.stylely()

import pylab
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl

#TP_20cm_15_ChD1 (34)

net1 = rf.Network('Plots/TP_20cm_15_ChD1.vna_0.s2p', f_unit='ghz')#33

net2 = rf.Network('Plots/TP_20cm_31_ChD1.vna_0.s2p', f_unit='ghz') #23

#net3 = rf.Network('Plots/TP_1m_32_ChD1.vna_0.s2p', f_unit='ghz')


with style.context('seaborn-ticks'):
    #Time domain reflectometry, measurement vs simulation
    fig0 = plt.figure(figsize=(8,4))
    ax0=plt.subplot(1,2,1)
    #major_ticks = np.arange(0, 6.5, 0.5)
    #minor_ticks = np.arange(0, 6.5, 0.1)
    ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.grid(True, color='0.8', which='minor')
    ax0.grid(True, color='0.4', which='major')
    net1_dc = net1.extrapolate_to_dc(kind='linear')
    net2_dc = net2.extrapolate_to_dc(kind='linear')
    #net3_dc = net3.extrapolate_to_dc(kind='linear')
    plt.title('Frequency')
    net1_dc.s11.plot_s_db(label='S11, TP_20cm_15 (34)')
    net2_dc.s11.plot_s_db(label='S11, TP_20cm_31 (36)')
    #net3_dc.s11.plot_s_db(label='S11, TP_1m_34 (34)')
    plt.ylim((-50.0, 50.0))
    plt.xlim((100000, 2500000000))
    ax1=plt.subplot(1,2,2)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.grid(True, color='0.8', which='minor')
    ax1.grid(True, color='0.4', which='major')
    plt.title('Time domain reflection step response (DC extrapolation)') #The time_step component of the z-matrix vs frequency
    net1_dc.s11.plot_z_time_step(pad=2000, window='hamming', z0=50, label='TD11, TP_20cm_15 (34)')
    net2_dc.s11.plot_z_time_step(pad=2000, window='hamming', z0=50, label='TD11, TP_20cm_31 (36)')
    #net3_dc.s11.plot_z_time_step(pad=2000, window='hamming', z0=50, label='TD11, TP_1m_32 (34)')
    plt.ylim((-100.0, 300.0))
    plt.xlim((0, 5))
    plt.tight_layout()
    fig0.savefig('Plots/36vs34_20cm_freq_time_Z_rf.png')
    
    pylab.show()
