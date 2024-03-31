#include <cmath>

class NonLinearArithmetic
{
public:
    static int square(int number);
    static int cube(int number);
};

int NonLinearArithmetic::square(int number)
{
    return number * number;
}

int NonLinearArithmetic::cube(int number)
{
    return number * number * number;
}

int main()
{
    NonLinearArithmetic NLA;

    int x;
    int y;
    int z;

    int result = NLA.cube(x);
    int result2 = NLA.square(x);

    return 0;
}
