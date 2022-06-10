import mne
import numpy as np
import pandas as pd
from scipy.stats import norm as Normal
from scipy.signal import welch, resample_poly, butter, sosfilt, detrend
from scipy.signal import medfilt2d
from scipy.signal import medfilt
from scipy.ndimage import gaussian_filter 
from scipy.ndimage import gaussian_filter1d 
import gc
import fractions
from numpy.fft import irfft, rfftfreq
from typing import List, Tuple

from tqdm.auto import tqdm
from functools import reduce
import intervaltree



bands = {}
bands['SO'] = (0.5,2)
bands['saw'] = (2,4)
bands['swa'] = (0.5,4)
bands['theta'] = (4,8)
bands['alpha'] = (8,12)
bands['sigma'] = (12,15)
bands['beta'] = (15,35)
bands['gamma_low'] = (30,50)

def smoothX_2D(X,median_x=15,median_y=1,sig=8):
    X = np.array(medfilt2d(X,[median_y,median_x]))
    X = np.array(gaussian_filter(X,sigma=sig))
    return X

def smoothx_1D(x,median_x=15,sig=8):
    x = medfilt(x,median_x)
    x = gaussian_filter1d(x,sigma=sig)
    return x


def find_next(x0,x_):
    """
    Find next closest index in x_ after x0.
    x0 and x_ are positive integer indices of some data. 
    """
    x_ = np.array(x_)
    dx_ = x_ - x0
    ## Possible next are positive x2_.
    ind = dx_>0
    ## Filter dx_ to only positives integers.
    dx_ = dx_[ind]
    ## Find min of the positives.
    ix = dx_.argmin()    
    ## Apply same filter to x_
    x_ = x_[ind]
    return x_[ix]


def get_intervals(t_,x_,tol=30): #x is a binary state vector
    """
    Returns intervals using binary state vector x and matching time vector t.
    

    """

    ###
    ##Find starts by using diff, where this is equal to one indicates a start. Add zero index if starting in positive state.
    ##starts_ are start indices
    ###
    if x_[0] == 1:
        x_ = np.diff(x_)
        starts_ = [0] + list(np.where(x_==1)[0]) 
    else:
        x_ = np.diff(x_)
        starts_ = list(np.where(x_==1)[0])
    ###
    ##Now get stop indices. These are places where x (diff(x) of original x) is minus 1. 
    ###
    stops_ = np.where(x_==-1)[0]
    ###
    ##Match start with stop for each interval.
    ###
    intv_ = []
    for i in np.arange(len(starts_)):
        x0 = starts_[i]
        try: 
            x1 = find_next(x0,stops_) 
            intv_.append((x0,x1))
        #there may not be a stop epoch, in that case append the length of the series
        except: 
            intv_.append((x0,len(x_)))
    ###
    ##Now merge close-by intervals by adding a tolerance on the end of each interval. 
    ##This may produce overlaps, and overlapping intervals will be merged. 
    ##Note merging is done in t-space. (In the case of sleep PSG, we are using 30-s epochs as units.)
    ###
    tintv_ = []
    for intv in intv_:
        t0 = t_[intv[0]]
        t1 = t_[intv[1]] + tol
        tintv_.append((t0,t1))

    tree = intervaltree.IntervalTree.from_tuples(tintv_)
    tree.merge_overlaps()
    tree = list(tree)
    #extract from tree and remove extra epochs
    tintv_ = []
    for i in range(len(tree)):
        t0 = tree[i][0]
        t1 = tree[i][1] - tol
        tintv_.append((t0,t1))
    return tintv_

def package_spec(a,eye=False):
    df_ = []

    dftod = pd.DataFrame(a.ToD)
    dftod.columns = ['ToD']
    df_.append(dftod)


    df0 = pd.DataFrame(a.stage)
    df0.columns = ['stage']
    df_.append(df0)

    if eye:
        df1 = pd.DataFrame(a.corr_eye)
        df1.columns = ['corr_eye']
        df_.append(df1)

    c_ = [f"osc_{np.round(freq,2)}" for freq in a.irasa_freqs]
    df2 = pd.DataFrame(a.Xosc.T)
    df2.columns = c_
    df_.append(df2)

    c_ = [f"ap_{np.round(freq,2)}" for freq in a.irasa_freqs]
    df3 = pd.DataFrame(a.Xap.T)
    df3.columns = c_
    df_.append(df3)

    # df_ = [df0,df1,df2,df3]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,
                        left_index=True,right_index=True,
                        how='outer'), df_)
    return df_merged


