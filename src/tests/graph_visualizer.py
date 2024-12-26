#!/usr/bin/env python3

from graphviz import (
    Digraph as Digraphviz,
    Graph as Graphviz
)


class GraphVisualizer:
    def __init__(self, nodes, graph, directed=True):
        self.m_nodes = nodes  # List of node names
        self.graph = graph    # Dictionary of adjacency lists with weights
        self.m_directed = directed

    def draw_graphviz(self):
        # Create a directed or undirected graph
        dot = Digraphviz(format='png') if self.m_directed else Graphviz(format='png')

        # Add nodes and edges to the graph
        for (node, colored) in self.m_nodes:
            dot.node(node, color='red' if colored else 'black')
            for adjacent, weight in self.graph[node]:
                # Add edge with weight
                dot.edge(node, adjacent, label=str(weight))

        # Render the graph to a file and display it
        dot.render('/tmp/graph', view=True)


# Example usage:
nodes = [('A', True), ('B', False), ('C', False), ('D', True)]
graph = {
    'A': [('B', 5), ('C', 3)],
    'B': [('C', 2)],
    'C': [('D', 7)],
    'D': [('A', 1)]
}

visualizer = GraphVisualizer(nodes, graph, directed=True)
visualizer.draw_graphviz()
