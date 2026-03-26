import pandas as pd
import numpy as np
import Filtering as filtering
from Filtering import getListOfCountries


def get_scoring(df, otherColumnMultiplier = 1, uniformity_multiplier = 1.75, flavor_multiplier = 1.5, aroma_multiplier = 1.25, species_multiplier = 0.9):
    """
    Calculates a score for each producer by weighting certain columns higher than others.

    :param df: The dataframe that stores the csv you want to score
    :param otherColumnMultiplier: the multiplier for any column that is a number and isn't one of the special columns provided, defaults to 1
    :param uniformity_multiplier: the multiplier for the uniformity, increase this to weight more heavily, defaults to 1.75
    :param flavor_multiplier: the multiplier for the flavour, increase this to weight more heavily, defaults to 1.5
    :param aroma_multiplier: the multiplier for the aroma, increase this to weight more heavily, defaults to 1.25
    :param species_multiplier: the multiplier for species, decrease to weight more heavily high caffeine, defaults to 0.9
    :return: returns a total score for each producer in a column, this can then be added to another dataframe
    """
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
    """
    Gets the scores for each country from the 'final score' column. And then averages them across producers before pairing this average with the country.

    :param df: The current dataframe being worked on.
    :param producer_per_country: The number of producers per country, you want to consider. E.g if this is set to 10, the top ten producers will be used to make decisions about the country. Defaults to 10
    :param number_of_countries: The number of countries you want to return, defaults to 10.
    :return: Returns a list of tuples (country, score) where country is the name of the country and its associated score
    """
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
