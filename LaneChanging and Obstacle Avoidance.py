# line follow, lane changing and obstacle avoidance code
import sys
import select
import tty
import termios
import pi2go, time

pi2go.init()
speed = 50
# serial connection to arduino for indicators
ard = serial.Serial('/dev/ttyUSB0',9600);
#tollgate 3 task 2
#lane change definition from inner lane to outer lane 
def left():
    pi2go.go(40,60)
    time.sleep(2.45)#1.92
    pi2go.go(60,35)
    time.sleep(1)
# lane change definition from outer lane to inner lane   
def right():
    pi2go.go(60,40)
    time.sleep(1.1)#1.45
    pi2go.go(35,60)
    time.sleep(1) 
# Tollgate 2 task 1a
# line follow based on the line sensor output of pi2go
def line(speed):
    left = pi2go.irLeftLine()
    right = pi2go.irRightLine()  
    if left == False and right == True:
        pi2go.forward(speed)
    elif right == True and left == True:
        pi2go.spinLeft(speed - 20) # speed-20 to smoothen the line follow
    elif left == True and right == False:
        pi2go.spinRight(speed - 20)  # speed-20 to smoothen the line follow
    elif left == False and right == False:
        pi2go.forward(speed)

#uses the IR sensors on the left,right & front of pi2go to check if there are any obstacle
def isObstaclePresent():
    if pi2go.irAll():
        return True
    else:
        return False

		
# for command line interaction
def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())
    i = 0 # mode
    while 1:
        dist = int(pi2go.getDistance())
        dist = dist/4 # dist/4 is approx 18~20 cm
        print 'mode=',i
        print 'linefollow'
        line(speed)
# Tollgate 3 Task 1
# if detects obstacle at 18~20 cm, it slows down & if less, the bot stops else it continues following line with speed = 50 
        if dist< 4:
        pi2go.stop()   
           print 'stop'
           time.sleep(1.5)
        elif dist == 4:
          speed = 30
		  print 'speed = 30'
        if isData():
            c = sys.stdin.read(1)
            if c == '\x6c':         # lane change 'l'
                print 'mode =', i+1
                print 'left-lane change'
                ard.write('2') #LED blink for lane change
                left()
                ard.write('4')# blink stops			
            elif c == '\x72': # lane change 'r'
                print 'mode =', i+1
                print 'right-lanechange'
                ard.write('3')# LED blink control to arduino
                right()
				ard.write('4')#LED blink stops after lane change action
            elif c == '\x20': #spacebar
                print 'stop'
                ard.write('1') #
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
        else:
		    speed = 50
			i = 0
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    pi2go.cleanup()
    