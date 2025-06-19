import harp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
reader = harp.create_reader(r'C:\Users\Phd Programme\Documents\CAJAL25\Experiments\ao_stim_test_2025_06_17T17_50_08\ao_stim_test_2025_06_17T17_50_08_HarpBehavior.harp')

dir(reader)

df = reader.DigitalInputState.read()
df_analog = reader.AnalogData.read()

frames = df['DI3'].values.tolist()
time = df['DI3'].index.to_list()

diffs = np.diff(time)


print(diffs)
plt.figure()
plt.plot(diffs)
plt.title("Difference between consecutive frames")
plt.xlabel("Index")
plt.ylabel("Difference")
plt.show()

plt.scatter(time, frames)
plt.show()


print(sum(frames))
print(df_analog.shape) #The analog data time stamps begin when I start the script.

time = df.iloc[:, 0].values.tolist()

frames_analog = df_analog['AnalogInput0'].values.tolist()

plt.plot(time, frames)
plt.show()
print(sum(frames))
print(len(frames))
print(df.head())

