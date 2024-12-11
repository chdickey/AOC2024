from functools import cache

def blink_stones(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif (len(str(stone)) % 2) == 0:
            split_stone = str(stone)
            split_stone = split_stone[0:len(split_stone)//2] + " " + split_stone[len(split_stone)//2:]
            split_stones = [int(s) for s in split_stone.split(" ")]
            new_stones.append(split_stones[0])
            new_stones.append(split_stones[1])
        else:
            new_stones.append(stone * 2024)
    return new_stones

@cache
def blink_stone(stone, blink_times, stone_count):
    if blink_times < 1:
        return stone_count
    if stone == 0:
        stone_count = blink_stone(1, blink_times - 1, stone_count)
    elif (len(str(stone)) % 2) == 0:
        split_stone = str(stone)
        split_stone = split_stone[0:len(split_stone)//2] + " " + split_stone[len(split_stone)//2:]
        split_stones = [int(s) for s in split_stone.split(" ")]
        stone_count = blink_stone(split_stones[0], blink_times - 1, stone_count) + blink_stone(split_stones[1], blink_times - 1, stone_count)
    else:
        stone_count = blink_stone(stone * 2024, blink_times - 1, stone_count)
    return stone_count

def part_one():
    stones_count = 0
    with open("./day_11/day_11_input.txt") as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        stones = [int(stone) for stone in lines[0]]
        print(stones)
        for stone in stones:
            stones_count += blink_stone(stone, 25, 1)
        #for blink in range(25):
        #    stones = blink_stones(stones)
            #print(stones)
        #stones_count = len(stones)
    print(f"Stone count after 25 blinks = {stones_count}")
    return stones_count

def part_two():
    stones_count = 0
    with open("./day_11/day_11_input.txt") as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        stones = [int(stone) for stone in lines[0]]
        print(stones)
        for stone in stones:
            count = blink_stone(stone, 75, 1)
            print(f"Blink stone {stone} array = {count}")
            stones_count += count
    print(f"Stone count after 75 blinks = {stones_count}")
    return stones_count

if __name__ == "__main__":
    print("Advent of Code - Day 11")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
