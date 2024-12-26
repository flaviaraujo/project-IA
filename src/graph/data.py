from .graph import Graph


def init_graph(option: int) -> Graph:
    graph = Graph(directed=False)
    match option:
        case 1:
            # TODO Create catastrophes
            # c1 = Catastrophe(...)
            # c2 = Catastrophe(...)

            # Create the nodes
            n_A = graph.add_node("A")
            n_B = graph.add_node("B", catastrophe=True)
            n_C = graph.add_node("C")
            n_D = graph.add_node("D")
            n_E = graph.add_node("E")
            n_F = graph.add_node("F")
            # n_F = graph.add_node("F", catastrophe=c2)

            # Create the edges
            try:
                graph.add_edge(n_A, n_B, 2, travel_method="air")
                graph.add_edge(n_A, n_B, 3, travel_method="land")
                graph.add_edge(n_A, n_B, 3, travel_method="water")
                graph.add_edge(n_A, n_C, 3, travel_method="land")
                graph.add_edge(n_B, n_D, 4, travel_method="water")
                graph.add_edge(n_B, n_E, 5, travel_method="air")
                graph.add_edge(n_B, n_E, 6, travel_method="land")
                graph.add_edge(n_C, n_F, 6, travel_method="land")
                graph.add_edge(n_D, n_E, 7, travel_method="land")
                graph.add_edge(n_E, n_F, 8, travel_method="land")
            except ValueError as e:
                print(e)
                return None

            # TODO Add heuristics
            # OPTION calculate heuristics
            # EXAMPLE sum the distances from all catastrophes

            # TODO Add destructible nodes or edges

            return graph
        case 2:
            return None
        case 3:
            return None
        case _:
            raise ValueError("Invalid option")
