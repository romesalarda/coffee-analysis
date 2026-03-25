import pandas as pd
import numpy as np
import Filtering as filtering
from Filtering import getListOfCountries


def get_scoring(df):
    total_score = pd.Series(0, index=df.index)
    total_score += np.where(df['species'] == 'Arabica', 1.25, 1.0)
    total_score += np.where(df['uniformity'] >= 8, df['uniformity'] * 1.75, df['uniformity'].fillna(0))
    total_score += np.where(df['flavor'] >= 7.5, df['flavor'] * 1.5, df['flavor'].fillna(0))
    total_score += np.where(df['aroma'] >= 7, df['aroma'] * 1.25, df['aroma'].fillna(0))
    cols_to_exclude = ['species', 'uniformity', 'flavor', 'aroma']
    other_nums = df.drop(columns = cols_to_exclude).select_dtypes(include = [np.number])
    total_score += other_nums.sum(axis=1)
    return total_score

def get_country_score(df):
    totals = (df.groupby('country_of_origin')['final_score']
              .mean()
              .sort_values(ascending=False)
              .head(10))
    return list(totals.items())