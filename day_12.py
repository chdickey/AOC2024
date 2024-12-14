import numpy as nu

class area:
    positions = []
    perimeter = 0
    empty_areas = []

    def __init__(self, positions = [], perimeter = 0):
        self.positions = positions
        self.perimeter = perimeter

    @staticmethod
    def find_areas(positions):
        areas = []
        positions_search = positions.copy()
        while len(positions_search) > 0:
            group = []
            position = area.__find_top_left(positions_search)
            positions_search = area.__find_area(positions_search, position, group)
            if len(group) > 0:
                areas.append(area(group))
        return areas
    
    def bounds(self):
        rows = list(set([pos[0] for pos in self.positions]))
        rows.sort()
        row_min = 99999
        row_max = 0
        col_min = 99999
        col_max = 0
        for row in rows:
            cols = list(set([pos[1] if pos[0] == row else -1 for pos in self.positions]))
            cols.sort()
            if -1 in cols:
                cols.remove(-1)
            col_min = cols[0] if cols[0] < col_min else col_min
            col_max = cols[-1] if cols[-1] > col_max else col_max
        cols = list(set([pos[1] for pos in self.positions]))
        cols.sort()
        for col in cols:
            rows = list(set([pos[0] if pos[1] == col else -1 for pos in self.positions]))
            rows.sort()
            if -1 in rows:
                rows.remove(-1)
            row_min = rows[0] if rows[0] < row_min else row_min
            row_max = rows[-1] if rows[-1] > row_max else row_max
        return [(row_min, col_min),(row_max, col_max)]

    def surface(self):
        return len(self.positions)
    
    def side_count(self):
        return self.outside_count() + self.inside_count()
        
    def inside_count(self):
        empty_areas = self.__find_empty_areas()
        inside_count = 0
        if len(empty_areas) > 0:
            for empty_area in empty_areas:
                inside_count += empty_area.outside_count()
        return inside_count
    
    def outside_count(self):
        position = self.top_left_position()
        empty_areas = self.__find_empty_areas()
        areas_positions = set()
        if len(empty_areas) > 0:
            for empty_area in empty_areas:
                areas_positions |= set(empty_area.positions)
        outside_count = area.__calculate_outside_sides(set(self.positions) | areas_positions, position, position, 0, 0)
        return outside_count

    def top_left_position(self):
        return area.__find_top_left(self.positions)

    def get_map(self):
        bounds = self.bounds()
        map = nu.full((bounds[1][0] - bounds[0][0] + 1, bounds[1][1] - bounds[0][1] + 1), ".", dtype=nu.str_)
        for position in self.positions:
            map[position[0] - bounds[0][0], position[1] - bounds[0][1]] = "#"
        return map
    
    @staticmethod
    def __find_top_left(positions):
        if positions == None or len(positions) <= 0:
            return None
        top = 999999
        left = 999999
        for position in positions:
            if position[0] < top:
                top = position[0]
        for position in positions:
            if position[0] == top and position[1] < left:
                left = position[1]
        return (top, left)

    @staticmethod
    def __find_area(positions, position, group = []):
        if position in positions:
            group.append(position)
            positions.remove(position)
            area.__find_area(positions, (position[0]-1, position[1]), group)
            area.__find_area(positions, (position[0], position[1]-1), group)
            area.__find_area(positions, (position[0]+1, position[1]), group)
            area.__find_area(positions, (position[0], position[1]+1), group)
        return positions
    
    @staticmethod
    def __calculate_outside_sides(positions, position_start, position, direction, side_count):
        if position == (56, 84):
            print("break")
        if position_start == position and side_count > 3 and (direction == 0 or direction == 4):
            return side_count
        if direction == 0:
            if (position[0]-1, position[1]) in positions:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, (position[0]-1, position[1]), 3, side_count)
            elif (position[0], position[1]+1) in positions:
                return area.__calculate_outside_sides(positions, position_start, (position[0], position[1]+1), 0, side_count)
            else:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, position, 1, side_count)
        if direction == 1:
            if (position[0], position[1]+1) in positions:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, (position[0], position[1]+1), 0, side_count)
            elif (position[0]+1, position[1]) in positions:
                return area.__calculate_outside_sides(positions, position_start, (position[0]+1, position[1]), 1, side_count)
            else:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, position, 2, side_count)
        if direction == 2:
            if (position[0]+1, position[1]) in positions:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, (position[0]+1, position[1]), 1, side_count)
            elif (position[0], position[1]-1) in positions:
                return area.__calculate_outside_sides(positions, position_start, (position[0], position[1]-1), 2, side_count)
            else:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, position, 3, side_count)
        if direction == 3:
            if (position[0], position[1]-1) in positions:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, (position[0], position[1]-1), 2, side_count)
            elif (position[0]-1, position[1]) in positions:
                return area.__calculate_outside_sides(positions, position_start, (position[0]-1, position[1]), 3, side_count)
            else:
                side_count += 1
                return area.__calculate_outside_sides(positions, position_start, position, 0, side_count)
        #if direction == 4:
        #    if (position[0]-1, position[1]) in self.positions:
        #        side_count += 1
        #        return self.__calculate_outside_sides(position_start, (position[0]-1, position[1]), 3, side_count)
        #    elif (position[0], position[1]+1) in self.positions:
        #        return self.__calculate_outside_sides(position_start, (position[0], position[1]+1), 4, side_count)
        #    else:
        #        side_count += 1
        #        return self.__calculate_outside_sides(position_start, position, 5, side_count)
        #if direction == 5:
        #    if (position[0], position[1]+1) in self.positions:
        #        side_count += 1
        #        return self.__calculate_outside_sides(position_start, (position[0], position[1]+1), 4, side_count)
        #    elif (position[0]+1, position[1]) in self.positions:
        #        return self.__calculate_outside_sides(position_start, (position[0]+1, position[1]), 5, side_count)
        #    else:
        #        side_count += 1
        #        return self.__calculate_outside_sides(position_start, position, 6, side_count)
        #if direction == 6:
        #    if (position[0]+1, position[1]) in self.positions:
        #        side_count += 1
        #        return self.__calculate_outside_sides(position_start, (position[0]+1, position[1]), 5, side_count)
        #    elif (position[0], position[1]-1) in self.positions:
        #        return self.__calculate_outside_sides(position_start, (position[0], position[1]-1), 6, side_count)
        return None

    def __find_empty_spaces(self):
        empty_spaces = []
        rows = list(set([pos[0] for pos in self.positions]))
        rows.sort()
        for row in rows:
            cols = list(set([pos[1] if pos[0] == row else -1 for pos in self.positions]))
            cols.sort()
            if -1 in cols:
                cols.remove(-1)
            outside_positions = []
            outside = False
            for col in range(cols[0], cols[-1]+1):
                if col not in cols:
                    outside_positions.append((row, col))
                    outside = True
                else:
                    if outside and len(outside_positions) > 0:
                        empty_spaces.extend(outside_positions)
                        outside_positions = []
                    outside = False
        #print(f"Empty spaces = {empty_spaces}")

        return empty_spaces

    def __find_empty_areas(self):
        empty_spaces = self.__find_empty_spaces()
        tested_areas = area.find_areas(empty_spaces)
        empty_areas = []
        for empty_area in tested_areas:
            empty_rows = list(set([pos[0] for pos in empty_area.positions]))
            empty_rows.sort()
            inside = False
            for empty_row in empty_rows:
                empty_cols = list(set([pos[1] if pos[0] == empty_row else -1 for pos in empty_area.positions]))
                empty_cols.sort()
                if -1 in empty_cols:
                    empty_cols.remove(-1)
                if not((empty_row, empty_cols[0]-1) in self.positions and (empty_row, empty_cols[-1]+1) in self.positions):
                    break
            else:
                empty_cols = list(set([pos[1] for pos in empty_area.positions]))
                empty_cols.sort()
                for empty_col in empty_cols:
                    empty_rows = list(set([pos[0] if pos[1] == empty_col else -1 for pos in empty_area.positions]))
                    empty_rows.sort()
                    if -1 in empty_rows:
                        empty_rows.remove(-1)
                    if not((empty_rows[0]-1, empty_col) in self.positions and (empty_rows[-1]+1, empty_col) in self.positions):
                        break
                else:
                    inside = True
            if inside:
                empty_areas.append(empty_area)
        return empty_areas

