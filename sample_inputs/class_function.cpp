#include <iostream>

// Function that accepts any numerical value
template <typename T>
void printValue(T value) {
    value;
}

// Class that accepts any numerical value
template <typename T>
class Number {
private:
    T value;

public:
    Number(T initialValue) : value(initialValue) {}

    void setValue(T newValue) {
        value = newValue;
    }

    T getValue() const {
        return value;
    }
};

int main() {
    // Test the function with different numerical types
    printValue(10);
    printValue(3.14);
    printValue('A');

    // Test the class with different numerical types
    Number<int> intNumber(5);
    intNumber.getValue();

    Number<double> doubleNumber(3.14);
    doubleNumber.getValue();

    Number<char> charNumber('B');
    charNumber.getValue();

    return 0;
}
