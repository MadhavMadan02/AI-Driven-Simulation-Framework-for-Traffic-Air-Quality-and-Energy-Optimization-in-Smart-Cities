// Pin definitions
#define PIR_PIN D5         // PIR sensor OUT pin
#define LDR_DO_PIN D2      // LDR Module DO pin
#define LED_PIN D6         // LED streetlight pin

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(LDR_DO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  int ldrState = digitalRead(LDR_DO_PIN);  // 1 = dark, 0 = bright
  int pirState = digitalRead(PIR_PIN);     // 1 = motion, 0 = no motion

  Serial.print("LDR: ");
  Serial.print(ldrState == 1 ? "Dark" : "Bright");
  Serial.print(" | PIR: ");
  Serial.println(pirState == 1 ? "Motion" : "No Motion");

  if (ldrState == 1 && pirState == 1) {
    digitalWrite(LED_PIN, HIGH); 
  } else {
    digitalWrite(LED_PIN, LOW);  
  }

  delay(200); 
}