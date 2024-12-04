
def get_input_lists(file_path):
    list1 = []
    list2 = []
    lists = {}
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            ids = line.split()
            list1.append(int(ids[0]))
            list2.append(int(ids[1]))
    lists["list1"] = sorted(list1)
    lists["list2"] = sorted(list2)
    return lists

def part_one():
    lists = get_input_lists("./day_1/day_1_input.txt")
    #print(lists)
    total_distance = 0
    for row in range(len(lists["list1"])):
        total_distance += abs(lists["list1"][row] - lists["list2"][row])
    print(f"Total distance between list = {total_distance}")
    return total_distance

def part_two():
    lists = get_input_lists("./day_1/day_1_input.txt")
    similarity = 0
    for number in lists["list1"]:
        #print("number={}, count={}", number, lists["list2"].count(number))
        similarity += int(number) * lists["list2"].count(number)
    print(f"Total similarity between list = {similarity}")
    return similarity

if __name__ == "__main__":
    print("Advent of Code - Day 1")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()