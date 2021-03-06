#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <math.h>
#include "foot.h"

#ifndef isnormal
#define isnormal(x) ((x==x)) // NaN returns false
#endif

const float part1 = 33;
const float part2 = 90.5;
const float part3 = 83.5;
const float toDeg = 180 / PI;

Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x42);

#define SERVOFREQ 60
#define PULSE (1000/SERVOFREQ)
#define SERVOMIN  (0.5 * 4096 / PULSE)  // this is the 'minimum' pulse length count (out of 4096) - 1ms
#define SERVOMAX  (2.5 * 4096 / PULSE) // this is the 'maximum' pulse length count (out of 4096) - 2ms



void writeServo(uint8_t n, float rotation, bool mirror) {
  Adafruit_PWMServoDriver& pwm = n < 16 ? pwm1 : pwm2;
  rotation = mirror ? 180 - rotation : rotation;
  int pulse = SERVOMIN + (rotation/180)*(SERVOMAX-SERVOMIN);
  n = n < 16 ? n : n - 16;
  pwm.setPWM(n, 0, pulse);
}


void updateServo(ServoCtrl& ctrl, float interval, bool mirror)
{
  
  ctrl.passedTime += interval;
  if(ctrl.passedTime >= ctrl.targetTime) {
    ctrl.passedTime = ctrl.targetTime; // prevent overflow
    writeServo(ctrl.servoNum, ctrl.targetPos, mirror);
    //Serial.println(ctrl.targetPos);
  } else {
    int curPos = ctrl.startPos + (ctrl.targetPos - ctrl.startPos) * ((float)ctrl.passedTime / ctrl.targetTime);
    int movement = (ctrl.targetPos - ctrl.startPos) * (interval / ctrl.targetTime);
    curPos += movement; //(ABS(movement) > 0 ? movement : SIGN(ctrl.targetPos - ctrl.startPos));
    writeServo(ctrl.servoNum, curPos, mirror);
    //Serial.print(curPos);
    //Serial.print(" to ");
    //Serial.println(ctrl.targetPos);
  }
}

void moveServo(ServoCtrl& ctrl, int pos, float ms)
{
  ctrl.startPos = ctrl.targetPos;
  ctrl.targetPos = pos;
  ctrl.targetTime = ms;
  ctrl.passedTime = 0;
}

float lawOfCosines(float a, float b, float c) {
  //Serial.print("LawOfCosines"); Serial.print(a); Serial.print("/"); Serial.print(b); Serial.print("/"); Serial.println(c); Serial.print("="); Serial.println((a*a + b*b - c) / 2 * a * b);
  return acos((a*a + b*b - c*c) / (2 * a * b));
}

Foot::Foot() : servos{ServoCtrl(90), ServoCtrl(0), ServoCtrl(90)}, mirror(false), isAttached(false) {}

void Foot::attach(int pin1, int pin2, int pin3, bool mirror){  
  servos[0].servoNum = pin1;
  servos[1].servoNum = pin2;
  servos[2].servoNum = pin3;
  this->mirror = mirror;

  writeServo(servos[0].servoNum, servos[0].startPos, mirror);
  writeServo(servos[1].servoNum, servos[1].startPos, mirror);
  writeServo(servos[2].servoNum, servos[2].startPos, mirror); 

  isAttached = true;
}
void Foot::moveTo(float x, float y, float z, long ms){
  float alpha, beta, gamma;
  if(! isAttached) {
    Serial.println("Foot is not attached!");
    return;
  }
  x = max(1, x);
  // https://appliedgo.net/roboticarm/ 

  alpha = atan(z/x) * toDeg;
  float zxf = sqrt(x*x + z*z) / x;
  x -= part1;
  x *= zxf; 

  float dist = sqrt(x*x + y*y);

  float d1  = atan2(y, x);
  float d2 = lawOfCosines(dist, part2, part3);

  beta = (d1 + d2) * toDeg;
  gamma = lawOfCosines(part2, part3, dist) * toDeg;

  if(!isnormal(alpha) || !isnormal(beta) || !isnormal(gamma)) {
    Serial.println("ERROR: Abort moving foot, result contains NaN");
    return;
  }
  
  Serial.println("OK");
  //Serial.print("Move to "); Serial.print(x); Serial.print("/"); Serial.print(y); Serial.print("/"); Serial.println(z);
  //Serial.print("Equals "); Serial.print(alpha); Serial.print("/"); Serial.print(beta); Serial.print("/"); Serial.println(gamma);
  //Serial.print("Using "); Serial.print(dist); Serial.print("/"); Serial.print(d1); Serial.print("/"); Serial.println(d2);

   moveServo(servos[0], 90 + alpha, ms);
   moveServo(servos[1], 90 - beta, ms);
   moveServo(servos[2], 180 - gamma, ms);
}

void Foot::update(int ms) {
  updateServo(servos[0], ms, mirror);
  updateServo(servos[1], ms, mirror);
  updateServo(servos[2], ms, mirror);
}

bool Foot::isDone(){
  return servos[0].passedTime >= servos[0].targetTime
         && servos[1].passedTime >= servos[1].targetTime
         && servos[2].passedTime >= servos[2].targetTime;
}

void Foot::setupPWM(){
  pwm1.begin();
  pwm2.begin();
  pwm1.setPWMFreq(SERVOFREQ);
  pwm2.setPWMFreq(SERVOFREQ);
}
