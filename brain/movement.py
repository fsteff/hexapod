from serial_protocol import connect_arduino, move_foot
import time

height = -40
side = 90
lift = 50
dist = 70
speed = 0.7

arduino_port = 'dev/ttyUSB0'
serial = connect_arduino(arduino_port)
time.sleep(0.5)

def gait(foot, step, ms):
  x = side
  y = height
  z = 0

  if foot == 0 or foot == 3: 
    z = -100
  elif foot == 2 or foot == 5: 
    z = 100

  if step == 1:
    z += dist/4
  elif step == 2:
    z += dist/2
  elif step == 3:
    y += lift
  elif step == 4:
    z -= dist/2
  elif step == 5:
    z -= dist/4

  move_foot(serial, foot, x, y, z, int(ms))


move_foot(serial, 0, 50, 0 , -100, 500)
move_foot(serial, 1, 50, 0 , 0, 500)
move_foot(serial, 2, 50, 0 , 100, 500)
move_foot(serial, 3, 50, 0 , -100, 500)
move_foot(serial, 4, 50, 0 , 0, 500)
move_foot(serial, 5, 50, 0 , 100, 500)
time.sleep(1)

move_foot(serial, 0, 60, height/3 , -100, 250)
move_foot(serial, 2, 60, height/3 , 100, 250)
move_foot(serial, 3, 60, height/3 , -100, 250)
move_foot(serial, 4, 60, height/3 , 0, 250)
move_foot(serial, 5, 60, height/3 , 100, 250)
time.sleep(0.25)

move_foot(serial, 0, 70, height*0.66 , -100, 250)
move_foot(serial, 1, 70, height*0.66 , 0, 250)
move_foot(serial, 2, 70, height*0.66 , 100, 250)
move_foot(serial, 3, 70, height*0.66 , -100, 250)
move_foot(serial, 4, 70, height*0.66 , 0, 250)
move_foot(serial, 5, 70, height*0.66 , 100, 250)
time.sleep(0.25)

move_foot(serial, 0, side, height , -100, 250)
move_foot(serial, 1, side, height , 0, 250)
move_foot(serial, 2, side, height , 100, 250)
move_foot(serial, 3, side, height , -100, 250)
move_foot(serial, 4, side, height , 0, 250)
move_foot(serial, 5, side, height , 100, 250)
while True:
  for i in range(0, 6):
    t = time.time()
    for f in range(0, 3):
      gait(f, (i+f*2)%6, speed * 100)
      gait(f+3, (i+3+f*2)%6, speed * 100)
    passed = time.time() - t
    rest = speed - passed
    if rest > 0:
      time.sleep(rest)

while True:
  move_foot(serial, 0, side, height + lift , -150, 250)
  move_foot(serial, 1, side, height, 25, 250)
  move_foot(serial, 2, side, height, 125, 250)
  move_foot(serial, 3, side, height, -175, 250)
  move_foot(serial, 4, side, height + lift, 0, 250)
  move_foot(serial, 5, side, height, 175, 250)
  time.sleep(0.25)
  move_foot(serial, 0, side, height, -200, 250)
  move_foot(serial, 1, side, height, 50, 250)
  move_foot(serial, 2, side, height, 150, 250)
  move_foot(serial, 3, side, height, -150, 250)
  move_foot(serial, 4, side, height, -50, 250)
  move_foot(serial, 5, side, height, 200, 250)
  time.sleep(0.25)

  move_foot(serial, 0, side, height, -175, 250)
  move_foot(serial, 1, side, height + lift, 0, 250)
  move_foot(serial, 2, side, height, 175, 250)
  move_foot(serial, 3, side, height, -125, 250)
  move_foot(serial, 4, side, height, -25, 250)
  move_foot(serial, 5, side, height + lift, 150, 250)
  time.sleep(0.25)
  move_foot(serial, 0, side, height, -150, 250)
  move_foot(serial, 1, side, height, -50, 250)
  move_foot(serial, 2, side, height, 200, 250)
  move_foot(serial, 3, side, height, -100, 250)
  move_foot(serial, 4, side, height, 0, 250)
  move_foot(serial, 5, side, height, 100, 250)
  time.sleep(0.25)

  move_foot(serial, 0, side, height, -125, 250)
  move_foot(serial, 1, side, height, -25, 250)
  move_foot(serial, 2, side, height + lift, 150, 250)
  move_foot(serial, 3, side, height + lift , -150, 250)
  move_foot(serial, 4, side, height, 25, 250)
  move_foot(serial, 5, side, height, 125, 250)
  time.sleep(0.25)
  move_foot(serial, 0, side, height, -100, 250)
  move_foot(serial, 1, side, height, 0, 250)
  move_foot(serial, 2, side, height, 100, 250)
  move_foot(serial, 3, side, height, -200, 250)
  move_foot(serial, 4, side, height, 50, 250)
  move_foot(serial, 5, side, height, 150, 250)
  time.sleep(0.25)