def calculate_plants_groups(plants):
    plants_groups = {}
    for plant, regions in plants.items():
        perimeters = []
        groups = []
        for region in regions:
            perimeter = 4
            group = {(region[0], region[1])}
            for region2 in regions:
                if region[0] == region2[0] and abs(region[1] - region2[1]) == 1 or \
                    region[1] == region2[1] and abs(region[0] - region2[0]) == 1:
                    perimeter -= 1
                    group.add((region2[0], region2[1]))
            perimeters.append(perimeter)
            groups.append(group)
        plants_groups[plant] = (perimeters, groups)
    for plant_groups in plants_groups.values():
        i = 0
        while i < len(plant_groups[1]):
            j = i + 1
            while j < len(plant_groups[1]):
                if not plant_groups[1][i].isdisjoint(plant_groups[1][j]):
                    plant_groups[0][i]  += plant_groups[0][j]
                    plant_groups[1][i] |= plant_groups[1][j]
                    del plant_groups[0][j]
                    del plant_groups[1][j]
                    j = i + 1
                else:
                    j += 1
            i += 1
    return plants_groups

def search_plants(map):
    plants_positons = {}
    for row in range(map.shape[0]):
        for col in range(map.shape[1]):
            if map[row, col] not in plants_positons:
                plants_positons[map[row,col]] = [(row, col)]
            else:
                plants_positons[map[row,col]].append((row, col))
    plants = {}
    for plant, positions in plants_positons.items():
        areas = []
        for region in positions:
            perimeter = 4
            group = {(region[0], region[1])}
            for region2 in positions:
                if region[0] == region2[0] and abs(region[1] - region2[1]) == 1 or \
                    region[1] == region2[1] and abs(region[0] - region2[0]) == 1:
                    perimeter -= 1
                    group.add((region2[0], region2[1]))
            areas.append(area(group, perimeter))
        plants[plant] = areas
    for areas in plants.values():
        i = 0
        while i < len(areas):
            j = i + 1
            while j < len(areas):
                if not areas[i].positions.isdisjoint(areas[j].positions):
                    areas[i].perimeter += areas[j].perimeter
                    areas[i].positions |= areas[j].positions
                    del areas[j]
                    j = i + 1
                else:
                    j += 1
            i += 1
    return plants

