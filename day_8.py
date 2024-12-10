import numpy as nu, re

def get_frequencies(map):
    frequencies = []
    for row in map:
        for col in row:
            if re.search("\\w", col) != None and col not in frequencies:
                frequencies.append(col)
    return frequencies

def search_antinodes(map, antinodes_map, frequency):
    antinodes_map_freq = nu.full_like(map, ".")
    map_size = (nu.size(map, 0), nu.size(map, 1))
    frequency_locations = nu.where(map == frequency)
    antinodes_map_freq[frequency_locations[0][0], frequency_locations[1][0]] = frequency
    for location_no1 in range(len(frequency_locations[0])-1):
        position1 = (frequency_locations[0][location_no1], frequency_locations[1][location_no1])
        for location_no2 in range(location_no1+1,len(frequency_locations[0])):
            position2 = (frequency_locations[0][location_no2], frequency_locations[1][location_no2])
            antinodes_map_freq[position2[0], position2[1]] = frequency
            position_offset = (position2[0] - position1[0], position2[1] - position1[1])
            position_antinode = (position1[0] - position_offset[0], position1[1] - position_offset[1])
            if position_antinode[0] >= 0 and position_antinode[0] < map_size[0] and \
                position_antinode[1] >= 0 and position_antinode[1] < map_size[1]:
                antinodes_map[position_antinode[0], position_antinode[1]] = "#"
                if antinodes_map_freq[position_antinode[0], position_antinode[1]] == frequency:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "%"
                else:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "#"
            position_antinode = (position2[0] + position_offset[0], position2[1] + position_offset[1])
            if position_antinode[0] >= 0 and position_antinode[0] < map_size[0] and \
                position_antinode[1] >= 0 and position_antinode[1] < map_size[1]:
                antinodes_map[position_antinode[0], position_antinode[1]] = "#"
                if antinodes_map_freq[position_antinode[0], position_antinode[1]] == frequency:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "%"
                else:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "#"
    #print(antinodes_map_freq)
    return antinodes_map_freq

def search_antinodes_with_harmonics(map, antinodes_map, frequency):
    antinodes_map_freq = nu.full_like(map, ".")
    map_size = (nu.size(map, 0), nu.size(map, 1))
    frequency_locations = nu.where(map == frequency)
    antinodes_map_freq[frequency_locations[0][0], frequency_locations[1][0]] = frequency
    for location_no1 in range(len(frequency_locations[0])-1):
        position1 = (frequency_locations[0][location_no1], frequency_locations[1][location_no1])
        for location_no2 in range(location_no1+1,len(frequency_locations[0])):
            position2 = (frequency_locations[0][location_no2], frequency_locations[1][location_no2])
            antinodes_map[position1[0], position1[1]] = "#"
            antinodes_map[position2[0], position2[1]] = "#"
            antinodes_map_freq[position2[0], position2[1]] = frequency
            position_offset = (position2[0] - position1[0], position2[1] - position1[1])
            harmonic = 1
            position_antinode = (position1[0] - (position_offset[0] * harmonic), position1[1] - (position_offset[1] * harmonic))
            while position_antinode[0] >= 0 and position_antinode[0] < map_size[0] and \
                position_antinode[1] >= 0 and position_antinode[1] < map_size[1]:
                antinodes_map[position_antinode[0], position_antinode[1]] = "#"
                if antinodes_map_freq[position_antinode[0], position_antinode[1]] == frequency:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "%"
                else:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "#"
                harmonic += 1
                position_antinode = (position1[0] - (position_offset[0] * harmonic), position1[1] - (position_offset[1] * harmonic))
            harmonic = 1
            position_antinode = (position2[0] + (position_offset[0] * harmonic), position2[1] + (position_offset[1] * harmonic))
            while position_antinode[0] >= 0 and position_antinode[0] < map_size[0] and \
                position_antinode[1] >= 0 and position_antinode[1] < map_size[1]:
                antinodes_map[position_antinode[0], position_antinode[1]] = "#"
                if antinodes_map_freq[position_antinode[0], position_antinode[1]] == frequency:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "%"
                else:
                    antinodes_map_freq[position_antinode[0], position_antinode[1]] = "#"
                harmonic += 1
                position_antinode = (position2[0] + (position_offset[0] * harmonic), position2[1] + (position_offset[1] * harmonic))
    #print(antinodes_map_freq)
    return antinodes_map_freq

def part_one():
    total_antinodes = 0
    with open("./day_8/day_8_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        #print(map)
        antinodes_map = nu.empty_like(map)
        #print(antinodes_map)
        frequencies = get_frequencies(map)
        for frequency in frequencies:
            antinodes_map_freq = search_antinodes(map, antinodes_map, frequency)
            #nu.savetxt(".\\day_8\\antinodes_{0}.txt".format(frequency), antinodes_map_freq, "%s", "")
    total_antinodes = nu.count_nonzero(antinodes_map == "#")
    print(f"Total locations = {total_antinodes} antinodes")
    return total_antinodes

def part_two():
    total_antinodes = 0
    with open("./day_8/day_8_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        antinodes_map = nu.empty_like(map)
        frequencies = get_frequencies(map)
        for frequency in frequencies:
            antinodes_map_freq = search_antinodes_with_harmonics(map, antinodes_map, frequency)
            #nu.savetxt(".\\day_8\\antinodes_{0}.txt".format(frequency), antinodes_map_freq, "%s", "")
    total_antinodes = nu.count_nonzero(antinodes_map == "#")
    print(f"Total locations = {total_antinodes} antinodes")
    return total_antinodes

if __name__ == "__main__":
    print("Advent of Code - Day 8")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
