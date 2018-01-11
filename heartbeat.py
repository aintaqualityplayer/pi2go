# initially created hearbeat code and it uses LCM
import threading
import GPS as gps
from time import sleep
import time,os
from deis2016comm import heartbeat_t, merging_t, platooning_t
import lcm
from operator import itemgetter
import math
import detect as fun
import pi2go

lc = lcm.LCM("udpm://224.0.0.1:7667?ttl=10")
#def send_lcm_heartbeat():
print "ready to send"
global pre_y,pre_x
global lc,id
#id_,x_,y_ = gps.gps_client(id)
msg = heartbeat_t()
msg.id = 6
msg.timestamp = time.time()
#msg.x = x_
#msg.y = y_
#msg.speed = speed_(x_,y_,preX,preY)
msg.direction = -1                  #we don't use the direction here, just remain for no reason
msg.platoon_id = platoon_id
msg.platoon_pos = platoon_pos
lc.publish('HEARTBEAT',msg.encode())
print "send heartbeat"
