import pandas as pd
import numpy as np
import Filtering as filtering
from Filtering import getListOfCountries


def get_scoring(df, otherColumnMultiplier = 1, uniformity_multiplier = 1.75, flavor_multiplier = 1.5, aroma_multiplier = 1.25, species_multiplier = 0.9):
    total_score = pd.Series(0, index=df.index)
    total_score += np.where(df['species'] == 'Robusta', species_multiplier, 1.0)
    total_score += np.where(df['uniformity'] >= 0, df['uniformity'] * uniformity_multiplier, df['uniformity'].fillna(0))
    total_score += np.where(df['flavor'] >= 0, df['flavor'] * flavor_multiplier, df['flavor'].fillna(0))
    total_score += np.where(df['aroma'] >= 0, df['aroma'] * aroma_multiplier, df['aroma'].fillna(0))
    cols_to_exclude = ['species', 'uniformity', 'flavor', 'aroma', 'number_of_bags', 'final_weight']
    other_nums = df.drop(columns=cols_to_exclude).select_dtypes(include=[np.number])
    total_score += other_nums.sum(axis=1) * otherColumnMultiplier
    return total_score


def get_country_score(df, producer_per_country = 10, number_of_countries = 10):
    totals = (df.groupby('country_of_origin')['final_score']
              .nlargest(producer_per_country)
              .groupby(level=0)
              .mean()
              .sort_values(ascending=False)
              .head(number_of_countries)
              )
    return list(totals.items())

# for score in df['final_score']:
# print(score)
