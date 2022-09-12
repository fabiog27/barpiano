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
  Serial.begin(9600);
  Serial.setTimeout(1);
  FastLED.addLeds<CHIP_SET, RGB_PIN, COLOR_CODE>(LEDs, RGB_LED_NUM);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 500);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  if (Serial.available() > 0) {
    message = message + Serial.readString();
    int length = message.length();
    if (message.charAt(0) != 'A') {
      Serial.println("Error: message should start with A");
      Serial.println(message);
      message = "";
      return;
    }
    if (length < 21) {
      return;
    }
    if (length > 21 || message.charAt(20) != 'Z') {
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
      if (currentChar == ' ') {
        stage++;
        tempPos = 0;
        continue;
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
    Serial.print("update LED\n");
    Serial.println(startIndexAsNum);
    Serial.println(endIndexAsNum);
    Serial.println(rAsNum);
    Serial.println(gAsNum);
    Serial.println(bAsNum);
    updateLEDs(startIndexAsNum, endIndexAsNum, rAsNum, gAsNum, bAsNum);
    message = "";
  }
}

void printChars(char * chars) {
  for (int i = 0; i < 3; i++) {
    Serial.print(chars[i]);
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

void FULL_BEANS(void) {
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB(255, 255, 255);
  }
  FastLED.show();
  delay(10000);
  for (int i = 0; i < RGB_LED_NUM; i++)
    LEDs[i] = CRGB(0, 0, 0 );
  FastLED.show();
}

// RED LED TOGGLE
void Toggle_RED_LED(void) {
  for (int i = 0; i < 256; i++) {
    int r = 255 - i;
    int g = i;
    int b = 0;
    for (int i = 0; i < RGB_LED_NUM; i++)
      LEDs[i] = CRGB(r, g, b);
    FastLED.show();
    delay(10);
  }
  for (int i = 0; i < 256; i++) {
    int r = 0;
    int g = 255 - i;
    int b = i;
    for (int i = 0; i < RGB_LED_NUM; i++)
      LEDs[i] = CRGB(r, g, b);
    FastLED.show();
    delay(10);
  }
  for (int i = 0; i < RGB_LED_NUM; i++)
    LEDs[i] = CRGB(0, 0, 0 );
  FastLED.show();
}
// Move the Red LED
void Scrolling_RED_LED(void)
{
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Red;
    FastLED.show();
    delay(10);
    LEDs[i] = CRGB::Black;
    FastLED.show();
    delay(10);

  }
}
// Orange/White/Green color green
void O_W_G_scroll() {
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Orange;
    delay(50);
    FastLED.show();
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Black;
    delay(50);
    FastLED.show();
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::White;
    delay(50);
    FastLED.show();
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Black;
    delay(50);
    FastLED.show();
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Green;
    delay(50);
    FastLED.show();
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB::Black;
    delay(50);
    FastLED.show();
  }
}
// Red/Green/Blue color Rotate
void Rotate_color(void) {
  for (int i = 0; i < 20; i++) {
    for (int clr = 0; clr < RGB_LED_NUM; clr++) {
      if (clr > 0) {
        LEDs[clr - 1] = CRGB(160, 60, 0);
      }
      for (int j = 0; j < 16; j++) {
        if (clr + j < RGB_LED_NUM) {
          LEDs[clr + j] = CRGB::White;
        }
      }
      int otherDirection = RGB_LED_NUM - clr;
      for (int j = 0; j < 16; j++) {
        if (otherDirection - j > 0) {
          LEDs[otherDirection - j] = CRGB::White;
        }
      }
      if (otherDirection < RGB_LED_NUM) {
        LEDs[otherDirection + 1] = CRGB(160, 60, 0);
      }
      if (clr % 4 == 0) {
        FastLED.show();
      }
    }
  }
}
// Blue, Green , Red 
void r_g_b() {
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB ( 0, 0, 255);
    if (i % 2 == 0) {
      FastLED.show();
    }
    delay(1);
  }
  for (int i = RGB_LED_NUM; i >= 0; i--) {
    LEDs[i] = CRGB ( 0, 255, 0);
    if (i % 2 == 0) {
      FastLED.show();
    }
    delay(1);
  }
  for (int i = 0; i < RGB_LED_NUM; i++) {
    LEDs[i] = CRGB ( 255, 0, 0);
    if (i % 2 == 0) {
      FastLED.show();
    }
    delay(1);
  }
  for (int i = RGB_LED_NUM; i >= 0; i--) {
    LEDs[i] = CRGB ( 0, 0, 0);
    if (i % 2 == 0) {
      FastLED.show();
    }
    delay(1);
  }
}
// random color show
void random_color(void) {
  for (int i = 0; i < 50; i++) {
    // loop over the NUM_LEDS
    for (int i = 0; i < RGB_LED_NUM; i++) {
      // choose random value for the r/g/b
      a = random(0, 255);
      b = random(0, 255);
      c = random(0, 255);
      // Set the value to the led
      LEDs[i] = CRGB (a, b, c);
      delay(1);
    }
    FastLED.show();
  }
}

void color_wave(void) {
  for (int led = 0; led < RGB_LED_NUM; led++) {
    int min = led > 50 ? led - 50 : 0;
    int max = led < RGB_LED_NUM - 50 ? led + 50 : led;
    for (int i = 0; i < min; i++) {
      LEDs[i] = CRGB::Black;
    }
    for (int i = min; i < max; i++) {
      LEDs[i] = CRGB::Red;
    }
    for (int i = max; i < RGB_LED_NUM; i++) {
      LEDs[i] = CRGB::Black;
    }
    FastLED.show();
  }
}