import numpy as nu

def move_guard(map, guard_position, guard_direction):
    row = guard_position[0]
    col = guard_position[1]
    if guard_direction == "^":
        if row > 0 and map[row-1, col] == "#":
            guard_direction = ">"
            col += 1
        else:
            row -= 1
    elif guard_direction == ">":
        if col < (nu.size(map, 1)-1) and map[row, col+1] == "#":
            guard_direction = "v"
            row += 1
        else:
            col += 1
    elif guard_direction == "v":
        if row < (nu.size(map, 0)-1) and map[row+1, col] == "#":
            guard_direction = "<"
            col -= 1
        else:
            row += 1
    elif guard_direction == "<":
        if col > 0 and map[row, col-1] == "#":
            guard_direction = "^"
            row -= 1
        else:
            col -= 1
    return ((row, col), guard_direction)

def move_guard2(map, guard_position, guard_direction):
    row = guard_position[0]
    col = guard_position[1]
    while move_obstrued(map, guard_position, guard_direction):
        guard_direction = turn_guard(guard_direction)
    if guard_direction == "^":
        row -= 1
    elif guard_direction == ">":
        col += 1
    elif guard_direction == "v":
        row += 1
    elif guard_direction == "<":
        col -= 1
    return ((row, col), guard_direction)
    

def turn_guard(guard_direction, reverse = False):
    if (not reverse and guard_direction == "^") or (reverse and guard_direction == "v"):
        guard_direction = ">"
    elif (not reverse and guard_direction == ">") or (reverse and guard_direction == "<"):
        guard_direction = "v"
    elif (not reverse and guard_direction == "v") or (reverse and guard_direction == "^"):
        guard_direction = "<"
    elif (not reverse and guard_direction == "<") or (reverse and guard_direction == ">"):
        guard_direction = "^"
    return guard_direction

def move_obstrued(map, guard_position, guard_direction):
    obstrued = False
    row = guard_position[0]
    col = guard_position[1]
    if guard_direction == "^":
        if row > 0 and map[row-1, col] == "#":
            obstrued = True
    elif guard_direction == ">":
        if col < (nu.size(map, 1)-1) and map[row, col+1] == "#":
            obstrued = True
    elif guard_direction == "v":
        if row < (nu.size(map, 0)-1) and map[row+1, col] == "#":
            obstrued = True
    elif guard_direction == "<":
        if col > 0 and map[row, col-1] == "#":
            obstrued = True
    return obstrued

def other_branch_exist(map, guard_position, guard_direction):
    branch_found = False
    if guard_direction == "^":
        obstruction_position = nu.where(map[guard_position[0], guard_position[1]:] == "#")
        path_position = nu.where(map[guard_position[0], guard_position[1]:] == ">")
        if map[guard_position[0], guard_position[1]] == ">" or (len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][0] < obstruction_position[0][0]) or \
            map[guard_position[0], guard_position[1] + obstruction_position[0][0] - 1] == "v")):
            branch_found = True
            #if map[guard_position[0], guard_position[1] + obstruction_position[0][0] - 1] == "v":
                #print(map[guard_position[0], guard_position[1]:])
                #print(path_position)
                #print(obstruction_position)
                #if input(guard_direction) == "q":
                #    exit()
    elif guard_direction == ">":
        obstruction_position = nu.where(map[guard_position[0]:, guard_position[1]] == "#")
        path_position = nu.where(map[guard_position[0]:, guard_position[1]] == "v")
        if map[guard_position[0], guard_position[1]] == "v" or (len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][0] < obstruction_position[0][0]) or \
            map[guard_position[0] + obstruction_position[0][0] - 1, guard_position[1]] == "<")):
            branch_found = True
            #if map[guard_position[0] + obstruction_position[0][0] - 1, guard_position[1]] == "<":
                #print(map[guard_position[0]:, guard_position[1]])
                #print(path_position)
                #print(obstruction_position)
                #if input(guard_direction) == "q":
                #    exit()
    elif guard_direction == "v":
        obstruction_position = nu.where(map[guard_position[0], :guard_position[1]] == "#")
        path_position = nu.where(map[guard_position[0], :guard_position[1]] == "<")
        if map[guard_position[0], guard_position[1]] == "<" or (len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][-1] > obstruction_position[0][-1]) or \
            map[guard_position[0], guard_position[1] - obstruction_position[0][-1]] == "^")):
            branch_found = True
            #if map[guard_position[0], guard_position[1] - obstruction_position[0][-1]] == "^":
                #print(map[guard_position[0], :guard_position[1]])
                #print(path_position)
                #print(obstruction_position)
                #if input(guard_direction) == "q":
                #    exit()
    elif guard_direction == "<":
        obstruction_position = nu.where(map[:guard_position[0], guard_position[1]] == "#")
        path_position = nu.where(map[:guard_position[0], guard_position[1]] == "^")
        if map[guard_position[0], guard_position[1]] == "^" or (len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][-1] > obstruction_position[0][-1]) or \
            map[guard_position[0] - obstruction_position[0][-1], guard_position[1]] == ">")):
            branch_found = True
            #if map[guard_position[0] - obstruction_position[0][-1], guard_position[1]] == ">":
                #print(map[:guard_position[0], guard_position[1]])
                #print(path_position)
                #print(obstruction_position)
                #if input(guard_direction) == "q":
                #    exit()
    return branch_found

