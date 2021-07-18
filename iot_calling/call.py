import re
import os
import time
import uuid
import serial
from twilio.rest import Client

def alert():

  global count

  if count != 1: return(1)
                   
  call = client.calls.create(
    twiml='<Response><Say>Hello. This is a Dalek, Exterminate!</Say></Response>',
    to = os.environ["MYPHONE"],
    from_ = os.environ["TWILIOPHONE"]
                    )
                    
  return(1)

# The serial output was wonky and returned multiple values for one button press.
# I didn't want to blow up my phone so this count variable is a flag for when the button was
# triggered and only calls me once. (See the if statement in alert().) The script needs to 
# be reset after that. 

count = 0
account_sid = os.environ["TWILIOSID"]
auth_token = os.environ["TWILIOTOKEN"]
client = Client(account_sid, auth_token)

#-create connection to serial drive
ser = serial.Serial('/dev/ttyACM0', 9600) #ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.flushInput()

while 1:
  #line = set(ser.readline().decode("utf-8"))
  #print(line)
  if (ser.in_waiting > 0):
    count = count + 1
    alert()
