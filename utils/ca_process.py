import numpy as np
from settings.settings import neuropil_correction, cells_only
import os

def load_s2p_files(dp_s2p, neuropil_cor=neuropil_correction):
    """ this function loads the suite2p output files 
    #can refine this to load only a subset of files 
    https://mouseland.github.io/suite2p/_build/html/outputs.html 
    Parameters: s2p datapath, neuropil correction value (if 0, do no correction) 
    Returns:F, Spks, ops,iscell,stat,Fneu """ 
    
    os.chdir(dp_s2p)
    F = np.load('F.npy')
    Spks = np.load('Spks.npy')
    ops = np.load('ops.npy', allow_pickle=True).item() #from the suite2p github 
    iscell = np.load('iscell.npy') #first col is binary yes or no and second col is prob. classifier that is cell 
    stat = np.load('stat.npy', allow_pickle=True)
    Fneu = np.load('Fneu.npy')

    if neuropil_cor > 0: 
        F = F-Fneu*neuropil_cor
        for idx,i in enumerate(F): 
            F[idx] = i-np.min(i)
    return F, Spks, ops,iscell,stat,Fneu

def preprocess_imaging(dp_s2p, mode):
    """ 'Gives you dff for cells of interest and stim triggers 
    Paramters: iscell, F, stat, FOVsizeum, dp_StimF, mode (median or 10% median dff)
    Returns: FNc, iscell_list, x,y, StimFs
    
    '"""
    F, Spks, ops,iscell,stat,Fneu = load_s2p_files(dp_s2p)

    if cells_only:
        iscell_list = get_curated_cells(iscell) ###################
        Fc = F[iscell_list] 
    else:
        Fc = F
        iscell_list = np.arange(len(F))
    if mode == 'median':
        FNc = dff_median(Fc)
    elif mode == '10': 
        FNc = dff_10percent(Fc)
    coords = get_cell_centroids(stat, iscell_list)
    return FNc, iscell_list, coords

def dff_10percent(traces): 
    """ this function calculates the dff using the 10% median method for the baseline.
    Refer to: https://www.scientifica.uk.com/learning-zone/how-to-compute-%CE%B4f-f-from-calcium-imaging-data
    Parameters: traces (raw fluorescecnce from suite2p)
    Returns: ΔF/F (cells x frames) """
    a = np.empty_like(traces) 
    k = int(len(traces[0])/10)
    for idx,i in enumerate(traces): 
        bsl = np.median(i[np.argpartition(i, k)[:k]])
        a[idx] = (i-bsl)/bsl
    return a

def dff_median(traces): 
    """ this function calculates the dff using the median method for the baseline.
    Parameters: traces (raw fluorescecnce from suite2p)
    Returns: ΔF/F (cells x frames) """
    a = np.empty_like(traces) 
    k = int(len(traces[0])/10)
    for idx,i in enumerate(traces): 
        bsl = np.median(i)#[np.argpartition(i, k)[:k]])
        a[idx] = (i-bsl)/bsl
    return a

def get_cell_centroids(stat, index_list):
    #this function finds the x and y centroids from the stat file from suite2p 
    coords = np.array([(stat[i]['med'][1], stat[i]['med'][0]) for i in index_list])
    return coords.T  # shape will be (2, N) - {x, y} for each cell

def get_curated_cells(iscell): 
    """ this function returns the indices of the cells that are curated (iscell[:,0] == 1)
    Parameters: iscell (from suite2p)
    Returns: indices of curated cells """
    if cells_only:
        sorted=np.where(iscell[:,0] == 1)[0]
    else:
        sorted = np.arange(len(iscell))
    return sorted

