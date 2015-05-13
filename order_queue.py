__author__ = 'Harsh Malewar'

import Pyro4
import Queue
import json
import socket

Pyro4.config.REQUIRE_EXPOSE = True

ordersQueue = Queue.Queue()
counter=0
class OrderQueue(object):

    def __init__(self):
        print("Queue started")

    @Pyro4.expose
    def get_order(self):
        #        ret = ordersQueue.get()
        #print 'Queueu returning ', ret
        #ordersQueue.task_done()
        global counter
        counter=counter+1
        print counter
        return ordersQueue.get()

    @Pyro4.expose
    def add_order(self, json_message):
        print("New order received!")
        ordersQueue.put(json_message)


order = OrderQueue()
myIp = str(socket.gethostbyname(socket.gethostname()))
print("My IP Address: " + myIp)
daemon=Pyro4.Daemon(myIp)                 # make a Pyro daemon
ns=Pyro4.locateNS()
uri=daemon.register(order)        # register the greeting object as a Pyro object
ns.register("lavic.server", uri)
print("Ready. uri =" + str(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
