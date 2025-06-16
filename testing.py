from utils.generate_yaml import generate_yaml_file
import numpy as np

length = 10  # or any desired length
mXLocationPixels = np.random.randint(0, 513, length)
mYLocationPixels = np.random.randint(0, 513, length)


generate_yaml_file(mXLocationPixels, mYLocationPixels, 10, 15)