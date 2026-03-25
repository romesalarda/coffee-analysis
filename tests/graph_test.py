import pytest
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')  # Use a non-interactive backend for testing to avoid GUI issues

from render import BaseGraph, BarGraph, ScatterGraph, PieChart

def test_base_graph():
    
    graph = BaseGraph()
    graph.define_figure()
    graph.define_graph_metadata(title="Base Graph Test", x_label="X-axis", y_label="Y-axis")

    pytest.raises(NotImplementedError, graph.build, x=[1, 2, 3], y=[4, 5, 6])

    assert graph.fig is not None
    assert graph.ax is not None

    assert graph.ax.get_title() == "Base Graph Test"
    assert graph.ax.get_xlabel() == "X-axis"
    assert graph.ax.get_ylabel() == "Y-axis"

    plt.close()

def test_bar_chart():
    graph = BarGraph()
    x = ['a', 'b', 'c']
    y = [1, 2, 3]
    graph.define_figure()
    graph.build(x, y)

    plt.close()

def test_scatter_graph():
    graph = ScatterGraph()
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    graph.define_figure()
    graph.build(x, y)

    plt.close()

def test_pie_chart():
    graph = PieChart()
    labels = ['A', 'B', 'C']
    values = [30, 50, 20]
    graph.define_figure()
    graph.build(labels, values)

    plt.close()
    