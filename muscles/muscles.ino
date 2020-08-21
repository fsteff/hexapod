#include "foot.h"

#define SIGN(x) (x >= 0 ? 1 : -1)
#define ABS(x) (x >= 0 ? x : -x)

Foot feet[6];
char serialBuf[64] = {0};
uint8_t serialPos = 0;

void processSerial() {
  int32_t values[5] = {0,0,0,0,0};
  uint8_t pos = 0;
  for(uint8_t i = 0; i < 5; i++) {
    bool isNegative = false;
    for(; pos < serialPos && (isDigit(serialBuf[pos]) || serialBuf[pos] == '-'); pos++) {
      if(serialBuf[pos] == '-') {
        isNegative = true;
      } else {
        uint8_t n = serialBuf[pos] - '0';
        values[i] = values[i] * 10 + n;
      }    
    }
    if(isNegative) values[i] = -values[i];
    pos++;
  }

  if (values[0] < 6) {
    feet[values[0]].moveTo(values[1], values[2], values[3], values[4]);   
  } else {
    Serial.print("ERROR: Invalid foot number: ");
    Serial.println(values[0]);
  }

}

void setup() {
  Serial.begin(9600);
  Serial.println("Hello");
  Foot::setupPWM();

  feet[0].attach(16,17,18);
  feet[1].attach(19,20,21);
  feet[2].attach(22,23,24);

  feet[3].attach(0,1,2, true);
  feet[4].attach(3,4,5, true);
  feet[5].attach(6,7,8, true);
  delay(1000);
}

void loop() {
  char ch;
  while (Serial.available()) {
    ch = Serial.read();
    Serial.print(ch);
    serialBuf[serialPos++] = ch;
    if (ch == '\n' || serialPos >= sizeof(serialBuf)) {
      Serial.println("");
      serialBuf[serialPos] = 0;
      if(serialPos > 1) processSerial();
      serialPos = 0;
    }
  }


  delay(10);
  for(int i = 0; i < 6; i++) {
    feet[i].update(10);
  }
}
