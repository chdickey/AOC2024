import numpy as nu, re

def parse_input_data(lines, double_map = False):
    data = []
    data_lines = re.split(r"(?:\r?\n){2,}", ("".join(lines)).strip())
    map_lines = [list(line.strip()) for line in data_lines[0].split()]
    if double_map:
        bigmap_lines = ""
        for line in map_lines:
            for char in line:
                if char == "O":
                    bigmap_lines += "[]"
                elif char == "@":
                    bigmap_lines += "@."
                elif char in "\r\n":
                    bigmap_lines += char
                else:
                    bigmap_lines += char*2
            bigmap_lines += "\n"
        map = nu.array([list(line.strip()) for line in bigmap_lines.split()])
    else:
        map = nu.array(map_lines)
    #print(map)
    action = "".join(data_lines[1].split())
    return map, action

def move_robot(map, position, move):
    x = 0
    y = 0
    if move == "^":
        y = -1
    elif move == "<":
        x = -1
    elif move == "v":
        y = 1
    elif move == ">":
        x = 1
    # check for box = add robot len
    robot_count = 0
    while map[position[0]+y*(1 + robot_count), position[1]+x*(1 + robot_count)] == "O":
        robot_count += 1
    # check for wall = don't move
    if map[position[0]+y*(1 + robot_count), position[1]+x*(1 + robot_count)] == "#":
        x = 0
        y = 0
    if x != 0:
        for box in range(robot_count, 0, -1):
            map[position[0], position[1]+x*(1 + box)] = "O"
        map[position[0], position[1]+x] = "@"
        map[position[0], position[1]] = "."
    elif y != 0:
        for box in range(robot_count, 0, -1):
            map[position[0]+y*(1 + box), position[1]] = "O"
        map[position[0]+y, position[1]] = "@"
        map[position[0], position[1]] = "."
    return (position[0]+y, position[1]+x)

def move_robot_big_map(map, position, move, move_count):
    x = 0
    y = 0
    if move == "^":
        y = -1
    elif move == "<":
        x = -1
    elif move == "v":
        y = 1
    elif move == ">":
        x = 1
    # check for box = add robot len
    robot_count = 0
    boxes = []
    if x != 0:
        while map[position[0], position[1]+x*(1 + robot_count)] in "[]":
            robot_count += 1
    elif y != 0:
        boxes = findBoxAboveOrBelow(map, position, y)
        boxes = list(dict.fromkeys(boxes))
        if len(boxes) > 0 and y > 0:
            boxes.sort(key=lambda tup: tup[0], reverse=True)
            robot_count = boxes[0][0] - position[0]
        elif len(boxes) > 0:
            boxes.sort(key=lambda tup: tup[0])
            robot_count = position[0] - boxes[0][0]
    # check for wall = don't move
    if x != 0:
        if map[position[0], position[1]+x*(1 + robot_count)] == "#":
            x = 0
    elif y != 0:
        if map[position[0]+y, position[1]] == "#":
            y = 0
        else:
            for box in boxes:
                if map[box[0]+y, box[1]] == "#":
                    y = 0
                    break
    if x != 0:
        for box in range(robot_count, 0, -1):
            if x > 0:
                map[position[0], position[1]+x*(1 + box)] = "]" if (box % 2) == 0 else "["
            else:
                map[position[0], position[1]+x*(1 + box)] = "[" if (box % 2) == 0 else "]"
        map[position[0], position[1]+x] = "@"
        map[position[0], position[1]] = "."
    elif y != 0:
        for box in boxes:
            map[box[0]+y, box[1]] = map[box[0], box[1]]
            map[box[0], box[1]] = "."
        map[position[0]+y, position[1]] = "@"
        map[position[0], position[1]] = "."
    return (position[0]+y, position[1]+x)

def findBoxAboveOrBelow(map, position, direction = 1):
    boxes = []
    if map[position[0]+direction, position[1]] == "[":
        boxes.append((position[0]+direction, position[1]))
        boxes.append((position[0]+direction, position[1] + 1))
        boxes.extend(findBoxAboveOrBelow(map, (position[0]+direction, position[1]), direction))
        boxes.extend(findBoxAboveOrBelow(map, (position[0]+direction, position[1] + 1), direction))
    elif map[position[0]+direction, position[1]] == "]":
        boxes.append((position[0]+direction, position[1]))
        boxes.append((position[0]+direction, position[1] - 1))
        boxes.extend(findBoxAboveOrBelow(map, (position[0]+direction, position[1]), direction))
        boxes.extend(findBoxAboveOrBelow(map, (position[0]+direction, position[1] - 1), direction))
    return boxes

def calculateSumGPS(map, box_format = "O"):
    total = 0
    count = 0
    # sum of O following row * 100 + col
    for row in range(map.shape[0]):
        for col in range(map.shape[1]):
            if map[row, col] == box_format:
                total += (row * 100) + col
                count += 1
    return total, count

def part_one():
    total_gps = 0
    count_gps = 0
    with open("./day_15/day_15_input.txt") as file:
        lines = file.readlines()
        map, action = parse_input_data(lines)
        #print(map)
        #print(action)
        position = nu.where(map == "@")
        position = (int(position[0][0]), int(position[1][0]))
        #print(position)
        key = ""
        for move in action:
            position = move_robot(map, position, move)
            #print(f"move={move}")
            #print(map)
            #if key != "c":
            #    key = input()
            #    if key == "q":
            #        break
        total_gps, count_gps = calculateSumGPS(map)
        file.close()
    print(f"Sum of all {count_gps} GPS coordinates is {total_gps}")

def part_two():
    total_gps = 0
    count_gps = 0
    with open("./day_15/day_15_input.txt") as file:
        lines = file.readlines()
        map, action = parse_input_data(lines, True)
        #print(map)
        position = nu.where(map == "@")
        position = (int(position[0][0]), int(position[1][0]))
#        report_file = open("./day_15/day_15_report.txt", "w")
        #print(position)
        key = ""
        move_count = 0
        for move in action:
#            position_last = position
            position = move_robot_big_map(map, position, move, move_count)
#            report_file.write("-"*80 + "\n")
#            report_file.write(f"count={move_count}, move={move}, position={position}\n")
#            map[position_last[0], position_last[1]] = "%"
#            nu.savetxt(report_file, map, "%s", "")
#            map[position_last[0], position_last[1]] = "."
            #print(f"move={move}, position={position}")
            #print(map)
            #if key != "c":
            #    key = input()
            #    if key == "q":
            #        break
            move_count += 1
        total_gps, count_gps = calculateSumGPS(map, "[")
        #print(map)
#        report_file.close()
        file.close()
    print(f"Sum of all {count_gps} GPS coordinates is {total_gps}")

if __name__ == "__main__":
    print("Advent of Code - Day 15")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
