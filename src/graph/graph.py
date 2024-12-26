from .node import Node

# Libraries for graphical representation
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import (
    Digraph as Digraphviz,
    Graph as Graphviz
)


# Constructor, string representation and representation of the graph
# Methods for:
# - printing, counting, adding and removing edges
# - adding heuristic values to nodes
# - drawing the graph using matplotlib or graphviz
class Graph:
    def __init__(self, directed: bool = False):
        self.nodes = []
        self.directed = directed
        self.graph = {}  # dictionary to store nodes, edges and costs
        self.h = {}  # dictionary to store heuristic values

    def __str__(self):
        out = ""
        for key_node, adj_nodes in self.graph.items():
            if adj_nodes:
                adj_nodes = ", ".join([f'({n}, {c})' for n, c in adj_nodes])
            else:
                adj_nodes = "None"
            out += f"{key_node}: {adj_nodes}\n"
        return out

    def __repr__(self):
        return str(self)

    def print_edges(self):
        out = ""
        printed_edges = set()
        for node1, adj_nodes in self.graph.items():
            for (node2, cost) in adj_nodes:
                if self.directed:
                    out += f"{node1} -> {node2} cost: {cost}\n"
                else:
                    # For undirected graphs, only print the edge
                    # if it hasn't been printed yet
                    if (node2, node1) not in printed_edges:
                        out += f"{node1} <-> {node2} cost: {cost}\n"
                        printed_edges.add((node1, node2))
        return out

    def get_num_edges(self):
        edges = sum([len(adj_nodes) for adj_nodes in self.graph.values()])
        return edges if self.directed else edges // 2

    def add_node(self, node, catastrophe=None):
        if isinstance(node, str):
            node = Node(node, catastrophe)

        if node in self.nodes:
            return node

        self.nodes.append(node)
        self.graph[node] = self.graph.get(node, [])
        return node

    def add_edge(self, node1, node2, distance, travel_method="land"):
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Node not previously added to the graph")

        # Add the edge to the graph
        self.graph[node1].append((node2, (distance, travel_method)))

        # if the graph is undirected, add the edge in the other direction
        if not self.directed:
            self.graph[node2].append((node1, (distance, travel_method)))

    def remove_edge(self, node1, node2):
        a = self.graph[node1]
        for (node1, (distance, travel_method)) in a:
            if node1 == node2:
                a.remove((node1, (distance, travel_method)))
                return
        pass

    def add_heuristic(self, node, value):
        if node in self.nodes:
            self.h[node] = value
        pass

    def draw_matplotlib(self):
        # Create list of nodes
        g = nx.DiGraph()
        for node in self.nodes:
            g.add_node(node.name)
            for (adjacent, (distance, _)) in self.graph[node]:
                g.add_edge(node.name, adjacent.name, distance=distance)
                if not self.directed:
                    g.add_edge(adjacent.name, node.name, distance=distance)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos,
                         with_labels=True,
                         font_weight="bold",
                         arrows=True)
        labels = nx.get_edge_attributes(g, "distance")
        nx.draw_networkx_edge_labels(g, pos,
                                     edge_labels=labels)

        plt.draw()
        plt.show()

    def draw_graphviz(self):
        # Create a directed or undirected graph
        dot = Digraphviz(format="png") if self.directed else Graphviz(format="png")
        dot.attr(rankdir="TB")

        drawn_edges = set()

        # Add nodes and edges to the graph
        for node in self.nodes:

            # Add node with red color if it has a catastrophe
            if node.catastrophe is None:
                dot.node(node.name)
            else:
                dot.node(node.name, color='red')

            for adjacent, (distance, travel_method) in self.graph[node]:
                # Define edge color based on travel method
                color = "black"
                match travel_method:
                    case "land":
                        color = "green"
                    case "water":
                        color = "blue"
                    case "air":
                        color = "red"

                # Add edge with distance
                if (node.name, adjacent.name) not in drawn_edges:
                    dot.edge(node.name, adjacent.name, label=str(distance), color=color)
                    drawn_edges.add((adjacent.name, node.name))

        # Render the graph to a file and display it
        dot.render('/tmp/graph', view=True)
