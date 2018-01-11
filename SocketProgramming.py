#event listen for our bot
#GROUP 6 being server
# task 2 & 4 being the A & C respectively of the platoon order A, B, C
import socket, sys
import os
#import SockGPS
import time
import sys
import select
import tty
import termios
import pi2go, time

pi2go.init()
HOST = 'localhost'   
PORT = 8040
speed = 70
#################FUNCTION DEFINITIONS#########################
def left():
    pi2go.go(40,60)
    time.sleep(2.35)
    pi2go.go(70,35)
    time.sleep(1)
   
def right():
    pi2go.go(60,40)
    time.sleep(1.2)
    pi2go.go(35,65)
    time.sleep(1) 

def line(speed):
    left = pi2go.irLeftLine()
    right = pi2go.irRightLine()  
    if left == False and right == True:
        pi2go.forward(speed)
    elif right == True and left == True:
        pi2go.spinLeft(speed - 35)
    elif left == True and right == False:
        pi2go.spinRight(speed - 35)
    elif left == False and right == False:
        pi2go.forward(speed)

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
old_settings = termios.tcgetattr(sys.stdin)
############################################################################################
# socket creation
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # DGRAM-Datagram in UDP
    print 'Socket created.'
except socket.error:
    print 'Unable to create socket.'
    sys.exit()

# socket binding
try:
    s.bind((HOST, PORT))
    print 'Socket bind completed.'
except socket.error:
    print 'Unable to bind.'
    sys.exit()
try:
  tty.setcbreak(sys.stdin.fileno())
  while True:
	  
    line(speed)
    print 'line follow'
    distance = pi2go.getDistance()
    dist = int(distance/4)
    if dist <= 3:
        pi2go.stop()
        time.sleep(1.75)
    if dist == 4:
       speed = 50
#       print 'obstacle detected setting speed t0 30..."
    if isData():
            c = sys.stdin.read(1)
            if c == '\x20': #spacebar
                print 'stop'
                pi2go.stop()
                time.sleep(5)
            elif c == '\x65': #e to exit from program
                print 'exiting...'
                sys.exit(0)
    try:
        # receiving data from client
        d = s.recvfrom(1000000)
        msg = d[0]  # message from client
        add = d[1]  # address of client
        print 'Message from [' + add[0] + ':' + str(add[1]) + ']: ' + msg.strip()
        
        if msg == '1': #receiving merge request
            reply = 'ACK\nCreating space...'
            s.sendto(reply, add)
            speed = 30 #decreased speed to create space
            time.sleep(2.5)
            reply1 = 'Ready, you can merge'
            s.sendto(reply1, add)
            time.sleep(5)
            speed = 50#increases speed after sending ack
      #  elif msg == '2': #ack after receiving 'merge completed' response from other bot
      #      time.sleep(0.75)
      #      reply = 'Roger that.'
      #      s.sendto(reply, add)
            
        else:
            reply = 'Message unrecognized!'
            s.sendto(reply, add)
            
        if not msg:    # if there is no message
            break

        #reply = 'Okay...' + msg
        #s.sendto(reply, add)
    except socket.error, msg:
        print 'Message not received.'
        
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    pi2go.cleanup()

s.close()
