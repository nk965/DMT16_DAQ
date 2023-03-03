// Include the AccelStepper Library
#include <AccelStepper.h>
#include <string.h>

const int max_bytes = 4;
uint8_t receivedData[max_bytes];
int RDYECommand = 0b00001000;
int SDYECommand = 0b00000010;
int SDYE2Command = 0b00010110;
int EDYECommand = 0b00010111;
int TestCommand = 0b1101001;

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;
// const int steps_per_rev = 200; // Steps per revolution
int speed = 0;         // The speed variable used to set stuff - there are 2 variables because this allows the motor to remember the speed after reset
int const_speed = 200; // Steps per second

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance of a stepper motor
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

String input;
unsigned int no_steps = 0; // Variable to store the current number of steps
unsigned int total_steps = 0;       // Total number of steps issued - used in reset to turn the correct number of times backwards. In steps, so NOT revs
float turn_counter;    // Turn counter - in REVS NOT STEPS
float duty = 0.2;      // Duty cycle value
float period = 0.25;    // Period of pulses - max period is around 9 seconds and a bit
boolean pulse = 0;     // Pulse mode: 1 = enabled, 0 = disabled
boolean on_off = 0;    // During pulse mode: on = 1 (pulsing), off = 0 (stop)
boolean toggle4 = LOW;
// Pulse variables

unsigned int on_period_counter = 0;  // Max counter val for on period before switch
unsigned int off_period_counter = 0; // Max counter val for off period before switch
unsigned int current_counter = 0;    // Current value of counter - incremented by timer
unsigned int clock_freq = 10000;     // 10 kHz interrupt

unsigned int timeout_val = 5000;
unsigned int timeout_counter = 0;
boolean start_timer_flush = 0;
uint8_t temp_buffer[4];

void setup()
{
  pinMode(dirPin, OUTPUT);
  myStepper.setMaxSpeed(1000);
  Serial1.begin(230400);
  myStepper.setSpeed(0);
  Serial1.flush();
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(10, OUTPUT); // If it receives the RIGHT commands (reads the identifier)
  pinMode(12, OUTPUT); // If the serial buffer flushes
  pinMode(13, OUTPUT); // If it receives ANYTHING


  cli(); // stop interrupts

  // set timer4 interrupt at 10kHz
  TCCR4A = 0; // set entire TCCR1A register to 0
  TCCR4B = 0; // same for TCCR1B
  TCNT4 = 0;  // initialize counter value to 0
  // set compare match register for 10kHz increments
  // OCR4A = 1599/1; // = (16*10^6) / (Prescaler*desired_freq) - 1 (must be <65536)
  OCR4A = 1599;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR4B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1 prescaler
  TCCR4B |= (1 << CS10);
  // enable timer compare interrupt
  TIMSK4 |= (1 << OCIE4A);

  sei(); // allow interrupts
}

void readData(uint8_t *data, int length)
{

  // digitalWrite(10, HIGH);
  // delay(2500);
  // digitalWrite(10, LOW); 

  for (int i = 0; i < length; i++)
  {
    data[i] = (uint8_t)Serial1.read();
  }
}

ISR(TIMER4_COMPA_vect)
{ // timer1 interrupt 10 kHz

  if (start_timer_flush == 1){
    timeout_counter++;
  }
  // If pulse mode:
  if (pulse == 1)
  {

    // If motor is in on duty:

    if (on_off)
    {

      // digitalWrite(10, HIGH);
      // If the on period has not been reached:
      if (current_counter <= on_period_counter)
      {

        // Keep counting
        current_counter++;
      }
      else
      {
        // If period has been reached, switch to off period
        on_off = 0;
        current_counter = 0;
      }
    }

    // If not on, then must be off:
    else
    {

      // If the off period has not been reached:
      if (current_counter <= off_period_counter)
      {

        // Keep counting
        current_counter++;
      }
      else
      {
        // If period has been reached, switch to off period
        on_off = 1;
        current_counter = 0;
      }
    }
  }
}

