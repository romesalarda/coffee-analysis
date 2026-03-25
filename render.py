import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typing
import os

# 1. plotting categories i.e. (favour, aroma, uniformity, body) bar chart 
# 2. scatter graph of flavour vs cupper points
# 3. annotate the scatter graph with the owner of the coffee

class BaseGraph:

    WORKING_DIR = "graphs"

    def __init__(self, description=None, *args, **kwargs):

        self.description = description
        self.graph_type = kwargs.get('graph_type', 'bar')

        self.kwargs = kwargs
        self.args = args
        self.fig = None
        self.ax = None

    @classmethod
    def define_working_directory(cls, path):
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
        self.fig.savefig(path)
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

    def nuke(self):
        '''
        Removes the current figure and axes, effectively resetting the graph instance to its initial state. 
        This can be useful when you want to completely reset the graph instance without creating a new one.
        '''
        self.ax, self.fig = None, None

class BarGraph(BaseGraph):

    def build(self, x: typing.Iterable[typing.Any], y: typing.Iterable[typing.Any]):
        self.ax.bar(x, y)
        self.show()


class ScatterGraph(BaseGraph):

    def build(self, 
               x: typing.Iterable[typing.Any], 
               y: typing.Iterable[typing.Any]
               ):
        self.ax.scatter(x, y)
        self.show()


class PieChart(BaseGraph):

    def build(self, 
               labels: typing.Iterable[typing.Any], 
               values: typing.Iterable[typing.Any]
               ):
        self.ax.pie(values, labels=labels)
        self.show()

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

