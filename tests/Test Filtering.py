import pytest

import Filtering
import Filtering as Filter
import pandas as pd

@pytest.fixture(scope='module')
def csv():
    print("Setting up csv")
    df = pd.read_csv("/../data/simplified_coffee_ratings.csv")
    yield df

def test_getCountries(csv):
    df2 = Filtering.getListOfCountries(csv)
    assert 'United States' in df2
    assert 'Rwanda' in df2


