from bokeh.models import (
    Plot,
    Range1d,
    HoverTool,
    TapTool,
    BoxSelectTool,
    LassoSelectTool,
)
from bokeh.plotting import curdoc
import sys

sys.path.append("../src")
from utils import get_graph_renderer


plot = Plot(
    width=400, height=400, x_range=Range1d(-1.3, 1.3), y_range=Range1d(-1.3, 1.3)
)
plot.title.text = "CustomJS を使った描画"
graph_renderer = get_graph_renderer()


def update_color(indices):
    connected_indices, color_list = [], []
    for i in range(len(indices)):
        node = graph_renderer.node_renderer.data_source.data["index"][indices[i]]
        for j in range(len(graph_renderer.edge_renderer.data_source.data["start"])):
            if node == graph_renderer.edge_renderer.data_source.data["start"][j]:
                neighbor_node = graph_renderer.edge_renderer.data_source.data["end"][j]
                neighbor_index = graph_renderer.node_renderer.data_source.data[
                    "index"
                ].index(neighbor_node)
                connected_indices.append(neighbor_index)
        for j in range(len(graph_renderer.edge_renderer.data_source.data["end"])):
            if node == graph_renderer.edge_renderer.data_source.data["end"][j]:
                neighbor_node = graph_renderer.edge_renderer.data_source.data["start"][
                    j
                ]
                neighbor_index = graph_renderer.node_renderer.data_source.data[
                    "index"
                ].index(neighbor_node)
                connected_indices.append(neighbor_index)
    for i in range(len(graph_renderer.node_renderer.data_source.data["index"])):
        if i in indices:
            color_list.append("red")
        elif i in connected_indices:
            color_list.append("yellow")
        else:
            color_list.append("blue")
    # 直接graph_renderer.node_renderer.data_source.data["color"][i] = "red" としても描画に反映されない
    graph_renderer.node_renderer.data_source.data["color"] = color_list


# callback はattr, old, new を引数に持つ
def callback(attr, old, new):
    update_color(new)


# 選択したnodeの変更でコールバックする
graph_renderer.node_renderer.data_source.selected.on_change("indices", callback)
hover_tool = HoverTool(tooltips=[("index", "@index"), ("color", "@color")])
plot.renderers.append(graph_renderer)
plot.add_tools(TapTool(), BoxSelectTool(), LassoSelectTool(), hover_tool)
# python script の場合はcurdoc().add_root()する
curdoc().add_root(plot)
