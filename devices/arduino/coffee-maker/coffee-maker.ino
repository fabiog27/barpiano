#include <ArduinoJson.h>

#define COFFEE_PIN 4
#define ESPRESSO_PIN 3
#define COFFEE_TIME 30
#define ESPRESSO_TIME 20

bool isMakingCoffee = false;
StaticJsonDocument<200> jsonDoc;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(200);
  pinMode(COFFEE_PIN, OUTPUT);
  pinMode(ESPRESSO_PIN, OUTPUT);
  digitalWrite(COFFEE_PIN, LOW);
  digitalWrite(ESPRESSO_PIN, LOW);
}

void loop() {
  String message = Serial.readString();
  if (message.length() > 0) {
    if (isMakingCoffee) {
      Serial.print("Coffee making in progress, please wait");
    } else {
      DeserializationError error = deserializeJson(jsonDoc, message);
      if (error) {
        Serial.print("deserializeJson failed: \n");
        Serial.print(error.f_str());
        Serial.print("\n");
      }
      const String coffeeType = jsonDoc["coffeeType"];
      const int coffeeAmount = jsonDoc["coffeeAmount"];
      Serial.println("1");
      makeCoffee(coffeeType, coffeeAmount);
    }
  }
}

void makeCoffee(String coffeeType, int coffeeAmount) {
  if (coffeeType.equals("c")) {
    digitalWrite(COFFEE_PIN, HIGH);
    delay(200);
    digitalWrite(COFFEE_PIN, LOW);
    delay(COFFEE_TIME * 1000);
  }
}