def irasa(x,sf,bandpass=None,win_sec=4,h_=np.linspace(1.01,1.5,5)):
    r"""
    Notes:
        1. When resampling, the self-affine property theoretically 
            gives a rescaled spectra, with scaling h^H. 
            By taking the product of the reciprocal pairs this gets factored out. 
            Thus, we don't need to know H or both rescaling with h^H. 

        2. Assumes no missing data. Data is regulary sampled.

        3. IRASA can produce artifactual negative peaks in the osc spectra. 
            These may be, also, artificially anti-correlated with their originating peak counterparts.
            This is a limitation of using reciprocal up, down pairs. 

    Use of scipy.signal.poly_ for resampling comes from YASA implementation.
    Citation:
    Vallat, Raphael, and Matthew P. Walker. 
    “An open-source, high-performance tool for automated sleep staging.” 
    Elife 10 (2021). doi: https://doi.org/10.7554/eLife.70092

    

    """
    kwargs_welch = dict(average='median', window='hamming',scaling='spectrum')
    # x = detrend(x)
    # print(len(x))
    ## 
    freqs, psd_raw = welch(x, sf, nperseg=int(sf*win_sec), **kwargs_welch)#,nfft=int(sf*win_sec))
    cross_spect = np.zeros((len(h_),len(psd_raw)))
    for i,h in enumerate(h_):
        # print(h)
        h = np.round(h,4)
        # Get the upsampling/downsampling (h, 1/h) factors as integer
        rat = fractions.Fraction(str(h))
        up, down = rat.numerator, rat.denominator
        data_up = resample_poly(x, up, down, axis=-1)
        data_down = resample_poly(x, down, up, axis=-1)
        # try:
        # Calculate the PSD using same params as original
        freqs_up, psd_up = welch(data_up, h * sf, nperseg=int(sf*win_sec), **kwargs_welch)#,nfft=int(sf*win_sec))
        freqs_dw, psd_dw = welch(data_down, sf / h, nperseg=int(sf*win_sec), **kwargs_welch)#,nfft=int(sf*win_sec))
        # print((len(data_up),len(data_down)))
        # Geometric mean of h and 1/h
        cross_spect[i, :] = np.sqrt(psd_up * psd_dw)
        # except:
        #     print((len(x),rat,len(data_up),len(data_down)))
    psd_aperiodic = np.median(cross_spect,0)
    psd_osc = psd_raw - psd_aperiodic
    
    return freqs, psd_raw, psd_aperiodic, psd_osc

def mneannot_2_dfstg(annot_mne,raw_mne,dic_stg2num):
    ## initialize dfstg from t0 to end of recording (30-s epochs), 
    ## initialize all stages as wake
    ## then iterate through annotations and replace wake stages in dfstg 
    t0 = raw_mne.info['meas_date']
    t1 = t0 + pd.to_timedelta(raw_mne.times[-1], unit='s')
    t_ = pd.date_range(start=t0,end=t1,freq='30S')
    dfstg = pd.DataFrame(columns=['datetime','epoch','seconds','stage'])
    dfstg['datetime'] = t_
    dfstg['epoch'] = dfstg.index.copy()
    dfstg['seconds'] = dfstg.epoch*30
    dfstg.index = dfstg.datetime
    dfstg = dfstg.drop('datetime',axis=1)
    dfstg.stage = -1

    for i in range(len(annot_mne)):
        s0 = annot_mne.onset[i]
        s1 = s0 + annot_mne.duration[i]
        dfstg.loc[(dfstg.seconds>=s0)&(dfstg.seconds<s1),'stage'] = dic_stg2num[annot_mne.description[i]]
    return dfstg


