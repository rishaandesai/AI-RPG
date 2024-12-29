import random
import sys


def a_star(start, goal, heuristic=lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])):
    def reconstruct_path(came_from, node):
        return reconstruct_path(came_from, came_from[node]) + [node] if node in came_from else [node]

    open_set, came_from = {start}, {}
    g_score, f_score = {start: 0}, {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda n: f_score.get(n, float('inf')))
        if current == goal:
            return reconstruct_path(came_from, goal)

        open_set.remove(current)
        for neighbor in [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.add(neighbor)
    return []


def generate(cells_x, cells_y, cell_size=5):
    class Cell:
        def __init__(self, x, y, id):
            self.x, self.y, self.id = x, y, id
            self.connected, self.room, self.connected_to = False, None, []

        def connect(self, other):
            self.connected_to.append(other)
            other.connected_to.append(self)
            self.connected = other.connected = True

    cells = {(x, y): Cell(x, y, y * cells_x + x) for y in range(cells_y) for x in range(cells_x)}
    first, last = random.choice(list(cells.values())), None
    current = first
    first.connected = True

    while any(not cell.connected for cell in cells.values()):
        unconnected_neighbors = [n for n in [(current.x + dx, current.y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                                 if n in cells and not cells[n].connected]
        if unconnected_neighbors:
            neighbor = cells[random.choice(unconnected_neighbors)]
            current.connect(neighbor)
            current, last = neighbor, neighbor
        else:
            current = random.choice([cell for cell in cells.values() if cell.connected])

    for _ in range(random.randint((cells_x + cells_y) // 4, (cells_x + cells_y) // 1.2)):
        a, b = random.sample(list(cells.values()), 2)
        if b not in a.connected_to:
            a.connect(b)

    tiles = {(x, y): " " for x in range(cells_x * cell_size) for y in range(cells_y * cell_size)}
    rooms = []
    for cell in cells.values():
        width, height = random.randint(3, cell_size - 2), random.randint(3, cell_size - 2)
        x, y = cell.x * cell_size + random.randint(1, cell_size - width - 1), cell.y * cell_size + random.randint(1, cell_size - height - 1)
        room = [(x + dx, y + dy) for dx in range(width) for dy in range(height)]
        cell.room = room
        rooms.append(room)

    for a, b in {(min(a.id, b.id), max(a.id, b.id)): (a.room, b.room) for a in cells.values() for b in a.connected_to}.values():
        corridor = [tile for tile in a_star(random.choice(a), random.choice(b)) if tile not in a + b]
        rooms.append(corridor)

    for room in rooms:
        for tile in room:
            tiles[tile] = "."

    for x, y in [(x, y) for x in range(cells_x * cell_size) for y in range(cells_y * cell_size) if tiles[(x, y)] == " "]:
        if any(tiles.get((x + dx, y + dy), " ") == "." for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
            tiles[(x, y)] = "#"

    tiles[random.choice(first.room)], tiles[random.choice(last.room)] = "<", ">"

    for y in range(cells_y * cell_size):
        sys.stdout.write("".join(tiles[(x, y)] for x in range(cells_x * cell_size)) + "\n")


if __name__ == "__main__":
    generate(2, 1, 8)