def find_plants_regions(map):
    plants = {}
    for row in range(map.shape[0]):
        for col in range(map.shape[1]):
            if map[row, col] not in plants:
                plants[map[row,col]] = [(row, col)]
            else:
                plants[map[row,col]].append((row, col))
    return plants

def find_top_left(group):
    top = 9999
    left = 9999
    for position in group:
        if position[0] < top:
            top = position[0]
    for position in group:
        if position[0] == top and position[1] < left:
            left = position[1]
    return (top, left)

def calculate_sides(group, position_start, position, direction, side_count):
    if position_start == position and side_count > 3 and direction == 0:
        return side_count
    if direction == 0:
        if (position[0], position[1]+1) in group:
            return calculate_sides(group, position_start, (position[0], position[1]+1), 0, side_count)
        else:
            side_count += 1
            return calculate_sides(group, position_start, position, 1, side_count)
    if direction == 1:
        if (position[0], position[1]+1) in group:
            side_count += 1
            return calculate_sides(group, position_start, (position[0], position[1]+1), 0, side_count)
        elif (position[0]+1, position[1]) in group:
            return calculate_sides(group, position_start, (position[0]+1, position[1]), 1, side_count)
        else:
            side_count += 1
            return calculate_sides(group, position_start, position, 2, side_count)
    if direction == 2:
        if (position[0]+1, position[1]) in group:
            side_count += 1
            return calculate_sides(group, position_start, (position[0]+1, position[1]), 1, side_count)
        elif (position[0], position[1]-1) in group:
            return calculate_sides(group, position_start, (position[0], position[1]-1), 2, side_count)
        else:
            side_count += 1
            return calculate_sides(group, position_start, position, 3, side_count)
    if direction == 3:
        if (position[0], position[1]-1) in group:
            side_count += 1
            return calculate_sides(group, position_start, (position[0], position[1]-1), 2, side_count)
        elif (position[0]-1, position[1]) in group:
            return calculate_sides(group, position_start, (position[0]-1, position[1]), 3, side_count)
        else:
            side_count += 1
            return calculate_sides(group, position_start, position, 4, side_count)
    if direction == 4:
        if (position[0]-1, position[1]) in group:
            side_count += 1
            return calculate_sides(group, position_start, (position[0]-1, position[1]), 3, side_count)
        elif (position[0], position[1]+1) in group:
            return calculate_sides(group, position_start, (position[0], position[1]+1), 4, side_count)
    return side_count


