import numpy as nu, sys, collections
from functools import cache


def searchPath(map, position, direction, cost, path, paths, tested_path):
    if position in path or position in tested_path:
        tested_path.union(set(path))
        return
    if cost > 350000:
        tested_path.union(set(path))
        return
    path.append(position)
    if map[position[0], position[1]] == "E":
        paths.append((cost, path))
        print(f"Paths found = {len(paths)}\r", end="")
        return
    if direction == 0: # Haut
        if map[position[0]-1, position[1]] != "#":
            searchPath(map, (position[0]-1, position[1]), 0, cost+1, path.copy(), paths, tested_path)
        if map[position[0], position[1]-1] != "#":
            searchPath(map, (position[0], position[1]-1), 3, cost+1001, path.copy(), paths, tested_path)
        if map[position[0], position[1]+1] != "#":
            searchPath(map, (position[0], position[1]+1), 1, cost+1001, path.copy(), paths, tested_path)
    if direction == 1: # Droite
        if map[position[0], position[1]+1] != "#":
            searchPath(map, (position[0], position[1]+1), 1, cost+1, path.copy(), paths, tested_path)
        if map[position[0]-1, position[1]] != "#":
            searchPath(map, (position[0]-1, position[1]), 0, cost+1001, path.copy(), paths, tested_path)
        if map[position[0]+1, position[1]] != "#":
            searchPath(map, (position[0]+1, position[1]), 2, cost+1001, path.copy(), paths, tested_path)
    if direction == 2: # Bas
        if map[position[0]+1, position[1]] != "#":
            searchPath(map, (position[0]+1, position[1]), 2, cost+1, path.copy(), paths, tested_path)
        if map[position[0], position[1]-1] != "#":
            searchPath(map, (position[0], position[1]-1), 3, cost+1001, path.copy(), paths, tested_path)
        if map[position[0], position[1]+1] != "#":
            searchPath(map, (position[0], position[1]+1), 1, cost+1001, path.copy(), paths, tested_path)
    if direction == 3: # Gauche
        if map[position[0], position[1]-1] != "#":
            searchPath(map, (position[0], position[1]-1), 3, cost+1, path.copy(), paths, tested_path)
        if map[position[0]-1, position[1]] != "#":
            searchPath(map, (position[0]-1, position[1]), 0, cost+1001, path.copy(), paths, tested_path)
        if map[position[0]+1, position[1]] != "#":
            searchPath(map, (position[0]+1, position[1]), 2, cost+1001, path.copy(), paths, tested_path)
    tested_path.union(set(path))
    return

def getAvailableDirection(map, position, direction):
    directions = []
    if direction == 0: # Haut
        if map[position[0]-1, position[1]] != "#":
            directions.append(0)
        if map[position[0], position[1]+1] != "#":
            directions.append(1)
        if map[position[0], position[1]-1] != "#":
            directions.append(3)
    if direction == 1: # Droite
        if map[position[0], position[1]+1] != "#":
            directions.append(1)
        if map[position[0]-1, position[1]] != "#":
            directions.append(0)
        if map[position[0]+1, position[1]] != "#":
            directions.append(2)
    if direction == 2: # Bas
        if map[position[0]+1, position[1]] != "#":
            directions.append(2)
        if map[position[0], position[1]+1] != "#":
            directions.append(1)
        if map[position[0], position[1]-1] != "#":
            directions.append(3)
    if direction == 3: # Gauche
        if map[position[0], position[1]-1] != "#":
            directions.append(3)
        if map[position[0]-1, position[1]] != "#":
            directions.append(0)
        if map[position[0]+1, position[1]] != "#":
            directions.append(2)
    return directions

def getNextPosition(position, direction):
    new_position = position
    if direction == 0:
        new_position = (position[0]-1, position[1])
    elif direction == 1:
        new_position = (position[0], position[1]+1)
    elif direction == 2:
        new_position = (position[0]+1, position[1])
    elif direction == 3:
        new_position = (position[0], position[1]-1)
    return new_position

def searchPath2(map, position, direction, cost, path, paths, tested_paths = []):
    tested_path = []
    found = False
    while map[position[0], position[1]] != "E" and cost < 400000:
        if position in path or position in tested_paths:
            break
        path.append(position)
        tested_path.append(position)
        directions = getAvailableDirection(map, position, direction)
        if len(directions) <= 0:
            break
        if len(directions) > 1:
            bad_path = set()
            for i in range(0, len(directions)):
                success, sub_path = searchPath2(map, getNextPosition(position, directions[i]), directions[i], cost + (1 if direction == directions[i] else 1001), path.copy(), paths, tested_paths)
                if not success:
                    bad_path |= set(sub_path) #(set([p for p in sub_path if p not in path]))
                    #sub_path = [p for p in sub_path if p not in path]
                    tested_paths.extend([bad_path])
                #found |= success
            #tested_paths.extend(bad_path)
        elif len(directions) > 0:
            cost += 1 if direction == directions[0] else 1001
            direction = directions[0]
            position = getNextPosition(position, direction)
    else:
         if map[position[0], position[1]] == "E":
            paths.append((cost, path))
            print(f"Paths found = {len(paths)}\r", end="")
            found = True
    
    return found, tested_path

def findRoute(paths, start, end, route, routes):
    route.append(start)
    if len(route) > 200:
        return
    for path in paths[start]:
        if path == end:
            route.append(end)
            routes.append(route)
            break
        elif path not in route:
            findRoute(paths, path, end, route.copy(), routes)

