
def createRulesDictionnary(rules):
    rules_dict = {}
    for rule in rules:
        if rule[0] in rules_dict:
            rules_dict[rule[0]].append(rule[1])
        else:
            rules_dict[rule[0]] = [rule[1]]
    return rules_dict


def isUpdateGood(update, rules_dict):
    middle_page = update[len(update)//2]
    for pos, page in enumerate(update):
        if page in rules_dict:
            for rule in rules_dict[page]:
                pos2 = -1
                if rule in update:
                    pos2 = update.index(rule)
                if pos2 >= 0 and pos > pos2:
                    middle_page = 0
                    break
        if middle_page == 0:
            break
    return middle_page

def correctUpdateOrder(update, rules_dict):
    max_iter = 500
    nb_iter = 0
    pos = 0
    while pos < len(update) and nb_iter < max_iter:
        nb_iter += 1
        page = update[pos]
        if page in rules_dict:
            for rule in rules_dict[page]:
                pos2 = -1
                if rule in update:
                    pos2 = update.index(rule)
                if pos2 >= 0 and pos > pos2:
                    #update = [*update[:pos2], *update[pos2+1:pos+1], update[pos2], *update[pos+1:]]
                    update = [*update[:pos2], update[pos], *update[pos2:pos], *update[pos+1:]]
                    pos = pos2
                    break
            else:
                pos += 1
        else:
            pos += 1
    if nb_iter >= max_iter:
        print("error")
    return update

def part_one():
    total_page_number = 0
    with open("./day_5/day_5_input.txt") as file:
        #lines = [line for line in file.readlines()]
        update_section = False
        rules = []
        updates = []
        for line in file.readlines():
            if len(line.strip()) <= 0:
                update_section = True
                continue
            if update_section:
                updates.append([int(x) for x in line.strip().split(",")])
            else:
                rules.append([int(x) for x in line.strip().split("|")])
        rules_dict = createRulesDictionnary(rules)
        for update in updates:
            total_page_number += isUpdateGood(update, rules_dict)
    print(f"Total correctly-ordered updates = {total_page_number}")
    return total_page_number

def part_two():
    total_page_number = 0
    with open("./day_5/day_5_input.txt") as file:
        #lines = [line for line in file.readlines()]
        update_section = False
        rules = []
        updates = []
        for line in file.readlines():
            if len(line.strip()) <= 0:
                update_section = True
                continue
            if update_section:
                updates.append([int(x) for x in line.strip().split(",")])
            else:
                rules.append([int(x) for x in line.strip().split("|")])
        rules_dict = createRulesDictionnary(rules)
        for update in updates:
            if isUpdateGood(update, rules_dict) <= 0:
                new_update = correctUpdateOrder(update, rules_dict)
                #print(f"old update = {update}")
                #print(f"new update = {new_update}")
                total_page_number += new_update[len(new_update)//2]
    print(f"Total correctly-reordered updates = {total_page_number}")
    return total_page_number


if __name__ == "__main__":
    print("Advent of Code - Day 5")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
