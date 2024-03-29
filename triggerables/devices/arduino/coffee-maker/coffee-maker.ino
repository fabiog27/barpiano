#include <ArduinoJson.h>

#define POWER_PIN 18
#define ESPRESSO_1_PIN 19
#define ESPRESSO_2_PIN 21
#define CLEAN_PIN 22
#define COFFEE_2_PIN 23
#define COFFEE_1_PIN 25
#define STEAM_PIN 26

StaticJsonDocument<200> jsonDoc;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(200);
  setupPin(POWER_PIN);
  setupPin(ESPRESSO_1_PIN);
  setupPin(ESPRESSO_2_PIN);
  setupPin(CLEAN_PIN);
  setupPin(COFFEE_2_PIN);
  setupPin(COFFEE_1_PIN);
  setupPin(STEAM_PIN);
}

void setupPin(int number) {
  pinMode(number, OUTPUT);
  digitalWrite(number, HIGH);
}

void loop() {
  String message = Serial.readString();
  if (message.equals("Aget device funcZ")) {
    Serial.println("coffee-maker");
    return;
  }
  if (message.length() > 0) {
    executeAction(message);
  }
}

void executeAction(String action) {
  if (action.equals("power")) {
    simulateButtonPress(POWER_PIN);
    Serial.println("Pressed power button");
  } else if (action.equals("espresso")) {
    simulateButtonPress(ESPRESSO_1_PIN);
    Serial.println("Pressed button: One espresso");
  } else if (action.equals("doubleEspresso")) {
    simulateButtonPress(ESPRESSO_2_PIN);
    Serial.println("Pressed button: Two espressos");
  } else if (action.equals("clean")) {
    simulateButtonPress(CLEAN_PIN);
    Serial.println("Pressed button: Clean");
  } else if (action.equals("doubleCoffee")) {
    simulateButtonPress(COFFEE_2_PIN);
    Serial.println("Pressed button: Two coffees");
  } else if (action.equals("coffee")) {
    simulateButtonPress(COFFEE_1_PIN);
    Serial.println("Pressed button: One coffee");
  } else if (action.equals("steam")) {
    simulateButtonPress(STEAM_PIN);
    Serial.println("Pressed button: Steam");
  } else {
    Serial.print("Error: Unknown action ");
    Serial.print(action);
    Serial.print("\r\n");
  }
}

void simulateButtonPress(int pinNumber) {
    digitalWrite(pinNumber, LOW);
    delay(500);
    digitalWrite(pinNumber, HIGH);
}
