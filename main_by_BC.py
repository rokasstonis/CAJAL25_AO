import harp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# %%
# pip install harp-python
# pip install matplotlib

DATA_ROOT = (r"C:\Users\Phd Programme\Downloads\data")
reader = harp.create_reader(DATA_ROOT / "behavior.harp", keep_type=True)

# %% Goals for analysis
# 1. Plot trial trajectory
# 2. Plot speed vs distance
# 3. Check 2p frame time
# 4. Check camera frame time
# 5. Time of reward


# %% Trial Trajectory + Time of reward

trial_number = pd.read_csv(DATA_ROOT / "trial-number0.csv")
current_position = pd.read_csv(DATA_ROOT / "current-position.csv")

max_trial = trial_number["Value"].values[-1]

reward_delivery = reader.OutputSet.read()
reward_delivery = reward_delivery[reward_delivery["MessageType"] == "WRITE"]["SupplyPort0"]
#print(reader.OutputSet.read())

plt.figure()
for i_trial in range(max_trial - 1):
    trial_ts = trial_number.loc[i_trial]["Seconds"]
    trial_p1_ts = trial_number.loc[i_trial + 1]["Seconds"]
    # Add trial position
    slice = (current_position["Seconds"].values > trial_ts) \
        & (current_position["Seconds"].values < trial_p1_ts)
    trial_position = current_position[slice]

    plt.plot(trial_position["Seconds"] - trial_ts, trial_position["Value"], color="k")

    # Add water reward
    #print(trial_ts)
    #print(reward_delivery.index.values)
    slice_rwd = (reward_delivery.index.values > trial_ts) & (reward_delivery.index.values < trial_p1_ts)
    trial_reward_delivery = reward_delivery[slice_rwd]

    plt.scatter(trial_reward_delivery.index.values - trial_ts, (trial_reward_delivery.index.values * 0) + 15)

plt.xlabel("Time second trial start (s)")
plt.ylabel("Position (cm)")
plt.show()

# %% 3. Check 2p frames

di = reader.DigitalInputState.read()
di = di[di["MessageType"] == "EVENT"]["DI3"]
frame_times = di[di == True]
plt.figure()
plt.plot(np.diff(frame_times.index.values))
plt.xlabel("Frame Number")
plt.ylabel("Inter frame interval (s)")
plt.show()

# %% 4. Check camera frames

cam0 = reader.Camera0Frame.read()
cam0 = cam0[cam0["MessageType"] == "EVENT"]
plt.figure()
plt.plot(np.diff(cam0.index.values))
plt.xlabel("Frame Number")
plt.ylabel("Inter frame interval (s)")
plt.show()