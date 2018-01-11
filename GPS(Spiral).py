import time
import GPS as gps
import serial
import math
import pi2go
import termios
import sys
import select
import tty

pi2go.init()

global speed = 60
global init_dist[] ={1,2,3,4,5,6}
def ult_dist():

    dist = pi2go.getDistance()
    dist = dist/4
    return dist

        
def linefollow(speed):    
    left = pi2go.irLeftLine()
    right = pi2go.irRightLine()
    if left == False and right == True:
        pi2go.forward(speed)
    elif right == True and left == True:
        pi2go.spinLeft(speed - 30)
    elif left == True and right == False:
        pi2go.spinRight(speed - 30)
    elif left == False and right == False:
        pi2go.forward(speed)
      

def isData():
   return select.select([sys.stdin],[],[],0) == ([sys.stdin],[],[])
old_settings = termios.tcgetattr(sys.stdin)

# this function returns the quadrants based on the spiral id 6 #and he detected spiral id.
def dir(x_, y_):
    centerx = 317
    centery = 404

    angle = math.atan2((y_ - centery), (x_ - centerx))

    for i in xrange(-2, 2):
        if angle >= i * math.pi / 2 and angle < (i + 1) * math.pi / 2:
            quadrant = i

    return quadrant

# this function definition finds if other robots with spiral ids #1-5 are present on the right of the bot with spiral id 6 and all #the calculatons are based on considering the center of the #intersection and dividing the limits to two circles around the #center and then detectin the spirals on the lmited circles.
# Stops only when spirals detected on right side.

def find(id_, x_, y_, init_dist_, quadrant_6, distance_6):

    centerx = 317
    centery = 404
    radius = 450  
    i_radius = 150


    if (x_ == 0 and y_ == 0) or (x_ == -1 and y_ == -1):    # GPS 
        print 'false' #if 0 or -1

    else:

        dx = abs(x_ - centerx)
        dy = abs(y_ - centery)


        if ((dx + dy) <= radius):
            print 'true'

            dist_ = math.sqrt((dx * dx) + (dy * dy))

            quadrant_ = dir(x_, y_)
            print 'quadrant_', quadrant_
            print 'quadrant_6', quadrant_6

            if ((dx + dy) <= i_radius):
                if distance_6 < 380: 
                    pi2go.stop()                
                    print 'stop1'
                    time.sleep(2)
                    
                if quadrant_6 == -2:
                    if quadrant_ == -1:
                        print 'ID %d found on right quadrant 0' %id_
                        if init_dist_ > distance_:
                            print 'near the center'
                            if distance_6 < 380:
                                print 'stop2'
                                pi2go.stop()
                                #print 'stop'
                                time.sleep(2)   # stop
                                
                            init_dist_ = distance_

                        elif (distance_ + 5 <= init_dist_ or init_dist_ >= distance_ - 5):
                            print 'ID %d has stopped' %id_
                            if distance_6 < 380:
                                pi2go.stop()
                                print 'stop3'
                                time.sleep(2)

                        else:
                            init_dist_ = distance_

                if quadrant_6 == -1:
                    if quadrant_ == 0:
                        print 'ID %d found on right quarant -1' % id_
                        if init_dist_ > distance_:
                            print 'arriving center'
                            if distance_6 < 380:
                                print 'stop4'
                                pi2go.stop()          # stop
                                time.sleep(2)
                            init_dist_ = distance_

                        elif (distance_ + 5 <= init_dist_ or init_dist_ >= distance_ - 5):
                            print 'ID %d has stopped' %id_
                            if distance_6 < 380:
                                pi2go.stop()
				          time.sleep(2)
                        else:
                      #      print 'moving away'
                            init_dist_ = distance_

                if quadrant_6 == 0:
                    if quadrant_ == 1:
                        print 'ID %d found on right quadrant 1' % id_

                        if init_dist_ > distance_:
                            print 'arriving center'
                            if distance_6 < 380:
                                print 'stop5'
                                pi2go.stop()       # stop
                                time.sleep(2)
                            prev_dist_ = dist_

                        elif (dist_ + 5 <= prev_dist_ or prev_dist_ >= dist_ - 5):
                            print 'ID %d has stopped moving' %id_
                            if dist_6 < 380:
                                pi2go.irAll()
			               pi2go.stop()#new
			 	          time.sleep(2)

                        else:
                            init_dist_ = distance_

                if quad_6 == 1:
                    if quad_ == -2:
                        print 'ID %d found on right quadrant -2' % id_

                        if init_dist_ > distance_:
                            print 'arriving center'
                            if distance_6 < 380:
                                print 'stop6'
                                pi2go.stop()   # stop
                                time.sleep(2)
                            init_dist_ = distance_

                        elif (distance_ + 5 <= init_dist_ or init_dist_ >= distance_ - 5):
                            print 'ID %d has stopped ' %id_
                            if distance_6 < 380:
                                pi2go.irAll()
			           	pi2go.stop()
				          time.sleep(2)
                        else:
                init_dist_ = distance_

        else:
            print 'false'

    return init_dist_


