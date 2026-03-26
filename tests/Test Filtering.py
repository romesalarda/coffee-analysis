import pytest

import Filtering
import Filtering as Filter
import pandas as pd
import os

@pytest.fixture(scope='module')
def csv():
    cwd = os.getcwd()
    if "tests" in cwd:
        filepath = "test_data/test_coffee_ratings.csv"
    else:
        filepath = "tests/test_data/test_coffee_ratings.csv"
    filepath = os.path.join(cwd, filepath)
    df = pd.read_csv(filepath)
    yield df

def test_getCountries(csv):
    df2 = Filtering.getListOfCountries(csv)
    df2List = df2.values.tolist()
    assert 'Mexico' in df2List
    assert 'Nicaragua' in df2List

def test_filterByNumProducers(csv):
    numProducers = 2
    df2 = Filtering.filterByNumOfProducers(csv, numProducers)
    df2List = df2['country_of_origin'].values.tolist()
    assert 'India' in df2List
    assert 'Nicaragua' not in df2List

def test_filterByColumnValue(csv):
    df2 = Filtering.filterByColumnValue(csv, 'processing_method','Washed / Wet')
    df2List = df2['processing_method'].values.tolist()
    df2List = list(set(df2List))
    assert len(df2List) == 1
    assert df2List[0] == 'Washed / Wet'

def test_filterNaColumns(csv):
    df2 = Filtering.filterNAColumn(csv, ['processing_method'])
    df2List = df2['processing_method'].values.tolist()
    assert 'NA' not in df2List

def test_filterByColumnNotExist(csv):
    pytest.raises(ValueError, Filtering.filterByColumnValue, csv, 'wrfghg','Happy')

def test_filterNaColumnNoCsv(csv):
    pytest.raises(ValueError, Filtering.filterNAColumn, None, [])

def test_filterInvalidProducers(csv):
    pytest.raises(ValueError, Filtering.filterByNumOfProducers, csv, 0)
