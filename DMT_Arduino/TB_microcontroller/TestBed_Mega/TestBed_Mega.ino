int incomingByte;

void setup() {
  Serial.begin(230400);
  // Serial1.begin(230400);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    // read the incoming byte:
    incomingByte = Serial.read();

    
    
    // say what you got:
    Serial.write(incomingByte);
    // Serial1.write(incomingByte);
  }
}