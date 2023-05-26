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
#define back_contact_pin 14
#define front_contact_pin 15
const int dirPin = 2;
const int stepPin = 3;
const byte mechanical_stop_pin = 21; // Mechanical stop switch
// const int steps_per_rev = 200; // Steps per revolution
int speed = 0;         // The speed variable used to set stuff - there are 2 variables because this allows the motor to remember the speed after reset
int const_speed = 200; // Steps per second

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance of a stepper motor
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

String input;
int no_steps = 0; // Variable to store the current number of steps
int total_steps = 0;       // Total number of steps issued - used in reset to turn the correct number of times backwards. In steps, so NOT revs
int backwards_stop_steps = 0; // Stores wherever the switch is upon reset at the back wall
int forwards_stop_steps = 0; // Stores wherever the switch is upon reset at the front wall
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

unsigned int timeout_val = 5000; // Timer value = 0.5 seconds (10 kHz interrupt)
unsigned int timeout_counter = 0; // Counter for 0.5 seconds
boolean start_timer_flush = 0; // Start timer flag
uint8_t temp_buffer[4]; // Temporary buffer for reading serial data to clear erroneous stuff

boolean backwards_stop_flag = 0;
boolean forwards_stop_flag = 0;
boolean current_direction = 1; // 0 = left, 1 = right
boolean master_stop_flag = 0;
boolean back_detected = 0;
boolean front_detected = 0;

void setup()
{
  pinMode(dirPin, OUTPUT); // Direction pin for stepper motor
  myStepper.setMaxSpeed(1000); // Set the maximum speed of the stepper
  Serial1.begin(230400); // Start Serial1 UART
  myStepper.setSpeed(0); // Set the initial speed of the stepper to 0
  Serial1.flush(); // Flush the UART terminal for extra safety
  pinMode(LED_BUILTIN, OUTPUT); // Setup for built in LED on board
  pinMode(7, OUTPUT); // GP/IO for RDYE and EDYE
  pinMode(10, OUTPUT); // If it receives the RIGHT commands (reads the identifier)
  pinMode(12, OUTPUT); // If the serial buffer flushes
  pinMode(13, OUTPUT); // If it receives ANYTHING
  pinMode(back_contact_pin, INPUT); // Setup the back contact switch reading pin
  pinMode(front_contact_pin, INPUT); // Setup the front contact switch reading pin

  // Preliminary read, so that in the setup before any commands are called it cannot self-destruct (basically a forced interrupt)

  back_detected = digitalRead(back_contact_pin);
  front_detected = digitalRead(front_contact_pin);

  // If it has hit the back wall:
  if ((back_detected == 1) && (front_detected == 0)){
    // Stop it from going back any further
        backwards_stop_flag = 1;

        // Reset the stop point
        backwards_stop_steps = myStepper.currentPosition();

        // Set the total displacement to wherever it stopped
        total_steps = backwards_stop_steps;

        // Reset the moveto command so that it doesn't want to go over anymore
        myStepper.moveTo(total_steps);
        myStepper.setSpeed(0);
        
        // Stop the stepper's current run command immediately - next iteration it won't be called again
        myStepper.stop();
  }
  // If it has hit the front wall:
  else if ((front_detected == 1) && (back_detected == 0)){
    // Stop it from going forwards any further
    forwards_stop_flag = 1;

    // Reset the stop point
    forwards_stop_steps = myStepper.currentPosition();

    // Set the total displacement to wherever it stopped
    total_steps = forwards_stop_steps;

    // Reset the moveto command so that it doesn't want to go over anymore
    myStepper.moveTo(total_steps);
    myStepper.setSpeed(0);

    // Stop the stepper's current run command immediately - next iteration it won't be called again
    myStepper.stop();
  }
  // Otherwise, it is currently not hitting anything.
  else{

    // Reset the stop flags so that it is free to move in both directions again
    backwards_stop_flag = 0;
    forwards_stop_flag = 0;
  }

  // Mechanical stop interrupt
  pinMode(mechanical_stop_pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(mechanical_stop_pin), mechanical_stop, CHANGE); // Configure EXT1 with ISR record pulse to trigger

  cli(); // stop interrupts

  // set timer4 interrupt at 10kHz
  TCCR4A = 0; // set entire TCCR1A register to 0
  TCCR4B = 0; // same for TCCR1B
  TCNT4 = 0;  // initialize counter value to 0
  // set compare match register for 10kHz increments
  // OCR4A = 1599/1; // = (16*10^6) / (Prescaler*desired_freq) - 1 (must be <65536)
  OCR4A = 1599;// = (16*10^6) / (1*10000) - 1 (must be <65536)
  // turn on CTC mode
  TCCR4B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1 prescaler
  TCCR4B |= (1 << CS10);
  // enable timer compare interrupt
  TIMSK4 |= (1 << OCIE4A);

  sei(); // allow interrupts
}

