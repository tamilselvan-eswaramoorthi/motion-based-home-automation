
#define LED 13

void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        Serial.println(serialListener);
        if(serialListener == 'H') {
        digitalWrite(LED, HIGH);
        }
        else if (serialListener == 'L') {
        serialListener = Serial.read();
        digitalWrite(LED, LOW);
        }
    }
}
