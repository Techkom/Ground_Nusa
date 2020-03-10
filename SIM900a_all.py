import serial
import os, time

# Enable Serial Communication
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

# Transmiting AT Commands to the Modem
# '\r\n' indicates the Enter key

def SMS(Number,Message):
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    port.write('+++'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    # Disable Echo
    port.write('ATE0'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    # Select Message format as Text Mode
    port.write('AT+CMGF=1'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    # New SMS Message Indication
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    # Sending a message to a particular Number
    port.write('AT+CMGS='+Number+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)
    
    # Message
    port.write(Message+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)