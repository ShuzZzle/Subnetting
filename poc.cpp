#include <iostream>
#include <bitset>


using namespace std;
uint8_t alpha = 255;
uint8_t red = 255;
uint8_t green = 255;
uint8_t blue = 0;
uint32_t color;

int main()
{
    // Put it together :)
    //FORMAT: AARRGGBB
    color = (alpha << 24) | (red << 16) | (green << 8) | blue;


    // Extraction
    std::cout << "Binary representation before everything: " << std::bitset<32>(color) << std::endl;
    std::cout << "Alpha: " << ((color >> 24) & 0xFF) << std::endl;
    std::cout << "Binary representation: " << std::bitset<32>(color >> 24) << "\n" << std::endl;
    std::cout << "Red: " << ((color >> 16) & 0xFF) <<  std::endl;
    std::cout << "Binary representation: " << std::bitset<32>(color >> 16) << "\n" << std::endl;
    std::cout << "Green: " << ((color >> 8) & 0xFF) <<  std::endl;
    std::cout << "Binary representation: " << std::bitset<32>(color >> 8) << "\n" << std::endl;
    std::cout << "Red: " << ((color) & 0xFF) <<  std::endl;
    std::cout << "Binary representation: " << std::bitset<32>(color) << std::endl;
    return 0;
}