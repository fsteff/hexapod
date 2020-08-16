from serial_protocol import connect_arduino, move_foot
import time

height = -50

arduino_port = 'COM17'
serial = connect_arduino(arduino_port)
time.sleep(0.5)

move_foot(serial, 0, 100, height , -100, 500)
move_foot(serial, 1, 100, height , 0, 500)
move_foot(serial, 2, 100, height , 100, 500)
time.sleep(1)
while True:
  move_foot(serial, 0, 100, height + 50 , -150, 250)
  move_foot(serial, 1, 100, height, 25, 250)
  move_foot(serial, 2, 100, height, 125, 250)
  time.sleep(0.25)
  move_foot(serial, 0, 100, height, -200, 250)
  move_foot(serial, 1, 100, height, 50, 250)
  move_foot(serial, 2, 100, height, 150, 250)
  time.sleep(0.25)

  move_foot(serial, 0, 100, height, -175, 250)
  move_foot(serial, 1, 100, height + 50, 0, 250)
  move_foot(serial, 2, 100, height, 175, 250)
  time.sleep(0.25)
  move_foot(serial, 0, 100, height, -150, 250)
  move_foot(serial, 1, 100, height, -50, 250)
  move_foot(serial, 2, 100, height, 200, 250)
  time.sleep(0.25)

  move_foot(serial, 0, 100, height, -125, 250)
  move_foot(serial, 1, 100, height, -25, 250)
  move_foot(serial, 2, 100, height + 50, 150, 250)
  time.sleep(0.25)
  move_foot(serial, 0, 100, height, -100, 250)
  move_foot(serial, 1, 100, height, 0, 250)
  move_foot(serial, 2, 100, height + 50, 100, 250)
  time.sleep(0.25)
