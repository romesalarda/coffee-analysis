import pytest
import pandas as pd
import Filtering
import Weighting
import os

cwd = os.getcwd()
if "tests" in cwd:
    filepath = "test_data/test_coffee_ratings.csv"
else:
    filepath = "tests/test_data/test_coffee_ratings.csv"
filepath = os.path.join(cwd, filepath)
df = pd.read_csv(filepath)

def test_filterNAColumn():
    clean = Filtering.filterNAColumn(df, ["variety"])
    assert (clean['variety'] == 'NA').sum() == 0
    
def test_get_listOfCountries_single_country():
    df_t= pd.DataFrame({
        "country_of_origin": ["India", "India", "India"],
        "species": ["Robusta", "Robusta", "Robusta"]
    })
    assert Filtering.getListOfCountries(df_t).count() == 1
    
def test_get_listOfCountries_multiple_countries():
    df_t= pd.DataFrame({
        "country_of_origin": ["India", "Brazil", "Turkey"],
        "species": ["Robusta", "Robusta", "Robusta"]
    })
    assert Filtering.getListOfCountries(df_t).count() == 3

def test_filterNumOfProducers_min_1_returns_all_countries():
    df_t = pd.DataFrame({
        "country_of_origin": ["India", "India", "India", "Uganda", "Uganda", "Honduras"],
        "farm_name":         ["farm_a", "farm_b", "farm_c", "farm_x", "farm_y", "farm_z"],
        "species":           ["Robusta", "Robusta", "Robusta", "Robusta", "Robusta", "Arabica"]
    })
    result = Filtering.filterByNumOfProducers(df_t, 1)
    assert set(result["country_of_origin"].unique()) == {"India", "Uganda", "Honduras"}

def test_filterNumOfProducers_min_2_removes_single_producer_country():
    df_t = pd.DataFrame({
        "country_of_origin": ["India", "India", "India", "Uganda", "Uganda", "Honduras"],
        "farm_name":         ["farm_a", "farm_b", "farm_c", "farm_x", "farm_y", "farm_z"],
        "species":           ["Robusta", "Robusta", "Robusta", "Robusta", "Robusta", "Arabica"]
    })
    result = Filtering.filterByNumOfProducers(df_t, 2)
    assert "Honduras" not in result["country_of_origin"].values
    
# Weighting tests
robustadf = pd.DataFrame({
        "species":     ["Robusta"],
        "uniformity":  [6.0],    # < 8, so raw 6.0
        "flavor":      [6.0],    # < 7.5, so raw 6.0
        "aroma":       [6.0],    # < 7, so raw 6.0
        "acidity":     [6.0],
        "body":        [6.0],
        "balance":     [6.0],
        "aftertaste":  [6.0],
        "sweetness":   [6.0],
        "clean_cup":   [6.0],
        "cupper_points": [6.0],
        "moisture":    [0.1],
    })


def test_high_uniformity_bonus():
    high = pd.DataFrame({
        "species": ["Arabica"], "uniformity": [10.0], "flavor": [6.0],
        "aroma": [6.0], "acidity": [6.0], "body": [6.0], "balance": [6.0],
        "aftertaste": [6.0], "sweetness": [6.0], "clean_cup": [6.0],
        "cupper_points": [6.0], "moisture": [0.1], "number_of_bags": [1]
    })
    low = high.copy()
    low["uniformity"] = 6.0  
    assert Weighting.get_scoring(high).iloc[0] > Weighting.get_scoring(low).iloc[0]


def test_high_flavor_bonus():
    high = pd.DataFrame({
        "species": ["Arabica"], "uniformity": [10.0], "flavor": [8.0],
        "aroma": [6.0], "acidity": [6.0], "body": [6.0], "balance": [6.0],
        "aftertaste": [6.0], "sweetness": [6.0], "clean_cup": [6.0],
        "cupper_points": [6.0], "moisture": [0.1], "number_of_bags": [1]
    })
    low = high.copy()
    low["flavor"] = 6.0  
    assert Weighting.get_scoring(high).iloc[0] > Weighting.get_scoring(low).iloc[0]

def test_high_aroma_bonus():
    high = pd.DataFrame({
        "species": ["Arabica"], "uniformity": [10.0], "flavor": [8.0],
        "aroma": [7.5], "acidity": [6.0], "body": [6.0], "balance": [6.0],
        "aftertaste": [6.0], "sweetness": [6.0], "clean_cup": [6.0],
        "cupper_points": [6.0], "moisture": [0.1], "number_of_bags": [1]
    })
    low = high.copy()
    low["aroma"] = 6.0  
    assert Weighting.get_scoring(high).iloc[0] > Weighting.get_scoring(low).iloc[0]
    
    
    
