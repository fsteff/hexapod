import serial, io, time

def readline(ser, wait=True):
  while wait or ser.in_waiting: 
    line = ser.readline().decode('iso8859_2')
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    line = line.strip()
    if len(line) > 0:
      return line
  return ''

def connect_arduino(port):
  ser = serial.Serial(port, 
    baudrate=9600, 
    bytesize = serial.EIGHTBITS, 
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE, 
    xonxoff = False,
    timeout=5,
    write_timeout=2,
    rtscts=False, 
    dsrdtr=False
    )
  print('<< ' + readline(ser))
  print('successfully connected to serial port ' + port + ' / ' + ser.name)
  return ser

def move_foot(ser, nr, x, y, z, ms = 1000):
  while ser.in_waiting:
    line = readline(ser, False)
    if len(line) > 0:
      print('>> ' + line)

  msg = '{:d} {:d} {:d} {:d} {:d}\r\n'.format(int(nr), int(x), int(y), int(z), int(ms))
  ser.write(msg.encode())
  ser.flush()
  print('>> ' + msg[:-2])
  echo = readline(ser)
  if echo != msg[:-2]:
    print('ERROR: echo of sent message does not match: ' + echo)

  aw = readline(ser)
  print('<< ' + aw)
  if not aw.startswith('OK'):
    print('ERROR: arduino did not acknowlege command')


    