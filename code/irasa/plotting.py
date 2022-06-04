

from matplotlib import rc
from matplotlib import rcParams
import matplotlib.pyplot as plt
plt.ion()
import seaborn as sns
from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd

# rcParams['axes.facecolor'] = 'white'

def simpleaxis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

def plot_style(fs=14,figsize=(10,5)):
    font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : fs}
    rc('font', **font)
    rcParams['axes.spines.right'] = False
    rcParams['axes.spines.left'] = False
    rcParams['axes.spines.bottom'] = False
    rcParams['axes.spines.top'] = False
    rcParams["figure.figsize"] = figsize

def plot_w_ptlab(x,y,ptlab,color=None,xlab=None,ylab=None,fs=10,ax=None,label=None):
    if len(color)>0:
        ax.plot(x,y,'o',color=color,label=label)
    else:    
        ax.plot(x,y,'.')
    for i in range(len(ptlab)):
        ax.annotate(ptlab[i],xy=(x[i],y[i]),fontsize=fs)
    if xlab:
        ax.set_xlabel(xlab)
    if ylab:
        ax.set_ylabel(ylab)

def plot_montage(lm): #lm is path/name of luna montage with columns ch, x, y, z (no header)
    DF = pd.read_csv(lm,sep='\t')
    ax = plt.axes(projection='3d')
    ax.plot3D(DF['x'],DF['y'],DF['z'])
    for i, txt in enumerate(DF['ch']):
        ax.text(DF['x'].iloc[i], DF['y'].iloc[i],DF['z'].iloc[i],txt)
    return