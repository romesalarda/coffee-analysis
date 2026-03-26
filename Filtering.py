import pandas as pd

'''Removes rows that have na in specific columns'''
def filterNAColumn(df, listOfColumns):
    """
    Remove producers that have NA values in specific columns

    Args:
        df (DataFrame): The current dataframe
        listOfColumns (list[string): The list of columns to remove based on NA values

    Returns:
        DataFrame: A dataframe without NA values in those columns
    """
    if df is None:
        raise ValueError("df cannot be None")
    for column in listOfColumns:
        if column not in df.columns:
            raise ValueError("Column: " + column + " does not exist")
    clean_df = df.dropna(subset=listOfColumns)
    return clean_df

'''Gets a list of countries in the frame'''
def getListOfCountries(df):
    """
    Returns a list of countries in the frame

    Args:
        df (DataFrame): The current dataframe

    Returns:
        DataFrame: A dataframe of countries in the frame
    """
    if df is None:
        raise ValueError("df cannot be None")
    df_country = df['country_of_origin']
    df_country2 = df_country.drop_duplicates(inplace=False)
    return df_country2

'''filter by the number of producers'''
def filterByNumOfProducers(df, minNumOfProducers):
    """
    Remove countries who do not have enough producers.

    Args:
        df (DataFrame): The current dataframe
        minNumOfProducers (int): The minimum number of producers for operations in a country.

    Returns:
        :return: The filtered dataframe
    """
    if df is None:
        raise ValueError("df cannot be None")
    elif minNumOfProducers < 1:
        raise ValueError("minNumOfProducers cannot be less than 1")
    countries = getListOfCountries(df)
    for country in countries:
        df2 = df[df['country_of_origin'] == country]
        df3 = df2.drop_duplicates(subset=['farm_name'])
        numOfProducers = len(df3)
        if numOfProducers < minNumOfProducers:
            df = df[~(df['country_of_origin'] == country)]
    return df

def filterByColumnValue(df, column, value):
    """
    Filter by a value that the column must have

    Args:
        df (DataFrame): The current dataframe
        column (string): The column that the value is in.
        value (String): The value that you want the column to have

    Returns:
        DataFrame: A new dataframe, containing only those elements that were had the deried value in the column
    """
    if df is None:
        raise ValueError("df cannot be None")
    elif column not in df.columns:
        raise ValueError("column not found")
    elif value not in df[column].values:
        raise ValueError("value not found")
    df = df[df[column] == value]
    return df

def removeLittleProducers(df, minimumProduction = 500):
    """
    Removes producers that do not produce enough kg of beans

    Args:
        df (DataFrame): The current dataframe
        minimumProduction (int): The minimum amount of beans each producer must produce to be sustainable.

    Returns:
        DataFrame: A new dataframe without producers who cannot produce enough beans.
    """
    listOfNums = df['bag_weight'].values.tolist()
    listOfConverted = []
    for num in listOfNums:
        numString = num.split(' ')
        if numString[1] == "kg":
            listOfConverted.append( int(numString[0]) )
        elif numString[1] == "lbs":
            listOfConverted.append( int(numString[0]) / 2.205 )
        else:
            listOfConverted.append( int(numString[0])  )
    df['final_weight'] = df['number_of_bags'] * listOfConverted
    df = df[df['final_weight'] >= minimumProduction]
    return df