import re

def parse_input_data(lines, coord_offset = 0):
    data = []
    data_lines = re.split(r"(?:\r?\n){2,}", ("".join(lines)).strip())
    for data_line in data_lines:
        paramA = re.findall("A: X.(\\d*), Y.(\\d*)", data_line)
        paramB = re.findall("B: X.(\\d*), Y.(\\d*)", data_line)
        paramP = re.findall("X=(\\d*), Y=(\\d*)", data_line)
        #print(f"Line={data_line} => A={paramA}, B={paramB}, P={paramP}")
        data.append([(int(paramA[0][0]), int(paramA[0][1])), (int(paramB[0][0]), int(paramB[0][1])), \
                     (int(paramP[0][0])+coord_offset, int(paramP[0][1])+coord_offset)])
    return data

# Multiplier un des deux variables des deux équations pour obtenir la même dénominateur
# Soustraire les équations
# Résoudre l'équation restante avec une seule variable
# Remplacer la variable par sa valeur trouvé dans une des deux équations
# Résoudre l'autre variable
def solve_equations(equation_data):
    a1 = equation_data[0][0] * equation_data[1][1]
    r1 = equation_data[2][0] * equation_data[1][1]
    a2 = equation_data[0][1] * equation_data[1][0]
    r2 = equation_data[2][1] * equation_data[1][0]
    if ((r2 - r1) % (a2 - a1)) != 0:
        return None
    x = (r2 - r1) / (a2 - a1)
    y = (equation_data[2][0] - (x * equation_data[0][0])) / equation_data[1][0]
    if (y % 1) != 0:
        return None
    return (x, y)



def part_one():
    total_tokens = 0
    with open("./day_13/day_13_input.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines)
        for data_equation in data:
            result = solve_equations(data_equation)
            tokens = 0
            if result != None:
                tokens = result[0] * 3 + result[1]
            print(f"Equation {data_equation} => {result} = {tokens}")
            total_tokens += tokens
    print(f"Total number of tokens = {total_tokens}")

def part_two():
    total_tokens = 0
    with open("./day_13/day_13_input.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines, 10000000000000)
        for data_equation in data:
            result = solve_equations(data_equation)
            tokens = 0
            if result != None:
                tokens = result[0] * 3 + result[1]
            print(f"Equation {data_equation} => {result} = {tokens}")
            total_tokens += tokens
    print(f"Total number of tokens = {total_tokens}")

if __name__ == "__main__":
    print("Advent of Code - Day 13")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
