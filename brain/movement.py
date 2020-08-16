from serial_protocol import connect_arduino, move_foot
import time

arduino_port = 'COM17'
serial = connect_arduino(arduino_port)
move_foot(serial, 0, 100, 0 , -50, 1000)
move_foot(serial, 1, 100, 0 , 50, 1000)



