

def equation_data(line):
    data = line.split(": ")
    numbers = [int(x) for x in data[1].split(" ")]
    return (int(data[0]), numbers)

def calibration_test(result, numbers, operators, total):
    if result < total:
        return []
    new_operators = operators.copy()
    if len(numbers) > 0:
        new_operators.append("*")
        new_operators = calibration_test(result, numbers[1:], new_operators, total * numbers[0])
        if len(new_operators) <= 0:
            new_operators = operators.copy()
            new_operators.append("+")
            new_operators = calibration_test(result, numbers[1:], new_operators, total + numbers[0])
    else:
        if result == total:
            #print("success")
            return operators
        else:
            return []
    return new_operators

def calibration_test2(result, numbers, operators, total):
    if result < total:
        return []
    new_operators = operators.copy()
    if len(numbers) > 0:
        new_operators.append("*")
        new_operators = calibration_test2(result, numbers[1:], new_operators, total * numbers[0])
        if len(new_operators) <= 0:
            new_operators = operators.copy()
            new_operators.append("+")
            new_operators = calibration_test2(result, numbers[1:], new_operators, total + numbers[0])
            if len(new_operators) <= 0:
                new_operators = operators.copy()
                new_operators.append("||")
                new_operators = calibration_test2(result, numbers[1:], new_operators, int(str(total) + str(numbers[0])))
    else:
        if result == total:
            #print("success")
            return operators
        else:
            return []
    return new_operators

def part_one():
    calibration_result = 0
    with open("./day_7/day_7_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            result, numbers = equation_data(line)
            operators = calibration_test(result, numbers[1:], [], numbers[0])
            if len(operators) > 0:
                calibration_result += result
            #print(f"{result}; {numbers} = {operators} => calibration result = {calibration_result}")
            #if input("exit?") == "q":
            #    break;
    print(f"Total calibration result = {calibration_result} ")
    return calibration_result

def part_two():
    calibration_result = 0
    with open("./day_7/day_7_input.txt") as file:
        lines = file.readlines()
        for line in lines:
            result, numbers = equation_data(line)
            operators = calibration_test2(result, numbers[1:], [], numbers[0])
            if len(operators) > 0:
                calibration_result += result
            #print(f"{result}; {numbers} = {operators} => calibration result = {calibration_result}")
            #if input("exit?") == "q":
            #    break;
    print(f"Total calibration result = {calibration_result} ")
    return calibration_result


if __name__ == "__main__":
    print("Advent of Code - Day 7")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
