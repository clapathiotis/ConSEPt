#include <iostream>
#include <string>

struct Person {
    std::string name;
    int age;
};

int main() {
    Person person;

    std::cout << "Enter name: ";
    std::getline(std::cin, person.name);

    std::cout << "Enter age: ";
    std::cin >> person.age;

    std::cout << "Entered information:" << std::endl;
    std::cout << "Name: " << person.name << std::endl;
    std::cout << "Age: " << person.age << std::endl;

    return 0;
}
