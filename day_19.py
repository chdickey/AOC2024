import re, collections

def parse_input_data(lines):
    data_lines = re.split(r"(?:\r?\n){2,}", ("".join(lines)).strip())
    towels = [towel.strip() for towel in data_lines[0].split(",")]
    towels.sort(key=lambda s: len(s), reverse=True)
    designs = [line.strip() for line in data_lines[1].split()]
    return towels, designs

def findTowel(design, towels):
    for towel in towels:
        if towel == design[:len(towel)]:
            return towel
    return ""

def isDesignPossible(design, towels):
    towel = findTowel(design, towels)
    tested_global = set()
    tested_towel = set()
    pattern = [towel]
    patterns = collections.deque([(pattern, tested_towel)])
    #report_file = open(f"./day_19/day_19_report_{design}.txt", "w")
    while patterns:
        #print(f"Patterns = {len(patterns):3d}, Tested = {len(tested_towel):3d}, design:{''.join(pattern):<65}\r",end="")
        #print(f"Patterns = {len(patterns):3d}, Tested = {len(tested_towel):3d}\r",end="")
        if "".join(pattern) == design:
            #report_file.close()
            return True
        towel = findTowel(design[len("".join(pattern)):], [t for t in towels if t not in tested_towel and "".join(pattern)+t not in tested_global])
        if len(towel) > 0:
            #report_file.write(f"{''.join(pattern)}{towel}\n")
            tested_towel.add(towel) #.update([t for t in towels if t == towel[:len(t)]])
            tested_towel = set([t[len(towel):] for t in tested_towel if len(towel) < len(t) and towel == t[:len(towel)]])
            pattern = pattern + [towel]
            patterns.append((pattern, tested_towel))
        else:
            pattern, tested_towel = patterns.pop()
            tested_global.add("".join(pattern))
            if not patterns:
                break
            pattern, tested_towel = patterns.pop()
            if len(pattern) > 0:
                patterns.append((pattern, tested_towel))
    #report_file.close()
    return False

def countDesignPossible(design, towels, main = False):
    count = 0
    towel = findTowel(design, towels)
    tested_global = set()
    tested_towel = set()
    possibles = set()
    pattern = [towel]
    patterns = collections.deque([(pattern, tested_towel)])
    if main:
        report_file = open(f"./day_19/day_19_report_{design}.txt", "w")
    while patterns:
        #print(f"Patterns = {len(patterns):3d}, Tested = {len(tested_towel):3d}, design:{''.join(pattern):<65}\r",end="")
        #print(f"Patterns = {len(patterns):3d}, Tested = {len(tested_towel):3d}\r",end="")
        if "".join(pattern) == design:
            #report_file.close()
            count = 1
            for part in pattern:
                count += countDesignPossible(part, [t for t in towels if len(t) < len(part)])
            possibles.add((",".join(pattern), count))
            pattern, tested_towel = patterns.pop()
            #patterns.clear()
            #tested_global.add("".join(pattern))
            tested_global = set()
            #patterns.append((pattern, tested_towel))
            #return count
        towel = findTowel(design[len("".join(pattern)):], [t for t in towels if t not in tested_towel and "".join(pattern)+t not in tested_global])
        if len(towel) > 0:
            #report_file.write(f"{''.join(pattern)}{towel}\n")
            tested_towel.add(towel) #.update([t for t in towels if t == towel[:len(t)]])
            tested_towel = set([t[len(towel):] for t in tested_towel if len(towel) < len(t) and towel == t[:len(towel)]])
            pattern = pattern + [towel]
            patterns.append((pattern, tested_towel))
        else:
            pattern, tested_towel = patterns.pop()
            tested_global.add("".join(pattern))
            if not patterns:
                break
            pattern, tested_towel = patterns.pop()
            if len(pattern) > 0:
                patterns.append((pattern, tested_towel))
    if main:
        report_file.write("\n".join([str(p[1])+" = "+p[0] for p in possibles]))
        report_file.close()
        count = 1
        for possible in possibles:
            count *= possible[1]
    return count

def part_one():
    count = 0
    with open("./day_19/day_19_input.txt") as file:
        lines = file.readlines()
        towels, designs = parse_input_data(lines)
        count_all = 0
        for design in designs:
            count_all += 1
            if isDesignPossible(design, towels):
                count += 1
            else:
                print(f"Desgin impossible to create: {design:<75}")
            #print(f"Total = {count_all:3d}, possibles = {count:3d}\r", end="")
        #print(towels)
        #print(designs)
    print()
    print(f"Number of possibles designs = {count}")

def part_two():
    count = 0
    with open("./day_19/day_19_input.txt") as file:
        lines = file.readlines()
        towels, designs = parse_input_data(lines)
        count_all = 0
        for design in designs:
            count += countDesignPossible(design, towels, True)
            #print(f"Total = {count_all:3d}, possibles = {count:3d}\r", end="")
        #print(towels)
        #print(designs)
    print()
    print(f"Number of possibles designs = {count}")

if __name__ == "__main__":
    print("Advent of Code - Day 19")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
