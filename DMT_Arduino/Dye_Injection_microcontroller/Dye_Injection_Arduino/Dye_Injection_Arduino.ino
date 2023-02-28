// Include the AccelStepper Library
#include <AccelStepper.h>
#include <string.h>

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;
const int steps_per_rev = 200; // Steps per revolution
int speed = 0; // The speed variable used to set stuff - there are 2 variables because this allows the motor to remember the speed after reset
int const_speed = 200; // Steps per second

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance of a stepper motor
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

String input;
float no_turns; // Variable for storing the number of steps requested using turn or pulse command
int total_steps; // Total number of steps issued - used in reset to turn the correct number of times backwards. In steps, so NOT revs
float turn_counter; // Turn counter - in REVS NOT STEPS
float duty = 0.4; // Duty cycle value
float period = 0.5; // Period of pulses - max period is around 9 seconds and a bit
boolean pulse = 0; // Pulse mode: 1 = enabled, 0 = disabled
boolean on_off = 0; // During pulse mode: on = 1 (pulsing), off = 0 (stop)

// Pulse variables

unsigned int on_period_counter = 0; // Max counter val for on period before switch
unsigned int off_period_counter = 0; // Max counter val for off period before switch
unsigned int current_counter = 0; // Current value of counter - incremented by timer
unsigned int clock_freq = 10000; // 10 kHz interrupt


void setup() {
  pinMode(dirPin, OUTPUT);
  myStepper.setMaxSpeed(1000);
  Serial.begin(230400);
  myStepper.setSpeed(0);
  Serial.flush();
  pinMode(LED_BUILTIN, OUTPUT);

  cli();//stop interrupts

  //set timer1 interrupt at 10kHz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 10kHz increments
  OCR1A = 1599;// = (16*10^6) / (Prescaler*desired_freq) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1 prescaler
  TCCR1B |= (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  sei();//allow interrupts

}

void loop() {

  // If it receives something from the serial port:

  if(Serial.available() > 0){

        // Wait until it sees an enter key
        input = Serial.readStringUntil('\n');
        // Serial.write(input);

        // If the command is "turn", e.g. "turn 3":
        if (input.substring(0,5) == "turn "){

          // Disable pulse mode
          pulse = 0;

          // Record the demanded number of steps
          no_turns = input.substring(5).toFloat();

          // Set the speed to be whatever it currently is
          speed = const_speed;

          // Add it to the total step count
          turn_counter = turn_counter + no_turns;
        }

        // If user wants to reset:
        else if (input == "reset"){

          // Disable pulse mode
          pulse = 0;

          // Max speed backwards
          speed = -800;

          // Reset the step counter - now we are back at square zero
          turn_counter = 0;
        }

        // If input is the speed of the motor:
        else if (input.substring(0,6) == "speed "){

          // Set the speed to be whatever is inputted
          const_speed = input.substring(6).toInt();
        }

        // If the input is the duty cycle:
        else if (input.substring(0,5) == "duty "){

          // Extract anything after duty_ and turn into a float, then store the duty cycle
          duty = input.substring(5).toFloat();
        }

        // If the input is the period of the pulse:
        else if (input.substring(0,7) == "period "){

          // Store the period
          period = input.substring(7).toFloat();
        }

        // If pulse mode requested:
        if (input.substring(0,6) == "pulse "){

          // Enable pulse mode
          pulse = 1;

          // Extract the number of steps
          no_turns = input.substring(6).toFloat();

          // Set the speed to whatever it was set to
          speed = const_speed;

          // Record the total steo count
          turn_counter = turn_counter + no_turns;

          // Calculate off-time:
          // On time in ms = period in seconds * duty * ticks/second = ticks
          
          on_period_counter = round(period*duty*clock_freq);
          off_period_counter = round(period*(1-duty)*clock_freq);

          current_counter = 0;

          on_off = 1;
        }
    }

  // The total number of steps is the steps per revolution * number of revolutions
  total_steps = (int)round(steps_per_rev*turn_counter);

  // Tell the stepper to move to that place
  myStepper.moveTo(total_steps);

  // If the stepper hasn't reached there yet, and is not on pulse mode:
  if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 0)){

    // Set the speed to what we want and keep running
    myStepper.setSpeed(speed);
    myStepper.run();
  }
  // If the stepper hasn't reached there yet, and is on pulse mode:
  else if ((abs(myStepper.distanceToGo()) > 0) && (pulse == 1)){

    // If the mode is on:
    if (on_off){
    
      // Then turn the motor
      myStepper.setSpeed(speed);
      myStepper.run();      
    }

    // If not, leave it alone
  }

}
ISR(TIMER1_COMPA_vect){//timer1 interrupt 10 kHz

  // If pulse mode:
  if (pulse == 1){
    
    // If motor is in on duty:

    if (on_off){

      // If the on period has not been reached:
      if (current_counter <= on_period_counter){

        // Keep counting
        current_counter++;

      }
      else{

        // If period has been reached, switch to off period
        on_off = 0;
        current_counter = 0;
      }
    }

    // If not on, then must be off:
    else{
      // If the off period has not been reached:
      if (current_counter <= off_period_counter){

        // Keep counting
        current_counter++;

      }
      else{
        // If period has been reached, switch to off period
        on_off = 1;
        current_counter = 0;
      }
    }

  }
}