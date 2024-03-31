
int main() {
    int x;
    int y;

    klee_assume(x > 0);
    klee_assume(y >= 0);
    klee_assume(x + y == 10);
    klee_assume(x + y == -5);  // Introducing conflicting constraint


    if (x > 5) {
        if (y < 5) {
            if (x + y == 15) {  // Unreachable constraint due to conflict
                return 1;
            }
        }
    }

    return 0;
}
