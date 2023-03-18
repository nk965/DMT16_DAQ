#include <AccelStepper.h>

const int max_bytes = 4; // Max length for Arduino communication protocol

// Hex Identifiers - always at the first byte of each transmission
int ITBCommand = 0b00010100;   // ITB Command - Initialises Testbed, contains stabilising delay
int STBCommand = 0b00000001;   // STB Command - Info for initial actuator position + time duration for transient experiment
int STB2Command = 0b00010001;  // STB2 Command - Info for branch temperature (for future application for temp closed loop control)
int IDYECommand = 0b00010101;  // IDYE Command - Info for speed (steps/second)
int IDYE2Command = 0b00010011; // IDYE2 Command - Info for duty cycle, and cycle period
int IDYE3Command = 0b00011000; // IDYE3 Command - Sends RDYE and starts dye injection, contains info: pulse mode + steps
int RTBCommand = 0b00000111;   // RTB Command - Iteratively receives actuator input data from PC
int ETB1Command = 0b00001001;  // ETB1 Command -
int ETB2Command = 0b00001010;  // ETB2 Command - Tells Testbed actuators to stop the flow, resets Dye Injection system (EDYE)

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t
uint8_t SDYEmessage[max_bytes];  // Sends info to dye injection microcontroller, (steps/second)
uint8_t SDYE2message[max_bytes]; // Sends info to dye injection microcontroller, (duty cycle, cycle period)
uint8_t RDYEmessage[max_bytes];  // Sends info to dye injection microcontroller, (starts, pulse mode + steps)
uint8_t EDYEmessage[max_bytes];  // Sends info to dye injection microcontroller, (resets dye injection)

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;
const byte interruptPin = 20;        // Pin change interrupt pin
const byte mechanical_stop_pin = 21; // Mechanical stop switch

// Other variables
const int steps_per_rev = 200;       // Steps per revolution
const unsigned int timer_speed = 10; // 5 Hz timer
const int motor_speed = 1000;
double measured_speed = 0;  // The speed measured (Y)
double after_PID_speed = 0; // K(U-Y) in the control system
double current_total_steps = 0;
double next_total_steps = 0;
double error = 0;          // E = U-Y in control system
long current_distance = 0; // Current position of the motor

// Converter for RTB User Inputs
union
{
  unsigned char bytes[8]; // Assumes a big-endian system
  double value;
} converter;

double requested_speed = 0; // U in the control system (mL/s)

// PID Characteristics
double PID_input_buffer[3] = {0, 0, 0};  // Buffer for bilinear multistep transfer function
double PID_output_buffer[3] = {0, 0, 0}; // Output buffer
double Kp = 2;
double Ki = 0;
double Kd = 0;

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance of a stepper motor
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

// Initialises UART, with baud rate of 230400
void setup()
{
  pinMode(dirPin, OUTPUT);     // Direction pin for stepper motor
  myStepper.setMaxSpeed(2000); // Set the maximum speed of the stepper
  myStepper.setSpeed(0);       // Set the initial speed of the stepper to 0
  myStepper.moveTo(0);

  Serial.begin(230400);  // Initialize Central PC Serial communication
  Serial1.begin(230400); // Initialise Dye Injection Serial Communication
  pinMode(10, OUTPUT);   // Debug Send LED
  pinMode(13, OUTPUT);   // Initialize GPIO Output Pin for start and end of Transient Experiment (first and end RTB)

  pinMode(interruptPin, INPUT_PULLUP);                                        // Configure pin 20 to be an interrupt pin
  attachInterrupt(digitalPinToInterrupt(interruptPin), record_pulse, CHANGE); // Configure EXT1 with ISR record pulse to trigger upon pin change
  pinMode(mechanical_stop_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(mechanical_stop_pin), mechanical_stop, CHANGE); // Configure EXT1 with ISR record pulse to trigger

  cli(); // stop interrupts

  // set timer4 interrupt at 5 Hz
  TCCR4A = 0; // set entire TCCR1A register to 0
  TCCR4B = 0; // same for TCCR1B
  TCNT4 = 0;  // initialize counter value to 0
  // set compare match register for 1kHz increments
  OCR4A = 24999; // = (16*10^6) / (5*64) - 1 (must be <65536)
  // turn on CTC mode
  TCCR4B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1 prescaler
  TCCR4B |= (1 << CS11) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK4 |= (1 << OCIE4A);

  sei(); // allow interrupts
}

// Flags and globals for interrupts
boolean time_start = 0;
unsigned int sensor_pulse_counter = 0;
boolean calculate_PID_vals = 1;
boolean stop_flag = 0;

// Triangular wave test code
int sign = 1;
int interval = 10;

// Interrupt service routine (ISR) for timer4
ISR(TIMER4_COMPA_vect)

{ // timer4 interrupt 5 Hz
  calculate_PID_vals = 1;
}

void record_pulse()
{
  sensor_pulse_counter++;
}

