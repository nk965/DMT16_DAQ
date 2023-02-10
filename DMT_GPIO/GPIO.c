#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pigpio.h>

#define NUM_PINS 32

int last[NUM_PINS];
int cb[NUM_PINS];
int py_data[NUM_PINS][4];
int num_entries = 1; // First row reserved for header

// Defining Callback Function, GPIO = Pin No., level = state (1=HIGH, 0=LOW), tick = time (in us) since RPi bootup
void cbf(int GPIO, int level, uint32_t tick)
{
if (last[GPIO] != -1)
{
int diff = tickDiff(last[GPIO], tick); // Time difference (in us) between the current event change and the last change
py_data[num_entries][0] = GPIO;
py_data[num_entries][1] = level;
py_data[num_entries][2] = tick;
py_data[num_entries][3] = diff;
//printf("G=%d l=%d t=%d d=%d\n", GPIO, level, tick, diff);
}
last[GPIO] = tick; // Resetting the new previous GPIO state and tick time
num_entries++;
}

int main(int argc, char *argv[])
{
int num_g;
int *G;

if (argc == 1)
{
num_g = NUM_PINS;
G = (int *)malloc(num_g * sizeof(int));
for (int i = 0; i < NUM_PINS; i++)
G[i] = i;
}
else
{
num_g = argc - 1;
G = (int *)malloc(num_g * sizeof(int));
for (int i = 1; i < argc; i++)
G[i - 1] = atoi(argv[i]);
}

if (gpioInitialise() < 0)
{
printf("Failed to connect to pigpio\n");
return 1;
}

for (int i = 0; i < NUM_PINS; i++)
last[i] = -1;

for (int i = 0; i < num_g; i++)
cb[i] = gpioSetAlertFunc(G[i], cbf);

// Closing Procedure
int loop = 1;
while (loop)
{
sleep(60);
}

printf("Tidying up\n");
for (int i = 0; i < num_entries; i++)
printf("%d %d %d %d\n", py_data[i][0], py_data[i][1], py_data[i][2], py_data[i][3]);
for (int i = 0; i < num_g; i++)
gpioSetAlertFunc(G[i], NULL);

gpioTerminate();

return 0