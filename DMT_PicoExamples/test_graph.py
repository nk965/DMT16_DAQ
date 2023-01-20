import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

temp_info = {
  "CHANNEL_1": {
    "Temperatures": [12.4, 13.5, 14.7],
    "Time Intervals": [200, 400, 600],
  },
  "CHANNEL_2": {
    "Temperatures": [12, 11.2, 10.5],
    "Time Intervals": [200, 468, 668],
  } 
}

fig, ax = plt.subplots()
for channel, data in temp_info.items():
    df = pd.DataFrame({'Time Intervals':data['Time Intervals'], 'Temperatures':data['Temperatures']})
    ax.plot(df['Time Intervals'], df['Temperatures'], '-o', label=channel)
sns.set_theme(style="darkgrid")
plt.title('Temperature over Time Interval')
plt.xlabel('Time Interval')
plt.ylabel('Temperature')
plt.legend()
plt.show()