// Include the AccelStepper Library
#include <AccelStepper.h>
#include <string.h>

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;
const int step = 200;
int speed = 0;
int const_speed = 200;

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);
String input;
int no_steps;
int total_steps;
int step_counter;
float duty = 0.5;
float period = 1;
int pulse = 0;
int pulse_counter = 0;
float cycles_per_ms = 0.1395;
// float cycles_per_ms = 0.01;
int delay_cycles = 0;
int total_cycles = 0;

void setup()
{
  pinMode(dirPin, OUTPUT);
  myStepper.setMaxSpeed(1000);
  Serial.begin(9600);
  myStepper.setSpeed(0);
  Serial.flush();
}

void reset()
{
  myStepper.moveTo(0);
}

void loop()
{
  if (Serial.available())
  {
    input = Serial.readStringUntil('\n');
    if (input.substring(0, 5) == "turn ")
    {
      pulse = 0;
      no_steps = input.substring(5).toInt();
      speed = const_speed;
      step_counter = step_counter + no_steps;
    }
    else if (input == "reset")
    {
      pulse = 0;
      speed = -800;
      step_counter = 0;
    }
    else if (input.substring(0, 6) == "speed ")
    {
      const_speed = input.substring(6).toInt();
    }
    else if (input.substring(0, 5) == "duty ")
    {
      duty = input.substring(5).toFloat();
    }
    else if (input.substring(0, 7) == "period ")
    {
      period = input.substring(7).toFloat();
    }
    if (input.substring(0, 6) == "pulse ")
    {
      pulse = 1;
      // Serial.println(pulse);
      no_steps = input.substring(6).toInt();
      speed = const_speed;
      step_counter = step_counter + no_steps;
      delay_cycles = round(period * (duty)*cycles_per_ms * 1000);
      total_cycles = round(period * cycles_per_ms * 1000);
      // Serial.println(delay_cycles);
    }
  }

  total_steps = step * step_counter;
  myStepper.moveTo(total_steps);

  Serial.println(pulse_counter);

  if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 0))
  {
    myStepper.setSpeed(speed);
    myStepper.run();
  }
  else if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 1))
  {
    if (pulse_counter <= delay_cycles)
    {
      myStepper.setSpeed(speed);
      myStepper.run();
    }
    if (pulse_counter <= total_cycles)
    {
      pulse_counter = pulse_counter + 1;
    }
    else
    {
      pulse_counter = 0;
    }
  }
}