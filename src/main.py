#!/usr/bin/env python3

import simulation_data
from graph.heurisitics import (
    heuristic_fn1,
    heuristic_fn2,
    heuristic_fn3
)

import argparse         # command line arguments
import json             # pretty printing


def input_option() -> int:
    try:
        option = int(input("Enter the option: "))
    except (ValueError, TypeError):
        option = -1  # Invalid option: continue
    except (EOFError, KeyboardInterrupt):
        option = 0  # Exit
    return option


def display_change_simulation_menu(simulation_option) -> None:
    print(
        "\n"
        f"Currently selected: {simulation_option}\n"
        "Change to:\n"
        "1 -> Medium city with 10 nodes\n"
        "2 -> Azores archipelago with 9 nodes\n"
        "3 -> Simulation test\n"
        "0 -> Back"
    )


def display_view_graph_menu() -> None:
    print(
        "\n"
        "View menu:\n"
        "1 -> Draw graph with graphviz\n"
        "2 -> Draw graph with matplotlib\n"
        "3 -> Print graph\n"
        "4 -> Print graph nodes\n"
        "5 -> Print graph edges\n"
        "6 -> Print heuristic values\n"
        "0 -> Back"
    )


def display_search_menu() -> None:
    print(
        "\n"
        "Search menu:\n"
        "1 -> Breadth-first search\n"
        "2 -> Depth-first search\n"
        "3 -> Uniform-cost search\n"
        "4 -> Greedy search\n"
        "5 -> A* search\n"
        "9 -> Change heuristic\n"
        "0 -> Back"
    )


def display_change_heuristic_menu(heuristic_option) -> None:
    print(
        "\n"
        f"Currently selected: {heuristic_option}\n"
        "Change heuristic function:\n"
        "1 -> Heuristic 1\n"
        "2 -> Heuristic 2\n"
        "3 -> Heuristic 3\n"
        "0 -> Back"
    )


def display_main_menu(verbose) -> None:
    print(
        "\n"
        "Main menu:\n"
        "1 -> Change simulation\n"
        "2 -> View graph menu\n"
        "3 -> View catastrophes, fleet and supplies\n"
        "4 -> Search menu\n"
        "9 -> " + ("Disable" if verbose else "Enable") + " verbose mode\n"
        "0 -> Exit"
    )


def change_simulation_menu(mission_planner, heuristic_option, simulation_option):
    while True:
        display_change_simulation_menu(simulation_option)
        option = input_option()
        match option:
            case 0:
                return mission_planner, heuristic_option, simulation_option
            case 1:
                simulation_option = 1
                break
            case 2:
                simulation_option = 2
                break
            case 3:
                simulation_option = 3
                break
            case _:
                print("Invalid option")

    mission_planner, heuristic_option = \
        simulation_data.init_simulation(simulation_option)

    return (mission_planner, heuristic_option, simulation_option)


def view_graph_menu(graph) -> None:
    while True:
        display_view_graph_menu()
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                graph.draw_graphviz()
            case 2:
                graph.draw_matplotlib()
            case 3:
                print(graph, end="")
            case 4:
                print(json.dumps(graph.serialize_nodes(), indent=2))
            case 5:
                graph.print_edges()
            case 6:
                print("Heuristic values:")
                print(json.dumps(graph.h, indent=2))
            case _:
                print("Invalid option")
    pass


def search_menu(mission_planner, heuristic_option, verbose) -> None:
    while True:
        display_search_menu()
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                mission_planner.planner(verbose, "bfs")
            case 2:
                mission_planner.planner(verbose, "dfs")
            case 3:
                mission_planner.planner(verbose, "ucs")
            case 4:
                mission_planner.planner(verbose, "greedy")
            case 5:
                mission_planner.planner(verbose, "astar")
            case 9:
                heuristic_option = change_heuristic_menu(heuristic_option, mission_planner)
            case _:
                print("Invalid option")


def change_heuristic_menu(heuristic_option, mission_planner) -> int:
    while True:
        display_change_heuristic_menu(heuristic_option)
        option = input_option()
        match option:
            case 0:
                return
            case 1:
                heuristic_option = 1
                heuristic_fn1({
                    'graph': mission_planner.graph,
                    'catastrophes': mission_planner.catastrophes,
                    'vehicles': mission_planner.get_vehicles_list()
                })
                break
            case 2:
                heuristic_option = 2
                heuristic_fn2({
                    'graph': mission_planner.graph,
                    'catastrophes': mission_planner.catastrophes,
                    'vehicles': mission_planner.get_vehicles_list()
                })
                break
            case 3:
                heuristic_option = 3
                heuristic_fn3({
                    'graph': mission_planner.graph,
                    'catastrophes': mission_planner.catastrophes,
                    'vehicles': mission_planner.get_vehicles_list()
                })
                break
            case _:
                print("Invalid option")

    return heuristic_option


def main(verbose) -> None:
    simulation_option = 1
    mission_planner, heuristic_option = \
        simulation_data.init_simulation(simulation_option)

    while True:
        display_main_menu(verbose)
        option = input_option()
        match option:
            case 0:
                break
            case 1:
                mission_planner, heuristic_option, simulation_option = \
                    change_simulation_menu(mission_planner, heuristic_option, simulation_option)
            case 2:
                view_graph_menu(mission_planner.graph)
            case 3:
                print("Catastrophes:")
                print(json.dumps(mission_planner.serialize_catastrophes(), indent=2))

                print("\nFleet:")
                print(json.dumps(mission_planner.serialize_fleet(), indent=2))

                print("\nSupplies:")
                print(json.dumps(mission_planner.serialize_supplies(), indent=2))
            case 4:
                search_menu(mission_planner, heuristic_option, verbose)
            case 9:
                verbose = not verbose
                print("Verbose mode " + ("enabled" if verbose else "disabled"))
            case _:
                print("Invalid option")


if __name__ == "__main__":
    # Parse command line verbose argument
    arg_parser = argparse.ArgumentParser(description="Mission Planner")
    arg_parser.add_argument("-v", "--verbose",
                            help="Enable verbose mode",
                            action="store_true")
    args = arg_parser.parse_args()

    # Main menu loop
    main(verbose=args.verbose)
