import socket
import sys
import time
import struct
import math


def gps_client(id_):
	
	server_ip = '194.47.3.234'
        host = ""
        server_port = 9090
        my_port = 9091


        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
                print 'Failed to create socket'
                sys.exit()
        try:
	 	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error:
		print 'Socket reuse unsuccess'
	s.settimeout(1)
        #ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	try:
        	s.bind((host,my_port))
	except socket.error:
		print 'Socket not  binded'

        msg = struct.pack('>hhh',id_,0,0)   # Big Endian (>)


	while True:
		try:
        		s.sendto(msg,(server_ip,server_port))

	        	id = s.recv(1024)
	        	x = s.recv(1024)

		        y = s.recv(1024)
	       		id_ = struct.unpack('>h',id)[0]
		        x_ = struct.unpack('>h',x)[0]
        		y_ = struct.unpack('>h',y)[0]
	        	#print 'id x y',(id_,x_,y_)
	        	#time.sleep(0.01)
		except socket.timeout:
			id_ = -1
			x_ = 0
			y_ = 0
		#time.sleep(1)
		return id_,x_,y_

'''
while 1:
	id_,x_,y_=gps_client(6)
	print id_,x_,y_	

'''
