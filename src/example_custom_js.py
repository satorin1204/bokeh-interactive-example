from bokeh.io import output_file, show
from bokeh.models import (
    Plot,
    Range1d,
    HoverTool,
    TapTool,
    BoxSelectTool,
    LassoSelectTool,
    CustomJS,
)
from utils import get_graph_renderer

plot = Plot(
    width=400, height=400, x_range=Range1d(-1.3, 1.3), y_range=Range1d(-1.3, 1.3)
)
plot.title.text = "CustomJS を使った描画"
graph_renderer = get_graph_renderer()
# JavaScriptでコールバック関数を書く
code = """
    const indices = node_data.selected.indices;
    const connected_indices = [];
    var node, neighbor_node, neighbor_index;
    for (let i = 0; i < indices.length; i++) {
        node = node_data.data.index[indices[i]];
        for (let j = 0; j < edge_data.data.start.length; j++) {
            if (node == edge_data.data.start[j]) {
                neighbor_node =  edge_data.data.end[j];
                neighbor_index = node_data.data.index.indexOf(neighbor_node);
                connected_indices.push(neighbor_index);
            }
        }
        for (let j = 0; j < edge_data.data.end.length; j++) {
            if (node == edge_data.data.end[j]) {
                neighbor_node =  edge_data.data.start[j];
                neighbor_index = node_data.data.index.indexOf(neighbor_node);
                connected_indices.push(neighbor_index);
            }
        }
    }
    for (let i = 0; i < node_data.data.color.length; i++) {
        if (indices.includes(i)) {
            node_data.data.color[i] = "red";
        }
        else if (connected_indices.includes(i)){
            node_data.data.color[i] = "yellow";
        } else {
            node_data.data.color[i] = "blue";
        }
    }
    node_data.change.emit();
"""
# 必要なdata_sourceを渡す（今回はnodeとedgeのdata_source）
args = {
    "node_data": graph_renderer.node_renderer.data_source,
    "edge_data": graph_renderer.edge_renderer.data_source,
    "renderers": [graph_renderer.node_renderer],
}
callback = CustomJS(args=args, code=code)
# 選択したnodeの変更でコールバックする
graph_renderer.node_renderer.data_source.selected.js_on_change("indices", callback)
hover_tool = HoverTool(tooltips=[("index", "@index"), ("color", "@color")])
plot.renderers.append(graph_renderer)
plot.add_tools(TapTool(), BoxSelectTool(), LassoSelectTool(), hover_tool)

output_file("output/example_custom_js.html")
show(plot)
