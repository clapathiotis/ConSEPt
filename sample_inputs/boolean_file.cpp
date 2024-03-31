#include <iostream>

int main() {
    bool condition;

    std::cout << "Enter a boolean value (0 or 1): ";
    std::cin >> condition;

    if (condition) {
        std::cout << "Condition is true." << std::endl;
    } else {
        std::cout << "Condition is false." << std::endl;
    }

    return 0;
}
