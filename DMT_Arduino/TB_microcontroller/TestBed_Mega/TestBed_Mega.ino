int index = 0;          // Initialize an index variable to keep track of the next available position in the array
int incomingByte;

// Hex Identifiers (i.e., start byte)

int STBCommand = 0b00000001;
int RTBCommand = 0b00000111;
int ETB1Command = 0b00001001;
int ETB2Command = 0b00001010;

uint8_t receivedData[14];

void setup()
{
  Serial.begin(230400); // Initialize serial communication
}

void loop()
{

  delay(500);

  if (Serial.available() >= 14 || Serial.available() == 0)
  {
    for (int i = 0; i < 14; i++)
    {
      receivedData[i] = (uint8_t)Serial.read();
    } 
    if (receivedData[0] == STBCommand)
    {

      for (int i = 0; i < 14; i++) {

        Serial.write(receivedData[i]);

      }

    }

    if (receivedData[0] == RTBCommand)
    {
      Serial.print("RTB");
    }

    if (receivedData[0] == ETB1Command)
    {
      Serial.print("ETB1");
    }

    if (receivedData[0] == ETB2Command)
    {
      Serial.print("ETB2");
    }
  }
}

// void loop()
// {

//   if (Serial.available() > 0)
//   {

//     byte incomingByte = Serial.read();

//     if (incomingByte == STBCommand || incomingByte == RTBCommand || incomingByte == ETB1Command || incomingByte == ETB2Command)
//     {
//       dataIndex = 0; // Reset the index variable

//       while (Serial.available() && Serial.peek() != stopByte)
//       { // Loop until the stop byte is received or there is no more data available

//         dataArray[dataIndex++] = Serial.read(); // Add the incoming byte to the data array and increment the index

//         delay(10);
//       }
//       else
//       {

//         Serial.print("Error");
//       }
//     }
//   }
// }

// void loop() {

//   delay(500);

//   if (Serial.available() > 0) {
//     // read the incoming byte:
//     byte b = Serial.read();
//     myArray[index] = b;
//     index++;

//   }

//   size_t arraySize = sizeof(myArray) / sizeof(byte);

//   for (int i = 0; i < 16; i++) {

//     Serial.write(myArray[i]);

//   }
// }

/* void loop()
{

  if (Serial.available() > 0)
  {
    byte b = Serial.read();
    myArray[index] = b;
    index++;
    Serial.print(Serial.available());
  }
  if (Serial.available() == 2)
  {

    for (int i = 0; i < 3; i++)
    {
      Serial.write(Serial.available());
    }
  }
  else
  {

  }
} */