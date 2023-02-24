int incomingByte;

void setup() {
  Serial.begin(230400);
  // Serial1.begin(230400);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    if (incomingByte == 0b11111111) {

      digitalWrite(LED_BUILTIN, HIGH);
      Serial.write(incomingByte);

    }
    
    // say what you got:
    // Serial1.write(incomingByte);
  }
}