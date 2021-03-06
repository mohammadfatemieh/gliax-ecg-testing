# -*- coding: utf-8 -*-
"""
Created on 2018 Jul 6 

GLIA ECG DEBUG DATA ANALYSIS

Copyright (C) 2018 Luka Banovic <banovic@irnas.eu>

This script contains functions for ECG data analysis, customized for use with GliaX Open-Source ECG device.

All projects of Institute IRNAS are as usefully open-source as possible.

Firmware and software originating from the project is licensed under GNU GENERAL PUBLIC LICENSE v3
<http://www.gnu.org/licenses/gpl-3.0.en.html>.

Open data generated by our projects is licensed under CC0 <https://creativecommons.org/publicdomain/zero/1.0/legalcode>.

All our websites and additional documentation are licensed under Creative Commons Attribution-ShareAlike 4 .0 Unported License
<https://creativecommons.org/licenses/by-sa/4.0/legalcode>.

What this means is that you can use hardware, firmware, software and documentation without paying a royalty and knowing that 
you'll be able to use your version forever. You are also free to make changes but if you share these changes then you have to 
do so on the same conditions that you enjoy.

Koruza, GoodEnoughCNC and IRNAS are all names and marks of Institut IRNAS Rače. You may use these names and terms only to 
attribute the appropriate entity as required by the Open Licences referred to above. You may not use them in any other way 
and in particular you may not use them to imply endorsement or authorization of any hardware that you design, make or sell.

===============================================
NOTES:

    ECG Frequency range up to 200 Hz is clinically 
relevant.

    fs = 488 Hz
===============================================

"""
import os
os.chdir(r'')			# insert the path to working directory
import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, freqz
from scipy.fftpack import fft
from Glia_ECG_filters import baseline_filter, notch_filter, low_pass_filter


def load_dataset(filename):
    """
	This function reads the data from a .txt file.
    """
    data = pandas.read_csv(filename, header=1, names=['ts', 'I', 'II', 'V1', 'V2', 'V3', 'V4', 'V5','V6'])
    

    I = data['I']
    II = data['II']
    
    III = data['II']-data['I']
    aVR = (-II-I)/3
    aVL = (I-III)/3
    aVF = (II+III)/3
    
    V1 = data['V1']
    V2 = data['V2']
    V3 = data['V3']
    V4 = data['V4']
    V5 = data['V5']
    V6 = data['V6']
    
    sf = 488.
    time = np.linspace(0,len(I)/sf,len(I))
    return time, I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6


def plot_signals(filename):
    """
    """
    time, I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6 = load_dataset(filename)
    
    plt.subplot(3,4,1)
    plt.plot(time, I)
    plt.title('I')
    plt.subplot(3,4,2)
    plt.plot(time, II)
    plt.title('II')
    plt.subplot(3,4,3)
    plt.plot(time, III)
    plt.title('III')
    plt.subplot(3,4,4)
    plt.plot(time, aVR)
    plt.title('aVR')
    plt.subplot(3,4,5)
    plt.plot(time, aVL)
    plt.title('aVL')
    plt.subplot(3,4,6)
    plt.plot(time, aVF)
    plt.title('aVF')
    plt.subplot(3,4,7)
    plt.plot(time, V1)
    plt.title('V1')
    plt.subplot(3,4,8)
    plt.plot(time, V2)
    plt.title('V2')
    plt.subplot(3,4,9)
    plt.plot(time, V3)
    plt.title('V3')
    plt.subplot(3,4,10)
    plt.plot(time, V4)
    plt.title('V4')
    plt.subplot(3,4,11)
    plt.plot(time, V5)
    plt.title('V5')
    plt.subplot(3,4,12)
    plt.plot(time, V6)
    plt.title('V6')
    
def filter_signal(ecg_lead, plot_signals = False, plot_filters = False, plot_signal_ffts = False):
    """
    """
    sf = 488.
    b_baseline, a_baseline = baseline_filter(2, 40, 0.2, sf)
    b_notch, a_notch = notch_filter(50, sf, 15)
    b_low_pass, a_low_pass = low_pass_filter(2, 150., sf)
    
    baseline = filtfilt(b_baseline, a_baseline, ecg_lead)
    notch = filtfilt(b_notch, a_notch, baseline)
    lpf= filtfilt(b_low_pass, a_low_pass, notch)
    
    if plot_signals == True:
        time = np.linspace(0,len(ecg_lead)/sf,len(ecg_lead))
        plt.figure()
        plt.subplot(4,1,1)
        plt.plot(time, ecg_lead)
        plt.subplot(4,1,2)
        plt.plot(time, baseline)
        plt.subplot(4,1,3)
        plt.plot(time, notch)
        plt.subplot(4,1,4)
        plt.plot(time, lpf)
    
    if plot_filters == True:
        nfft = 1024;
        w_baseline, H_baseline = freqz(b_baseline, a_baseline, nfft)
        w_notch, H_notch = freqz(b_notch, a_notch, nfft)
        w_lpf, H_lpf = freqz(b_low_pass, a_low_pass, nfft)
        
        f_filt = sf/2*np.linspace(0, 1, len(H_baseline))
        
        plt.figure()
        plt.subplot(4,1,1)
        plt.plot(f_filt, 20*np.log10(abs(H_baseline)))
        plt.title('Baseline Filter')
        plt.subplot(4,1,2)
        plt.plot(f_filt, 20*np.log10(abs(H_notch)))
        plt.title('Notch Filter')
        plt.subplot(4,1,3)
        plt.plot(f_filt, 20*np.log10(abs(H_lpf)))
        plt.title('Low Pass Filter')
        plt.subplot(4,1,4)
        plt.plot(f_filt, 20*np.log10(abs(H_baseline*H_notch*H_lpf)))
        plt.title('All combined')
        
        
        
    if plot_signal_ffts == True:
        nfft = 1024;
        fft_raw = abs(fft(ecg_lead, nfft))
        fft_baseline = abs(fft(baseline, nfft))
        fft_notch = abs(fft(notch, nfft))
        fft_lpf = abs(fft(lpf, nfft))
        
        f_fft = sf/2*np.linspace(0, 1, nfft/2+1)
        
        plt.figure()
        plt.hold(True)
        plt.plot(f_fft, 20*np.log10(fft_raw[0:len(f_fft)]))
        plt.plot(f_fft, 20*np.log10(fft_baseline[0:len(f_fft)]))
        plt.plot(f_fft, 20*np.log10(fft_notch[0:len(f_fft)]))
        plt.plot(f_fft, 20*np.log10(fft_lpf[0:len(f_fft)]))
        
        
        
    return lpf
    
