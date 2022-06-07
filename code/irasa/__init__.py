import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
# import seaborn as sns
# from scipy.stats import zscore
# from scipy.signal import welch
# from scipy.signal import detrend
# from scipy.ndimage import gaussian_filter 
# from scipy.signal import medfilt2d
# from scipy.signal import medfilt
import mne
from mne.datasets.sleep_physionet.age import fetch_data
from tqdm.auto import tqdm

# from scipy.ndimage import gaussian_filter1d

# from statsmodels.stats.weightstats import ttest_ind

# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go


# import statsmodels.api as sm
# from scipy.stats import spearmanr



from .util import *
from .plotting import *


## dictionary to convert mne physionet example stages to common digit staging
dic_stg2num = {}
dic_stg2num['Sleep stage W'] = 0
dic_stg2num['Sleep stage 1'] = 1
dic_stg2num['Sleep stage 2'] = 2
dic_stg2num['Sleep stage 3'] = 3
dic_stg2num['Sleep stage 4'] = 3
dic_stg2num['Sleep stage R'] = 4
dic_stg2num['Sleep stage ?'] = -1




