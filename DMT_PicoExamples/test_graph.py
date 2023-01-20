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

df = pd.DataFrame()

# iterate over the dictionary, adding the data for each channel to the dataframe
for channel, data in temp_info.items():
    channel_df = pd.DataFrame(data)
    channel_df['Channels'] = channel
    df = pd.concat([df, channel_df])

# reshape the dataframe, so that the channels are in a single column
df = pd.melt(df, id_vars=['Channels'], value_vars=['Temperatures', 'Time Intervals'])

print(df)

# use seaborn's lineplot function to plot the data
sns.lineplot(x='variable', y='value', hue='Channels', data=df)

# add labels and a title
plt.title('Temperature over Time Interval')
plt.xlabel('Time Interval')
plt.ylabel('Temperature')
plt.show()