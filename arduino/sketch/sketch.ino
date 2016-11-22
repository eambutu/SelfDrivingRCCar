int left = 11;
int right = 10;
int forward = 8;   
int back = 9;
int led = 13;

void setup() {
    // put your setup code here, to run once:
    pinMode(left, OUTPUT);
    pinMode(right, OUTPUT);
    pinMode(forward, OUTPUT);
    pinMode(back, OUTPUT);
    pinMode(led, OUTPUT);
    Serial.begin(9600);
}

void loop(){
    if (Serial.available() > 0) {
        int incomingByte = Serial.read(); 
        digitalWrite(left, LOW);
       digitalWrite(right, LOW);
       digitalWrite(forward, LOW);
       digitalWrite(back, LOW);
       Serial.print(incomingByte);
       Serial.print("\n");
       if (incomingByte & 0x01==1) {
       Serial.print("left\n");
       digitalWrite(left, HIGH);
       }
       if (incomingByte & 0x02) {
       Serial.print("right\n");
       digitalWrite(right, HIGH);
       }
       if (incomingByte & 0x04) {
       Serial.print("forward\n");
       digitalWrite(forward, HIGH);
       }
       if (incomingByte & 0x08) {
       Serial.print("backwards\n");
       digitalWrite(back, HIGH);
       }
                                                                                                                                }
}
