# The Graph class holds the following attributes:
# - directed: boolean indicating if the graph is directed
# - nodes: list of nodes
# - graph: dictionary to store nodes, edges and costs
# - h: dictionary to store heuristic values
# - destructive_nodes: dictionary of destructive nodes conditions
# - destructive_edges: dictionary of destructive edges conditions

# The Graph class holds the following methods:
# - string representation of the graph
# - print, count, add and remove edges
# - add/update heuristic values to nodes
# - draw the graph using matplotlib or graphviz

# Edge info: (distance, speed_multiplier, travel_method, access_level)

from .node import Node
from vehicle import convert_access_level_to_str

from heapq import heappush, heappop
import copy

# Libraries for graphical representation
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import (
    Digraph as DigraphViz,
    Graph as GraphViz
)


class Graph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.nodes = []
        self.graph = {}
        self.h = {}
        self.destructive_nodes = {}
        self.destructive_edges = {}

    def __str__(self):
        out = ""
        for key_node, adj_nodes in self.graph.items():
            if adj_nodes:
                adj_nodes = ", ".join([f'({n.name}, {c})' for n, c in adj_nodes])
            else:
                adj_nodes = "None"
            out += f"{key_node.name}: {adj_nodes}\n"
        return out

    def __repr__(self):
        return str(self)

    def copy(self):
        return copy.deepcopy(self)

    def print_edges(self):
        printed_edges = set()
        for node1, adj_nodes in self.graph.items():
            for (node2, (distance, speed_mult, travel_method, access_level)) in adj_nodes:

                access_level_str = convert_access_level_to_str(access_level)

                if self.directed:
                    print(
                        f"{node1.name} -> {node2.name} "
                        f"distance: {distance} "
                        f"speed_multiplier: {speed_mult:.2f} "
                        f"travel_method: {travel_method.ljust(5)} "
                        f"access_level: {access_level_str}"
                    )
                else:
                    # For undirected graphs, only print the edge
                    # if it hasn't been printed yet
                    if (node2, node1) not in printed_edges:
                        print(
                            f"{node1.name} <-> {node2.name} "
                            f"distance: {distance} "
                            f"speed_multiplier: {speed_mult:.2f} "
                            f"travel_method: {travel_method.ljust(5)} "
                            f"access_level: {access_level_str}"
                        )
                        printed_edges.add((node1, node2))

    def serialize_nodes(self):
        return [node.serialize() for node in self.nodes]

    def get_num_edges(self):
        edges = sum([len(adj_nodes) for adj_nodes in self.graph.values()])
        return edges if self.directed else edges // 2

    def add_node(self, node, fuel, catastrophe, vehicles, supplies):
        if isinstance(node, str):
            node = Node(node, fuel, catastrophe, vehicles, supplies)

        self.nodes.append(node)
        self.graph[node] = self.graph.get(node, [])

    def add_edge(self, node1, node2, distance, speed_mult, travel_method, access_level):
        if isinstance(node1, str):
            node1 = next((n for n in self.nodes if n.name == node1), None)

        if isinstance(node2, str):
            node2 = next((n for n in self.nodes if n.name == node2), None)

        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Node not previously added to the graph")

        # Add the edge to the graph
        edge_info = (distance, speed_mult, travel_method, access_level)
        self.graph[node1].append((node2, edge_info))

        # if the graph is undirected, add the edge in the other direction
        if not self.directed:
            self.graph[node2].append((node1, edge_info))

    def destroy_node(self, node):
        # Get the node object if it's a string
        if isinstance(node, str):
            node = next((n for n in self.nodes if n.name == node), None)

        if node is None:
            return

        # Remove the node from the list of nodes
        self.nodes.remove(node)
        # Remove all edges that contain the node
        del self.graph[node]

    def destroy_edges(self, node1, node2):
        if isinstance(node1, str):
            node1 = next((n for n in self.nodes if n.name == node1), None)

        if isinstance(node2, str):
            node2 = next((n for n in self.nodes if n.name == node2), None)

        if node1 is None or node2 is None:
            return

        a = self.graph[node1]
        for (node1, edge_info) in a:
            if node1 == node2:
                a.remove((node1, edge_info))
                return

        # if the graph is undirected, remove the edge in the other direction
        if not self.directed:
            a = self.graph[node2]
            for (node2, edge_info) in a:
                if node2 == node1:
                    a.remove((node2, edge_info))
                    return

    # Calculates the shortest distance from node1 to node2
    # without considering the vehicle's travel method and access level.
    # Uses Dijkstra's algorithm with a priority queue.
    # Returns None if the nodes are not in the graph or if there isn't any path
    def get_distance(self, node1, node2, vehicle):
        if isinstance(node1, str):
            node1 = next((n for n in self.nodes if n.name == node1), None)

        if isinstance(node2, str):
            node2 = next((n for n in self.nodes if n.name == node2), None)

        if node1 is None or node2 is None:
            return None

        # Priority queue for Dijkstra's algorithm
        priority_queue = [(0, node1)]  # (current_distance, current_node)
        distances = {node: float('inf') for node in self.nodes}
        distances[node1] = 0

        # Dictionary to track the predecessor of each node
        # Uncomment predecessors lines to print the path
        # predecessors = {node: None for node in self.nodes}

        # Set to track visited nodes
        visited = set()

        while priority_queue:
            current_distance, current_node = heappop(priority_queue)

            # If the current node is already visited, skip it
            if current_node in visited:
                continue

            visited.add(current_node)

            # If the current node is the destination, return the distance
            if current_node == node2:
                # path = []
                # while current_node:
                #     path.append(current_node.name)
                #     current_node = predecessors[current_node]
                # path.reverse()  # Reverse to get the path from start to end
                # print(f"Path found: {' -> '.join(path)}")
                return current_distance

            # Skip processing if this is not the shortest path to current_node
            if current_distance > distances[current_node]:
                continue

            neighbors = self.graph[current_node]
            for neighbor, (distance, _, edge_travel_method, edge_access_level) in neighbors:

                # Check if the vehicle can travel through the edge
                if not vehicle.is_travel_possible(edge_travel_method, edge_access_level):
                    continue

                # Calculate the potential new distance
                new_distance = current_distance + distance

                # Update shortest distance if a better path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    # predecessors[neighbor] = current_node
                    heappush(priority_queue, (new_distance, neighbor))

        # print(f"No path found from {node1.name} to {node2.name}.")
        # If we finish the loop without finding node2, return infinity
        return float('inf')

    def draw_matplotlib(self):
        # Create list of nodes
        g = nx.DiGraph()
        for node in self.nodes:
            g.add_node(node.name)
            for (adjacent, (distance, _, _, _)) in self.graph[node]:
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
        dot = (
            DigraphViz(format="png")
            if self.directed
            else GraphViz(format="png")
        )
        dot.attr(rankdir="TB")  # Top to bottom

        drawn_edges = set()

        # Add nodes and edges to the graph
        for node in self.nodes:

            # Add node with red color if it has a catastrophe
            if node.catastrophe is None:
                dot.node(node.name)
            else:
                dot.node(node.name, color='red')

            for adjacent, (distance, _, travel_method, access_level) in self.graph[node]:
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
                access_level = 4 - access_level  # Invert access level
                if (node.name, adjacent.name) not in drawn_edges:
                    dot.edge(node.name, adjacent.name,
                             label=str(distance), color=color,
                             penwidth=str(2 ** (access_level - 1)))
                    drawn_edges.add((adjacent.name, node.name))

        # Render the graph to a file and display it
        dot.render('/tmp/graph', view=True)
