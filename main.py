import pandas as pd

if __name__ == "__main__":
    from render import BarGraph, ScatterGraph, PieChart, HeatMap

    from Weighting import get_scoring, get_country_score
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
    results = get_country_score(df4)
    countries = [i[0] for i in results]
    scores = [i[1] for i in results]
    top_countries = countries

    # set save dir
    BarGraph.define_working_directory("temp")

    # create bar graph of top 10 countries by score
    bar_graph = BarGraph()
    bar_graph.define_figure()
    bar_graph.define_graph_metadata(title="Top 10 Countries by Coffee Score", x_label="Country", y_label="Average Score")
    bar_graph.build(top_countries, scores)
    bar_graph.save_graph("top_countries_bar.png")
    bar_graph.show()

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

    report_body = f"""
                      This report outlines country with the best bean-buying prospects.\n <br>
                      These results are based on data published by the Coffee Quality Database and compiled by data scientist James LeDoux available <a href=https://github.com/jldbc/coffee-quality-database>here</a>. \n
                      The data contains reviews of around 1300 coffee beans from across the world.\n
                      
                      <h3> Methodology </h3>\n
                      First the data is parsed and filtered to remove suppliers with key missing or invalid values in key data fields. This is done so that only real data is used in the process and not any kind of guessing or interpolation between similar suppliers.\n <br>
                      Next we removed countries with less than {3} suppliers from the dataset. This was done as these kinds of countries are prone to generating biased data - and since they are less valuable as trading partners.
                      And finally, the last filter we apply is to ensure that the coffee uses a <i>Washed/Wet</i> processing method. This is a requirement identified as necessary to ensure consistency across coffee outlets. <br> <br>
                      A coffee's quality is described in the dataset as a list of scores in the following categories: <br><i>(aroma,flavor,aftertaste,acidity,body,balance,uniformity,clean_cup,sweetness,cupper_points,moisture)</i><br>
                      We apply a weighted sum to each supplier across each of these categories such that for supplier i: <br>
                      <i>score<sub>i</sub> = (w<sub>a</sub> . aroma<sub>i</sub>) + (w<sub>f</sub> . flavour<sub>i</sub>) + (w<sub>u</sub> . uniformity<sub>i</sub>) + Σ<sub>other</sub> (w<sub>other</sub> + other<sub>i</sub>) <br>
                      and w<sub>a</sub>=<b>{1.0}</b>, w<sub>f</sub>=<b>{1.0}</b>, w<sub>u</sub>=<b>{1.0}</b>, w<sub>other</sub>=<b>{1.0}</b></i> <br> <br>

                      At this point an average of each countries to {20} top suppliers is taken. These are the values used in determining which country is the best to trade with.
                      <h3> Results </h3>\n
                   """


    heat_map = HeatMap()
    heat_map.define_figure()
    heat_map.define_graph_metadata(title="Correlation Heatmap of Coffee Attributes")
    # top 10 countries on y and then on x is the categories, each value is the score for that attribute for that country
    # 
    categories = ['aroma', 'flavor', 'body', 'uniformity']
    heat_map.build(categories, top_countries, df4.groupby('country_of_origin')[categories].mean().loc[top_countries].values)
    heat_map.show()

    generate_report(f"The best country to buy coffee from is <b>{top_countries[0]}</b>.\nThis answer was reached by taking an <b> average </b> of each countries local suppliers - weighted according to customer preferences.", [bar_graph.WORKING_DIR + "/top_countries_bar.png"], "report.pdf")
