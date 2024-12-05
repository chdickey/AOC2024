
def part_one():
    safe_reports = 0
    with open("./day_2/day_2_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            safe = True
            last_span = 0
            levels = line.split()
            for index in range(1, len(levels)):
                span = int(levels[index]) - int(levels[index-1])
                if abs(span) < 1 or abs(span) > 3 or (last_span > 0 and span < 0) or (last_span < 0 and span > 0):
                    safe = False
                    break
                last_span = span
            if safe and last_span != 0:
                safe_reports += 1
                #print(line)
    print(f"Number of safe reports = {safe_reports}")
    return safe_reports

def part_two():
    safe_reports = 0
    with open("./day_2/day_2_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            safe = True
            last_span = 0
            bad_level = 0
            levels = line.split()
            for index in range(1, len(levels)):
                span = int(levels[index]) - int(levels[index-1])
                if abs(span) < 1 or abs(span) > 3 or (last_span > 0 and span < 0) or (last_span < 0 and span > 0):
                    bad_level += 1
                    if bad_level > 1:
                        safe = False
                        break
                else:
                    last_span = span
            if safe and last_span != 0:
                safe_reports += 1
                if bad_level > 0:
                    print(line)
    print(f"Number of safe reports = {safe_reports}")
    return safe_reports

if __name__ == "__main__":
    print("Advent of Code - Day 2")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
