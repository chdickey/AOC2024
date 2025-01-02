import re

def parse_input_data(lines):
    data = {}
    data_lines = re.split(r"(?:\r?\n){2,}", ("".join(lines)).strip())
    for data_line in data_lines:
        if "Register A" in data_line:
            data["A"] = int(re.findall("A: (\\d*)", data_line)[0])
        if "Register B" in data_line:
            data["B"] =  int(re.findall("B: (\\d*)", data_line)[0])
        if "Register C" in data_line:
            data["C"] = int(re.findall("C: (\\d*)", data_line)[0])
        if "Program" in data_line:
            data["P"] = [int(n) for n in re.findall("(\\d),?", data_line)]
    return data

def operandValue(operand, regA, regB, regC):
    if operand >= 0 and operand < 4:
        return operand
    if operand == 4:
        return regA
    if operand == 5:
        return regB
    if operand == 6:
        return regC
    return None

def instruction(opcode, operand, regA, regB, regC):
    result = {}
    # Operands = 0=0, 1=1, 2=2, 3=3, 4=A, 5=B, 6=C, 7=Reserved
    if opcode == 0:
        # adv (division) = A // (2 * operand) => A
        result = {"A": regA // (2 ** operandValue(operand, regA, regB, regC))}
    elif opcode == 1:
        # bxl (bitwise XOR) of register B and operand => B
        result = {"B": regB ^ operand}
    elif opcode == 2:
        # bst (modulo) = operand % 8 => register B
        result = {"B": operandValue(operand, regA, regB, regC) % 8}
    elif opcode == 3:
        # jnz (jump not zero) = jump to operand if register A != 0
        if regA != 0:
            result = {"J": operand}
    elif opcode == 4:
        # bxc (bitwise XOR) of register B and register C => register B
        result = {"B": regB ^ regC}
    elif opcode == 5:
        # out (outputs) operand % 8 => outputs values comma separated
        result = {"O": operandValue(operand, regA, regB, regC) % 8}
    elif opcode == 6:
        # bdv (division) = A // (2 * operand) => B
        result = {"B": regA // (2 ** operandValue(operand, regA, regB, regC))}
    elif opcode == 7:
        # cdv (division) = A // (2 * operand) => C
        result = {"C": regA // (2 ** operandValue(operand, regA, regB, regC))}

    return result

def instructionReverse(opcode, operand, regA, regB, regC):
    result = {}
    # Operands = 0=0, 1=1, 2=2, 3=3, 4=A, 5=B, 6=C, 7=Reserved
    if opcode == 0:
        # adv (division) = A // (2 * operand) => A
        result = {"A": regA // (2 ** operandValue(operand, regA, regB, regC))}
    elif opcode == 1:
        # bxl (bitwise XOR) of register B and operand => B
        result = {"B": regB ^ operand}
    elif opcode == 2:
        # bst (modulo) = operand % 8 => register B
        result = {"B": operandValue(operand, regA, regB, regC) % 8}
    elif opcode == 3:
        # jnz (jump not zero) = jump to operand if register A != 0
        if regA != 0:
            result = {"J": operand}
    elif opcode == 4:
        # bxc (bitwise XOR) of register B and register C => register B
        result = {"B": regB ^ regC}
    elif opcode == 5:
        # out (outputs) operand % 8 => outputs values comma separated
        result = {"O": operandValue(operand, regA, regB, regC) % 8}
    elif opcode == 6:
        # bdv (division) = A // (2 * operand) => B
        result = {"B": regA // (2 ** operandValue(operand, regA, regB, regC))}
    elif opcode == 7:
        # cdv (division) = A // (2 * operand) => C
        result = {"C": regA // (2 ** operandValue(operand, regA, regB, regC))}

    return result

def part_one():
    with open("./day_17/day_17_input_sm2.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines)
        print(data)
        # 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        final_outputs = data["P"].copy()
        operation = 0
        outputs = []
        while operation < (len(data["P"]) - 1):
            op_result = instruction(data["P"][operation], data["P"][operation+1], data["A"], data["B"], data["C"])
            print(f"Operation:({data['P'][operation]}, {data['P'][operation+1]}) = {op_result}")
            if "H" in op_result:
                print(f"Halt on operation: {operation}")
                break
            data["A"] = op_result.get("A", data["A"])
            data["B"] = op_result.get("B", data["B"])
            data["C"] = op_result.get("C", data["C"])
            if "O" in op_result:
                outputs.append(str(op_result["O"]))
            if "J" in op_result:
                operation = op_result["J"] * 2
            else:
                operation += 2
        print(outputs)
        print(f"Final result = {','.join(outputs)}")


def part_two():
    result = 0
    with open("./day_17/day_17_input.txt") as file:
        lines = file.readlines()
        data = parse_input_data(lines)
        print(data)
        report_file = open("./day_17/day_17_report7.txt", "w")
        original_data = data.copy()
        #i = 40107841238 #32
        #i = 164281717714621 - 1
        nb_stop = 0
        #i = 164281713379865
        i =0b0000000000000000100101010110100100100000
        i =0b0000100101010110100100100011111111111111
        i = 0b100101010110100111010001011011010110111010111101
        i = 0b100101010110100111010000000000000000000000000000

        #i = 164281706420918
        j = 8 #38249
        print(f">{0b100 << (j*3) | 0b101 << ((j-1)*3) | 0b101 << ((j-2)*3) | 0b011 << ((j-3)*3)}")
        while i > 0 and nb_stop < 1000:#(j+i) < 99999999999999999:
            data = original_data.copy()
            data["A"] = i
            operation = 0
            outputs = []
            while operation < (len(data["P"]) - 1):
                op_result = instruction(data["P"][operation], data["P"][operation+1], data["A"], data["B"], data["C"])
                #print(f"Operation:({data['P'][operation]}, {data['P'][operation+1]}) = {op_result}")
                if "H" in op_result:
                    #print(f"Halt on operation: {operation}")
                    break
                data["A"] = op_result.get("A", data["A"])
                data["B"] = op_result.get("B", data["B"])
                data["C"] = op_result.get("C", data["C"])
                if "O" in op_result:
                    outputs.append(str(op_result["O"]))
                if "J" in op_result:
                    operation = op_result["J"] * 2
                else:
                    operation += 2
            print(f"{i:12d}=>{outputs}\r", end="")
            #report_file.write(f"Test {i:10d} -> {outputs}\n")
            if int("".join([str(o) for o in original_data["P"]])) == int("".join(outputs)):
                print()
                result = i
                print(f"Found: {result}")
                report_file.write(f"Test {i:10d} -> {outputs}\n")
                #break
            if len(outputs) < len(original_data["P"]):
                nb_stop += 1
            else:
                nb_stop = 0
            i -= 1
#            if i > (0b100 << (j*3) | 0b101 << ((j-1)*3) | 0b010 << ((j-2)*3) | 0b110 << ((j-3)*3) | 0b100 << ((j-4)*3) | 0b111 << ((j-5)*3) | 0b010 << ((j-6)*3) | 0b001 << ((j-7)*3) | 0b100 << ((j-8)*3)):
#                print()
#                print(f">{0b100 << (j*3) | 0b101 << ((j-1)*3) | 0b010 << ((j-2)*3) | 0b110 << ((j-3)*3) | 0b100 << ((j-4)*3) | 0b111 << ((j-5)*3) | 0b010 << ((j-6)*3) | 0b001 << ((j-7)*3) | 0b011 << ((j-8)*3)}")
#                j += 1
#                i = (0b100 << (j*3) | 0b101 << ((j-1)*3) | 0b010 << ((j-2)*3) | 0b110 << ((j-3)*3) | 0b100 << ((j-4)*3) | 0b111 << ((j-5)*3) | 0b010 << ((j-6)*3) | 0b001 << ((j-7)*3) | 0b011 << ((j-8)*3))
        report_file.close()
        print()
        print(f"Final result = {result}")

if __name__ == "__main__":
    print("Advent of Code - Day 17")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
