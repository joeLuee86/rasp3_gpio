#!/usr/bin/python
#
#


import threading
import time
import socket
 

s = socket.socket()         # ?? socket ??
host = socket.gethostname() # ???????
port = 1234                # ?????

s.connect(("10.233.140.214", port))
s.send("Hello, World!")
s.close()  