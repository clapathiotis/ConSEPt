#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// stack-buffer-overflow error
void print_elements(char array_param[6]){
  for (int i = 0; i <= 6; i++){
    std::cout << array_param[i] << std::endl;
  }
}

// use of uninitialized memory error
int uninit_value(int argc) {
  int* a = new int[10];
  a[5] = 0;

  if (a[argc])
    printf("xx\n");

  return 0;
}

// attempting free on memory that was not alloc error
int createAndFreeMemory(int a) {
    int *ptr = &a;
    free(ptr);
    std::cout << *ptr << " " << &ptr << std::endl;
    return 0;
}
