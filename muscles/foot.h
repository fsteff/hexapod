#ifndef FOOT_H
#define FOOT_H

#include <Servo.h>

struct ServoCtrl {
  const Servo servo;
  int startPos;
  int targetPos;
  long targetTime;
  long passedTime;

  ServoCtrl(int curPos = 90) 
   : startPos(curPos), targetPos(curPos), targetTime(0), passedTime(0) {}
};

class Foot{
  private:
    ServoCtrl servos[3];
    bool isAttached;
  public:
    Foot();
    void attach(int pin1, int pin2, int pin3);
    void moveTo(float x, float y, float z, long ms);
    void update(int ms);
    bool isDone();
};

#endif
