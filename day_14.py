import numpy as nu, re

def parse_input_data(lines):
    data = []
    for line in lines:
        params = re.findall("p=(\\d*),(\\d*) v=(-?\\d*),(-?\\d*)", line)
        #print(params)
        #print(f"Line={line} => ({params[0][1]}, {params[0][0]}), ({params[0][3]}, {params[0][2]})")
        data.append([(int(params[0][1]), int(params[0][0])), (int(params[0][3]), int(params[0][2]))])
    return data

def advance_robot(formula, position, size, times = 1):
    new_position = position
    y = formula[0] * times + position[0]
    x = formula[1] * times + position[1]
    y = y % size[0]
    x = x % size[1]
    return (y, x)

def part_one():
    final_result = 0
    with open("./day_14/day_14_input.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines)
        map = nu.full((103, 101), 0, dtype=nu.int_)
        for robot_data in data:
            position = advance_robot(robot_data[1], robot_data[0], (map.shape[0], map.shape[1]), 100)
            map[position[0], position[1]] += 1
        #print(map)
        map[:, map.shape[1]//2] = map[:, map.shape[1]//2] * 0
        map[map.shape[0]//2, :] = map[map.shape[0]//2, :]  * 0
        quadrant1 = map[0:map.shape[0]//2, 0:map.shape[1]//2]
        quadrant2 = map[map.shape[0]//2:, 0:map.shape[1]//2]
        quadrant3 = map[0:map.shape[0]//2, map.shape[1]//2:]
        quadrant4 = map[map.shape[0]//2:, map.shape[1]//2:]
        print(map)
        final_result = quadrant1.sum() * quadrant2.sum() * quadrant3.sum() * quadrant4.sum()
        print(f"{quadrant1.sum()} x {quadrant2.sum()} x {quadrant3.sum()} x {quadrant4.sum()} = {final_result}")
    print(f"Results  = {final_result}")
    return final_result

def part_two():
    final_result = 0
    with open("./day_14/day_14_input.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines)
        report_file = open("./day_14/day_14_report.txt", "w")
        possibilities = []
        for seconde in range(10000):
            print(f"Time = {seconde} secondes\r", end="")
            map = nu.full((103, 101), " ", dtype=nu.str_)
            positions = []
            for robot_data in data:
                position = advance_robot(robot_data[1], robot_data[0], (map.shape[0], map.shape[1]), seconde)
                positions.append(position)
                map[position[0], position[1]] = "#"
            tree_positions = []
            for position in positions:
                for i in range(1,5):
                    if not (position[0]+i, position[1]-i) in positions:
                        break
                    elif not (position[0]+i, position[1]+i) in positions:
                        break
                else:
                    tree_positions.append(position)
            if len(tree_positions) > 0:
                possibilities.append(seconde)
                final_result += 1
                report_file.write("-"*80 + "\n")
                report_file.write(f"Test {seconde} -> {tree_positions}\n")
                nu.savetxt(report_file, map, "%s", "")
                #print(map)
        #print(map)
        report_file.close()
        print()
    print(f"Results = {final_result} => {possibilities}")
    return final_result

if __name__ == "__main__":
    print("Advent of Code - Day 14")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