// Function for reading data
void readData(uint8_t *data, int length)
{

  // Read data serially however many times specified
  for (int i = 0; i < length; i++)
  {
    data[i] = (uint8_t)Serial1.read();
  }
}

void mechanical_stop()
{

  // Read the state of the contact switches
  back_detected = digitalRead(back_contact_pin);
  front_detected = digitalRead(front_contact_pin);

  // If it has hit the back wall:
  if ((back_detected == 1) && (front_detected == 0)){
    
    // Stop it from going back any further
        backwards_stop_flag = 1;

        // Reset the stop point
        backwards_stop_steps = myStepper.currentPosition();

        // Set the total displacement to wherever it stopped
        total_steps = backwards_stop_steps;

        // Reset the moveto command so that it doesn't want to go over anymore
        myStepper.moveTo(total_steps);
        myStepper.setSpeed(0);
        
        // Stop the stepper's current run command immediately - next iteration it won't be called again
        myStepper.stop();
  }
  // If it has hit the front wall:
  else if ((front_detected == 1) && (back_detected == 0)){
    // Stop it from going forwards any further
    forwards_stop_flag = 1;

    digitalWrite(7, LOW); // GP/IO low to siginify the end of dye injection

    // Reset the stop point
    forwards_stop_steps = myStepper.currentPosition();

    // Set the total displacement to wherever it stopped
    total_steps = forwards_stop_steps;

    // Reset the moveto command so that it doesn't want to go over anymore
    myStepper.moveTo(total_steps);
    myStepper.setSpeed(0);

    // Stop the stepper's current run command immediately - next iteration it won't be called again
    myStepper.stop();
  }
  // Otherwise, it is currently not hitting anything.
  else{

    // Reset the stop flags so that it is free to move in both directions again
    backwards_stop_flag = 0;
    forwards_stop_flag = 0;
  }
  
}


