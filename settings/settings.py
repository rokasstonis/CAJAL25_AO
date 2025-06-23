from pathlib import Path
from datetime import date


base_dir = Path(r"C:\Users\Phd Programme\Documents\CAJAL25\Experiments")
exp_dir = base_dir / "Test_Experiment"
output_dir = base_dir / date.today().strftime('%Y-%m-%d')

imaging_frame_rate = 43.2  # Hz
FOVsizeum = 574  # Size of the field of view in micrometers
neuropil_correction = 0.7  # Neuropil correction factor
cells_only = True  # If True, only cells are processed; if False, all ROIs are processed

dff_mode = 'median'  # Options: 'median' or '10'