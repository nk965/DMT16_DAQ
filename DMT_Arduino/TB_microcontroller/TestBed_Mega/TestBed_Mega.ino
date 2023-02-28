const int max_bytes = 4; // Max length for Arduino communication protocol 

// Hex Identifiers
int STBCommand = 0b00000001; // STB Command - Info for Testbed actuators, stabilising delay, temperatures, length of experiment
int STB1Command = 0b00010101; // STB1 Command - Info for Dye Injection Microcontroller, runs SDYE
int RTBCommand = 0b00000111; // RTB Command - Iteratively receives actuator input data from PC 
int ETB1Command = 0b00001001; // ETB1 Command - Sends GP/IO to Raspberry Pi, signalling end of transient conditions
int ETB2Command = 0b00001010; // ETB2 Command - Tells Testbed actuators to stop the flow
int STB2Command = 0b00010001;
int STB3Command = 0b00010010;
int STB4Command = 0b00010011;
int ITBCommand = 0b00010100; 

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t

// Initialises UART, with baud rate of 230400
void setup()
{
  Serial.begin(9600);  // Initialize Central PC Serial communication
  Serial1.begin(9600); // Initialise Dye Injection Serial Communication
}

// Receives messages from UART, byte by byte 
void readData(uint8_t *data, int length)
{
  for (int i = 0; i < length; i++)
  {
    data[i] = (uint8_t)Serial.read();
  }
}

// Sends messages through UART
void sendData(uint8_t* data, int dataSize) {
  for (int i = 0; i < dataSize; i++) {
    Serial.write(data[i]);
  }
}

// Main loop function 
void loop()
{

  if (Serial.available() >= max_bytes)
  {
    readData(receivedData, max_bytes);
    if (receivedData[0] == ITBCommand)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == STBCommand)
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == STB2Command)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == STB1Command) // Sends SDYE (i.e., info for dye injection)
    {
      sendData(receivedData, max_bytes); // Debugging print

      // Send SDYE

    }
    else if (receivedData[0] == STB3Command)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == STB4Command)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == RTBCommand) // RTB - 2 byte has actuator position, first iteration sends RDYE
    {
      sendData(receivedData, max_bytes); // Debugging print

      // On first iteration, sends RDYE

    }
    else if (receivedData[0] == ETB1Command) // ETB1 - sending GP/IO at end of experiment
    {
      sendData(receivedData, max_bytes); // Debugging print

      // Send GP/IO at end of experiment

    }
    else if (receivedData[0] == ETB2Command) // ETB2 - tells Testbed to stop flowing
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
  }

}