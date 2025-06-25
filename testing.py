from utils.generate_yaml import generate_yaml_file
from utils.trigger_handling import get_stim_frames
from utils.ca_process import preprocess_imaging #, interpolate_blanked_periods

from settings.settings import dff_mode, imaging_frame_rate
import matplotlib.pyplot as plt
import numpy as np

# length = 10  # or any desired length
# mXLocationPixels = np.random.randint(0, 513, length)
# mYLocationPixels = np.random.randint(0, 513, length)


# generate_yaml_file(mXLocationPixels, mYLocationPixels, 10, 15)


dp_s2p = r'C:\Users\TeachingLab\Desktop\behavior-analysis\data\suite2p_outputs_20250625'
FNc, iscell_list, coords, spikes= preprocess_imaging(dp_s2p, 'median')
print(spikes.shape)
plt.figure(figsize=(12, FNc.shape[0]))
offset = 5
for i in range(FNc.shape[0]):
    plt.plot(FNc[i] + i * offset, label=f'ROI {i+1}')
plt.xlabel('Time (frames)')
plt.ylabel('Z-scored dF/F + offset')
plt.title('FNc traces for all ROIs')
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

# print (interpolated_traces.shape)