# this function definition initates the robot and reads the #spiral id within the given limits around the center of the #intersection which is (317,404)

def intersection():
    centerx = 317
    center_y = 404
    radius = 370  
    global prev_dist[]= {1,2,3,4,5,6}
    init_dist[] = {270,270,270,270,270,270}    
    tty.setcbreak(sys.stdin.fileno())
    speed = 50
    try:	
		
       while 1:
        linefollow(speed)
        print 'linefollow 1'
        # ultrasonic sensor's obstacle detection
        obs = ult_dist()
        if (obs <= 4):
            pi2go.stop()
            print 'stop when bot is in front'
            time.sleep(1.2)
        elif (obs == 5):
            speed = 35
            #print 'speed = 45'
        # manual input to control bot
        if isData():
            c = sys.stdin.read(1)
            if c == '\x6c':         # lane change 'l'
                print 'left-lane change'
               # ard.write('2')
                left()               
            elif c == '\x72': # lane change 'r'
                print 'right-lanechange'
               # ard.write('3')
                right()
            elif c == '\x20': #spacebar
                print 'stop'
               # ard.write('1')
                #ard.write('4')
                pi2go.stop()
                time.sleep(5)
   #             sys.exit(0)
            elif c == '\x77': # 'w'
                print 'forward'
                pi2go.forward(speed)
                time.sleep(3)
            elif c == '\x73': #'s'
                print 'reverse' # 's'
                pi2go.reverse(speed)
                time.sleep(3)
            elif c == '\x61': # 'a'
                print 'left'
                pi2go.spinLeft(speed)
                time.sleep(3)
            elif c == '\x64': # 'd'
                print 'right'
                pi2go.spinRight(speed)
                time.sleep(3)
            elif c == '\x2e': #period
                print 'increase speed'
                speed = max(0, speed + 10)
            elif c == '\x2c': # comma 
                print 'decrease speed'
                speed = min(100, speed-10)
            elif c == '\x65': #e to exit from program
                print 'exiting...'
                sys.exit(0)
        
        id_1, x_1, y_1 = gps.gps_client(1)
        id_2, x_2, y_2 = gps.gps_client(2)
        id_3, x_3, y_3 = gps.gps_client(3)
        id_4, x_4, y_4 = gps.gps_client(4)
        id_5, x_5, y_5 = gps.gps_client(5)
        id_6, x_6, y_6 = gps.gps_client(6)
        
        print id_6, x_6, y_6

        if id_6 == 6:
            if (x_6 == 0 and y_6 == 0) or (x_6 == -1 and y_6 == -1) :  # not valid or GPS values 0 or -1
                print 'no id'
                
                continue

            else:
                dx = abs(x_6 - centerx)
                dy = abs(y_6 - centery)

                if ((dx + dy) <= radius):
                    print 'true'
                    distance_6 = math.sqrt((dx * dx) + (dy * dy))        # 200 - to stop at intersection
                    quadrant_6 = dir(x_6, y_6)

                    if (int_dist[5] > distance_6 or (distance_6+ 5 <= init_dist[5] or init_dist[5] >= distance_6 - 5)):
                        print 'ID %d arriving Intersection' %id_6

                        if id_1 == 1:

                            init_dist[0] = find(id_1, x_1, y_1, init_dist[0], quadrant_6, distance_6)

                        if id_2 == 2:

                            init_dist[1] = find(id_2, x_2, y_2, init_dist[1], quadrant_6, distance_6)

                        if id_3 == 3:

                            prev_dist_3 = find(id_3, x_3, y_3, init_dist[2], quadrant_6, distance_6)

                        if id_4 == 4:

                            init_dist[3] = find(id_4, x_4, y_4, init_dist[3], quadrant_6, distance_6)

                        if id_5 == 5:

                            init_dist[4] = find(id_4, x_4, y_4, init_dist[4], quadrant_6, distance_6)

                        init_dist[5] = distance_6

                    else:
                        print 'ID %away from Intersection' % id_6
                        init_dist[5] = distance_6


                else:
                    print 'Id %d not at Intersection' %id_6
    finally:
           termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
           pi2go.cleanup()



intersection()




