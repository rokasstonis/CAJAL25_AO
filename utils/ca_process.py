import numpy as np
import os

def load_s2p_files(dp_s2p, neuropil_correction):
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

    if neuropil_correction > 0: 
        F = F-Fneu*neuropil_correction
        for idx,i in enumerate(F): 
            F[idx] = i-np.min(i)
    return F, Spks, ops,iscell,stat,Fneu

def preprocess_imaging(iscell, F, stat, FOVsizeum, mode):
    """ 'Gives you dff for cells of interest and stim triggers 
    Paramters: iscell, F, stat, FOVsizeum, dp_StimF, mode (median or 10% median dff)
    Returns: FNc, iscell_list, x,y, StimFs
    
    '"""
    iscell_list = get_curated_cells(iscell)
    Fc = F[iscell_list] 
    if mode == 'median':
        FNc = dff_median(Fc)
    elif mode == '10': 
        FNc = dff_10percent(Fc)
    x, y = get_cell_centroids(stat, iscell_list)
    xa = [i*(FOVsizeum/512) for i in x]
    yb = [i*(FOVsizeum/512) for i in y]
    return FNc, iscell_list, xa,yb, x,y

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
    x,y = zip(*[(stat[i]['med'][1], stat[i]['med'][0]) for i in index_list])
    return x,y

def get_curated_cells(iscell): 
    return np.where(iscell[:,0] == 1)[0]

