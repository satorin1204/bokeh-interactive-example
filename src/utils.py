import string
import numpy as np
import networkx as nx
from bokeh.plotting import from_networkx
from bokeh.models import (
    Circle,
    MultiLine,
)


def get_graph_renderer():
    G = nx.Graph()
    # アルファベットの数だけノード作成、ランダムにエッジを生やす
    nodes = list(string.ascii_uppercase)
    edges = np.array(np.meshgrid(nodes, nodes)).T.reshape(-1, 2)
    edges = np.random.permutation(edges)[:100]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.data_source.data["color"] = ["blue"] * len(nodes)
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="color")
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="black", line_alpha=0.8, line_width=1
    )
    return graph_renderer
