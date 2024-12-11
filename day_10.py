import numpy as nu

def find_trailheads(map):
    return [(int(point[0]), int(point[1])) for point in nu.transpose(nu.where(map == 0))]

def calculate_trail_ends(map, point, ends = [], trails = []):
    row_max = map.shape[0] - 1
    col_max = map.shape[1] - 1
    trails.append(point)
    if map[point[0], point[1]] == 9:
        if not point in ends:
            ends.append(point)
            #print(f"found={point}")
        return ends, trails
    else:
        if point[0] > 0 and map[point[0]-1, point[1]] == (map[point[0], point[1]] + 1):
            calculate_trail_ends(map, (point[0]-1, point[1]), ends, trails)
        if point[0] < row_max and map[point[0]+1, point[1]] == (map[point[0], point[1]] + 1):
            calculate_trail_ends(map, (point[0]+1, point[1]), ends, trails)
        if point[1] > 0 and map[point[0], point[1]-1] == (map[point[0], point[1]] + 1):
            calculate_trail_ends(map, (point[0], point[1]-1), ends, trails)
        if point[1] < col_max and map[point[0], point[1]+1] == (map[point[0], point[1]] + 1):
            calculate_trail_ends(map, (point[0], point[1]+1), ends, trails)
    return ends, trails

def calculate_trail_score(map, point, score, ends = [], trails = []):
    row_max = map.shape[0] - 1
    col_max = map.shape[1] - 1
    trails.append(point)
    if map[point[0], point[1]] == 9:
        if not point in ends:
            ends.append(point)
            #print(f"found={point}")
        score += 1
        return score, ends, trails
    else:
        if point[0] > 0 and map[point[0]-1, point[1]] == (map[point[0], point[1]] + 1):
            score = calculate_trail_score(map, (point[0]-1, point[1]), score, ends, trails)[0]
        if point[0] < row_max and map[point[0]+1, point[1]] == (map[point[0], point[1]] + 1):
            score = calculate_trail_score(map, (point[0]+1, point[1]), score, ends, trails)[0]
        if point[1] > 0 and map[point[0], point[1]-1] == (map[point[0], point[1]] + 1):
            score = calculate_trail_score(map, (point[0], point[1]-1), score, ends, trails)[0]
        if point[1] < col_max and map[point[0], point[1]+1] == (map[point[0], point[1]] + 1):
            score = calculate_trail_score(map, (point[0], point[1]+1), score, ends, trails)[0]
    return score, ends, trails

def part_one():
    total_score = 0
    with open("./day_10/day_10_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines, dtype=int)
        print(map)
        trailheads = find_trailheads(map)
        #print(trailheads)
        for trailhead in trailheads:
            ends, trails = calculate_trail_ends(map, trailhead, [], [])
            total_score += len(ends)
            print(f"Score for ({trailhead[0]:04d},{trailhead[1]:04d} = {len(ends):03d} (total={total_score:04d})")
            #print(f"Score for ({trailhead[0]:04d},{trailhead[1]:04d} = {len(ends):03d} (total={total_score:04d}) trail -> {trails})")
    print(f"Total score = {total_score}")
    return total_score

def part_two():
    total_score = 0
    with open("./day_10/day_10_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines, dtype=int)
        print(map)
        trailheads = find_trailheads(map)
        #print(trailheads)
        for trailhead in trailheads:
            score, ends, trails = calculate_trail_score(map, trailhead, 0, [], [])
            total_score += score
            print(f"Score for ({trailhead[0]:04d},{trailhead[1]:04d} = {score} (total={total_score:04d})")
            #print(f"Score for ({trailhead[0]:04d},{trailhead[1]:04d} = {len(ends):03d} (total={total_score:04d}) trail -> {trails})")
    print(f"Total score = {total_score}")
    return total_score

if __name__ == "__main__":
    print("Advent of Code - Day 10")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
    