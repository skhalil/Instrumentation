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

cable_length = '100'
add_redo = True
redo = ''
if add_redo == True: redo = 'redo'
subfile = '0'; comp=''

if   subfile == '0': comp = '11'
elif subfile == '1': comp = '21'
##
# *.s2p Files format
# Each record contains 1 stimulus value and 4 S-parameters (total of 9 values)
#Stim  Real (S11)  Imag(S11)  Real(S21)  Imag(S21)  Real(S12)  Imag(S12)  Real(S22)  Imag(S22)

# ==== our file format for vna_0: ====
#!freq  RelS11    ImS11    RelS12    ImS12    RelS13    ImS13    RelS14   ImS14

# parameter in file => read from software

# S11 S13          00  01            S11 S12
#            ---->           ----> 
# S12 S14          10  11            S21 S22


# ==== our file format for vna_1: ====
#!freq  RelS21    ImS21    RelS22    ImS22    RelS23    ImS23    RelS24   ImS24

# parameter in file => read from software

# S21 S23          00  01            S11 S12
#            ---->           ----> 
# S22 S24          10  11            S21 S22


#
#TP_20cm_15_ChD1 (34)

if cable_length == '20':
    net1 = rf.Network('Plots/TP_20cm_15_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')#33
    net2 = rf.Network('Plots/TP_20cm_31_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') #23
    net3 = rf.Network('Plots/TP_20cm_49_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '35' and add_redo==False:
    net2 = rf.Network('Plots/TP_35cm_18_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') #23
    net5 = rf.Network('Plots/TP_35cm_27_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net6 = rf.Network('Plots/TP_35cm_28_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net7 = rf.Network('Plots/TP_35cm_29_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net8 = rf.Network('Plots/TP_35cm_56_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net9 = rf.Network('Plots/TP_35cm_57_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '35' and add_redo:
    net4 = rf.Network('Plots/Redo_VNA/TP_35cm_56_ChD1_Redo.vna_'+subfile+'.s2p', f_unit='ghz')
    net5 = rf.Network('Plots/TP_35cn_59_ChD1_right_config.vna_'+subfile+'.s2p', f_unit='ghz')
    net6 = rf.Network('Plots/TP_35cn_59_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net8 = rf.Network('Plots/TP_35cm_56_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')   
    net10 = rf.Network('Plots/Redo_VNA/TP_35cm_60_ChD1_Redo.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '100' and add_redo==False:
    net1 = rf.Network('Plots/TP_1m_20_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.Network('Plots/TP_1m_21_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') 
    net3 = rf.Network('Plots/TP_1m_23_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net4 = rf.Network('Plots/TP_1m_32_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') 
    net5 = rf.Network('Plots/TP_1m_33_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '100' and add_redo:
    net1 = rf.Network('Plots/Redo_VNA/TP_1m_53_ChD0_rwy.vna_'+subfile+'.s2p', f_unit='ghz')
    #net2 = rf.Network('Plots/Redo_VNA/082620_TP_53_1m_ChD0_SK.vna_'+subfile+'.s2p', f_unit='ghz') #55 34G_CHD1
    #net3 = rf.Network('Plots/TP_1m_32_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')        
elif cable_length == '140':
    net1 = rf.Network('Plots/TP_1p4m_35_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.Network('Plots/TP_1p4m_36_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') 
    net3 = rf.Network('Plots/TP_1p4m_37_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net4 = rf.Network('Plots/TP_1p4m_38_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') 
    net5 = rf.Network('Plots/TP_1p4m_39_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')    
    net6 = rf.Network('Plots/TP_1p4m_40_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '200':
    net1 = rf.Network('Plots/TP_2m_46_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.Network('Plots/TP_2m_47_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    
netref = rf.Network('Plots/calibration_test.vna_'+subfile+'.s2p', f_unit='ghz')


#net1 = rf.Network('Plots/TP_20cm_15_ChD1.vna_3.s2p', f_unit='ghz')#33

#net2 = rf.Network('Plots/TP_20cm_31_ChD1.vna_3.s2p', f_unit='ghz') #23

#net3 = rf.Network('Plots/TP_1m_32_ChD1.vna_0.s2p', f_unit='ghz')


with style.context('seaborn-ticks'):
    #Time domain reflectometry, measurement vs simulation
    fig0 = plt.figure(figsize=(10,4))
    ax0=plt.subplot(1,2,1)
    #major_ticks = np.arange(0, 6.5, 0.5)
    #minor_ticks = np.arange(0, 6.5, 0.1)
    ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.grid(True, color='0.8', which='minor')
    ax0.grid(True, color='0.4', which='major')
    if cable_length == '20':
        net1_dc = net1.extrapolate_to_dc(kind='linear')
        net2_dc = net2.extrapolate_to_dc(kind='linear')
        net3_dc = net3.extrapolate_to_dc(kind='linear')
    elif cable_length == '35' and add_redo == False:
        net2_dc = net2.extrapolate_to_dc(kind='linear')
        net5_dc = net5.extrapolate_to_dc(kind='linear')
        net6_dc = net6.extrapolate_to_dc(kind='linear')
        net7_dc = net7.extrapolate_to_dc(kind='linear')
        net8_dc = net8.extrapolate_to_dc(kind='linear')
        net9_dc = net9.extrapolate_to_dc(kind='linear')
    elif cable_length == '35' and add_redo:
        net4_dc = net4.extrapolate_to_dc(kind='linear')
        net5_dc = net5.extrapolate_to_dc(kind='linear')
        net6_dc = net6.extrapolate_to_dc(kind='linear')
        net8_dc = net8.extrapolate_to_dc(kind='linear')
        net10_dc = net10.extrapolate_to_dc(kind='linear')
    elif cable_length == '100' and add_redo==False:
        net1_dc = net1.extrapolate_to_dc(kind='linear')
        net2_dc = net2.extrapolate_to_dc(kind='linear')
        net3_dc = net3.extrapolate_to_dc(kind='linear')
        net4_dc = net4.extrapolate_to_dc(kind='linear')
        net5_dc = net5.extrapolate_to_dc(kind='linear')
    elif cable_length == '100' and add_redo:
        net1_dc = net1.extrapolate_to_dc(kind='linear')
        #net2_dc = net2.extrapolate_to_dc(kind='linear')
        #net3_dc = net3.extrapolate_to_dc(kind='linear')        
    elif cable_length == '140':
        net1_dc = net1.extrapolate_to_dc(kind='linear')
        net2_dc = net2.extrapolate_to_dc(kind='linear')
        net3_dc = net3.extrapolate_to_dc(kind='linear')
        net4_dc = net4.extrapolate_to_dc(kind='linear')
        net5_dc = net5.extrapolate_to_dc(kind='linear')
        net6_dc = net6.extrapolate_to_dc(kind='linear')  
    elif cable_length == '200':
        net1_dc = net1.extrapolate_to_dc(kind='linear')
        net2_dc = net2.extrapolate_to_dc(kind='linear')
        
    netref_dc = netref.extrapolate_to_dc(kind='linear')
    plt.title('Frequency')
    if cable_length == '20':
        net1_dc.s11.plot_s_db(label='S'+comp+', TP_20cm_15 (34)')
        net2_dc.s11.plot_s_db(label='S'+comp+', TP_20cm_31 (36)')
        net3_dc.s11.plot_s_db(label='S'+comp+', TP_20cm_49 (34)')
    elif cable_length == '35' and add_redo == False:
        net2_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_18 (36)')
        net5_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_27 (34)')
        net6_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_28 (34)')
        net7_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_29 (34)')
        net8_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_56 (34)')
        net9_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_57 (34)')
    elif cable_length == '35' and add_redo == True:
        net4_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_56_redo (34)')
        net5_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_59_rc (34)')
        net6_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_59_wc (34)')
        net8_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_56 (34)')
        net10_dc.s11.plot_s_db(label='S'+comp+', TP_35cm_60_redo (34)')            
    elif cable_length == '100' and add_redo==False:
        net1_dc.s11.plot_s_db(label='S'+comp+', TP_1m_20 (36)')
        net2_dc.s11.plot_s_db(label='S'+comp+', TP_1m_21 (36)')
        net3_dc.s11.plot_s_db(label='S'+comp+', TP_1m_23 (36)')
        net4_dc.s11.plot_s_db(label='S'+comp+', TP_1m_32 (34)')
        net5_dc.s11.plot_s_db(label='S'+comp+', TP_1m_33 (34)')
    elif cable_length == '100' and add_redo:
        net1_dc.s11.plot_s_db(label='S'+comp+', TP_1m_53_D0 (36)')
        #net2_dc.s11.plot_s_db(label='S'+comp+', TP_1m_55_sk (36)')
        #net3_dc.s11.plot_s_db(label='S'+comp+', TP_1m_32 (34)')
    elif cable_length == '140':
        net1_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_35 (36)')
        net2_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_36 (36)')
        net3_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_37 (36)')
        net4_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_38 (36)')
        net5_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_39 (34)')
        net5_dc.s11.plot_s_db(label='S'+comp+', TP_1p4m_40 (34)')
    elif cable_length == '200':
        net1_dc.s11.plot_s_db(label='S'+comp+', TP_2m_46 (34)')
        net2_dc.s11.plot_s_db(label='S'+comp+', TP_2m_47 (34)')
        
    netref_dc.s11.plot_s_db(label='S'+comp+', Calibration')
    plt.ylim((-50.0, 50.0))
    plt.xlim((100000, 6000000000))
    ax1=plt.subplot(1,2,2)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.grid(True, color='0.8', which='minor')
    ax1.grid(True, color='0.4', which='major')
    plt.title('Time domain reflection step response (DC extrapolation)') #The time_step component of the z-matrix vs frequency
    if cable_length == '20':
        net1_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_15 (34)')
        net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_31 (36)')
        net3_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_49 (34)')
    elif cable_length == '35' and add_redo == False:
        net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_18 (36)')
        net5_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_27 (34)')
        net6_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_28 (34)')
        net7_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_29 (34)')
        net8_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_56 (34)')
        net9_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_57 (34)')
    elif cable_length == '35' and add_redo:
        net4_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_56_redo (34)')
        net5_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_59_rc (34)')
        net6_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_59_wc (34)')
        net8_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_56 (34)')
        net10_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_60_redo (34)')            
    elif cable_length == '100' and add_redo==False:
        net1_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_20 (36)')
        net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_21 (36)')
        net3_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_23 (36)')
        net4_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_32 (34)')
        net5_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_33 (34)')
    elif cable_length == '100' and add_redo:
        net1_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_53_D0 (36)')
        #net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_53_sk (36)')
        #net3_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_32 (34)')    
    elif cable_length == '140':
        net1_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_35 (36)')
        net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_36 (36)')
        net3_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_37 (36)')
        net4_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_38 (36)')
        net5_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_39 (34)')
        net6_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_40 (34)')
    elif cable_length == '200':
        net1_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_2m_46 (34)')
        net2_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_2m_47 (34)')
        
    netref_dc.s11.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration')
    
    plt.ylim((-100.0, 400.0))
    plt.xlim((0, 25))
    plt.tight_layout()
    #fig0.savefig('Plots/36vs34_'+cable_length+'cm_freq_time_Z_rf_'+comp+redo+'.png')
    fig0.savefig('Plots/36G_'+cable_length+'cm_freq_time_Z_rf_'+comp+redo+'.png')
    
    pylab.show()
