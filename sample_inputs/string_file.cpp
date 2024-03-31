#include <iostream>
#include <string>

int main() {
    std::string text;

    std::cout << "Enter a string: ";
    std::getline(std::cin, text);

    std::cout << "Entered text: " << text << std::endl;

    return 0;
}
