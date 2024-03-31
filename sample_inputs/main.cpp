#include "calculator.h"
#include "math_functions.h"
#include "utils.h"
#include "data_structures.h"

int main() {
    Calculator calculator;
    MathFunctions mathFunctions;
    Utils utils;
    DataStructures dataStructures;

    int x = 10;
    int y = 5;
    int z = 2;

    int result1 = calculator.add(x, y);
    int result2 = calculator.subtract(x, y);
    int result3 = calculator.multiply(x, y);
    int result4 = calculator.divide(x, y);

    double powerResult = mathFunctions.power(x, z);

    bool isPrime = utils.isPrime(x);

    int maxValue = dataStructures.getMaxValue(x, y, z);
    int minValue = dataStructures.getMinValue(x, y, z);

    return 0;
}
