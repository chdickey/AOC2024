from functools import cache

class Robot:
    key = "A"
    sequence = ""
    keypad = {}

    def __init__(self, key = "A", sequence = "", keypad = {}):
        self.key = key
        self.sequence = sequence
        self.keypad = keypad

def numericKeyPad():
    keyPad= {}
    keyPad["A"] = {"A": "A", "0": "<A", "1": "^<<A", "2": "<^A", "3": "^A", "4": "^^<<A", "5": "<^^A", 
                   "6": "^^A", "7": "^^^<<A", "8": "<^^^A", "9": "^^^A"}
    keyPad["0"] = {"A": ">A", "0": "A", "1": "^<A", "2": "^A", "3": ">^A", "4": "<^^A", "5": "^^A", 
                   "6": ">^^A", "7": "<^^^A", "8": "^^^A", "9": ">^^^A"}
    keyPad["1"] = {"A": ">>vA", "0": ">vA", "1": "A", "2": ">A", "3": ">>A", "4": "^A", "5": ">^A", 
                   "6": ">>^A", "7": "^^A", "8": ">^^A", "9": ">>^^A"}
    keyPad["2"] = {"A": ">vA", "0": "vA", "1": "<A", "2": "A", "3": ">A", "4": "<^A", "5": "^A", 
                   "6": ">^A", "7": "<^^A", "8": "^^A", "9": ">^^A"}
    keyPad["3"] = {"A": "vA", "0": "<vA", "1": "<<A", "2": "<A", "3": "A", "4": "<<^A", "5": "<^A", 
                   "6": "^A", "7": "<<^^A", "8": "<^^A", "9": "^^A"}
    keyPad["4"] = {"A": ">>vvA", "0": ">vvA", "1": "vA", "2": ">vA", "3": ">>vA", "4": "A", "5": ">A", 
                   "6": ">>A", "7": "^A", "8": ">^A", "9": ">>^A"}
    keyPad["5"] = {"A": ">vvA", "0": "vvA", "1": "v<A", "2": "vA", "3": ">vA", "4": "<A", "5": "A", 
                   "6": ">A", "7": "<^A", "8": "^A", "9": ">^A"}
    keyPad["6"] = {"A": "vvA", "0": "vv<A", "1": "v<<A", "2": "v<A", "3": "vA", "4": "<<A", "5": "<A", 
                   "6": "A", "7": "<<^A", "8": "<^A", "9": "^A"}
    keyPad["7"] = {"A": ">>vvvA", "0": ">vvvA", "1": "vvA", "2": ">vvA", "3": ">>vvA", "4": "vA", "5": ">vA", 
                   "6": ">>vA", "7": "A", "8": ">A", "9": ">>A"}
    keyPad["8"] = {"A": "vvv>A", "0": "vvvA", "1": "vv<A", "2": "vvA", "3": ">vvA", "4": "v<A", "5": "vA", 
                   "6": ">vA", "7": "<A", "8": "A", "9": ">A"}
    keyPad["9"] = {"A": "vvvA", "0": "vvv<A", "1": "vv<<A", "2": "vv<A", "3": "vvA", "4": "v<<A", "5": "v<A", 
                   "6": "vA", "7": "<<A", "8": "<A", "9": "A"}
    return keyPad

def directionalKeyPad(human = False):
    keyPad = {}
    if human:
        keyPad["A"] = {"A": "A", "^": "<A", ">": "vA", "v": "<vA", "<": "<v<A"}
        keyPad["^"] = {"A": ">A", "^": "A", ">": ">vA", "v": "vA", "<": "v<A"}
        keyPad[">"] = {"A": "^A", "^": "<^A", ">": "A", "v": "<A", "<": "<<A"}
        keyPad["v"] = {"A": ">^A", "^": "^A", ">": ">A", "v": "A", "<": "<A"}
        keyPad["<"] = {"A": ">>^A", "^": ">^A", ">": ">>A", "v": ">A", "<": "A"}
    else:
        keyPad["A"] = {"A": "A", "^": "<A", ">": "vA", "v": "<vA", "<": "v<<A"}
        keyPad["^"] = {"A": ">A", "^": "A", ">": ">vA", "v": "vA", "<": "<vA"}
        keyPad[">"] = {"A": "^A", "^": "<^A", ">": "A", "v": "<A", "<": "<<A"}
        keyPad["v"] = {"A": ">^A", "^": "^A", ">": ">A", "v": "A", "<": "<A"}
        keyPad["<"] = {"A": ">>^A", "^": ">^A", ">": ">>A", "v": ">A", "<": "A"}
    return keyPad

