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

def guard_alignment(guard_direction):
    guard_alignment = ""
    if guard_direction == "^" or guard_direction == "v":
        guard_alignment = "|"
    elif guard_direction == ">" or guard_direction == "<":
        guard_alignment = "-"
    return guard_alignment

def path_alignment(path_alignment, guard_alignment):
    new_alignment = guard_alignment
    if (path_alignment == "|" and guard_alignment == "-") or (path_alignment == "-" and guard_alignment == "|"):
        new_alignment = "+"
    return new_alignment

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

def other_branch_exist2(map, guard_position, guard_direction):
    branch_found = False
    if guard_direction == "^":
        obstruction_position = nu.where(map[guard_position[0], guard_position[1]:] == "#")
        path_position = nu.where(map[guard_position[0], guard_position[1]:] == "-")
        path_position2 = nu.where(map[guard_position[0], guard_position[1]:] == "+")
        if len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][0] < obstruction_position[0][0]) or \
            (len(path_position2[0]) > 0 and path_position2[0][0] < obstruction_position[0][0])):
            branch_found = True
    elif guard_direction == ">":
        obstruction_position = nu.where(map[guard_position[0]:, guard_position[1]] == "#")
        path_position = nu.where(map[guard_position[0]:, guard_position[1]] == "|")
        path_position2 = nu.where(map[guard_position[0]:, guard_position[1]] == "+")
        if len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][0] < obstruction_position[0][0]) or \
            (len(path_position2[0]) > 0 and path_position2[0][0] < obstruction_position[0][0])):
            branch_found = True
    elif guard_direction == "v":
        obstruction_position = nu.where(map[guard_position[0], :guard_position[1]] == "#")
        path_position = nu.where(map[guard_position[0], :guard_position[1]] == "-")
        path_position2 = nu.where(map[guard_position[0], :guard_position[1]] == "+")
        if len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][-1] > obstruction_position[0][-1]) or \
            (len(path_position2[0]) > 0 and path_position2[0][-1] > obstruction_position[0][-1])):
            branch_found = True
    elif guard_direction == "<":
        obstruction_position = nu.where(map[:guard_position[0], guard_position[1]] == "#")
        path_position = nu.where(map[:guard_position[0], guard_position[1]] == "|")
        path_position2 = nu.where(map[:guard_position[0], guard_position[1]] == "+")
        if len(obstruction_position[0]) > 0 and ((len(path_position[0]) > 0 and path_position[0][-1] > obstruction_position[0][-1]) or \
            (len(path_position2[0]) > 0 and path_position2[0][-1] > obstruction_position[0][-1])):
            branch_found = True
    return branch_found

def other_branch_exist3(map, guard_position, guard_direction):
    branch_found = False
    if guard_direction == "^":
        obstruction_position = nu.where(map[guard_position[0], guard_position[1]:] == "#")
        if len(obstruction_position[0]) > 0:
            branch_found = True
    elif guard_direction == ">":
        obstruction_position = nu.where(map[guard_position[0]:, guard_position[1]] == "#")
        if len(obstruction_position[0]) > 0:
            branch_found = True
    elif guard_direction == "v":
        obstruction_position = nu.where(map[guard_position[0], :guard_position[1]] == "#")
        if len(obstruction_position[0]) > 0:
            branch_found = True
    elif guard_direction == "<":
        obstruction_position = nu.where(map[:guard_position[0], guard_position[1]] == "#")
        if len(obstruction_position[0]) > 0:
            branch_found = True
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
        #map[guard_position[0], guard_position[1]] = guard_direction
        #guard_position, guard_direction = move_guard2(map, guard_position, guard_direction)
        while guard_position[0] >= 0 and guard_position[1] >= 0 and guard_position[0] < max_pos_row and guard_position[1] < max_pos_col:
            if not move_obstrued(map, guard_position, guard_direction): # and other_branch_exist2(map, guard_position, guard_direction):
                obstruction_position, test_direction = move_guard2(map, guard_position, guard_direction)
                #if guard_direction != test_direction:
                #    continue
                map_test = nu.copy(map)
                map_test[obstruction_position[0], obstruction_position[1]] = "#"
                test_position = guard_position
                test_direction = guard_direction
                map_test[test_position[0], test_position[1]] = test_direction #path_alignment(map_test[test_position[0], test_position[1]], guard_alignment(test_direction))#test_direction
                test_position, test_direction = move_guard2(map_test, test_position, test_direction)
                iter_max = 20000
                iter_nb = 0
                while test_position[0] >= 0 and test_position[1] >= 0 and test_position[0] < max_pos_row and test_position[1] < max_pos_col and iter_nb < iter_max:
                    iter_nb += 1
                    if (test_position[0] == guard_position[0] and test_position[1] == guard_position[1] and (guard_direction == test_direction)) or \
                        (map[test_position[0], test_position[1]] == test_direction):# or test_direction == turn_guard(guard_direction)):
                        positions += 1
                        if map_obtructions[obstruction_position[0], obstruction_position[1]] != "O":
                            map_test[obstruction_position[0], obstruction_position[1]] = "O"
                            nu.savetxt(".\\day_6\\trap_{0:4}.txt".format(positions), map_test, "%s", "")
                        map_obtructions[obstruction_position[0], obstruction_position[1]] = "O"
                        #if not (test_position[0] == (start_position[0]-1) and test_position[1] == start_position[1]):
                        #if not (obstruction_position[0] == (start_position[0]) and obstruction_position[1] == start_position[1]):
                        #    map_obtructions[obstruction_position[0], obstruction_position[1]] = "O"
                        print(f"Number of possibilities = {positions} obtructions\r", end="")
                        #print(map_test[test_position[0]-8:test_position[0]+8, test_position[1]-8:test_position[1]+8])
                        #if input("direction=" + test_direction) == "q":
                        #    exit()
                        break
                    map_test[test_position[0], test_position[1]] = test_direction #path_alignment(map_test[test_position[0], test_position[1]], guard_alignment(test_direction))#test_direction#test_direction
                    test_position, test_direction = move_guard2(map_test, test_position, test_direction)
                if iter_nb >= iter_max and 0 == 1:
                    if map_obtructions[obstruction_position[0], obstruction_position[1]] != "O":
                        map_test[obstruction_position[0], obstruction_position[1]] = "O"
                        nu.savetxt(".\\day_6\\trap_z_{0:4}.txt".format(positions), map_test, "%s", "")
                    positions += 1
                    map_obtructions[obstruction_position[0], obstruction_position[1]] = "O"
            map[guard_position[0], guard_position[1]] = guard_direction #path_alignment(map[guard_position[0], guard_position[1]], guard_alignment(guard_direction))#test_direction#guard_direction
            if move_obstrued(map, guard_position, guard_direction):
                guard_direction = turn_guard(guard_direction)
            else:
                guard_position, guard_direction = move_guard2(map, guard_position, guard_direction)
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
