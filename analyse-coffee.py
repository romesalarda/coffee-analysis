import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import Filtering as filtering
import Weighting as weighting

def setup_dataFrame(df, min_producers = 3):
    df2 = filtering.filterNAColumn(df, ['country_of_origin', 'processing_method', 'aroma',
                      'flavor','body','uniformity','cupper_points'])
    df3 = filtering.filterByNumOfProducers(df2, min_producers)
    df4 = filtering.filterByColumnValue(df3, 'processing_method', "Washed / Wet")
    score_column = weighting.get_scoring(df4)
    df4['final_score'] = score_column
    return df4

def getBestCoffee(df, per_country_producers = 10, number_of_countries = 10):
    df4 = setup_dataFrame(df)
    packaging = weighting.get_country_score(df4, per_country_producers, number_of_countries)
    return packaging

def getBestProducerInCountry(df, country):
    clean_df = setup_dataFrame(df)
    df2 = clean_df[df['country_of_origin'] == country]
    max_value = df2['final_score'].idxmax()
    producer = df2.loc[max_value, 'farm_name']
    score = df2.loc[max_value, 'final_score']
    return producer, score

df = pd.read_csv("data/simplified_coffee_ratings.csv")
df10 = getBestCoffee(df, 10, 10)
for (country, score) in df10:
    print(country, score)
print("Best Producer")
(producer, score) = getBestProducerInCountry(df, df10[0][0])
print(producer, score)