// Interrupt service routine (ISR) for timer4
ISR(TIMER4_COMPA_vect)
{ // timer4 interrupt 10 kHz

  // If the buffer flush flag is triggered:
  if (start_timer_flush == 1){

    // Increment the counter
    timeout_counter++;
  }

  // Below is the main code for pulsing:

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

  // Code to detect random voltage spikes as UART
  // If there is between 1 and 3 bits in the serial buffer:
  if ((Serial1.available() < max_bytes) && ((Serial1.available() > 0))){

    // If the timer for the flush hasn't been triggered yet:
    if (start_timer_flush == 0){

      //Start timing
      start_timer_flush = 1;
    }

    // If it has been triggered:
    else{

      // If the timeout counter has been reached:
      if (timeout_counter >= timeout_val){
        
        // Debug pin - shows that memory has been reset
        digitalWrite(12, HIGH);
        delay(100);
        digitalWrite(12, LOW);
        
        // Read this junk data into the buffer - does nothing other than force clear the buffer
        readData(temp_buffer, (int)Serial1.available());

        // Just in case, clear the UART buffer (this is not what clears it apparently)
        Serial1.flush();

        // Reset the flush counters
        start_timer_flush = 0;
        timeout_counter = 0;
      }
    }
    
    
  }

  // If it receives something from the serial port (which is 4 long or above):
  if (Serial1.available() >= max_bytes)
  {

    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);

    // Read data into the buffer - only 4 long (max_bytes = 4)
    readData(receivedData, max_bytes);

    current_direction = 1; // By default it is going forwards

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

        digitalWrite(10, HIGH);
        delay(100);
        digitalWrite(10, LOW);

        pulse = 0;
      }
      // If pulse mode requested:
      else if (receivedData[1] == 'p')
      {

        digitalWrite(10, HIGH);
        delay(100);
        digitalWrite(10, LOW);

        // Calculate off-time:
        // On time in ms = period in seconds * duty * ticks/second = ticks

        on_period_counter = round(period * duty * clock_freq);
        off_period_counter = round(period * (1 - duty) * clock_freq);

        current_counter = 0;

        on_off = 1;

        // Enable pulse mode
        pulse = 1;
      }

      digitalWrite(7, HIGH); // GP/IO high to siginify the start of dye injection

    }
    else if (receivedData[0] == TestCommand)
    {
      // digitalWrite(10, HIGH);
      // delay(100);
      // digitalWrite(10, LOW);
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
    // If the EDYE command is called:
    else if (receivedData[0] == EDYECommand)
    {
      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW);

      digitalWrite(7, LOW); // GP/IO low to siginify the end of dye injection

      // Disable pulse mode
      pulse = 0;

      // Max speed backwards
      speed = -800;

      // Reset all of the step variables - we go extra far back so that the master stop switch can be hit

      total_steps = backwards_stop_steps - 20000;
      no_steps = 0;

      // Store the current direction as backwards
      current_direction = 0;
    }
    else{
        Serial1.flush();
        speed = 0;
    }

    start_timer_flush = 0;
    timeout_counter = 0;

  }

  // Start of testing code

  // digitalWrite(11, HIGH);
  // delay(1000);
  // digitalWrite(11, LOW);
  
  // on_period_counter = round(period * duty * (float)clock_freq);
  // off_period_counter = round(period * (1 - duty) * (float)clock_freq);

  // pulse = 1;
  // speed = const_speed;
  // total_steps = 200;

  // End of testing code

  // The total number of steps gets incremented by the number of steps requested
  total_steps = total_steps + no_steps;
  no_steps = 0;

  if (master_stop_flag == 0){
    
    // If it has been commanded to spin forwards:
    if (speed > 0){
      
      // If it is allowed to spin forwards:
      if (forwards_stop_flag == 0){

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
        if (abs(myStepper.distanceToGo()) == 0){
          digitalWrite(7, LOW); // GP/IO low to siginify the end of dye injection
        }    
      }
      // If it is not allowed to spin:
      else{

        // Stop spinning
        myStepper.setSpeed(0);
        myStepper.stop();
      }
    }
    // If it has been commanded to spin backwards
    else if (speed < 0){
      
      // If it is allowed to spin backwards:
      if (backwards_stop_flag == 0){

        // Tell the stepper to move to that place
        myStepper.moveTo(total_steps);
        
        // If the stepper hasn't reached there yet, and is not on pulse mode:
        if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 0))
        {

          // Set the speed to what we want and keep running
          myStepper.setSpeed(speed);
          myStepper.run();
        }
      }
      // If it is not allowed to spin:
      else{

        // Stop spinning
        myStepper.setSpeed(0);
        myStepper.stop();
      }
    }
    // If it has been commanded to stop (speed == 0):
    else{
      myStepper.setSpeed(speed);
      myStepper.stop();
    }
      
  }
  // If master stop:
  else{
    myStepper.setSpeed(0);
        myStepper.stop();
  }
 
}