import numpy as nu
import collections

def shortestPath(map):
    row_count = map.shape[0]
    col_count = map.shape[1]
    start = nu.where(map == "S")
    start = (int(start[0][0]), int(start[1][0]))
    paths = collections.deque([(start, [])])
    visited = set()
    visited.add(start)

    while paths:
        pos, path = paths.popleft()
        if map[pos[0], pos[1]] == "E":
            return "".join(path)
    
        for new_pos, dir in ((pos[0]+1, pos[1]), "D"), ((pos[0]-1, pos[1]), "U"), ((pos[0], pos[1]+1), "R"), ((pos[0], pos[1]-1), "L"):
            if 0 <= new_pos[0] < row_count and 0 <= new_pos[1] < col_count and map[new_pos[0], new_pos[1]] != "#" and new_pos not in visited:
                visited.add(new_pos)
                paths.append((new_pos, path + [dir]))

    return ""

def part_one():
    with open("./day_18/day_18_input.txt") as file:
        lines = [line.strip().split(",") for line in file.readlines()]
        lines = [(int(c[0]), int(c[1])) for c in lines]
        print(lines)
        map = nu.full((73, 73), ".")
        print(map)
        for i in range(map.shape[0]):
            map[i, 0] = "#"
            map[i, map.shape[1]-1] = "#"
        for i in range(map.shape[1]):
            map[0, i] = "#"
            map[map.shape[1]-1, i] = "#"
        map[1,1] = "S"
        map[71,71] = "E"
        for i in range(1024):
            map[lines[i][1]+1, lines[i][0]+1] = "#"
        print(map)
        #nu.savetxt("./day_18/map.txt", map, "%s", "")
        sp = shortestPath(map)
        print(f"Shortest path = {len(sp)}, {sp}")
        


def part_two():
    with open("./day_18/day_18_input.txt") as file:
        lines = [line.strip().split(",") for line in file.readlines()]
        lines = [(int(c[0]), int(c[1])) for c in lines]
        print(lines)
        map = nu.full((73, 73), ".")
        print(map)
        for i in range(map.shape[0]):
            map[i, 0] = "#"
            map[i, map.shape[1]-1] = "#"
        for i in range(map.shape[1]):
            map[0, i] = "#"
            map[map.shape[1]-1, i] = "#"
        map[1,1] = "S"
        map[71,71] = "E"
        for i in range(1024):
            map[lines[i][1]+1, lines[i][0]+1] = "#"
        #print(map)
        #nu.savetxt("./day_18/map.txt", map, "%s", "")
        for i in range(1024, len(lines)):
            map[lines[i][1]+1, lines[i][0]+1] = "#"
            sp = shortestPath(map)
            if len(sp) <= 0:
                print(f"Solution found item {i} with position {lines[i]}")
                break


if __name__ == "__main__":
    print("Advent of Code - Day 18")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
