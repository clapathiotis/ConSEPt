#include <stdio.h>
#include <klee/klee.h>

int get_sign(int x) {
  if (x == 0)
    return 0;

  if (x < 0)
    return -1;
  else
    return 1;
}

int main() {
  int x;
  int result = get_sign(x);
  printf("result = %d\n", result);
  return 1;
}