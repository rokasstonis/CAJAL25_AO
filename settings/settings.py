from pathlib import Path
from datetime import date

#change to your experiment folder
base_dir = Path(r"C:\Users\Phd Programme\Documents\CAJAL25\Experiments")


data_dir = base_dir / date.today().strftime('%Y-%m-%d')