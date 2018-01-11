
#tollgate 2, task 1a

import pi2go,time
import sys

pi2go.init()

speed = 60

try:

 while True:
   left = pi2go.irLeftLine()
   right = pi2go.irRightLine()
   if left == False and right == True:
      pi2go.forward(speed)
   elif left == True and right == True:
      pi2go.spinLeft(speed - 20)
   elif left == True and right == False:
      pi2go.spinRight(speed-20)
   elif left == False and right == False:
     pi2go.forward(speed)

finally:
   pi2go.cleanup()
   sys.exit(0)
