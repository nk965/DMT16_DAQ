int incomingByte;

void setup() {
  Serial.begin(230400);
  Serial1.begin(230400);
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.write(incomingByte);
    Serial1.write(incomingByte);
  }
}