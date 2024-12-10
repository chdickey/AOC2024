import numpy as nu

def convert_data(line):
    data = []
    for i in range(len(line)):
        if (i % 2) == 0:
            for n in range(int(line[i])):
                data.append(i // 2)
        else:
            for n in range(int(line[i])):
                data.append(-1)
    return data

def compress_data(compacted_data, start, end):
    counter = 0
    new_start = start
    new_end = end - 1
    while start < end:
        counter += 1
        #print(f"Counter = {counter}\r", end="")
        for i in range(start, end):
            if compacted_data[i] == -1:
                new_start = i
                break
        else:
            new_start = end
        for i in range(end - 1, new_start , -1):
            if compacted_data[i] != -1:
                new_end = i
                break
        else:
            new_end = new_start
        #print((new_start, new_end))
        if new_start < new_end:
            data = compacted_data[new_start]
            compacted_data[new_start] = compacted_data[new_end]
            compacted_data[new_end] = data
        start = new_start
        end = new_end

def part_one():
    checksum = 0
    with open("./day_9/day_9_input.txt") as file:
        lines = file.readlines()
        data = convert_data(lines[0].strip())
        compacted_data = nu.array(data)
        #print(compacted_data)
        compress_data(compacted_data, 0, nu.size(compacted_data))
        #print(compacted_data)
        for i in range(nu.size(compacted_data)):
            #print(f"Checksum = {checksum}\r", end="")
            if compacted_data[i] == -1:
                break
            checksum += i * compacted_data[i]
    print(f"Checksum = {checksum}")
    return checksum



def part_two():
    pass

if __name__ == "__main__":
    print("Advent of Code - Day 9")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
