import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import typing
import os

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.cm as cm
from matplotlib.colors import PowerNorm
from pyparsing import col


class BaseGraph:
    '''
    Base class for all graph types. Provides common functionality for defining the figure, saving the graph, and displaying it.
    Subclasses should implement the build method to define how the graph is constructed based on the provided data.
    '''
    WORKING_DIR = "graphs"

    def __init__(self, description=None, *args, **kwargs):
        '''
        Initializes the BaseGraph instance with optional description and graph type.

        Args:
            description: Optional; A brief description of the graph's purpose or content. This can be used for documentation or logging purposes.
            graph_type: Optional; A string indicating the type of graph (e.g., 'bar', 'scatter', 'pie', 'heatmap'). This can be used to determine default settings or file naming conventions when saving the graph.
        '''
        self.description = description
        self.graph_type = kwargs.get('graph_type', 'bar')

        self.kwargs = kwargs
        self.args = args
        self.fig = None
        self.ax = None

    @classmethod
    def define_working_directory(cls, path: typing.Optional[str] = None):
        '''
        Define the working directory for saving graphs. If no path is provided, it defaults to "graphs". If the specified directory does not exist, it will be created.
        '''
        cls.WORKING_DIR = path
        if not os.path.exists(cls.WORKING_DIR):
            os.makedirs(cls.WORKING_DIR)

    def define_figure(self):
        '''
        Hook method to define the figure and axes for the graph. 
        This method is called during initialization and can be overridden by subclasses if they require a different figure setup.
        '''
        self.fig, self.ax = plt.subplots()
        return self.fig, self.ax

    def build(self, x: typing.Iterable[typing.Any], y: typing.Iterable[typing.Any]):
        '''
        Builds the graph based on the provided data and graph type.
        
        Args:
            x: An iterable containing the x-axis data.
            y: An iterable containing the y-axis data.
        
        '''
        raise NotImplementedError("The build method must be implemented by subclasses to define how the graph is constructed.")
    
    def define_graph_metadata(self, title:str=None, x_label:str=None, y_label:str=None):
        '''
        Defines the graph metadata such as title, x-axis label, and y-axis label.
        '''
        if title:
            self.ax.set_title(title)
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)

    def save_graph(self, file_name: str = None, use_working_dir=True):
        '''
        Save graph to the specified path. If no path is provided, it saves to the default working directory with a filename based on the graph type.
        
        Args:
            file_name: Optional; The name of the file to save the graph as. If not provided, a default name based on the graph type and current timestamp will be used.
            use_working_dir: Optional; If True, saves the graph in the defined working directory. If False, saves in the current directory.
        
        '''
        time_stamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        if file_name is None:
            file_name = f"{self.graph_type}_graph_{time_stamp}.png"

        if use_working_dir:
            path = os.path.join(self.WORKING_DIR, file_name)
        else:
            path = os.path.join(self.WORKING_DIR, file_name)

        # plt.savefig(path)
        self.fig.savefig(path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to {path}")

    def show(self):
        '''
        Renders the graph to the screen. Wrapped in a try-except block to handle potential KeyboardInterrupt exceptions gracefully.
        '''
        try:
            plt.show()
        except KeyboardInterrupt as e:
            print("Graph display interrupted by user.")

    def clear(self):
        '''
        Clears the current figure and axes to reset the graph state. This can be useful when building multiple graphs in a loop or when reusing the same graph instance for different data.
        '''
        if self.fig and self.ax:
            self.ax.clear()
            self.fig.clf()

    def close(self):
        '''
        Closes the current figure to free up memory. This is particularly important when generating multiple graphs in a loop or when working with large datasets, as it helps prevent memory leaks and ensures that resources are properly released.
        '''
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
class BarGraph(BaseGraph):

    def define_figure(self):
        super().define_figure()
        plt.xticks(rotation=45, ha='right')

    def build(self, x: typing.Iterable[typing.Any], y: typing.Iterable[typing.Any]):
        self.ax.bar(x, y)


class ScatterGraph(BaseGraph):

    def build(self, 
               x: typing.Iterable[typing.Any], 
               y: typing.Iterable[typing.Any]
               ):
        self.ax.scatter(x, y)


class PieChart(BaseGraph):

    def build(self, 
               labels: typing.Iterable[typing.Any], 
               values: typing.Iterable[typing.Any]
               ):
        '''
        Builds a pie chart using the provided labels and values.

        Args:
            labels: An iterable containing the labels for each slice of the pie chart.
            values: An iterable containing the corresponding values for each label, which determine the size of each slice in the pie chart.
        '''

        self.ax.pie(values, labels=labels)

class HeatMap(BaseGraph):

    def build(self, 
               x: typing.Iterable[typing.Any], 
               y: typing.Iterable[typing.Any], 
               data: typing.Iterable[typing.Any],
               add_annotations: bool = True,
               normalise: bool = True
               ):
        '''
        Builds a heatmap using the provided x and y labels and the corresponding data values.

        Args:
            x: An iterable containing the labels for the x-axis (columns).
            y: An iterable containing the labels for the y-axis (rows).
            data: A 2D iterable (e.g., list of lists or numpy array) containing the values to be displayed in the heatmap. The shape of data should match the lengths of x and y.
            add_annotations: Optional; If True, adds annotations to each cell in the heatmap displaying the corresponding data value. Default is True.
            normalise: Optional; If True, normalizes the data values to a range between 0 and 1 before plotting the heatmap. This can help improve the visual representation of the data, especially when there are large variations in the values. Default is True.
        '''
        if normalise:
            data = np.array(data)
            data = data / np.max(data, axis=0)
            
        im = self.ax.imshow(data, aspect='auto', origin='lower')

        self.ax.set_xticks(range(len(x)))
        self.ax.set_yticks(range(len(y)))

        self.ax.set_xticklabels(x, rotation=45, ha='right')
        self.ax.set_yticklabels(y)

        self.fig.colorbar(im, ax=self.ax)

        if add_annotations:
            for i in range(len(y)):
                for j in range(len(x)):
                    self.ax.text(j, i, f"{data[i, j]:.2f}",ha="center", va="center", color="w")

class WorldHeatMap(BaseGraph):

    def __init__(self, description=None, *args, **kwargs):
        '''
        Initializes the WorldHeatMap instance with optional description and graph type.

        Args:
            description: Optional; A brief description of the graph's purpose or content. This can be used for documentation or logging purposes.
            graph_type: Optional; A string indicating the type of graph (e.g., 'bar', 'scatter', 'pie', 'heatmap'). This can be used to determine default settings or file naming conventions when saving the graph.
            colour_map: Optional; A string specifying the colormap to use for the heatmap. Default is 'inferno'. This can be any valid colormap recognized by matplotlib.
            edge_color: Optional; A string specifying the color to use for the edges of the countries on the map. Default is 'black'.
            resolution: Optional; A string specifying the resolution of the shapefile to use for the map. Default is '110m'. This can be '110m', '50m', or '10m' depending on the level of detail desired.
            category: Optional; A string specifying the category of the shapefile to use for the map
            name: Optional; A string specifying the name of the shapefile to use for the map. Default is 'admin_0_countries', which includes country boundaries.

        '''
        super().__init__(description, *args, **kwargs)

        self.colour_map = self.kwargs.get('colour_map', 'inferno')
        self.edge_color = self.kwargs.get('edge_color', 'black')
        self.resolution = self.kwargs.get('resolution', '110m')
        self.category = self.kwargs.get('category', 'cultural')
        self.name = self.kwargs.get('name', 'admin_0_countries')
        self.graph_type = 'world_heatmap'

    def build(self, data: typing.Dict[str, float]):
        '''
        Builds a world heatmap using the provided data dictionary, 
        where keys are country names and values are the corresponding scores or values to be visualized on the map.

        Args:
            data: A dictionary where the keys are country names (as they appear in the shapefile) and the values are the corresponding scores or values to be visualized on the map. 
            The values will be used to determine the color intensity for each country on the heatmap.
        '''
        shpfilename = shpreader.natural_earth(
            resolution=self.resolution,
            category=self.category,
            name=self.name
        )

        reader = shpreader.Reader(shpfilename)

        # fig = plt.figure(figsize=(10, 5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()

        cmap = cm.get_cmap(self.colour_map)  # choose a colormap
        norm = PowerNorm(gamma=0.5, vmin=min(data.values()), vmax=max(data.values()))

        for record in reader.records():
            name = record.attributes['NAME_LONG']

            value = data.get(name, 0)

            ax.add_geometries(
                [record.geometry],
                ccrs.PlateCarree(),
                facecolor=cmap(norm(value)),  # normalize
                edgecolor=self.edge_color
            )

        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05)
        cbar.set_label('Final Score')
        

if __name__ == "__main__":
    x = ['a', 'b', 'c']
    y = [1, 2, 3]

    plt.style.use('seaborn-v0_8-darkgrid')

    BaseGraph.define_working_directory("graphs")

    graph = BarGraph()
    graph.define_graph_metadata(
        title="Bar Graph Example", 
        x_label="Categories", 
        y_label="Values"
    )
    graph.build(x, y)
    graph.save_graph()