def part_one():
    total_score = 0
    with open("./day_12/day_12_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        plants = find_plants_regions(map)
        #print(plants)
        plants_groups = calculate_plants_groups(plants)
        #print(plants_groups)
        for plant, plant_groups in plants_groups.items():
            plant_score = 0
            for group in range(len(plant_groups[0])):
                plant_score += plant_groups[0][group] * len(plant_groups[1][group])
                print(f"Region {plant} = {len(plant_groups[1][group])}  * {plant_groups[0][group]} = {plant_score}")
            #regions = nu.where(map == plant)
            #print(f"Region {plant} = {len(regions[0])} * {perimeter} = {perimeter * (len(regions[0]) + 1)}")
            total_score += plant_score
    print(f"Total price = {total_score}")

def part_two():
    total_score = 0
    with open("./day_12/day_12_input.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]
        map = nu.array(lines)
        #plants = find_plants_regions(map)
        #print(plants)
        #plants_groups = calculate_plants_groups(plants)
        #print(plants_groups)
        report_file = open("./day_12/day_12_report.txt", "w")
        plants = search_plants(map)
        for plant, areas in plants.items():
            plant_score = 0
            #print(f"Groupe {plant} = {plant_groups}")
            for plant_area in areas:
                plant_map = plant_area.get_map()
                report_file.write("\n")
                sides_count = plant_area.side_count()
                area_score = sides_count * plant_area.surface()
                plant_score += area_score
                report_file.write(f"Region {plant} = {plant_area.surface()}  * {sides_count} = {area_score}\n")
                report_file.write(f"Position={plant_area.top_left_position()}, Surface={plant_area.surface()}, Outside={plant_area.outside_count()}, Inside={plant_area.inside_count()}\n")
                nu.savetxt(report_file, plant_map, "%s", "")
                print(f"Region {plant} = {plant_area.surface()}  * {sides_count} = {area_score}")
            print(f"Region {plant} total score = {plant_score}")
            #regions = nu.where(map == plant)
            #print(f"Region {plant} = {len(regions[0])} * {perimeter} = {perimeter * (len(regions[0]) + 1)}")
            total_score += plant_score
        report_file.close()
    print(f"Total price = {total_score}")


if __name__ == "__main__":
    print("Advent of Code - Day 12")
    part = input("Wich part do you want to test (1 or 2):")
    if part == "1":
        part_one()
    elif part == "2":
        part_two()
    