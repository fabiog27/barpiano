#include <FastLED.h>


#define RGB_PIN 5
#define RGB_LED_NUM 300
#define BRIGHTNESS 255
#define CHIP_SET WS2812B
#define COLOR_CODE GRB //sequence of colors in data stream

// Define the array of LEDs
CRGB LEDs[RGB_LED_NUM];

// define 3 byte for the random color
byte  a, b, c;
#define UPDATES_PER_SECOND 1000

String message;

void setup() {
  Serial.begin(921600);
  Serial.setTimeout(1);
  FastLED.addLeds<CHIP_SET, RGB_PIN, COLOR_CODE>(LEDs, RGB_LED_NUM);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 7000);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  if (Serial.available() > 0) {
    message = message + Serial.readStringUntil('X');
    int length = message.length();
    if (message.charAt(0) != 'A') {
      Serial.println("Error: message should start with A");
      Serial.println(message);
      message = "";
      return;
    }
    if (length < 17) {
      return;
    }
    if (length > 17 || message.charAt(16) != 'Z') {
      Serial.println("Error: ill-formatted message");
      Serial.println(message);
      message = "";
      return;
    }
    char startIndex[3] = {'0', '0', '0'};
    char endIndex[3] = {'0', '0', '0'};
    char r[3] = {'0', '0', '0'};
    char g[3] = {'0', '0', '0'};
    char b[4] = {'0', '0', '0'};
    byte stage = 0;
    byte tempPos = 0;
    for (int i = 1; i < length - 1; i++) {
      char currentChar = message.charAt(i);
      if (i > 1 && (i - 1) % 3 == 0) {
        stage++;
        tempPos = 0;
      }
      switch (stage) {
        case 0:
          startIndex[tempPos] = currentChar;
          break;
        case 1:
          endIndex[tempPos] = currentChar;
          break;
        case 2:
          r[tempPos] = currentChar;
          break;
        case 3:
          g[tempPos] = currentChar;
          break;
        case 4:
          b[tempPos] = currentChar;
          break;
      }
      tempPos++;
    }
    int startIndexAsNum = convertCharArrayToInt(startIndex);
    int endIndexAsNum = convertCharArrayToInt(endIndex);
    int rAsNum = convertCharArrayToInt(r);
    int gAsNum = convertCharArrayToInt(g);
    int bAsNum = convertCharArrayToInt(b);
    /*
    Serial.println("Update LEDs");
    Serial.println(startIndexAsNum);
    Serial.println(endIndexAsNum);
    Serial.println(rAsNum);
    Serial.println(gAsNum);
    Serial.println(bAsNum);
    */
    updateLEDs(startIndexAsNum, endIndexAsNum, rAsNum, gAsNum, bAsNum);
    message = "";
  }
}

int convertCharArrayToInt(char * chars) {
  int total = 0;
  bool shouldAdd = 0;
  int multiplier = 100;
  for (byte i = 0; i < 3; i++) {
    byte value = chars[i] - 48;
    if (value != 0) {
      shouldAdd = 1;
    }
    if (shouldAdd) {
      total += multiplier * value;
    }
    multiplier /= 10;
  }
  return total;
}


void updateLEDs(int startIndex, int endIndex, int r, int g, int b) {
  for (int i = startIndex; i <= endIndex; i++) {
    LEDs[i] = CRGB(r, g, b);
  }
  FastLED.show();
}
