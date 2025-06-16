from pathlib import Path
from datetime import date


base_dir = Path(r"C:\Users\Phd Programme\Documents\CAJAL25\Experiments")
exp_dir = base_dir / "Test_Experiment"
output_dir = base_dir / date.today().strftime('%Y-%m-%d')