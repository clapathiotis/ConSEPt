#include "data_structures.h"

int DataStructures::getMaxValue(int a, int b, int c) {
    int maxVal = a;
    if (b > maxVal) {
        maxVal = b;
    }
    if (c > maxVal) {
        maxVal = c;
    }
    return maxVal;
}

int DataStructures::getMinValue(int a, int b, int c) {
    int minVal = a;
    if (b < minVal) {
        minVal = b;
    }
    if (c < minVal) {
        minVal = c;
    }
    return minVal;
}
