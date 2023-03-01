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
int TestCommand = 0b00110000;

uint8_t receivedData[max_bytes]; // Array of length largest number of bytes recieved, typecasted to uint8_t
uint8_t message[max_bytes]; // Array of length largest number of bytes to be sent to Mega

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
    digitalWrite(10, HIGH);
    delay(100);
    digitalWrite(10, LOW);
  }
}

void sendMega(uint8_t *data, int dataSize)
{
  for (int i = 0; i < dataSize; i++)
  { 
    Serial1.write(data[i]);
    digitalWrite(10, HIGH);
    delay(100);
    digitalWrite(10, LOW);
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
    else if (receivedData[0] == TestCommand)
    {
      sendData(receivedData, max_bytes); // Debugging print
      delay(100);
      digitalWrite(10, LOW);
      sendMega(receivedData, max_bytes); // Sends to Arduino Mega
    }
    else if (receivedData[0] == STB2Command)
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == IDYECommand)
    {
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == IDYE2Command)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == IDYE3Command)
    {
      sendData(receivedData, max_bytes);
    }
    else if (receivedData[0] == RTBCommand) // RTB - 2 byte has actuator position, first iteration sends RDYE
    {
      if (receivedData[2] == 0b00000000)
      {
        digitalWrite(10, HIGH);
      }
      sendData(receivedData, max_bytes); // Debugging print
    }
    else if (receivedData[0] == ETB1Command) // ETB1 - sending GP/IO at end of experiment
    {
      digitalWrite(10, LOW);
      sendData(receivedData, max_bytes); // Debugging print

      // Send GP/IO at end of experiment
    }
    else if (receivedData[0] == ETB2Command) // ETB2 - tells Testbed to stop flowing
    {
      // Send ERPI (reset Dye Injection)
      sendData(receivedData, max_bytes); // Debugging print
    }
  }
}