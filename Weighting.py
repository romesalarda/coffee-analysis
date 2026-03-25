import pandas as pd
import numpy as np
import Filtering as filtering
from Filtering import getListOfCountries


def get_scoring(df):
    total_score = pd.Series(0, index=df.index)
    total_score += np.where(df['species'] == 'Robusta', 0.9, 1.0)
    total_score += np.where(df['uniformity'] >= 8, df['uniformity'] * 1.75, df['uniformity'].fillna(0))
    total_score += np.where(df['flavor'] >= 7.5, df['flavor'] * 1.5, df['flavor'].fillna(0))
    total_score += np.where(df['aroma'] >= 7, df['aroma'] * 1.25, df['aroma'].fillna(0))
    cols_to_exclude = ['species', 'uniformity', 'flavor', 'aroma', 'number_of_bags']
    other_nums = df.drop(columns = cols_to_exclude).select_dtypes(include = [np.number])
    total_score += other_nums.mean(axis=1)
    return total_score

'''Gets the score for each country by grouping them'''
def get_country_score(df):
    totals = (df.groupby('country_of_origin')['final_score']
              .mean()
              .sort_values(ascending=False)
              .head(10))
    return list(totals.items())
df = pd.read_csv("data/simplified_coffee_ratings.csv")
df['final_score'] = get_scoring(df)

# for score in df['final_score']:
    # print(score)
