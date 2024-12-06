import re, numpy as nu

def rotateTable(table):
    new_table = []
    for col in range(len(table[0])):
        letters = [row[col] for row in table if len(row) > col]
        new_row = "".join(letters)
        new_table.append(new_row)
    return new_table

def rotateTable45(table):
    new_table = []
    for col in range(len(table[0])-1,-1,-1):
        new_line = table[0][col]
        row = 1
        for col2 in range(col+1, len(table[0])):
            if len(table) > row and len(table[row]) > col2:
                new_line += table[row][col2]
            row += 1
        #print(new_line)
        new_table.append(new_line)
    for row in range(1, len(table)):
        new_line = table[row][0]
        col = 1
        for row2 in range(row+1, len(table)):
            if len(table[row2]) > col:
                new_line += table[row2][col]
            col += 1
        #print(new_line)
        new_table.append(new_line)
    return new_table

def rotateTable45rev(table):
    new_table = []
    for col in range(len(table[0])):
        new_line = table[0][col]
        row = 1
        for col2 in range(col-1, -1, -1):
            if len(table) > row and len(table[row]) > col2:
                new_line = table[row][col2] + new_line
            row += 1
        #print(new_line)
        new_table.append(new_line)
    for row in range(1, len(table)):
        new_line = table[row][-1]
        col = len(table[row])-2
        for row2 in range(row+1, len(table)):
            if len(table[row2]) > col and col >= 0:
                new_line = table[row2][col] + new_line
            col -= 1
        #print(new_line)
        new_table.append(new_line)
    return new_table

def countWordInTable(table, word):
    count = 0
    for line in table:
        words = re.findall(word, line)
        count += len(words)
        words = re.findall(word[::-1], line)
        count += len(words)
    return count

def getSubArray(table, char, row_size = 3, col_size = 3):
    sub_arrays = []
    row_span = (row_size - 1) // 2
    col_span = (col_size - 1) // 2
    for row in range(row_span, nu.size(table, 0) - row_span):
        for col in range(col_span, nu.size(table, 1) - col_span):
            if table[row, col] == char:
                sub_arrays.append(table[row-row_span:row+row_span+1, col-col_span:col+col_span+1])
    return sub_arrays
    
def verifySubArray(table):
    good = False
    if nu.size(table,0) >= 3 and nu.size(table,1) >= 3:
        good = True
        if not ((table[0,0] == "S" and table[2,2] == "M") or (table[0,0] == "M" and table[2,2] == "S")):
            good = False
        if not ((table[0,2] == "S" and table[2,0] == "M") or (table[0,2] == "M" and table[2,0] == "S")):
            good = False
    return good

def part_one():
    final_result = 0
    with open("./day_4/day_4_input.txt") as file:
        #lines = file.readlines()
        lines = [line.strip() for line in file.readlines()]
        final_result += countWordInTable(lines, "XMAS")
        lines2 = rotateTable(lines)
        final_result += countWordInTable(lines2, "XMAS")
        lines3 = rotateTable45(lines)
        final_result += countWordInTable(lines3, "XMAS")
        lines4 = rotateTable45rev(lines)
        final_result += countWordInTable(lines4, "XMAS")
    print(f"XMAS appear {final_result} times")

def part_two():
    final_result = 0
    with open("./day_4/day_4_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        table = nu.array(lines)
        sub_tables = getSubArray(table, "A")
        for sub_table in sub_tables:
            if verifySubArray(sub_table):
                final_result += 1
                print(sub_table)
    print(f"X-MAS appear {final_result} times")
    return final_result

if __name__ == "__main__":
    print("Advent of Code - Day 4")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
