# -*- coding: utf-8 -*-
"""
Created on 2018 Jul 6 

GLIA ECG FILTER PARAMETERS

Copyright (C) 2018 Luka Banovic <banovic@irnas.eu>

These functions generate good filter parameters for Glia ECG signal filtering.

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

from scipy.signal import cheby2
from iirnotch import design_notch_peak_filter

sf = 488
sf2 = sf/2

NFFT = 1024
#%% DC, Baseline filter, 

def baseline_filter( order, ripple, fc, sf):
    """
    Type - II Chebyshev filter acts as a baseline filter and DC filter.
    
    ripple = attenuation in dB at cutoff frequency
    fc = cutoff frequency in Hz
    sf = sampling frequency in Hz
    
    """
    b, a = cheby2(order, ripple, fc/sf, 'high')

    return b, a

#%% Notch filter

def notch_filter( notch_freq, sf, Q):
    """
    
    Notch IIR filter for mains noise removal. 
    
    notch_freq = notch frequency in Hz
    sf = sampling frequency
    Q = quality factor of IIR filter.
    
    """
    sf2 = sf/2.
    w0 = notch_freq/sf2
    
    b, a = design_notch_peak_filter(w0, Q, 'notch')
    return b, a

#%% Low pass filter

def low_pass_filter( order, ripple, fc, sf):
    """
    Low pass Chebyshev Type II IIR filter.
    
    order = filter order
    ripple = attenuation in dB at cutoff frequency
    fc = cutoff frequency
    sf = sampling frequency
    
    """
    b, a = cheby2(order, ripple, fc/sf, 'low')
    return b, a 