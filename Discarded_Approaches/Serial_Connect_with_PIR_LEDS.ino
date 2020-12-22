#define LED_GREEN_PIN 13
#define LED_RED_PIN 12
#define PIR_PIN 2

void powerOffLeds()
{
    digitalWrite(LED_GREEN_PIN, LOW);
    digitalWrite(LED_RED_PIN, LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(LED_GREEN_PIN, OUTPUT); //declare LED green as output
  pinMode(LED_RED_PIN, OUTPUT); // declare Ledred as output
  pinMode(PIR_PIN, INPUT); // declare sensor as input

  powerOffLeds();
}

void loop() {
  
  byte readValue = digitalRead(PIR_PIN); // read input value
  //Serial.println(sensorval); // print sensor value
  //delay (2000);
  
  if (readValue == HIGH) { // check if the sensor value is high
    //digitalWrite(ledPin, HIGH); // if it's high turn on the LED
    Serial.write(1); 
    delay(500);  // wait for 500 milliseconds 
  }
  if (Serial.available() > 0) {
    int ledNumber = Serial.read() - '0'; // subtracting with ‘0’, which will convert the character to the number it represents
  
   switch (ledNumber) {
    case 1:
      digitalWrite(LED_GREEN_PIN, HIGH);
      delay(5000);
    case 2:  
      digitalWrite(LED_RED_PIN, HIGH);
      delay(5000);
    default:
    break;  
    }
   }
  }

  
