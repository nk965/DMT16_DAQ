// Include the AccelStepper Library
#include <AccelStepper.h>
#include <string.h>

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;
const int steps_per_rev = 200; // Steps per revolution
int speed = 0;
int const_speed = 200; // Steps per second

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
//float cycles_per_ms = 0.01;
int delay_cycles = 0;
int total_cycles = 0;
boolean toggle1 = 0;

void setup() {
  pinMode(dirPin, OUTPUT);
  myStepper.setMaxSpeed(1000);
  Serial.begin(9600);
  myStepper.setSpeed(0);
  Serial.flush();
  pinMode(13, OUTPUT);

  cli();//stop interrupts

  //set timer1 interrupt at 1Hz

  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 15624;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  sei();//allow interrupts

}

void reset(){
  myStepper.moveTo(0);
}

void loop() {

  // If it receives something from the serial port:

  if(Serial.available() > 0){

        // Wait until it sees an enter key
        input = Serial.readStringUntil('\n');

        Serial.write(input);

        // If the command is "turn", e.g. "turn 3":
        if (input.substring(0,5) == "turn "){

          // Disable pulse mode
          pulse = 0;

          // Record the demanded number of steps
          no_steps = input.substring(5).toInt();

          // Set the speed to be whatever it currently is
          speed = const_speed;

          // Add it to the total step count
          step_counter = step_counter + no_steps;
        }

        // If user wants to reset:
        else if (input == "reset"){

          // Disable pulse mode
          pulse = 0;

          // Max speed backwards
          speed = -800;

          // Reset the step counter - now we are back at square zero
          step_counter = 0;
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
          no_steps = input.substring(6).toInt();

          // Set the speed to whatever it was set to
          speed = const_speed;

          // Record the total steo count
          step_counter = step_counter + no_steps;

          // Calculate off-time:
          // On time in ms = period in s * duty
          // 
          delay_cycles = round(period*(duty)*cycles_per_ms*1000);
          total_cycles = round(period*cycles_per_ms*1000);
        }
    }

  // The total number of steps is the steps per revolution * number of revolutions
  total_steps = steps_per_rev*step_counter;

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

    // If the pulses are still less than the no. of pulses when the duty cycle is low:
    if (pulse_counter <= delay_cycles){

      // keep running
      myStepper.setSpeed(speed);
      myStepper.run();
    }

    // If the number of pulses in a period is still not met:
    if (pulse_counter <= total_cycles){
      
      // Keep incrementing
      pulse_counter = pulse_counter + 1;
    }

    // If it has overflowed:
    else {
      // Reset the pulse counter
     pulse_counter = 0;
    }
  }
  delay(1);
}

ISR(TIMER1_COMPA_vect){//timer1 interrupt 1Hz toggles pin 13 (LED)
//generates pulse wave of frequency 1Hz/2 = 0.5kHz (takes two cycles for full wave- toggle high then toggle low)
  if (toggle1){
    digitalWrite(13,HIGH);
    toggle1 = 0;
  }
  else{
    digitalWrite(13,LOW);
    toggle1 = 1;
  }
}
