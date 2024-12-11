#include <iostream>
#include <vector>
#include <stdio.h>
#include <string>
#include <fstream>
#include <sstream>

uint64_t blink_stone(uint64_t stone, int blink_times, uint64_t stone_count)
{
    if (blink_times < 1)
        return stone_count;
    if (stone == 0)
    {
        stone_count = blink_stone(1, blink_times - 1, stone_count);
    }
    else
    {
        std::string split_stone = std::to_string(stone);
        if ((split_stone.length() % 2) == 0)
        {
            unsigned long stone1 = std::stol(split_stone.substr(0, split_stone.length() / 2));
            unsigned long stone2 = std::stol(split_stone.substr(split_stone.length() / 2));
            stone_count = blink_stone(stone1, blink_times - 1, stone_count) + blink_stone(stone2, blink_times - 1, stone_count);
        }
        else
        {
            stone_count = blink_stone(stone * 2024, blink_times - 1, stone_count);
        }
    }
    return stone_count;
}

void part(char part_no)
{
    std::cout << "Part " << part_no << "\n";
    std::string line, str_stone;
    std::ifstream file("day_11\\day_11_input.txt");
    uint64_t stones_count = 0;
    if (file.is_open()) 
    {

        std::getline(file, line);
        std::cout << line << "\n";
        std::vector<unsigned long> stones;
        std::stringstream str_stones(line);
        while (std::getline(str_stones, str_stone, ' '))
        {
            stones.push_back(std::stol(str_stone));
        }
        int blink_times = 25;
        if (part_no == '2')
        {
            blink_times = 75;
        }
        for (const uint64_t& stone : stones)
        {
            uint64_t count = blink_stone(stone, blink_times, 1);
            stones_count += count;
            std::cout << "Stone " << stone << " = " << count << std::endl;
        }
        std::cout << "Stones count = " << stones_count << "\n";
    }
    else
    {
        std::cout << "File not open!\n";
    }
    file.close();
}

int main()
{
    char part_no;
    std::cout << "Advent of Code - Day 11\n";
    std::cout << "Wich part do you want to test (1 or 2):";
    std::cin >> part_no;
    if (part_no == '1' || part_no == '2')
    {
        part(part_no);
    }
    else
    {
        std::cout << "Invalid part!\n";
    }
    std::cout << "Press ENTER to exit.";
    std::cin.clear();
    std::cin.ignore(std::numeric_limits <std::streamsize> ::max(), '\n');
    std::cin.get();
    //while (std::cin.get() != '\n');
    //std::cin >> part_no;
}