def processRobot(robots, no):
    sequence = ""
    print(f"Process robot: {no:2d}\r", end="")
    if no == 0: #Human
        if len(robots[no].keypad) <= 0:
            robots[no].keypad = directionalKeyPad(True)
        for key in robots[no+1].sequence:
            robots[no].sequence = robots[no].keypad[robots[no].key][key]
            sequence += robots[no].sequence
            robots[no].key = key
    elif no > 0:
        if len(robots[no].keypad) <= 0:
            robots[no].keypad = directionalKeyPad()
        for key in robots[no+1].sequence:
            robots[no].sequence = robots[no].keypad[robots[no].key][key]
            sequence += processRobot(robots, no - 1)
            robots[no].key = key
    return sequence

@cache
def processRobot2(keyStart, code, no):
    sequence = ""
    #print(f"Process robot: {no:2d}\r", end="")
    keypad = directionalKeyPad()
    last_key = keyStart
    if no == 0: #Human
        keypad = directionalKeyPad(True)
    for key in code:
        if no == 0:
            sequence += keypad[keyStart][key]
        else:
            seq, last_key  = processRobot2(last_key, keypad[keyStart][key], no - 1)
            sequence += seq
        keyStart = key
    return sequence, keyStart

def part_one():
    complexity = 0
    with open("./day_21/day_21_input.txt") as file:
        lines = file.readlines()
        codes = [list(line.strip()) for line in lines]
        numKp = numericKeyPad()
        dirKp = directionalKeyPad()
        dirKpH = directionalKeyPad(False)
        for code in codes:
            sequence = ""
            keyStartR1 = "A"
            keyStartR2 = "A"
            keyStartR3 = "A"
            for keyR1 in code:
                seqR1 = numKp[keyStartR1][keyR1]
                for keyR2 in seqR1:
                    seqR2 = dirKp[keyStartR2][keyR2]
                    for keyR3 in seqR2:
                        seqR3 = dirKpH[keyStartR3][keyR3]
                        sequence += seqR3
                        keyStartR3 = keyR3#seqR3[-1]
                    keyStartR2 = keyR2 #seqR2[-1]
                keyStartR1 = keyR1 #seqR1[-1]
            print(f"{code} = {sequence}  : {len(sequence)} * {int(''.join(code[:-1]))}")
            complexity += int("".join(code[:-1])) * len(sequence)
    print(f"Complexity of the codes = {complexity}")


def part_two():
    complexity = 0
    with open("./day_21/day_21_input.txt") as file:
        lines = file.readlines()
        codes = [list(line.strip()) for line in lines]
        numKp = numericKeyPad()
        dirKp = directionalKeyPad()
        dirKpH = directionalKeyPad(False)
        for code in codes:
            #robots = [Robot() for i in range(26)] 
            sequence = ""
            keyStart = "A"
            last_key = keyStart
            for key in code:
                print(f"Process robot: {25:2d}\r", end="")
                seq, last_key = processRobot2(last_key, numKp[keyStart][key], 24)
                sequence += seq
                #robots[25].sequence = numKp[robots[25].key][key]
                #sequence += processRobot(robots, 24)
                #robots[25].key = key
                keyStart = key
            print(f"{code} = {sequence}  : {len(sequence)} * {int(''.join(code[:-1]))}")
            complexity += int("".join(code[:-1])) * len(sequence)
    print(f"Complexity of the codes = {complexity}")

if __name__ == "__main__":
    print("Advent of Code - Day 21")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
