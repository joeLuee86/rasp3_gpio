#!/usr/bin/python
#
#


import threading
import time
import socket
 

threadLock = threading.Lock()
threads = []

gList = [0, 0, 0, 0]

def func1(params):
	print "func1" , params

def func2(params):
	print "func2" , params

def func3(params):
	print "func3" , params

CmdHdl = {
	"1" : func1,
	"2" : func2,
	"3" : func3
}

if __name__ == "__main__":

	s = socket.socket()         # ?? socket ??
	host = socket.gethostname() # ???????
	port = 1234                # ????
	s.bind(("10.233.140.214", port))        # ????

	s.listen(5)                 # ???????
	while True:
	    c, addr = s.accept()     # ????????
	    print '????:', addr
	    print c.recv(1024)
	    c.close()                # ????