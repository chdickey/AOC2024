import re

def part_one():
    final_result = 0
    with open("./day_3/day_3_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            operations = re.findall("mul\((\d{1,3}),(\d{1,3})\)", line)
            result = 0
            for operation in operations:
                result += int(operation[0]) * int(operation[1])
            #print(f"result={result}, for line={line}")
            final_result += result
    print(f"Results of the multiplications = {final_result}")
    return final_result

def part_two():
    final_result = 0
    step_first = False
    with open("./day_3/day_3_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            instructions = line.split("do()")
            if step_first:
                instructions = instructions[1:]
            for instruction in instructions:
                step_first = False
                instruction2 = instruction.split("don't()")
                if len(instruction2) > 1:
                    step_first = True
                operations = re.findall("mul\((\d{1,3}),(\d{1,3})\)", instruction2[0])
                result = 0
                for operation in operations:
                    result += int(operation[0]) * int(operation[1])
                #print(f"result={result}, for line={line}")
                final_result += result
    print(f"Results of the multiplications = {final_result}")
    return final_result

if __name__ == "__main__":
    print("Advent of Code - Day 3")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
    