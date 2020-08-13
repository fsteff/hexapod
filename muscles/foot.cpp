#include <Arduino.h>
#include <math.h>
#include "foot.h"

#ifndef isnormal
#define isnormal(x) ((x==x)) // NaN returns false
#endif

const float part1 = 33;
const float part2 = 90.5;
const float part3 = 83.5;
const float toDeg = 180 / PI;

void updateServo(ServoCtrl& ctrl, float interval)
{
  
  ctrl.passedTime += interval;
  if(ctrl.passedTime >= ctrl.targetTime) {
    ctrl.passedTime = ctrl.targetTime; // prevent overflow
    ctrl.servo.write(ctrl.targetPos);
    //Serial.println(ctrl.targetPos);
  } else {
    int curPos = ctrl.startPos + (ctrl.targetPos - ctrl.startPos) * ((float)ctrl.passedTime / ctrl.targetTime);
    int movement = (ctrl.targetPos - ctrl.startPos) * (interval / ctrl.targetTime);
    curPos += movement; //(ABS(movement) > 0 ? movement : SIGN(ctrl.targetPos - ctrl.startPos));
    ctrl.servo.write(curPos);
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

Foot::Foot() : servos{ServoCtrl(90), ServoCtrl(180), ServoCtrl(90)} {}

void Foot::attach(int pin1, int pin2, int pin3){
  servos[0].servo.attach(pin1);
  servos[1].servo.attach(pin2);
  servos[2].servo.attach(pin3);

  servos[0].servo.write(servos[0].startPos);
  servos[1].servo.write(servos[1].startPos);
  servos[2].servo.write(servos[2].startPos);
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
  gamma = 180 - lawOfCosines(part2, part3, dist) * toDeg;

  Serial.print("Move to "); Serial.print(x); Serial.print("/"); Serial.print(y); Serial.print("/"); Serial.println(z);
  Serial.print("Equals "); Serial.print(alpha); Serial.print("/"); Serial.print(beta); Serial.print("/"); Serial.println(gamma);
  //Serial.print("Using "); Serial.print(dist); Serial.print("/"); Serial.print(d1); Serial.print("/"); Serial.println(d2);

  if(!isnormal(alpha) || !isnormal(beta) || !isnormal(gamma)) {
    Serial.println("Abort, result contains NaN!");
    return;
  }

  moveServo(servos[0], 90 + alpha, ms);
  moveServo(servos[1], 90 + beta, ms);
  moveServo(servos[2], 180 - gamma, ms);
}

void Foot::update(int ms) {
  updateServo(servos[0], ms);
  updateServo(servos[1], ms);
  updateServo(servos[2], ms);
}

bool Foot::isDone(){
  return servos[0].passedTime >= servos[0].targetTime
         && servos[1].passedTime >= servos[1].targetTime
         && servos[2].passedTime >= servos[2].targetTime;
}
