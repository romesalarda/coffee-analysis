import pandas as pd

'''Removes rows that have na in specific columns'''
def filterNAColumn(df, listOfColumns):
    if df is None:
        raise ValueError("df cannot be None")
    for column in listOfColumns:
        if column not in df.columns:
            raise ValueError("Column: " + column + " does not exist")
    clean_df = df.dropna(subset=listOfColumns)
    return clean_df

'''Gets a list of countries in the frame'''
def getListOfCountries(df):
    if df is None:
        raise ValueError("df cannot be None")
    df_country = df['country_of_origin']
    df_country2 = df_country.drop_duplicates(inplace=False)
    return df_country2

'''filter by the number of producers'''
def filterByNumOfProducers(df, minNumOfProducers):
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

'''Filter by a value that the column must have'''
def filterByColumnValue(df, column, value):
    if df is None:
        raise ValueError("df cannot be None")
    elif column not in df.columns:
        raise ValueError("column not found")
    elif value not in df[column].values:
        raise ValueError("value not found")
    df = df[df[column] == value]
    return df

def removeLittleProducers(df, minimumProduction = 500):
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