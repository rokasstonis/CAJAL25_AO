from utils.generate_yaml import generate_yaml_file
from utils.trigger_handling import get_stim_frames
import numpy as np

# length = 10  # or any desired length
# mXLocationPixels = np.random.randint(0, 513, length)
# mYLocationPixels = np.random.randint(0, 513, length)


# generate_yaml_file(mXLocationPixels, mYLocationPixels, 10, 15)


stim_trigs=r"C:\Users\Phd Programme\Documents\CAJAL25\Example_data\Stimulation laser modulation waveform (20250618_15_28).txt"

print(get_stim_frames(stim_trigs))