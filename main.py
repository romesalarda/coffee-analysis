import pandas as pd

if __name__ == "__main__":
    from render import BarGraph, ScatterGraph, PieChart

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
    top_countries = df4.groupby('country_of_origin')['final_score'].mean().nlargest(10).index.tolist()

    # set save dir
    BarGraph.define_working_directory("temp")

    # create bar graph of top 10 countries by score
    bar_graph = BarGraph()
    bar_graph.define_figure()
    bar_graph.define_graph_metadata(title="Top 10 Countries by Coffee Score", x_label="Country", y_label="Average Score")
    bar_graph.build(top_countries, df4.groupby('country_of_origin')['final_score'].mean().loc[top_countries].values)
    bar_graph.save_graph("top_countries_bar.png")
    # bar_graph.show()

    # top 10 countries by aroma
    # top_countries_aroma = df4.groupby('country_of_origin')['aroma'].mean().nlargest(10).index.tolist()
    #Try using .loc[row_indexer,col_indexer] = value instead
    # top_countries_aroma_values = df4.groupby('country_of_origin')['aroma'].mean().loc[top_countries_aroma].values
    # scatter_graph = BarGraph()
    # scatter_graph.define_figure()
    # scatter_graph.define_graph_metadata(title="Top 10 Countries by Aroma", x_label="Country", y_label="Average Aroma Score")
    # scatter_graph.build(top_countries_aroma, top_countries_aroma_values)
    # scatter_graph.show()
    # scatter_graph.save_graph("top_countries_aroma.png")

    # top_countries_flavor = df4.groupby('country_of_origin')['flavor'].mean().nlargest(10).index.tolist()
    # top_countries_flavor_values = df4.groupby('country_of_origin')['flavor'].mean().loc[top_countries_flavor].values
    # scatter_graph_flavor = BarGraph()
    # scatter_graph_flavor.define_figure()
    # scatter_graph_flavor.define_graph_metadata(title="Top 10 Countries by Flavor", x_label="Country", y_label="Average Flavor Score")
    # scatter_graph_flavor.build(top_countries_flavor, top_countries_flavor_values)
    # scatter_graph_flavor.show()
    # scatter_graph_flavor.save_graph("top_countries_flavor.png")

    generate_report(f"The best country to buy coffee from is <b>{top_countries[0]}</b>.\nThis answer was reached by taking an <b> average </b> of each countries local suppliers - weighted according to customer preferences.", [bar_graph.WORKING_DIR + "/top_countries_bar.png"], "report.pdf")