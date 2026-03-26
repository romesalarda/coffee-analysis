import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.cm as cm
from matplotlib.colors import PowerNorm

# Load shapefile
shpfilename = shpreader.natural_earth(
    resolution='110m',
    category='cultural',
    name='admin_0_countries'
)

reader = shpreader.Reader(shpfilename)

# Data


if __name__ == "__main__":
    import pandas as pd
    from render import BarGraph, ScatterGraph, PieChart, HeatMap

    from Weighting import get_scoring
    from Filtering import filterByColumnValue, filterByNumOfProducers, filterNAColumn
    from generatePdf import generate_report

    df = pd.read_csv("data/simplified_coffee_ratings.csv")
    df2 = filterNAColumn(df,
                        ['country_of_origin', 'processing_method', 'aroma',
                        'flavor','body','uniformity','cupper_points'])
    df3 = filterByNumOfProducers(df2, 3)
    df4 = filterByColumnValue(df3,'processing_method',"Washed / Wet")
    df5 = df4['country_of_origin'].drop_duplicates(inplace=False)
    
    # need to get best 10 countries by score
    df4['final_score'] = get_scoring(df4)
    top_countries = df4.groupby('country_of_origin')['final_score'].mean().nlargest(50).index.tolist()
    top_countries_scores = df4.groupby('country_of_origin')['final_score'].mean().loc[top_countries].values

    country_values = dict(zip(top_countries, top_countries_scores))

    # country_values = {
    #     "United Kingdom": 2,
    #     "France": 1,
    #     "Germany": 3
    # }

    print(country_values)

    # Plot
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()

    cmap = cm.get_cmap('inferno')  # choose a colormap

    norm = PowerNorm(gamma=0.5, vmin=min(country_values.values()), vmax=max(country_values.values()))

    for record in reader.records():
        name = record.attributes['NAME_LONG']

        value = country_values.get(name, 0)

        ax.add_geometries(
            [record.geometry],
            ccrs.PlateCarree(),
            facecolor=cmap(norm(value)),  # normalize
            edgecolor='black'
        )

    plt.title("Country Heatmap")
    plt.show()