#include <klee/klee.h>
#include <stdio.h>

int main() {
    int choice;
    int possibly_zero;

    switch (choice) {
        case 1:
            printf("You chose option 1.\n");
            break;
        case 2: {
            int result = 10 / possibly_zero; // Division by zero
            printf("You chose option 2.\n");
            break;
        }
        case 3:
            printf("You chose option 3.\n");
            break;
        default:
            printf("Invalid choice. Please select an option between 1 and 3.\n");
            break;
    }

    return 0;
}
