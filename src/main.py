#!/usr/bin/env python3

from graph import data
import argparse


def input_option() -> int:
    try:
        option = int(input("Enter the option: "))
    except (ValueError, TypeError):
        option = -1  # Invalid option: continue
    except (EOFError, KeyboardInterrupt):
        option = 0  # Exit
    return option


def display_change_graph_menu(graph_option) -> None:
    print(
        "\n"
        f"Currently selected: {graph_option}\n"
        "Change graph to:\n"
        "1 - Graph 1\n"
        "2 - Graph 2\n"
        "3 - Graph 3\n"
        "0 - Back"
    )


def display_view_menu() -> None:
    print(
        "\n"
        "View menu:\n"
        "1 - Draw graph (graphviz)\n"
        "2 - Draw graph (matplotlib)\n"
        "3 - Print graph\n"
        "4 - Print graph nodes\n"
        "5 - Print graph edges\n"
        "6 - Print graph adjacency matrix\n"  # TODO Maybe?
        "0 - Back"
    )


def display_search_menu() -> None:
    print(
        "\n"
        "Search menu:\n"
        "1 - Breadth-first search\n"
        "2 - Depth-first search\n"
        "3 - Uniform-cost search\n"
        "4 - Greedy search\n"
        "5 - A* search\n"
        "9 - Change heuristic function\n"  # TODO change heuristic function menu
        "0 - Back"
    )


def display_main_menu(verbose) -> None:
    print(
        "\n"
        "Main menu:\n"
        "1 - Change graph\n"
        "2 - View menu\n"
        "3 - Search menu\n"
        "4 - " + ("Disable" if verbose else "Enable") + " verbose mode\n"
        "0 - Exit"
    )


def change_graph_menu(graph_option) -> None:
    while True:
        display_change_graph_menu(graph_option)
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                graph_option = 1
                break
            case 2:
                graph_option = 2
                break
            case 3:
                graph_option = 3
                break
            case _:
                print("Invalid option")
    graph = data.init_graph(graph_option)
    return graph, graph_option


def view_menu(graph) -> None:
    while True:
        display_view_menu()
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                graph.draw_graphviz()
            case 2:
                graph.draw_matplotlib()
            case 3:
                print(graph)
            case 4:
                print(graph.nodes)
            case 5:
                print(graph.edges)
            case 6:
                print(graph.adjacency_matrix)
            case _:
                print("Invalid option")
    pass


def search_menu(graph, verbose) -> None:
    # TODO
    pass


def main(verbose) -> None:
    graph_option = 1
    graph = data.init_graph(graph_option)

    while True:
        display_main_menu(verbose)
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                graph, graph_option = change_graph_menu(graph_option)
            case 2:
                view_menu(graph)
            case 3:
                search_menu(graph, verbose)
            case 4:
                verbose = not verbose
                print("Verbose mode " + ("enabled" if verbose else "disabled"))
            case _:
                print("Invalid option")


if __name__ == "__main__":
    # Parse command line arguments
    arg_parser = argparse.ArgumentParser(description="")  # TODO add description
    arg_parser.add_argument("-v", "--verbose",
                            help="Enable verbose mode",
                            action="store_true")
    args = arg_parser.parse_args()

    # Main menu loop
    main(verbose=args.verbose)
