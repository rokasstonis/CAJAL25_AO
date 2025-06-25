from scipy.ndimage import gaussian_filter
from scipy import stats
import numpy as np

FNc_s = np.array([gaussian_filter(i, sigma =sig) for i in FNc]) #just smoothed dff
z_FNc = stats.zscore(FNc_s, axis=1)


def interpolation(arr_3d,):
    result=np.zeros_like(arr_3d)
    for i in range(arr_3d.shape[0]):
        for j in range(arr_3d.shape[1]):
            arr=arr_3d[i,j,:]
            # If all elements are nan then cannot conduct linear interpolation.
            if np.sum(np.isnan(arr))==arr.shape[0]:
                result[i,j,:]=arr
            else:
                # If the first elemet is nan, then assign the value of its right nearest neighbor to it.
                if np.isnan(arr[0]):
                    arr[0]=arr[~np.isnan(arr)][0]
                # If the last element is nan, then assign the value of its left nearest neighbor to it.
                if np.isnan(arr[-1]):
                    arr[-1]=arr[~np.isnan(arr)][-1]
                # If the element is in the middle and its value is nan, do linear interpolation using neighbor values.
                for k in range(arr.shape[0]):
                    if np.isnan(arr[k]):
                        x=k
                        x1=x-1
                        x2=x+1
                        # Find left neighbor whose value is not nan.
                        while x1>=0:
                            if np.isnan(arr[x1]):
                                x1=x1-1
                            else:
                                y1=arr[x1]
                                break
                        # Find right neighbor whose value is not nan.
                        while x2<arr.shape[0]:
                            if np.isnan(arr[x2]):
                                x2=x2+1
                            else:
                                y2=arr[x2]
                                break
                        # Calculate the slope and intercept determined by the left and right neighbors.
                        slope=(y2-y1)/(x2-x1)
                        intercept=y1-slope*x1
                        # Linear interpolation and assignment.
                        y=slope*x+intercept
                        arr[x]=y
                result[i,j,:]=arr
    return result

def behaviour_pre_processing(dp_behav, StimFs, y_start, y_end): 
    os.chdir(dp_behav)
    Mouse_ID, Date = grab_file_info(dp_behav)
    behaviour_data = fully_sorted_data(dp_behav, Date)    
    behav_trial_lengths, behav_trials = behaviour_trial_function_1Map(behaviour_data, 1)
    img_trial_lengths = get_imaging_trial_lengths(StimFs)
    re_sampled_behav = re_sample_behaviour(behav_trials, img_trial_lengths, y_start, y_end)

    behav_speed = []
    for t in behav_trials:
        speed_list = []
        for i in range(20,len(t)):
            speed_list.append((np.max(t[i-20:i])-np.min(t[i-20:i]))*0.5/(20/55))
        speed_list = [speed_list[0]]*20 + speed_list
        behav_speed.append(speed_list)
    re_sampled_speed = re_sample_speed(behav_speed, img_trial_lengths)


    return re_sampled_behav, re_sampled_speed, behav_trial_lengths

def fully_sorted_data(dp_behav, Date):
    os.chdir(dp_behav)
    file_names = [i for i in os.listdir(dp_behav) if os.path.isfile(os.path.join(dp_behav,i)) and Date in i[:6]]
    file_names2 = []
    for x in sorted_nicely(file_names):
        file_names2.append(x)
    data  = []
    for i in file_names2:
        with open(i, 'r') as f:
            this_data = literal_eval('[' + ''.join(f.readlines()) + ']')
        data.append(this_data[0])
    return data 


#PLACE CELL FUNCTIONS 

def new_rate_map(traces, speed, y_start, y_end, binsize, triggers, trial_n, re_sampled_behav):
    tracesc = np.array(traces, copy=True)  
    bins = np.arange(y_start, y_end+binsize, binsize)
    master = np.zeros([len(trial_n), len(tracesc), len(bins)] )
    for tdx, t in enumerate(trial_n): 
        bt = re_sampled_behav[t]
        st = speed[t]
        tt = tracesc[:,triggers[t]:triggers[t+1]]
        dig = np.digitize(bt,bins)
        tt[:, np.where(st < 5)[0]] = np.nan
        master[tdx] = np.array([tt[:,dig == i].mean(axis=1) for i in range(0,len(bins))]).transpose()
    return interpolation(master)