
#tollgate 2, task 1a,1b and 1c
import pi2go,time
import sys

pi2go.init()

speed = 60

# based on time = speed/distance

try:
 initial_time = time.time()
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
   final_time =int(time.time() - x) 
   print final_time
   if final_time == 15:
     break  

 pi2go.stop()
 print 'stop'
 time.sleep(50)

finally:
   pi2go.cleanup()
   sys.exit(0)
