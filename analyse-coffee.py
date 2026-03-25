import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import Filtering as filtering
import Weighting as weighting

def setup_dataFrame(df):
    df2 = filtering.filterNAColumn(df, ['country_of_origin', 'processing_method', 'aroma',
                      'flavor','body','uniformity','cupper_points'])
    df3 = filtering.filterByNumOfProducers(df2, 3)
    df4 = filtering.filterByColumnValue(df3, 'processing_method', "Washed / Wet")
    score_column = weighting.get_scoring(df4)
    df4['final_score'] = score_column
    return df4

def getBestCoffee(df):
    df4 = setup_dataFrame(df)
    packaging = weighting.get_country_score(df4)
    return packaging

def getBestProducerInCountry(df, country):
    clean_df = setup_dataFrame(df)
    df2 = clean_df[df['country_of_origin'] == country]
    max_value = df2['final_score'].idxmax()
    producer = df2.loc[max_value, 'farm_name']
    score = df2.loc[max_value, 'final_score']
    return producer, score

df = pd.read_csv("data/simplified_coffee_ratings.csv")
df10 = getBestCoffee(df)
for (country, score) in df10:
    print(country, score)
print("Best Producer")
(producer, score) = getBestProducerInCountry(df, df10[0][0])
print(producer, score)
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