def part_one():
    positions = 0
    with open("./day_6/day_6_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        guard_direction = "^"
        guard_position = nu.where(map == guard_direction)
        guard_position = (int(guard_position[0][0]), int(guard_position[1][0]))
        max_pos_row = nu.size(map, 0)
        max_pos_col = nu.size(map, 1)
        #map[guard_position[0], guard_position[1]] = "X"
        #guard_position, guard_direction = move_guard2(map, guard_position, guard_direction)
        while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and guard_position[1] < max_pos_col:
            #map[guard_position[0], guard_position[1]] = guard_direction
            #print(map[guard_position[0]-3:guard_position[0]+3, guard_position[1]-3:guard_position[1]+3])
            map[guard_position[0], guard_position[1]] = "X"
            guard_position, guard_direction = move_guard2(map, guard_position, guard_direction)
            #input()
        positions = nu.count_nonzero(map == "X")
    print(f"Guard will visit {positions} positions")
    return positions

def part_two():
    positions = 0
    with open("./day_6/day_6_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        map_obtructions = nu.copy(map)
        guard_direction = "^"
        start_position = nu.where(map == guard_direction)
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        guard_position = start_position
        max_pos_row = nu.size(map, 0)
        max_pos_col = nu.size(map, 1)
        map[guard_position[0], guard_position[1]] = guard_direction
        guard_position, guard_direction = move_guard(map, guard_position, guard_direction)
        while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and guard_position[1] < max_pos_col:
            if guard_direction == "^" and map[guard_position[0]-1, guard_position[1]] != "#" and (map[guard_position[0], guard_position[1]] == ">" or other_branch_exist(map, guard_position, guard_direction)):
                if not map[guard_position[0]-1, guard_position[1]] in ["^", ">", "v", "<"]:
                    map_obtructions[guard_position[0]-1, guard_position[1]] = "O"
                    positions += 1
            elif guard_direction == ">" and map[guard_position[0], guard_position[1]+1] != "#" and (map[guard_position[0], guard_position[1]] == "v" or other_branch_exist(map, guard_position, guard_direction)):
                if not map[guard_position[0], guard_position[1]+1] in ["^", ">", "v", "<"]:
                    map_obtructions[guard_position[0], guard_position[1]+1] = "O"
                    positions += 1
            elif guard_direction == "v" and map[guard_position[0]+1, guard_position[1]] != "#" and (map[guard_position[0], guard_position[1]] == "<" or other_branch_exist(map, guard_position, guard_direction)):
                if not map[guard_position[0]+1, guard_position[1]] in ["^", ">", "v", "<"]:
                    map_obtructions[guard_position[0]+1, guard_position[1]] = "O"
                    positions += 1
            elif guard_direction == "<" and map[guard_position[0], guard_position[1]-1] != "#" and (map[guard_position[0], guard_position[1]] == "^" or other_branch_exist(map, guard_position, guard_direction)):
                if not map[guard_position[0], guard_position[1]-1] in ["^", ">", "v", "<"]:
                    map_obtructions[guard_position[0], guard_position[1]-1] = "O"
                    positions += 1
            map[guard_position[0], guard_position[1]] = guard_direction
            #print(map[guard_position[0]-3:guard_position[0]+3, guard_position[1]-3:guard_position[1]+3])
            guard_position, guard_direction = move_guard(map, guard_position, guard_direction)
            #input()
        print(f"Guard will visit {positions} positions counter")
        positions = nu.count_nonzero(map_obtructions == "O")
    print(f"Guard will visit {positions} positions")
    return positions

def part_two_brute_force():
    positions = 0
    log = open("./day_6/day_6_log.txt", "w")
    with open("./day_6/day_6_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        map_obtructions = nu.copy(map)
        guard_direction = "^"
        start_position = nu.where(map == guard_direction)
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        max_pos_row = nu.size(map, 0)
        max_pos_col = nu.size(map, 1)
        for obstruction_row in range(max_pos_row):
            for obstruction_col in range(max_pos_col):
                print(f"Test obstruction {obstruction_row:04d},{obstruction_col:04d} -> found={positions:04d}\r", end="")
                if map[obstruction_row, obstruction_col] == ".":
                    guard_position = start_position
                    guard_direction = "^"
                    obstruction_position = (obstruction_row, obstruction_col)
                    map_test = nu.copy(map)
                    map_test[obstruction_position[0], obstruction_position[1]] = "#"
                    places_visited = 10
                    places_walked = 0
                    while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and \
                        guard_position[1] < max_pos_col and places_walked < 50000:
                        places_walked += 1
                        if map_test[guard_position[0], guard_position[1]] == ".":
                            places_visited += 1
                        if (map_test[guard_position[0], guard_position[1]] == guard_direction and places_walked > 1) or places_walked >= (places_visited * 2):
                            #print(f"Obstruction found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}")
                            log.write(f"Obstruction found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}\n")
                            positions += 1
                            if map_obtructions[obstruction_position[0], obstruction_position[1]] != "O":
                                map_test[obstruction_position[0], obstruction_position[1]] = "O"
                                #nu.savetxt(".\\day_6\\trap_{%04d}x{%04d}.txt".format(obstruction_position[0], obstruction_position[1]), map_test, "%s", "")
                            map_obtructions[obstruction_position[0], obstruction_position[1]] = "O"
                            break
                        map_test[guard_position[0], guard_position[1]] = guard_direction
                        guard_position, guard_direction = move_guard2(map_test, guard_position, guard_direction)
                    else:
                        if places_walked >= 40000:
                            print(f"No exit found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}")
                            log.write(f"No exit found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}\n")
    log.close()
    print(f"Number of possibilities = {positions} obtructions")
    positions = nu.count_nonzero(map_obtructions == "O")
    print(f"Number of possibilities = {positions} obtructions")
    return positions

def part_two_brute_force_fast():
    positions = 0
    log = open("./day_6/day_6_log.txt", "w")
    with open("./day_6/day_6_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        map_obtructions = nu.copy(map)
        guard_direction = "^"
        start_position = nu.where(map == guard_direction)
        start_position = (int(start_position[0][0]), int(start_position[1][0]))
        max_pos_row = nu.size(map, 0)
        max_pos_col = nu.size(map, 1)
        map_path = nu.copy(map)
        guard_position = start_position
        guard_position, guard_direction = move_guard2(map_path, guard_position, guard_direction)
        while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and guard_position[1] < max_pos_col:
            map_path[guard_position[0], guard_position[1]] = "*"
            guard_position, guard_direction = move_guard2(map_path, guard_position, guard_direction)
        obstruction_positions = nu.where(map_path == "*")
        for obstruction_no in range(len(obstruction_positions[0])):
            obstruction_row = obstruction_positions[0][obstruction_no]
            obstruction_col = obstruction_positions[1][obstruction_no]
            print(f"Test obstruction {obstruction_row:04d},{obstruction_col:04d} -> found={positions:04d}\r", end="")
            if map[obstruction_row, obstruction_col] == ".":
                guard_position = start_position
                guard_direction = "^"
                obstruction_position = (obstruction_row, obstruction_col)
                map_test = nu.copy(map)
                map_test[obstruction_position[0], obstruction_position[1]] = "#"
                places_visited = 10
                places_walked = 0
                while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and \
                    guard_position[1] < max_pos_col and places_walked < 50000:
                    places_walked += 1
                    if map_test[guard_position[0], guard_position[1]] == ".":
                        places_visited += 1
                    if (map_test[guard_position[0], guard_position[1]] == guard_direction and places_walked > 1) or places_walked >= (places_visited * 2):
                        #print(f"Obstruction found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}")
                        log.write(f"Obstruction found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}\n")
                        positions += 1
                        if map_obtructions[obstruction_position[0], obstruction_position[1]] != "O":
                            map_test[obstruction_position[0], obstruction_position[1]] = "O"
                            #nu.savetxt(".\\day_6\\trap_{%04d}x{%04d}.txt".format(obstruction_position[0], obstruction_position[1]), map_test, "%s", "")
                        map_obtructions[obstruction_position[0], obstruction_position[1]] = "O"
                        break
                    map_test[guard_position[0], guard_position[1]] = guard_direction
                    guard_position, guard_direction = move_guard2(map_test, guard_position, guard_direction)
                else:
                    if places_walked >= 40000:
                        print(f"No exit found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}")
                        log.write(f"No exit found {obstruction_row:04d},{obstruction_col:04d} -> Walked={places_walked}, Visited={places_visited}\n")
    log.close()
    print(f"Number of possibilities = {positions} obtructions")
    positions = nu.count_nonzero(map_obtructions == "O")
    print(f"Number of possibilities = {positions} obtructions")
    return positions

if __name__ == "__main__":
    print("Advent of Code - Day 6")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
    elif part == "3":
        part_two_brute_force()
    elif part == "4":
        part_two_brute_force_fast()
