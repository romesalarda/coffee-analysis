import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv("data/simplified_coffee_ratings.csv")

df1 = df[df['country_of_origin'] == 'United States']
df2 = df1[['owner_1', 'flavor', 'cupper_points']]

fig, ax = plt.subplots()
df2.plot('flavor', 'cupper_points', kind='scatter', ax=ax)

clean_df = df2.dropna(subset=['flavor','cupper_points'])
m, b = np.polyfit(clean_df['flavor'], clean_df['cupper_points'], 1)

ax.plot(clean_df['flavor'], m * clean_df['flavor'] + b, color='blue', label = f'Fit: y={m:.2f}x+{b:.2f}')

for k, v in df1.iterrows():
    ax.annotate(v['owner_1'], xy=(v['flavor'],v['cupper_points']))

plt.legend()
plt.show()
