#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pigpio.h>

#define MAX_GPIO 32

int last[MAX_GPIO];
int cb[MAX_GPIO];
int py_data[MAX_GPIO+1][4];

// Defining Callback Function, GPIO = Pin No., level = state (1=HIGH, 0=LOW), tick = time (in us) since RPi bootup
void cbf(int gpio, int level, uint32_t tick)
{
   if (last[gpio] != -1) {
      int diff = tickDiff(last[gpio], tick); // Time difference (in us) between the current event change and the last change
      py_data[gpio][0] = gpio;
      py_data[gpio][1] = level;
      py_data[gpio][2] = tick;
      py_data[gpio][3] = diff;
      //printf("G=%d l=%d t=%d d=%d\n", GPIO, level, tick, diff);
   }
   last[gpio] = tick; // Resetting the new previous GPIO state and tick time
}

int main(int argc, char *argv[])
{
   int i, g, c, len;

   if (argc == 1) {
      len = MAX_GPIO;
      for (i = 0; i < MAX_GPIO; i++) {
         g = i;
         cb[i] = callback(g, EITHER_EDGE, cbf);
      }
   } else {
      len = argc - 1;
      for (i = 1; i < argc; i++) {
         g = atoi(argv[i]);
         cb[i-1] = callback(g, EITHER_EDGE, cbf);
      }
   }

   sleep(60);

   for (i = 0; i < len; i++) {
      cancel(cb[i]);
   }

   for (i = 0; i < len; i++) {
      for (c = 0; c < 4; c++) {
         printf("%d ", py_data[i][c]);
      }
      printf("\n");
   }

   return 0;
}