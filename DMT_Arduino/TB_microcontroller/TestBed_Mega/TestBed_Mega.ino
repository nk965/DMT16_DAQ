const int max_bytes = 4; // Max length for Arduino communication protocol

// Hex Identifiers - always at the first byte of each transmission
int ITBCommand = 0b00010100; // ITB Command - Initialises Testbed, contains stabilising delay 
int STBCommand = 0b00000001; // STB Command - Info for initial actuator position + time duration for transient experiment 
int STB2Command = 0b00010001; // STB2 Command - Info for branch temperature (for future application for temp closed loop control)
int IDYECommand = 0b00010101; // IDYE Command - Info for speed (steps/second)
int IDYE2Command = 0b00010011; // IDYE2 Command - Info for duty cycle, and cycle period  
int IDYE3Command = 0b00011000; // IDYE3 Command - Sends RDYE and starts dye injection, contains info: pulse mode + steps  
int RTBCommand = 0b00000111;  // RTB Command - Iteratively receives actuator input data from PC
int ETB1Command = 0b00001001; // ETB1 Command - 
int ETB2Command = 0b00001010; // ETB2 Command - Tells Testbed actuators to stop the flow, resets Dye Injection system (EDYE)

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t
uint8_t SDYEmessage[max_bytes]; // Sends info to dye injection microcontroller, (steps/second)
uint8_t SDYE2message[max_bytes]; // Sends info to dye injection microcontroller, (duty cycle, cycle period)
uint8_t RDYEmessage[max_bytes]; // Sends info to dye injection microcontroller, (starts, pulse mode + steps)
uint8_t EDYEmessage[max_bytes]; // Sends info to dye injection microcontroller, (resets dye injection)

// Initialises UART, with baud rate of 230400
void setup()
{
  Serial.begin(230400);  // Initialize Central PC Serial communication
  Serial1.begin(230400); // Initialise Dye Injection Serial Communication
  pinMode(10, OUTPUT);   // Debug Send LED
  pinMode(13, OUTPUT); // Initialize GPIO Output Pin for start and end of Transient Experiment (first and end RTB)
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

      SDYEmessage[0] = 0b00000010; // assign new hex identifier for SDYE
      SDYEmessage[1] = receivedData[1]; // (MSB) Speed in steps per second
      SDYEmessage[2] = receivedData[2]; // Speed in steps per second
      SDYEmessage[3] = receivedData[3]; // Padding

      sendMega(SDYEmessage, max_bytes); // sends SDYE to Dye Injection Microcontroller
    }
    else if (receivedData[0] == IDYE2Command)
    {      
      sendData(receivedData, max_bytes);

      SDYE2message[0] = 0b00010110; // assign new hex identifier for SDYE2
      SDYE2message[1] = receivedData[1]; // Duty Cycle
      SDYE2message[2] = receivedData[2]; // (MSB) of Period
      SDYE2message[3] = receivedData[3]; // Period

      sendMega(SDYE2message, max_bytes); // sends SDYE2 to Dye Injection Microcontroller
    }
    else if (receivedData[0] == IDYE3Command)
    {

      sendData(receivedData, max_bytes);

      RDYEmessage[0] = 0b00001000; // assign new hex identifier for RDYE
      RDYEmessage[1] = receivedData[1]; // Enable Pulse Mode
      RDYEmessage[2] = receivedData[2]; // (MSB) of Steps
      RDYEmessage[3] = receivedData[3]; // Steps

      sendMega(RDYEmessage, max_bytes); // sends RDYE to Dye Injection Microcontroller

    }
    else if (receivedData[0] == RTBCommand) // RTB - 2 byte has actuator position, first iteration sends RDYE
    {
      // If the padding is 00, then it is the first RTB command
      if (receivedData[3] == 0b00000000)
      {
        digitalWrite(13, HIGH);
      }
      // If the padding is 03, then it is the last RTB command
      else if (receivedData[3] == 0b00000011)
      {
        digitalWrite(13, LOW);
      }
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == ETB1Command)
    {
      sendData(receivedData, max_bytes); // Debugging print
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
}