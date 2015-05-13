import socket
import Pyro4
import sys
from random import random, randint

try:
    myIp = str(socket.gethostbyname(socket.gethostname()))
    Pyro4.config.THREADPOOL_SIZE = 2000
    port_num = randint(7000,9999)
    Pyro4.naming.startNSloop(host=myIp, port=port_num)
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise