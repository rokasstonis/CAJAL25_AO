import numpy as np
from pathlib import Path
from settings.settings import imaging_frame_rate

def get_stim_frames(txt_file):
    data = np.loadtxt(txt_file)
    timestamps = data[:, 0]
    values = data[:, 1]
    stim_onsets = np.where(values > 0)[0]

    frames = convert_to_frames(stim_onsets, frame_rate=imaging_frame_rate)

    return frames


def convert_to_frames(timestamps, frame_rate=43.2):
    """
    Convert timestamps in ms to frame indices based on the given frame rate.
    """
    frame_rate = 43.2  # Hz
    return np.round(timestamps/1000 * frame_rate).astype(int)


# timestamps, values = load_stim_triggers(stim_trigs)

# stim_onsets = np.where(values > 0)[0]

# print()

