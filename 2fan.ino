
#define FIR 13
#define SEC 12
void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        Serial.println(serialListener);
        if(serialListener == 'H1') {
        digitalWrite(FIR, HIGH);
        }
        else if (serialListener == 'L1') {
        serialListener = Serial.read();
        digitalWrite(FIR, LOW);
        }
        if(serialListener == 'H2') {
        digitalWrite(SEC, HIGH);
        }
        else if (serialListener == 'L2') {
        serialListener = Serial.read();
        digitalWrite(SEC, LOW);
        }
    }
}
