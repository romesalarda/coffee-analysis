import pandas as pd
import argparse

if __name__ == "__main__":
    from render import BarGraph, ScatterGraph, PieChart, HeatMap, WorldHeatMap, BaseGraph

    from Weighting import get_scoring, get_country_score
    from Filtering import filterByColumnValue, filterByNumOfProducers, filterNAColumn, removeLittleProducers
    from generatePdf import generate_report

    parser = argparse.ArgumentParser(description='Process coffee data and generate report.')
    parser.add_argument('--input', type=str, default='data/simplified_coffee_ratings.csv', help='Path to the input CSV file')
    parser.add_argument('--min_producers', type=int, default=3, help='Minimum number of producers for a country to be included')
    parser.add_argument('--weight_aroma', type=float, default=1.0, help='Weight for aroma score')
    parser.add_argument('--weight_flavor', type=float, default=1.0, help='Weight for flavor score')
    parser.add_argument('--weight_uniformity', type=float, default=1.0, help='Weight for uniformity score')
    parser.add_argument('--weight_species', type=float, default=1.0, help='Weight for species score')
    parser.add_argument('--weight_other', type=float, default=1.0, help='Weight for other scores')
    parser.add_argument('--cwd', type=str, default='temp/', help='Current working directory for saving outputs')
    parser.add_argument('--min_production', type=int, default=500, help='Minimum number of bags * weight for a producer to be included in the analysis (kg)')

    args = parser.parse_args()

    df = pd.read_csv(args.input)
    df2 = filterNAColumn(df,
                        ['country_of_origin', 'processing_method', 'aroma',
                        'flavor','body','uniformity','cupper_points'])
    df3 = filterByNumOfProducers(df2, args.min_producers)
    df4 = filterByColumnValue(df3,'processing_method',"Washed / Wet")
    df5 = df4['country_of_origin'].drop_duplicates(inplace=False)
    df6 = removeLittleProducers(df4, minimumProduction=args.min_production)
    # need to get best 10 countries by score
    df6['final_score'] = get_scoring(df6, 
                                    uniformity_multiplier=args.weight_uniformity,
                                    flavor_multiplier=args.weight_flavor,
                                    aroma_multiplier=args.weight_aroma,
                                    species_multiplier=args.weight_species,
                                    otherColumnMultiplier=args.weight_other
                                    )
                                     
    results = get_country_score(df6)
    countries = [i[0] for i in results]
    scores = [i[1] for i in results]
    top_countries = countries

    # set save dir
    BaseGraph.define_working_directory(args.cwd)

    # create bar graph of top 10 countries by score
    bar_graph = BarGraph()
    bar_graph.define_figure()
    bar_graph.define_graph_metadata(title="Top 10 Countries by Coffee Score", x_label="Country", y_label="Average Score")
    bar_graph.build(top_countries, scores)
    bar_graph.save_graph("top_countries_bar.png")

    categories_for_bar = ['aroma', 'flavor', 'body', 'uniformity']
    for category in categories_for_bar:
        top_countries_category = df6.groupby('country_of_origin')[category].mean().nlargest(10).index.tolist()
        top_countries_category_values = df6.groupby('country_of_origin')[category].mean().loc[top_countries_category].values
        bar_graph = BarGraph()
        bar_graph.define_figure()
        bar_graph.define_graph_metadata(title=f"Top 10 Countries by {category.capitalize()}", x_label="Country", y_label=f"Average {category.capitalize()} Score")
        bar_graph.build(top_countries_category, top_countries_category_values)
        bar_graph.save_graph(f"top_countries_{category}.png")

    report_body = f"""
                      This report outlines country with the best bean-buying prospects.\n <br>
                      These results are based on data published by the Coffee Quality Database and compiled by data scientist James LeDoux available <a href=https://github.com/jldbc/coffee-quality-database>here</a>. \n
                      The data contains reviews of around 1300 coffee beans from across the world.\n
                      
                      <h3> Methodology </h3>\n
                      First the data is parsed and filtered to remove suppliers with key missing or invalid values in key data fields. This is done so that only real data is used in the process and not any kind of guessing or interpolation between similar suppliers.\n <br>
                      Next we removed countries with less than {3} suppliers from the dataset. This was done as these kinds of countries are prone to generating biased data - and since they are less valuable as trading partners.
                      We then filter out suppliers who produce less than {500}kg of beans so that only those who produce a useful amount are considered<br>
                      And finally, the last filter we apply is to ensure that the coffee uses a <i>Washed/Wet</i> processing method. This is a requirement identified as necessary to ensure consistency across coffee outlets. <br> <br>
                      A coffee's quality is described in the dataset as a list of scores in the following categories: <br><i>(aroma,flavor,aftertaste,acidity,body,balance,uniformity,clean_cup,sweetness,cupper_points,moisture)</i><br>
                      We apply a weighted sum to each supplier across each of these categories such that for supplier i: <br>
                      <i>score<sub>i</sub> = (w<sub>a</sub> . aroma<sub>i</sub>) + (w<sub>f</sub> . flavour<sub>i</sub>) + (w<sub>u</sub> . uniformity<sub>i</sub>) + Σ<sub>other</sub> (w<sub>other</sub> + other<sub>i</sub>) <br>
                      and w<sub>a</sub>=<b>{1.0}</b>, w<sub>f</sub>=<b>{1.0}</b>, w<sub>u</sub>=<b>{1.0}</b>, w<sub>other</sub>=<b>{1.0}</b></i> <br> <br>

                      At this point an average of each countries top <i>{20}</i> suppliers is taken. These are the values used in determining which country is the best to trade with.
                      <h3> Results </h3>\n

                   """
    
    heat_map = HeatMap()
    heat_map.define_figure()
    heat_map.define_graph_metadata(title="Correlation Heatmap of Coffee Attributes")

    categories = ['aroma', 'flavor', 'body', 'uniformity']
    heat_map.build(categories, top_countries, df6.groupby('country_of_origin')[categories].mean().loc[top_countries].values)
    heat_map.save_graph("correlation_heatmap.png")

    world_heat_map = WorldHeatMap()
    world_heat_map.define_figure()
    world_heat_map.define_graph_metadata(title="World Heatmap of Coffee Scores")

    top_countries = df6.groupby('country_of_origin')['final_score'].mean().nlargest(10).index.tolist()
    top_countries_scores = df6.groupby('country_of_origin')['final_score'].mean().loc[top_countries].values

    world_heat_map.build(dict(zip(top_countries, top_countries_scores)))
    world_heat_map.save_graph("world_heatmap.png")

    graphs = ["temp/top_countries_bar.png", "temp/correlation_heatmap.png",  "temp/world_heatmap.png"]


    generate_report(report_body, graphs, "report.pdf")
