import pandas as pd

if __name__ == "__main__":
    from render import BarGraph, ScatterGraph, PieChart, HeatMap, WorldHeatMap, BaseGraph

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
    BaseGraph.define_working_directory("temp")

    # create bar graph of top 10 countries by score
    bar_graph = BarGraph()
    bar_graph.define_figure()
    bar_graph.define_graph_metadata(title="Top 10 Countries by Coffee Score", x_label="Country", y_label="Average Score")
    bar_graph.build(top_countries, df4.groupby('country_of_origin')['final_score'].mean().loc[top_countries].values)
    bar_graph.save_graph("top_countries_bar.png")

    categories_for_bar = ['aroma', 'flavor', 'body', 'uniformity']
    for category in categories_for_bar:
        top_countries_category = df4.groupby('country_of_origin')[category].mean().nlargest(10).index.tolist()
        top_countries_category_values = df4.groupby('country_of_origin')[category].mean().loc[top_countries_category].values
        bar_graph = BarGraph()
        bar_graph.define_figure()
        bar_graph.define_graph_metadata(title=f"Top 10 Countries by {category.capitalize()}", x_label="Country", y_label=f"Average {category.capitalize()} Score")
        bar_graph.build(top_countries_category, top_countries_category_values)
        bar_graph.save_graph(f"top_countries_{category}.png")

    heat_map = HeatMap()
    heat_map.define_figure()
    heat_map.define_graph_metadata(title="Correlation Heatmap of Coffee Attributes")

    categories = ['aroma', 'flavor', 'body', 'uniformity']
    heat_map.build(categories, top_countries, df4.groupby('country_of_origin')[categories].mean().loc[top_countries].values)
    heat_map.save_graph("correlation_heatmap.png")

    world_heat_map = WorldHeatMap()
    world_heat_map.define_figure()
    world_heat_map.define_graph_metadata(title="World Heatmap of Coffee Scores")

    top_countries = df4.groupby('country_of_origin')['final_score'].mean().nlargest(50).index.tolist()
    top_countries_scores = df4.groupby('country_of_origin')['final_score'].mean().loc[top_countries].values

    world_heat_map.build(dict(zip(top_countries, top_countries_scores)))
    world_heat_map.save_graph("world_heatmap.png")

    generate_report(f"The best country to buy coffee from is <b>{top_countries[0]}</b>.\nThis answer was reached by taking an <b> average </b> of each countries local suppliers - weighted according to customer preferences.", [bar_graph.WORKING_DIR + "/top_countries_bar.png"], "report.pdf")
