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

def convert_data_file(line):
    data = []
    for i in range(len(line)):
        if (i % 2) == 0:
            data.append((i // 2, int(line[i])))
        else:
            data.append((-1, int(line[i])))
    return data

def convert_file(file_data):
    data = []
    for i in range(nu.size(file_data, 0)):
        for n in range(file_data[i][1]):
            data.append(int(file_data[i][0]))
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

def clean_data(file_data):
    start = 0
    while start < nu.size(file_data, 0):
        if file_data[start][0] == -1 and file_data[start][1] == 0:
            file_data = nu.delete(file_data, start, 0)
        else:
            start += 1
    return file_data

def compress_file(file_data, start):
    counter = 0
    new_start = start
    end = nu.size(file_data, 0)
    while start < end and new_start < end:
        counter += 1
        block_size = -1
        block_id = -1
        #print(f"Counter = {counter}\r", end="")
        for i in range(start, end):
            if file_data[i][0] == -1:
                new_start = i
                block_size = file_data[i][1]
                break
        else:
            new_start = end
        for i in range(end - 1, new_start , -1):
            if file_data[i][0] != -1 and block_size >= file_data[i][1]:
                block_id = i
                break
        #else:
        #    new_start = end
        #print((new_start, new_end))
        if block_id >= 0 and block_size >= 0 and new_start < end:
            free_size = 0
            if block_size == file_data[block_id][1]:
                file_data[new_start][0] = file_data[block_id][0]
                file_data[block_id][0] = -1
            else:
                free_size = block_size - file_data[block_id][1]
                file_data[new_start][0] = file_data[block_id][0]
                file_data[new_start][1] = file_data[block_id][1]
                file_data[block_id][0] = -1
                file_data = nu.insert(file_data, new_start+1, (-1, free_size), 0)
                new_start += 1
            #    block_id += 1
            #if file_data[block_id-1][0] == -1:
            #    block_id -= 1
            #    #file_data[block_id-1][1] += block_size
            #    #file_data = nu.delete(file_data, block_id, 0)
            while block_id < (end-1) and file_data[block_id][0] == -1 and file_data[block_id+1][0] == -1:
                file_data[block_id][1] += file_data[block_id+1][1]
                file_data = nu.delete(file_data, block_id+1, 0)
                end = nu.size(file_data, 0)
                if (block_id+1) < new_start:
                    new_start -= 1
            if free_size > 0:
                while new_start < (end-1) and file_data[new_start][0] == -1 and file_data[new_start+1][0] == -1:
                    file_data[new_start][1] += file_data[new_start+1][1]
                    file_data = nu.delete(file_data, new_start+1, 0)
                    end = nu.size(file_data, 0)
            #if block_id >= 0 and block_id < start:
            #    start = block_id + 1
            #else:
            #    file_data[block_id][0] = -1
        #start = new_start
        #print(block_id)
        if block_id >= 0 and block_id < start:
            start = block_id
        else:
            start += 1
        end = nu.size(file_data, 0)
    return file_data

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
    checksum = 0
    with open("./day_9/day_9_input.txt") as file:
        lines = file.readlines()
        data = convert_data_file(lines[0].strip())
        file_data = nu.array(data)
        #print(file_data)
        file_data= clean_data(file_data)
        #print(file_data)
        compacted_file = compress_file(file_data, 0)
        compacted_data = convert_file(compacted_file)
        #print(compacted_data)
        for i in range(len(compacted_data)):
            print(f"Checksum = {checksum}\r", end="")
            if compacted_data[i] != -1:
                checksum += i * compacted_data[i]
    print(f"Checksum = {checksum}")
    return checksum

if __name__ == "__main__":
    print("Advent of Code - Day 9")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