void mechanical_stop()
{
  stop_flag = !stop_flag;
}

// Receives messages from UART, byte by byte
void readData(uint8_t *data, int length)
{
  for (int i = 0; i < length; i++)
  {
    data[i] = (uint8_t)Serial.read();
  }
}

// Sends messages through UART to Central PC
void sendData(uint8_t *data, int dataSize)
{
  for (int i = 0; i < dataSize; i++)
  {
    Serial.write(data[i]);
  }
}

// Sends messages through UART to other Arduino Mega (Dye Injection Microcontroller)
void sendMega(uint8_t *data, int dataSize)
{

  for (int i = 0; i < dataSize; i++)
  {
    Serial1.write(data[i]);
  }

  // digitalWrite(10, HIGH);
  // delay(100);
  // digitalWrite(10, LOW);
}

// Main loop function
void loop()
{

  if (Serial.available() >= max_bytes) // checks if it gets sufficient message from Central PC
  {

    readData(receivedData, max_bytes); // reads data, and tries to decode what it is
    if (receivedData[0] == ITBCommand) // 2nd byte: stabilising delay
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == STBCommand) // 2nd byte: initial actuator input, 3rd + 4th byte: time duration
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == STB2Command) // 2nd byte: branch pipe temperature
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == IDYECommand) // 2nd + 3rd byte: speed
    {
      sendData(receivedData, max_bytes); // Debugging print

      SDYEmessage[0] = 0b00000010;      // assign new hex identifier for SDYE
      SDYEmessage[1] = receivedData[1]; // (MSB) Speed in steps per second
      SDYEmessage[2] = receivedData[2]; // Speed in steps per second
      SDYEmessage[3] = receivedData[3]; // Padding

      sendMega(SDYEmessage, max_bytes); // sends SDYE to Dye Injection Microcontroller
    }
    else if (receivedData[0] == IDYE2Command)
    {
      sendData(receivedData, max_bytes);

      SDYE2message[0] = 0b00010110;      // assign new hex identifier for SDYE2
      SDYE2message[1] = receivedData[1]; // Duty Cycle
      SDYE2message[2] = receivedData[2]; // (MSB) of Period
      SDYE2message[3] = receivedData[3]; // Period

      sendMega(SDYE2message, max_bytes); // sends SDYE2 to Dye Injection Microcontroller
    }
    else if (receivedData[0] == IDYE3Command)
    {

      sendData(receivedData, max_bytes);

      RDYEmessage[0] = 0b00001000;      // assign new hex identifier for RDYE
      RDYEmessage[1] = receivedData[1]; // Enable Pulse Mode
      RDYEmessage[2] = receivedData[2]; // (MSB) of Steps
      RDYEmessage[3] = receivedData[3]; // Steps

      sendMega(RDYEmessage, max_bytes); // sends RDYE to Dye Injection Microcontroller
    }
    else if (receivedData[0] == RTBCommand) // RTB - 2 byte has actuator position, first iteration sends RDYE
    {

      // Copy the two bytes of data into the last two bytes of the union
      converter.bytes[6] = receivedData[1];
      converter.bytes[7] = receivedData[2];

      // Set the remaining bytes of the union to 0 (assuming a big-endian system)
      converter.bytes[0] = converter.bytes[1] = converter.bytes[2] = converter.bytes[3] = converter.bytes[4] = converter.bytes[5] = 0;

      // requested_speed = converter.value;

      // Start of PID loop

      while (true)
      {

        if (calculate_PID_vals == 1)
        {

          sendData(receivedData, max_bytes);

          // requested_speed = 10;

          //     // Triangular wave test code

          if ((int)requested_speed > 199)
          {
            sign = -1;
          }
          else if ((int)requested_speed < -199)
          {
            sign = 1;
          }

          requested_speed = requested_speed + sign * interval;

          // Convert the pulse counts into a speed value (mL/s)
          measured_speed = ((double)sensor_pulse_counter * (double)timer_speed / (double)1530) * (double)(1000);

          sensor_pulse_counter = 0;

          // Work out the error to put into the PID controller
          error = requested_speed - measured_speed;

          // Update input buffer
          PID_input_buffer[0] = PID_input_buffer[1];
          PID_input_buffer[1] = PID_input_buffer[2];
          PID_input_buffer[2] = error;

          // Put it through a digital PID controller
          PID_output_buffer[0] = PID_output_buffer[1];
          PID_output_buffer[1] = PID_output_buffer[2];
          PID_output_buffer[2] = PID_output_buffer[0] +
                                 (Kp + Ki / (2 * (double)timer_speed) + 2 * Kd * (double)timer_speed) * PID_input_buffer[2] + (Ki / (double)timer_speed - 4 * Kd * (double)timer_speed) * PID_input_buffer[1] + (-Kp + Ki / (2 * (double)timer_speed) + 2 * Kd * (double)timer_speed) * PID_input_buffer[0];

          // The new volumetric flow rate is recorded:
          after_PID_speed = PID_output_buffer[2];

          // Update the current total motor displacement
          current_total_steps = next_total_steps; // 99

          // Calculate the motor displacement with a calibration number (think of it as Kp2)
          next_total_steps = (1 * after_PID_speed); // Calibration //100

          // Serial.println(myStepper.distanceToGo());

          // Reset the pulse timers and don't calculate the value again until the value is read
          calculate_PID_vals = 0;
        }

        // If the motor has not hit the mechanical switch:
        if (stop_flag == 0)
        {

          // Set the destination for the motor to move
          myStepper.moveTo((long)(next_total_steps));

          // Work out where the motor currently is
          current_distance = myStepper.currentPosition();

          // If it is going the wrong way:

          if (current_distance < (long)next_total_steps)
          {

            // Turn the other way

            myStepper.setSpeed(motor_speed);
            myStepper.run();
          }

          // Otherwise turn the other other way
          else if (current_distance > (long)next_total_steps)
          {

            myStepper.setSpeed(-motor_speed);
            myStepper.run();
          }
          else
          {

            // If it hs reached its destination then stop
            myStepper.setSpeed(0);
            myStepper.stop();
          }
        }
      }

      // If the padding is 00, LED is HIGH showing RTB command
      if (receivedData[3] == 0b00000000)
      {
        digitalWrite(13, HIGH);
      }
      // If the padding is 01, LED is LOW showing another RTB command
      else if (receivedData[3] == 0b00000001)
      {
        digitalWrite(13, LOW);
      }
      // sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == ETB1Command)
    {
      digitalWrite(13, LOW);
      sendData(receivedData, max_bytes); // Debugging print
      stop_flag = 0;
    }
    else if (receivedData[0] == ETB2Command) // ETB2 - tells Testbed to stop flowing
    {
      // Send ERPI (reset Dye Injection)
      sendData(receivedData, max_bytes); // Debugging print

      EDYEmessage[0] = 0b00010111;
      EDYEmessage[1] = 0b00000000;
      EDYEmessage[2] = 0b00000000;
      EDYEmessage[3] = 0b00000000;

      Serial1.flush();

      sendMega(EDYEmessage, max_bytes); // sends EDYE to Dye Injection Microcontroller
    }
  }

  if (calculate_PID_vals == 1)
  {

    // Convert the pulse counts into a speed value (mL/s)
    measured_speed = ((double)sensor_pulse_counter * (double)timer_speed / (double)1530) * (double)(1000);

    Serial.println(measured_speed);

    // Triangular wave test code

    // if ((int)requested_speed > 199){
    //   sign = -1;
    // }
    // else if ((int)requested_speed < -199){
    //   sign = 1;
    // }

    // requested_speed = requested_speed + sign*interval;

    sensor_pulse_counter = 0;

    // Work out the error to put into the PID controller
    error = requested_speed - measured_speed;

    // Update input buffer
    PID_input_buffer[0] = PID_input_buffer[1];
    PID_input_buffer[1] = PID_input_buffer[2];
    PID_input_buffer[2] = error;

    // Put it through a digital PID controller
    PID_output_buffer[0] = PID_output_buffer[1];
    PID_output_buffer[1] = PID_output_buffer[2];
    PID_output_buffer[2] = PID_output_buffer[0] +
                           (Kp + Ki / (2 * (double)timer_speed) + 2 * Kd * (double)timer_speed) * PID_input_buffer[2] + (Ki / (double)timer_speed - 4 * Kd * (double)timer_speed) * PID_input_buffer[1] + (-Kp + Ki / (2 * (double)timer_speed) + 2 * Kd * (double)timer_speed) * PID_input_buffer[0];

    // The new volumetric flow rate is recorded:
    after_PID_speed = PID_output_buffer[2];

    // Update the current total motor displacement
    current_total_steps = next_total_steps; // 99

    // Calculate the motor displacement with a calibration number (think of it as Kp2)
    next_total_steps = (1 * after_PID_speed); // Calibration //100

    // Serial.println(myStepper.distanceToGo());

    // Reset the pulse timers and don't calculate the value again until the value is read
    calculate_PID_vals = 0;
  }

  // If the motor has not hit the mechanical switch:
  if (stop_flag == 0)
  {

    // Set the destination for the motor to move
    myStepper.moveTo((long)(next_total_steps));

    // Work out where the motor currently is
    current_distance = myStepper.currentPosition();

    // If it is going the wrong way:

    if (current_distance < (long)next_total_steps)
    {

      // Turn the other way

      myStepper.setSpeed(motor_speed);
      myStepper.run();
    }

    // Otherwise turn the other other way
    else if (current_distance > (long)next_total_steps)
    {

      myStepper.setSpeed(-motor_speed);
      myStepper.run();
    }
    else
    {

      // If it hs reached its destination then stop
      myStepper.setSpeed(0);
      myStepper.stop();
    }
  }
}