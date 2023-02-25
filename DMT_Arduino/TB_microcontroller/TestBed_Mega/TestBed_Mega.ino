const int max_bytes = 10; // Max length for Arduino communication protocol 

// Hex Identifiers
int STBCommand = 0b00000001; // STB Command - Info for Testbed actuators, stabilising delay, temperatures, length of experiment
int STB1Command = 0b0001111; // STB1 Command - Info for Dye Injection Microcontroller, runs SDYE
int RTBCommand = 0b00000111; // RTB Command - Iteratively receives actuator input data from PC 
int ETB1Command = 0b00001001; // ETB1 Command - Sends GP/IO to Raspberry Pi, signalling end of transient conditions
int ETB2Command = 0b00001010; // ETB2 Command - Tells Testbed actuators to stop the flow

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t

// Initialises UART, with baud rate of 230400
void setup()
{
  Serial.begin(230400);  // Initialize Central PC Serial communication
  Serial1.begin(230400); // Initialise Dye Injection Serial Communication
}

// Realises messages from UART, byte by byte 
void readData(uint8_t *data, int length)
{
  for (int i = 0; i < length; i++)
  {
    data[i] = (uint8_t)Serial.read();
  }
}

// Main loop function 
void loop()
{

  delay(10); // Short delay to ensure that data is being read

  if (Serial.available() >= max_bytes)
  {
    readData(receivedData, max_bytes);
    if (receivedData[0] == STBCommand)
    {
      Serial.write("STB");
    }
    if (receivedData[0] == STB1Command)
    {
      Serial.write("STB1");
    }
    else if (receivedData[0] == RTBCommand)
    {
      Serial.write("RTB");
    }
    else if (receivedData[0] == ETB1Command)
    {
      Serial.write("ETB1");
    }
    else if (receivedData[0] == ETB2Command)
    {
      Serial.write("ETB2");
    }
  }

  memset(receivedData, 0, sizeof(receivedData)); // Resets recievedData array after command has been read

}