#event send for our bot

# uses socket programming
# task 2 being the B of the platoon order A, B, C
# leaving a platoon is done automatically without any ACK
# GROUP 6 as client
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
HOST = 'localhost' #239.255.76.67
PORT = 8042 #7668
speed = 70

def left():
    pi2go.go(40,60)
    time.sleep(2.55)
    pi2go.go(70,35)
    time.sleep(1)
   
def right():
    pi2go.go(60,40)
    time.sleep(1.15)
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
# socket creation
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # DGRAM-Datagram in UDP
    print 'Socket created.'
except socket.error:
    print 'Unable to create socket.'
    sys.exit()

print 'Enter a choice: \n1.Merge Request\n2.Platoon Leave'
try:
 tty.setcbreak(sys.stdin.fileno())

 while True:
    
    line(speed)
    distance = pi2go.getDistance()
    dist = int(distance/4)
    if dist <= 3:
        pi2go.stop()
        time.sleep(1.75)
    if dist == 3:
       speed = 60
#       print 'obstacle detected setting speed tp 30..."
    if isData():
        msg = sys.stdin.read(1)
        #msg1 = str(msg)
        #time.sleep(2)      
        try:
            
            s.sendto(msg, (HOST, PORT))
            #s.sendto(event,(HOST, PORT))
            # receiving data from client
            d = s.recvfrom(1000000)
            reply = d[0]
            add = d[1]        
            print 'Server reply: ' + reply
            #time.sleep(2)
               
            if reply == 'ACK\nCreating space...':
                d1 = s.recvfrom(1000000)
                reply1 = d1[0]
                add1 = d1[1]
                print 'Server acknowledgement: ' + reply1
                i = 0
                for i in range(0,100):
                  line(speed)
                  print 'line 2'
                if reply1 == 'Ready, you can merge.':
                        print 'choose to merge:'
                        x = raw_input()
                        print 'left-lane change'
                        if x == 'l':
                         left()
                        elif x == 'r':
			 right()	
                                      
                     #elif msg == '\x72': # lane change 'r'
                        #print 'right-lanechange'
                        #right()
            #    else:
            #        print 'No acknowledgement received.'
                merge_comp = 'Merge Complete.'
                s.sendto(merge_comp, (HOST, PORT))

            elif reply == 'Roger that.':
                # LANE CHANGE DEFINITION
                if reply1 == 'Ready, you can merge.':
                     #if msg == '\x6c':         # lane change 'l'
                        #print 'left-lane change'
                        #left()               
                     #elif msg == '\x72': # lane change 'r'
                        print 'right-lanechange'
                        right()
                plat_leave = 'Exited Platoon.'
                s.sendto(plat_leave, (HOST, PORT))
                
        except socket.error, ID:
            print 'Unable to send message.'
            pi2go.stop()
           
finally:
            pi2go.stop()
            pi2go.cleanup()
            sys.exit(0)

            

s.close()
