import math
from queue import PriorityQueue
from itertools import count
from Node import Node

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None


class Warehouse:
    def __init__(self, filename):

        # ===== DEBUG START =====
        print(f"\n--- Testing {filename} ---")
        print(f"[DEBUG] Loading {filename}...")
        # =======================

        with open(filename, 'r') as f:
            lines = f.readlines()

        self.grid = [list(line.rstrip('\n')) for line in lines]
        self.height = len(self.grid)
        self.width = max(len(row) for row in self.grid)

        # Make all rows equal length
        for row in self.grid:
            while len(row) < self.width:
                row.append(' ')

        self.start = None
        self.goal = None
        self.walls = set()

        # Parse grid
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] == 'A':
                    self.start = (r, c)
                elif self.grid[r][c] == 'B':
                    self.goal = (r, c)
                elif self.grid[r][c] == '#':
                    self.walls.add((r, c))

        if self.start is None or self.goal is None:
            raise ValueError("Missing A or B in grid")

        # ===== DEBUG OUTPUT (YOU REQUESTED THIS) =====
        print(f"[DEBUG] Start: {self.start}, Goal: {self.goal}")
        print(f"[DEBUG] Walls: {len(self.walls)}")
        # ============================================

    # Heuristic (Euclidean distance)
    def heuristic(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def neighbors(self, state):
        r, c = state

        moves = [
            ("up", (r - 1, c)),
            ("down", (r + 1, c)),
            ("left", (r, c - 1)),
            ("right", (r, c + 1))
        ]

        result = []
        for action, (nr, nc) in moves:
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if (nr, nc) not in self.walls:
                    result.append((action, (nr, nc)))

        return result

    def solve(self, algorithm="astar"):
        frontier = PriorityQueue()
        counter = count()

        start_node = Node(self.start, cost=0)
        frontier.put((0, next(counter), start_node))

        cost_so_far = {self.start: 0}
        explored = set()

        while not frontier.empty():
            _, _, current = frontier.get()

            if current.state == self.goal:
                path = self.reconstruct_path(current)
                return path, explored

            explored.add(current.state)

            for action, next_state in self.neighbors(current.state):

                if algorithm == "greedy":
                    if next_state not in explored:
                        child = Node(next_state, current, action)
                        priority = self.heuristic(next_state)
                        frontier.put((priority, next(counter), child))

                elif algorithm == "astar":
                    new_cost = cost_so_far[current.state] + 1

                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost
                        child = Node(next_state, current, action, new_cost)

                        priority = new_cost + self.heuristic(next_state)
                        frontier.put((priority, next(counter), child))

        return None, explored

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    def visualize(self, path, explored, filename="warehouse_path.png"):
        if Image is None:
            print("Pillow not installed")
            return

        cell_size = 40
        img = Image.new("RGB", (self.width * cell_size, self.height * cell_size), "white")
        draw = ImageDraw.Draw(img)

        for r in range(self.height):
            for c in range(self.width):
                x, y = c * cell_size, r * cell_size

                if (r, c) in self.walls:
                    color = (50, 50, 50)
                elif (r, c) == self.start:
                    color = (0, 255, 0)
                elif (r, c) == self.goal:
                    color = (255, 0, 0)
                elif isinstance(path, list) and (r, c) in path:
                    color = (0, 0, 255)
                elif (r, c) in explored:
                    color = (255, 255, 0)
                else:
                    color = (255, 255, 255)

                draw.rectangle(
                    [x, y, x + cell_size, y + cell_size],
                    fill=color,
                    outline=(200, 200, 200)
                )

        img.save(filename)
        print(f"Saved {filename}")