class irasa_spectrogram:
    
    def __init__(self,**kwargs):
        self.raw = kwargs.get('raw_mne')
        self.ch = kwargs.get('ch','Fz')
        self.epoch_mask = kwargs.get('epoch_mask',None)
        self.dfstg = kwargs.get('dfstg',None)
        self.conj_eye = kwargs.get('conj_eye',False)
        self.epoch_sec = kwargs.get('epoch_sec',30)
        self.win_sec = kwargs.get('win_sec',4)
        self.h_ = kwargs.get('h_',np.linspace(1.01,1.5,5))
    
    def gentime(self,raw):
        t0 = pd.to_datetime(raw.info['meas_date'], utc=True)
        t1 = t0 + pd.to_timedelta(raw.times[-1], unit='s')
        sf = raw.info['sfreq']
        t_ = pd.date_range(start=t0,end=t1,freq=f'{1/sf}S')
        return t_

    def irasa_alltime(self):
        sf = self.raw.info['sfreq']
        x = self.raw[self.ch][0][0,:] * 1e6 
        self.irasa_freqs, self.irasa_raw, self.irasa_ap, self.irasa_osc = irasa(x,sf=sf,win_sec=self.win_sec)
        return

    def irasa_epoch(self,a):
        epoch = a[0]
        a = a[1]#self.epoched.get_group(epoch)
        self.ToD[epoch-1] = np.datetime64(a.time.values[0],'s')
        # print((epoch,a.time.values[0]))
        # print(len(a))
        ## run IRASA
        self.irasa_freqs, self.irasa_raw, irasa_ap, irasa_osc = irasa(a[self.ch],sf=self.sf,win_sec=self.win_sec,h_=self.h_)
        self.Xap[:,epoch-1] = irasa_ap[:]
        self.Xosc[:,epoch-1] = irasa_osc[:]
        # self.irasa_freqs, irasa_ap, irasa_osc = irasa_yasa(a[self.ch].values,sf=self.sf,win_sec=5,return_fit=False)
        # self.Xap[:,epoch-1] = irasa_ap[0,:]
        # self.Xosc[:,epoch-1] = irasa_osc[0,:]
        if np.shape(self.dfstg)!=():
            self.stage[epoch-1] = a['stage'].mode()[0] ## assume most are unique, if not use first
        if self.conj_eye:
            self.corr_eye[epoch-1] = np.corrcoef(a['LOC'],a['ROC'])[0,1]
        return

    def spectrogram(self):
        self.sf = self.raw.info['sfreq']
        df = pd.DataFrame()
        df['time'] = pd.to_datetime(self.gentime(self.raw),utc=True)
        df[self.ch] = self.raw[self.ch][0][0,:] * 1e6  # Convert data from V to uV - NOTE: MNE automatically converts units to V, thus need to convert back to uV
        if self.conj_eye:
            df['LOC'] = self.raw['LOC'][0][0,:]
            df['ROC'] = self.raw['ROC'][0][0,:]

        # print(type(self.dfstg))
        if np.shape(self.dfstg)!=():
            self.dfstg['time'] = self.dfstg.index.get_level_values('datetime')
            self.dfstg['time'] = pd.to_datetime(self.dfstg['time'],utc=True)
            df = pd.merge_asof(df,self.dfstg,on='time',direction="backward",tolerance=pd.Timedelta("30s"))
            df['stage'] = df['stage'].fillna(-1)
            # assert self.epoch_sec==30, 'Epoch duration must be 30 seconds if combining with staging.'
            
            
        
        df.index = df['time']

        t0 = pd.to_datetime(df.time.values[0])
        df['delta_seconds'] = (pd.to_datetime(df.time.values) - t0).total_seconds()
        df['epoch'] = 1 + (df['delta_seconds']/self.epoch_sec).astype(int)
        
        self.epoched = df.groupby('epoch')

        n = int(0.5*self.sf*self.win_sec) + 1 # n freq bins
        p = df.epoch.max()-1

        # self.epoched = [(epoch,a) for epoch,a in self.epoched]
        self.ToD = np.empty(p,dtype='datetime64[s]')
        self.Xap = np.empty((n,p))
        self.Xosc = np.empty((n,p))
        
        self.Xap[:] = np.nan
        self.Xosc[:] = np.nan
        
        if np.shape(self.dfstg)!=():
            self.stage = np.empty(p)
        if self.conj_eye:
            self.corr_eye = np.empty(p)

    

        del(df)
        gc.collect()

        for epoch,a in tqdm(self.epoched):
            ## only estimate if full epoch - could be less conservative and base this on limits of up/down sample of win_sec*sf
            if len(a)==int(self.epoch_sec*self.sf):
                # print(len(a))
                self.irasa_epoch((epoch,a))
            

       
            
        del(self.epoched,self.dfstg)
        gc.collect()
        return


class syn_1f_signal:
    def __init__(self,**kwargs):
        self.exponent = kwargs.get('exponent',1)
        self.sample_rate = kwargs.get('sample_rate',256)
        self.duration =  kwargs.get('duration',180) #seconds
        self.periodic_params = kwargs.get('periodic_params',None)
        self.aperiodic_signal = 0
        self.full_signal = 0
    def gensignal(self):
        n_samples = int(self.duration * self.sample_rate)
        amps = np.ones(n_samples//2, complex)
        self.freqs = rfftfreq(n_samples, d=1/self.sample_rate)
        self.freqs = self.freqs[1:]  # avoid divison by 0

        # Create random phases
        rand_dist = np.random.uniform(0, 2*np.pi, size=amps.shape)
        rand_phases = np.exp(1j * rand_dist)

        # Multiply phases to amplitudes and create power law
        amps *= rand_phases
        amps /= self.freqs ** (self.exponent / 2)

        # # Create colored noise time series from amplitudes
        self.aperiodic_signal = irfft(amps)
        self.full_signal = self.aperiodic_signal.copy()
        
        ## Add oscillations if period_params

        if self.periodic_params:
            for theta in self.periodic_params:
                freq_osc, amp_osc, width = theta
                amp_dist = Normal(freq_osc, width).pdf(self.freqs)
                # add same random phases
                amp_dist = amp_dist * rand_phases
                amps += amp_osc * amp_dist
            self.full_signal = irfft(amps)
        return
