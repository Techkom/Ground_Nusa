import serial
import os, time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

data = b"ATE0\r\n"
port.write(data)      # Disable the Echo
rcv = str(port.read(10))
print(rcv)
time.sleep(1)

data = b"AT+CMGF=1\r\n"
port.write(data) # Select Message format as Text mode 
rcv = str(port.read(10))
print(rcv)
time.sleep(1)

data = b"AT+CNMI=2,1,0,0,0\r\n"
port.write(data)   # New SMS Message Indications
rcv = port.read(10)
print(rcv)
time.sleep(1)

data = b"AT+CMGS='628111820089'\r\n"
port.write(data)
rcv = port.read(10)
print(rcv)
time.sleep(1)

data = b"Hello User\r\n"
port.write(data)  # Message
rcv = port.read(10)
print(rcv)

data= b"\x1A" 
port.write(data) # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print(rcv)
