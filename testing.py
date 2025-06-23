from utils.generate_yaml import generate_yaml_file
from utils.trigger_handling import get_stim_frames
from utils.ca_process import preprocess_imaging, interpolate_blanked_periods

from settings.settings import dff_mode, imaging_frame_rate
import matplotlib.pyplot as plt
import numpy as np

# length = 10  # or any desired length
# mXLocationPixels = np.random.randint(0, 513, length)
# mYLocationPixels = np.random.randint(0, 513, length)


# generate_yaml_file(mXLocationPixels, mYLocationPixels, 10, 15)


stim_trigs=r"C:\Users\Phd Programme\Documents\CAJAL25\Example_data\Stimulation laser modulation waveform (20250618_15_28).txt"

# print(get_stim_frames(stim_trigs))

dp_s2p = r'C:\Users\Phd Programme\Documents\CAJAL25\Example_data\StimRSP\suite2p\plane0'

FNc, iscell_list, coords= preprocess_imaging(dp_s2p, 'median')

print(FNc.shape)



#create a stim frame bool mask
stim_frames = get_stim_frames(stim_trigs)

stim_mask = np.ones(FNc.shape[1], dtype=bool)
stim_mask[stim_frames] = False


interpolated_traces = interpolate_blanked_periods(FNc, stim_mask) #plotting only!!!! - maybe don't do it here

plt.plot(FNc[20])
inverse_mask = ~stim_mask
for i in inverse_mask.nonzero()[0]:
    plt.axvline(x=i-2, color='r', linestyle='--')
plt.show()


plt.plot(interpolated_traces[20])
inverse_mask = ~stim_mask
for i in inverse_mask.nonzero()[0]:
    plt.axvline(x=i-2, color='r', linestyle='--')
plt.show()

num_rois, num_timepoints = FNc.shape

plt.figure(figsize=(12, num_rois * 1))


offset = 5  

for i in range(num_rois):
    
    plt.plot(FNc[i] + i * offset, label=f'ROI {i+1}')

plt.xlabel(f'Frames {imaging_frame_rate} Hz')
plt.ylabel('ΔF/F')
plt.yticks([]) 
plt.tight_layout()
plt.show()


# num_traces = interpolated_traces.shape[0]
# fig, axes = plt.subplots(num_traces, 1, figsize=(10, 2 * num_traces), sharex=True)

# if num_traces == 1:
#     axes = [axes]

# # Find contiguous periods where stim_mask is False
# stim_off = ~stim_mask
# starts = np.where(np.diff(np.concatenate(([0], stim_off.astype(int)))) == 1)[0]
# ends = np.where(np.diff(np.concatenate((stim_off.astype(int), [0]))) == -1)[0]

# for i, ax in enumerate(axes):
#     ax.plot(interpolated_traces[i])
#     ax.set_ylabel(f'Trace {i}')
#     ax.grid(True)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.set_title('')  # Remove any title

#     # Add red blocks for stim off periods
#     for start, end in zip(starts, ends):
#         ax.axvspan(start, end, color='red', alpha=0.5)

# axes[-1].set_xlabel('Frame')
# plt.tight_layout()
# plt.show()

print (interpolated_traces.shape)