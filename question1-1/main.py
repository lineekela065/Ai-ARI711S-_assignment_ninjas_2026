from warehouse_solver import Warehouse

if __name__ == "__main__":

    print("=" * 50)
    print("WAREHOUSE PATHFINDING (A* & GREEDY)")
    print("=" * 50)

    files = ["warehouse_small.txt", "warehouse_medium.txt", "warehouse_hard.txt"]

    for file in files:
        print(f"\n===== {file} =====")

        w = Warehouse(file)

        # GREEDY
        path_g, explored_g = w.solve("greedy")

        if isinstance(path_g, list):
            print(f"Greedy Path Length: {len(path_g)}")
        else:
            print("Greedy: No path found")

        print(f"Greedy Explored: {len(explored_g)}")
        w.visualize(path_g, explored_g, f"greedy_{file}.png")

        # A*
        path_a, explored_a = w.solve("astar")

        if isinstance(path_a, list):
            print(f"A* Path Length: {len(path_a)}")
        else:
            print("A*: No path found")

        print(f"A* Explored: {len(explored_a)}")
        w.visualize(path_a, explored_a, f"astar_{file}.png")