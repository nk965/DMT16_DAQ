const int max_bytes = 4; // Max length for Arduino communication protocol

// Hex Identifiers
int ITBCommand = 0b00010100;
int STBCommand = 0b00000001; // STB Command - Info for Testbed actuators, stabilising delay, temperatures, length of experiment
int STB2Command = 0b00010001;
int IDYECommand = 0b00010101;
int IDYE2Command = 0b00010011;
int IDYE3Command = 0b00011000;
int RTBCommand = 0b00000111;  // RTB Command - Iteratively receives actuator input data from PC
int ETB1Command = 0b00001001; // ETB1 Command - Sends GP/IO to Raspberry Pi, signalling end of transient conditions
int ETB2Command = 0b00001010; // ETB2 Command - Tells Testbed actuators to stop the flow, resets Dye Injection system
int TestCommand = 0b1101001;

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t
uint8_t SDYEmessage[max_bytes];
uint8_t SDYE2message[max_bytes];
uint8_t RDYEmessage[max_bytes];
uint8_t EDYEmessage[max_bytes];

// Initialises UART, with baud rate of 230400
void setup()
{
  Serial.begin(230400);  // Initialize Central PC Serial communication
  Serial1.begin(230400); // Initialise Dye Injection Serial Communication
  pinMode(10, OUTPUT);   // Initialize GPIO Output Pin for start and end of Transient Experiment
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

void sendMega(uint8_t *data, int dataSize)
{
  for (int i = 0; i < dataSize; i++)
  {
    Serial1.write(data[i]);
  }
}

// Main loop function
void loop()
{

  if (Serial.available() >= max_bytes)
  {
    readData(receivedData, max_bytes);
    if (receivedData[0] == STBCommand)
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == ITBCommand)
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == TestCommand)
    {
      digitalWrite(10, HIGH);
      delay(100);
      digitalWrite(10, LOW); 

      sendData(receivedData, max_bytes); // Debugging print
      
      delay(2500);

      sendMega(receivedData, max_bytes); // Sends to Arduino Mega
    }
    else if (receivedData[0] == STB2Command)
    { 
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == IDYECommand)
    {
      sendData(receivedData, max_bytes); // Debugging print

      SDYEmessage[0] = 0b00000010;
      SDYEmessage[1] = receivedData[1]; // (MSB) Speed in steps per second
      SDYEmessage[2] = receivedData[2]; // Speed in steps per second
      SDYEmessage[3] = receivedData[3]; // Padding

      sendMega(SDYEmessage, max_bytes);
    }
    else if (receivedData[0] == IDYE2Command)
    {      
      sendData(receivedData, max_bytes);

      SDYE2message[0] = 0b00010110;
      SDYE2message[1] = receivedData[1]; // Duty Cycle
      SDYE2message[2] = receivedData[2]; // (MSB) of Period
      SDYE2message[3] = receivedData[3]; // Period

      sendMega(SDYE2message, max_bytes);
    }
    else if (receivedData[0] == IDYE3Command)
    {

      sendData(receivedData, max_bytes);

      RDYEmessage[0] = 0b00001000;
      RDYEmessage[1] = receivedData[1]; // Enable Pulse Mode
      RDYEmessage[2] = receivedData[2]; // (MSB) of Steps
      RDYEmessage[3] = receivedData[3]; // Steps

      // digitalWrite(10, HIGH);  GP/IO - Jimmy to configure correct pin

      sendMega(RDYEmessage, max_bytes);
    }
    else if (receivedData[0] == RTBCommand) // RTB - 2 byte has actuator position, first iteration sends RDYE
    {
      // if (receivedData[2] == 0b00000000)
      // {
      //   digitalWrite(10, HIGH);
      // }
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == ETB1Command) // ETB1 - sending GP/IO at end of experiment
    {
      // digitalWrite(10, LOW);             // Send GP/IO at end of experiment
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

      // digitalWrite(10, LOW);  GP/IO - Jimmy to configure correct pin

      sendMega(EDYEmessage, max_bytes);
    }
  }
}