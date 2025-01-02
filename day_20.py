import numpy as nu
import collections

def shortestPath(map, start, end, max_len = 0, wall_tile = "#"):
    row_count = map.shape[0]
    col_count = map.shape[1]
    #start = nu.where(map == "S")
    #start = (int(start[0][0]), int(start[1][0]))
    paths = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while paths:
        pos, path = paths.popleft()
        if pos == end: #map[pos[0], pos[1]] == "E":
            return path
    
        for new_pos, dir in ((pos[0]+1, pos[1]), "D"), ((pos[0]-1, pos[1]), "U"), ((pos[0], pos[1]+1), "R"), ((pos[0], pos[1]-1), "L"):
            if 0 < new_pos[0] < row_count-1 and 0 < new_pos[1] < col_count-1 and map[new_pos[0], new_pos[1]] != wall_tile and new_pos not in visited:
                visited.add(new_pos)
                if max_len <= 0 or len(path) < max_len:
                    paths.append((new_pos, path + [new_pos]))

    return []

def findCheats(map, path, min_cheat = 100):
    cheats = set()
    for i in range(len(path)-min_cheat):
        for j in range(i+min_cheat+2, len(path)):
            if (path[i][0] == path[j][0] and abs(path[i][1] - path[j][1]) == 2) and \
                map[path[i][0], (path[i][1] + path[j][1])//2] == "#":
                cheats.add((path[i][0], (path[i][1] + path[j][1])//2, j-i-2))
            elif (path[i][1] == path[j][1] and abs(path[i][0] - path[j][0]) == 2) and \
                map[(path[i][0] + path[j][0])//2, path[i][1]] == "#":
                cheats.add(((path[i][0] + path[j][0])//2, path[i][1], j-i-2))
    return cheats

def findCheatsMulti(map, path, min_cheat = 100, max_len = 20):
    cheats = set()
    #cheats_found = set()
    for i in range(len(path)-min_cheat):
        for j in range(i+min_cheat+2, len(path)):
            if "#" in map[path[i][0], path[i][1]:path[j][1] if path[i][1] < path[j][1] else path[j][1]:path[i][1]] or \
                "#" in map[path[i][0]:path[j][0] if path[i][0] < path[j][0] else path[j][0]:path[i][0], path[i][1]]:
                pass
#            if (map[path[i][0], path[i][1] + (1 if path[i][1] < path[j][1] else -1)] == "#") and \
#                (map[path[j][0], path[j][1] + (1 if path[j][1] < path[i][1] else -1)] == "#" or map[path[j][0] + (1 if path[j][0] < path[i][0] else -1), path[j][1]] == "#"):
#                test_map = map.copy() #[1:map.shape[0]-1, 1:map.shape[1]-1]
                #test_map[path[i][0], path[i][1]] = "#"
                #test_map[path[j][0], path[j][1]] = "#"
#                test_pos = (path[i][0], path[i][1] + (1 if path[i][1] < path[j][1] else -1))
#                test_path = shortestPath(test_map, test_pos, path[j], 20, "*")
#                if 1 < len(test_path) <= 20 and (j-i-len(test_path)) >= min_cheat:
#                    if (test_pos, path[j]) not in cheats_found:
#                        cheats_found.add((test_pos, path[j]))
#                        cheats.add((test_pos, path[j], j-i-len(test_path), len(test_path)))
            
#            if (map[path[i][0] + (1 if path[i][0] < path[j][0] else -1), path[i][1]] == "#") and \
#                (map[path[j][0], path[j][1] + (1 if path[j][1] < path[i][1] else -1)] == "#" or map[path[j][0] + (1 if path[j][0] < path[i][0] else -1), path[j][1]] == "#"):
#                test_map = map.copy() #[1:map.shape[0]-1, 1:map.shape[1]-1]
                #test_map[path[i][0], path[i][1]] = "#"
                #test_map[path[j][0], path[j][1]] = "#"
#                test_pos = (path[i][0] + (1 if path[i][0] < path[j][0] else -1), path[i][1])
#                test_path = shortestPath(test_map, test_pos, path[j], 20, "*")
#                if 1 < len(test_path) <= 20 and (j-i-len(test_path)) >= min_cheat:
#                    if (test_pos, path[j]) not in cheats_found:
#                        cheats_found.add((test_pos, path[j]))
#                        cheats.add((test_pos, path[j], j-i-len(test_path), len(test_path)))
            for test_pos in (path[i][0]+1, path[i][1]), (path[i][0]-1, path[i][1]), (path[i][0], path[i][1]+1), (path[i][0], path[i][1]-1):
                if (map[test_pos[0], test_pos[1]] == "#") and 0 < test_pos[0] < map.shape[0]-1 and 0 < test_pos[1] < map.shape[1]-1: # and (map[path[j][0], path[j][1] + (1 if path[j][1] < path[i][1] else -1)] == "#" or map[path[j][0] + (1 if path[j][0] < path[i][0] else -1), path[j][1]] == "#"):
                    test_map = map.copy() #[1:map.shape[0]-1, 1:map.shape[1]-1]
                    test_path = shortestPath(test_map, test_pos, path[j], 19, "*")
                    if 1 < len(test_path) < 20 and (j-i-len(test_path)) >= min_cheat:
                        #if (test_pos, path[j]) not in cheats_found:
                            #cheats_found.add((test_pos, path[j]))
                        cheats.add((test_pos, path[j], j-i-len(test_path), len(test_path)))
    cheats_dp = cheats
    while len(cheats_dp) > 0:
        cheats_dp = set([c for c in cheats if c[0] ==])
    return cheats

def cheatsReport(cheats):
    report = {}
    cheats = list(cheats)
    while len(cheats) > 0:
        cheats_group = [c for c in cheats if c[2] == cheats[0][2]]
        report[cheats[0][2]] = len(cheats_group)
        cheats = list(set(cheats) - set(cheats_group))
    return report


def part_one():
    with open("./day_20/day_20_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        start_position = nu.where(map == "S")
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        end_position = nu.where(map == "E")
        end_position = (int(end_position[0][0]), int(end_position[1][0]))
        path = shortestPath(map, start_position, end_position)
        #print(path)
        min_cheat = 100
        cheats = findCheats(map, path, min_cheat)
        #print(cheats)
        report = cheatsReport(cheats)
        print(report)
        print(f"Number of cheats = {len(cheats)}")
        #tested_cheats = set()
        #for cheat in cheats:
        #    map_tested = map.copy()
        #    map[cheat[0], cheat[1]] = "."
        #    tested_path = shortestPath(map_tested)
        #    if len(tested_path) < (len(path) - min_cheat):
        #        tested_cheats.add(cheat)
        #print(f"Number of tested cheats = {len(tested_cheats)}")


def part_two():
    with open("./day_20/day_20_input_sm.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        start_position = nu.where(map == "S")
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        end_position = nu.where(map == "E")
        end_position = (int(end_position[0][0]), int(end_position[1][0]))
        path = shortestPath(map, start_position, end_position)
        #print(path)
        min_cheat = 50
        cheats = findCheatsMulti(map, path, min_cheat, 20)
        print(cheats)
        report = cheatsReport(cheats)
        print(report)
        print(f"Number of cheats = {len(cheats)}")

if __name__ == "__main__":
    #sys.setrecursionlimit(3000)
    print("Advent of Code - Day 20")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
