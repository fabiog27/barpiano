#include <ArduinoJson.h>

#define COFFEE_PIN 2
#define ESPRESSO_PIN 3
#define COFFEE_TIME 30
#define ESPRESSO_TIME 20

bool isMakingCoffee = false;
bool isLEDOn = false;
StaticJsonDocument<200> jsonDoc;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(200);
  pinMode(COFFEE_PIN, OUTPUT);
  pinMode(ESPRESSO_PIN, OUTPUT);
}

void loop() {
  String message = Serial.readString();
  if (message.length() > 0) {
    if (isMakingCoffee) {
      Serial.print("Coffee making in progress, please wait");
    } else {
      DeserializationError error = deserializeJson(jsonDoc, message);
      if (error) {
        Serial.print("deserializeJson failed: ");
        Serial.print(error.f_str());
        Serial.print("\n");
      }
      const String coffeeType = jsonDoc["coffeeType"];
      const int coffeeAmount = jsonDoc["coffeeAmount"];
      Serial.print("1");
      makeCoffee(coffeeType, coffeeAmount);
    }
  }
}

void makeCoffee(String coffeeType, int coffeeAmount) {
  if (coffeeType.equals("c")) {
    blinkLED(COFFEE_PIN, COFFEE_TIME * coffeeAmount);
  } else if (coffeeType.equals("e")) {
    blinkLED(ESPRESSO_PIN, ESPRESSO_TIME * coffeeAmount);
  }
}

void blinkLED(int pinNumber, int times) {
  byte value = 1;
  for (int i = 0; i < times; i++) {
    if (pinNumber == 2) {
      digitalWrite(pinNumber, value);
    } else {
      analogWrite(pinNumber, value * 255);
    }
    value++;
    value = value % 2;
    delay(1000);
  }
}
