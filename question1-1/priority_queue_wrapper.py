import math
from queue import PriorityQueue
from itertools import count
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None
import os


# ---------------------------
# Node Class
# ---------------------------
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost  # g(n)


# ---------------------------
# Warehouse Class
# ---------------------------
class Warehouse:
    def __init__(self, filename):
        print(f"\n[DEBUG] Loading {filename}...")

        with open(filename, 'r') as f:
            lines = f.readlines()
            self.grid = [list(line.rstrip('\n')) for line in lines]

        self.height = len(self.grid)
        if self.height == 0:
            raise ValueError("Empty file")

        self.width = max(len(row) for row in self.grid)

        # Normalize rows
        for row in self.grid:
            while len(row) < self.width:
                row.append(' ')

        self.start = None
        self.goal = None
        self.walls = set()

        # Parse grid
        for r in range(self.height):
            for c in range(self.width):
                cell = self.grid[r][c]
                if cell == 'A':
                    self.start = (r, c)
                elif cell == 'B':
                    self.goal = (r, c)
                elif cell == '#':
                    self.walls.add((r, c))

        if self.start is None or self.goal is None:
            raise ValueError("Missing A or B in grid")

        print(f"[DEBUG] Start: {self.start}, Goal: {self.goal}")
        print(f"[DEBUG] Walls: {len(self.walls)}")

    # ---------------------------
    # Heuristic (Euclidean)
    # ---------------------------
    def heuristic(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # ---------------------------
    # Neighbors
    # ---------------------------
    def neighbors(self, state):
        r, c = state
        moves = [
            ('up', (r - 1, c)),
            ('down', (r + 1, c)),
            ('left', (r, c - 1)),
            ('right', (r, c + 1))
        ]

        result = []
        for action, (nr, nc) in moves:
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if (nr, nc) not in self.walls:
                    result.append((action, (nr, nc)))

        return result

    # ---------------------------
    # SOLVE (Greedy or A*)
    # ---------------------------
    def solve(self, algorithm="astar"):
        print(f"\n[DEBUG] Running {algorithm.upper()}...")

        start_node = Node(self.start)

        frontier = PriorityQueue()
        counter = count()  # 🔥 tie-breaker


        frontier.put((0, next(counter), start_node))

        cost_so_far = {self.start: 0}
        self.explored_nodes = set()

        while not frontier.empty():
            _, _, current = frontier.get()

            # Goal check
            if current.state == self.goal:
                print("[DEBUG] Goal reached!")
                return self.reconstruct_path(current)

            self.explored_nodes.add(current.state)

            for action, next_state in self.neighbors(current.state):
                new_cost = cost_so_far[current.state] + 1

                # allow better paths
                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost

                    child = Node(next_state, current, action, new_cost)

                    if algorithm == "greedy":
                        priority = self.heuristic(next_state)
                    else:  # A*
                        priority = new_cost + self.heuristic(next_state)

                    frontier.put((priority, next(counter), child))

        print("[DEBUG] No path found")
        return None

    # ---------------------------
    # Reconstruct Path
    # ---------------------------
    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        print(f"[DEBUG] Path length: {len(path)}")
        return path

    # ---------------------------
    # Visualization
    # ---------------------------
    def visualize(self, path, filename="warehouse_path.png"):
        if path is None or Image is None:
            print("No visualization available")
            return

        cell_size = 40
        img = Image.new("RGB", (self.width * cell_size, self.height * cell_size), "white")
        draw = ImageDraw.Draw(img)

        for r in range(self.height):
            for c in range(self.width):
                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if (r, c) in self.walls:
                    color = (50, 50, 50)
                elif (r, c) == self.start:
                    color = (0, 255, 0)
                elif (r, c) == self.goal:
                    color = (255, 0, 0)
                elif (r, c) in path:
                    color = (0, 0, 255)
                elif (r, c) in self.explored_nodes:
                    color = (255, 255, 0)
                else:
                    color = (255, 255, 255)

                draw.rectangle([x1, y1, x2, y2], fill=color, outline=(200, 200, 200))

        img.save(filename)
        print(f"✓ Saved {filename}")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("WAREHOUSE PATHFINDING (A* & GREEDY)")
    print("=" * 50)

    test_files = ["warehouse_small.txt", "warehouse_medium.txt", "warehouse_hard.txt"]

    for filename in test_files:
        try:
            print(f"\n--- Testing {filename} ---")

            warehouse = Warehouse(filename)

            # Greedy
            path_greedy = warehouse.solve("greedy")
            warehouse.visualize(path_greedy, f"greedy_{filename}.png")

            # A*
            path_astar = warehouse.solve("astar")
            warehouse.visualize(path_astar, f"astar_{filename}.png")

        except Exception as e:
            print(f"Error: {e}")    



 
