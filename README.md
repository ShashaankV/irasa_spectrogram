# irasa_spectrogram

Extension of the [IRASA method](#refs) for time-varying spectral analyses. 

## Description

Time series such as EEG consist of oscillatory- and aperiodic-type activity. These represent different processes of interest. Aperiodic are likened to fractal series and power-law spectra, where there is broad decline in the power spectrum that follows a 1/frequency<sup>x</sup> function. 


IRASA (Irregular Resampling Auto-Spectral Analysis) is a method for taking a raw spectrum and estimating two new spectra - aperiodic and oscillatory spectra. 

In brief, IRASA and other resampling methods use the self-affine property of fractal series where up- or down- sampling such series results in similar statistical properties. A preserved power spectrum is one of these properties. For a purely fractal (w/ aperiodic 1/f spectrum), the spectrum is preserved but with a change in scale. This scale is given by h<sup>H</sup>, where h is the resampling factor and H is called the <a href=https://en.wikipedia.org/wiki/Hurst_exponent target="_blank"></href> Hurst exponent</a>. With a mixed oscillatory and aperiodic signal, up- and down- sampling can be used to shift the osc component while preserving the aperiodic component. Taking the inner product of such shifted spectra results in an attenuation of the osc component while preserving the aperiodic. To achieve this the h<sup>H</sup> scaling factor has to be accounted for. IRASA achieves this by using h, 1/h reciprocal pairs thus canceling the h<sup>H</sup> factor. 

In practice (see /notebook/example.ipynb) this works fairly well based on our predictive modeling results. However, there are some artifacts to be aware off. First, IRASA often adds small artifactual oscillatory peaks to the aperiodic estimate resulting in "negative osc power". These peaks are the "average" of the shifted true osc peaks. Second, there are edge effects. Aperiodic and oscillatory spectra should be analyzed within bands somewhat away from the band limits of the original signal. Near these extrema, baseline artifacts are introduced. This is important to note for preprocessing that uses bandpass filters. We recommend bandpassing after IRASA is implemented.  

<b>Motivation</b> <it>irasa_spectrogram</it> extends the algorithm implemented by [Vallat and Walker](#refs) which was written for a single power spectrum over an entire time seires. We are interested in tracking changes in the oscillatory (and aperiodic) across time. Thus, we extended this method to generate a time-frequency series (aka spectrogram). 
<!-- [insert figure] -->

In addition, the extended methods and parameters used here were motivated by several use cases: examining different stages of sleep, comparing oscillatory bands across sleep, and predicting sleep effects in performance. Thus, we've included methods to align the IRASA spectrograms with conventional sleep staging, compare oscillatory bands, smoothing to enhance signal (validated by [predictive performance](#refs)), etc.  




## Table of Contents

<!-- If your README is long, add a table of contents to make it easy for users to find what they need. -->

- [Installation](#installation)
- [Usage](#usage)
- [References](#refs)



## Installation

<!-- What are the steps required to install your project? Provide a step-by-step description of how to get the development environment running. -->

Install using pip -->
> pip install git+https://github.com/ShashaankV/irasa_spectrogram.git

Troubleshooting:

If pip fails to install then try upgrading pip. Alternatively you can download the source code and add to your path. Note using the source code directly, does not ensure that the other library requirements are installed. 

## Usage

<!-- Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png) -->

<b>Highly recommend going through the examples.ipynb.</b>

The primary implementation involves generating an irasa_spectrogram object. The only required argument is an MNE raw datafile. Optional arguments are:  ch (channel name), epoch_mask (table with binary filter for kept epochs), dfstg (pandas dataframe with scored sleep staging), conj_eye (boolean whether L/R eog is present and whether to calculate conjugate eye-movement), epoch_sec (window in seconds for epoch-level irasa), win_sec (window in sec for Welch-type method for FFT), h_ (array of upsample ratios).

As shown in the examples notebook, an example implementation using physionet data is:

<code>
    
    from irasa import *
    
    ## fetch_data is part of the mne library and should be installed/loaded when you installed irasa_spectrogram
    data = fetch_data(subjects=[3], recording=[1])[0]

    raw = mne.io.read_raw_edf(data[0], stim_channel='Event marker',
                                misc=['Temp rectal'])
    annot = mne.read_annotations(data[1])

    ##  mneannot_2_dfstg is an irasa_spectrogram helper function to get the physionet staging file in the proper format   
    dfstg = mneannot_2_dfstg(annot,raw,dic_stg2num)

    win_sec = 10

    a = irasa_spectrogram(raw_mne=raw,ch='EEG Fpz-Cz',dfstg=dfstg,win_sec=win_sec)

    a.spectrogram()
    
    ## plot the per-epoch normalized oscillatory spectrum
    
    X = a.Xosc

    normbd = (int(0.5*win_sec),int(15*win_sec)+1)
    bdnorm = np.tile(np.sum(X[normbd[0]:normbd[1],:],0),[np.shape(X)[0],1])
    Xn = X/bdnorm

    Xns = smoothX_2D(Xn)

    Xns = Xns[:int(35*win_sec),:]

    freqs = a.irasa_freqs[:int(35*win_sec)]

    plt.imshow(Xns,origin='lower',vmax=1e-2,aspect='auto')#,y=a.irasa_freqs, aspect='auto', color_continuous_scale="thermal",zmax = 1e-2)
    ind_ = np.arange(0,len(freqs),25)
    plt.gca().set_yticks(ind_);
    plt.gca().set_yticklabels(freqs[ind_]);
    plt.xlabel('epoch')
    plt.ylabel('Hz')
    


</code>

## Cite

For citing use:

<b>0094 Oscillatory Theta-Band Activity as a Sleep Stage Independent Measure of REM-like Activity throughout Sleep </b> Shashaank Vattikuti, Thomas Balkin, Allen Braun, Samantha Riedy, Tracy Doty, John Hughes <i>Sleep</i>, Volume 45, Issue Supplement_1, June 2022, Pages A42–A43, https://doi.org/10.1093/sleep/zsac079.092

## Tests


## References

1. Wen, H., & Liu, Z. (2016). Separating Fractal and Oscillatory Components in the Power Spectrum of Neurophysiological Signal. Brain topography, 29(1), 13–26. https://doi.org/10.1007/s10548-015-0448-0
2. Vallat, Raphael, and Matthew P. Walker. “An open-source, high-performance tool for automated sleep staging.” Elife 10 (2021). doi: https://doi.org/10.7554/eLife.70092
3. S Vattikuti, T Balkin, A Braun, S Riedy, T Doty, J Hughes (2022). 0097 REM-like Neural Activity Is Superior to NREM Parameters for Predicting Non-sleep Restricted Vigilance. Sleep 45 (Supplement_1), A43-A44