def findRoutesMulti(paths, start, end):
    routes_found = {}
    start_routes = []
    for pos in paths[start]:
        start_routes.append([start, pos])
    end_routes = []
    for pos in paths[end]:
        end_routes.append([end, pos])
    iter_count = 0
    while True:
        # find end routes
        for route in end_routes:
            if route[-1] in paths:
                path = paths[route[-1]]
                for pos in path:
                    for route2 in start_routes:
                        if pos in route2 and pos not in routes_found:
                            routes_found[pos] = route2.copy().extend(route)
                            print(f"Route found: {pos}")
                    if pos not in route:
                        if pos == path[-1]:
                            route.append(pos)
                        else:
                            route_added = route.copy()
                            route_added.append(pos)
                            end_routes.append(route_added)
        #find start route
        for route in start_routes:
            path = paths[route[-1]]
            if route[-1] in paths:
                for pos in path:
                    if pos not in route:
                        if pos == path[-1]:
                            route.append(pos)
                        else:
                            route_added = route.copy()
                            route_added.append(pos)
                            start_routes.append(route_added)
        #find intersection
        if len(routes_found) > 5 or iter_count > 9999999:
            break
    return routes_found

def removeDeadEnd(paths, exceptions = []):
    deadEnds = [path[0] for path in paths.items() if len(path[1]) <= 1 and path[0] not in exceptions]
    while len(deadEnds) > 0:
        for path in paths.items():
            i = 0
            while i < len(path[1]):
                if path[1][i] in deadEnds:# and path[0] not in exceptions:
                    path[1].remove(path[1][i])
                else:
                    i += 1
        for deadEnd in deadEnds:
            del paths[deadEnd]
        deadEnds = [path[0] for path in paths.items() if len(path[1]) <= 1 and path[0] not in exceptions]

def findPaths(map, intersections):
    paths = {}
    for intersection in intersections:
        neighbours = [i for i in intersections if i[0] == intersection[0] or i[1] == intersection[1]]
        top = None
        left = None
        bottom = None
        right = None
        for neighbour in neighbours:
            if neighbour[0] == intersection[0]:
                if neighbour[1] > intersection[1] and len(nu.where(map[neighbour[0], intersection[1]:neighbour[1]] == "#")[0]) <= 0 and (top == None or top[1] > neighbour[1]):
                    top = neighbour
                elif neighbour[1] < intersection[1] and len(nu.where(map[neighbour[0], neighbour[1]:intersection[1]] == "#")[0]) <= 0 and (bottom == None or bottom[1] < neighbour[1]):
                    bottom = neighbour
            elif neighbour[1] == intersection[1]:
                if neighbour[0] > intersection[0] and len(nu.where(map[intersection[0]:neighbour[0], neighbour[1]] == "#")[0]) <= 0 and (right == None or right[0] > neighbour[0]):
                    right = neighbour
                elif neighbour[0] < intersection[0] and len(nu.where(map[neighbour[0]:intersection[0], neighbour[1]] == "#")[0]) <= 0 and (left == None or left[0] < neighbour[0]):
                    left = neighbour
        neighbours = []
        if top != None:
            neighbours.append(top)
        if bottom != None:
            neighbours.append(bottom)
        if right != None:
            neighbours.append(right)
        if left != None:
            neighbours.append(left)
        paths[intersection] = neighbours
    return paths

def findIntersections(map):
    intersections = []
    for row in range(1, map.shape[0]-1):
        for col in range(1, map.shape[1]-1):
            if map[row, col] != "#" and (((map[row-1, col] != '#' and map[row+1, col] == '#') or \
                (map[row-1, col] == '#' and map[row+1, col] != '#')) or ((map[row, col-1] != '#' and map[row, col+1] == '#') or \
                (map[row, col-1] == '#' and map[row, col+1] != '#'))):
                intersections.append((row, col))
    return intersections


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
    with open("./day_16/day_16_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        start_position = nu.where(map == "S")
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        end_position = nu.where(map == "E")
        end_position = (int(end_position[0][0]), int(end_position[1][0]))
        intersections = findIntersections(map)
        #print(intersections)
        #input()
        paths = findPaths(map, intersections)
        #print(paths)
        removeDeadEnd(paths, [start_position, end_position])
        #print(paths)
        routes = []
        #findRoute(paths, start_position, end_position, [], routes)
        routes = findRoutesMulti(paths, start_position, end_position)
        print(routes)
        print(len(routes))
        #searchPath(map, start_position, 1, 0, [], paths, set())
        #searchPathArray(lines, start_position, 1, 0, [], paths)
        #searchPath2(map, start_position, 1, 0, [], paths)
        #print(f"Number of paths found = {len(paths)}")
        #lowest = (999999999999999, [])
        #for path in paths:
        #    if lowest[0] > path[0]:
        #        lowest = path
        #for pos in lowest[1]:
        #    map[pos[0], pos[1]] = "+"
        #nu.set_printoptions(threshold=sys.maxsize)
        #print(map)
        #nu.savetxt(".\\day_6\\trap_{%04d}x{%04d}.txt".format(obstruction_position[0], obstruction_position[1]), map_test, "%s", "")
        #print(f"Lowest path score = {lowest[0]}")

def part_two():
    total_gps = 0
    with open("./day_16/day_16_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        start_position = nu.where(map == "S")
        start_position = (int(start_position[0][0]), int(start_position[1][0]))

if __name__ == "__main__":
    #sys.setrecursionlimit(3000)
    print("Advent of Code - Day 16")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