void loop()
{

  // If it receives something from the serial port (which is 4 long or above):
  if ((Serial1.available() < max_bytes) && ((Serial1.available() > 0))){
    if (start_timer_flush == 0){
      start_timer_flush = 1;
    }
    else{
      if (timeout_counter >= timeout_val){

        digitalWrite(12, HIGH);
        delay(100);
        digitalWrite(12, LOW);
        
        readData(temp_buffer, (int)Serial1.available());
        
        Serial1.flush();
        start_timer_flush = 0;
        timeout_counter = 0;
      }
    }
    
    
  }

  if (Serial1.available() >= max_bytes)
  {

    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);

    // Read data into the buffer - only 4 long (max_bytes = 4)
    readData(receivedData, max_bytes);

    // If the command is RDYE:
    if (receivedData[0] == RDYECommand)
    {

      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);

      // Extract the number of steps we have inputted from 2 bytes
      no_steps = (((unsigned int)receivedData[2] << 8) | ((unsigned int)receivedData[3]));

      // Set the speed to be whatever it currently is
      speed = const_speed;

      // If turn mode:
      if (receivedData[1] == 't')
      {
        // Disable pulse mode

        // digitalWrite(10, HIGH);
        // delay(100);
        // digitalWrite(10, LOW);

        pulse = 0;
      }
      // If pulse mode requested:
      else if (receivedData[1] == 'p')
      {

        // digitalWrite(10, HIGH);
        // delay(100);
        // digitalWrite(10, LOW);

        // Calculate off-time:
        // On time in ms = period in seconds * duty * ticks/second = ticks

        on_period_counter = round(period * duty * clock_freq);
        off_period_counter = round(period * (1 - duty) * clock_freq);

        current_counter = 0;

        on_off = 1;

        // Enable pulse mode
        pulse = 1;
      }
    }
    else if (receivedData[0] == TestCommand)
    {
      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);
    }
    // If the SDYE command is called:
    else if (receivedData[0] == SDYECommand)
    {

      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);

      // Extract the speed we have inputted from 2 bytes
      const_speed = (unsigned int)(((unsigned int)receivedData[1] << 8) | ((unsigned int)receivedData[2]));
    }
    // If the SDYE2 command is called:
    else if (receivedData[0] == SDYE2Command)
    {

      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);

      // Extract the duty value
      duty = (float)receivedData[1] / ((float)255);

      // Extract the period we have inputted from 2 bytes
      period = (float)(((unsigned int)receivedData[2] << 8) | ((unsigned int)receivedData[3]))/float(100);
    }
    // If the EDYE command is called::
    else if (receivedData[0] == EDYECommand)
    {
      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);

      // digitalWrite(10, HIGH);
      // delay(500);
      // digitalWrite(10, LOW);

      // Disable pulse mode
      pulse = 0;

      // Max speed backwards
      speed = -800;

      // Reset all of the step variables
      total_steps = 0;
      no_steps = 0;
    }
    else{
        Serial1.flush();
    }

    start_timer_flush = 0;
    timeout_counter = 0;

  }

  // Testing code

  // digitalWrite(11, HIGH);
  // delay(1000);
  // digitalWrite(11, LOW);
  
  // on_period_counter = round(period * duty * (float)clock_freq);
  // off_period_counter = round(period * (1 - duty) * (float)clock_freq);

  // pulse = 1;
  // speed = const_speed;
  // total_steps = 200;

  // The total number of steps gets incremented by the number of steps requested
  total_steps = total_steps + no_steps;
  no_steps = 0;

  // Tell the stepper to move to that place
  myStepper.moveTo(total_steps);

  // If the stepper hasn't reached there yet, and is not on pulse mode:
  if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 0))
  {

    // Set the speed to what we want and keep running
    myStepper.setSpeed(speed);
    myStepper.run();
  }
  // If the stepper hasn't reached there yet, and is on pulse mode:
  else if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 1))
  {

    // If the mode is on:
    if (on_off)
    {

      // Then turn the motor
      myStepper.setSpeed(speed);
      myStepper.run();
    }

    // If not, leave it alone
  }
}