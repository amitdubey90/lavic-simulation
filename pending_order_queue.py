from Queue import Queue
import socket
import Pyro4

Pyro4.config.REQUIRE_EXPOSE = True

pendingQueue = Queue();
class PendingQueue:

    @Pyro4.expose
    def addOrder(self, order):
        pendingQueue.put(order)
        print "-------------------------"
        print order
        print "-------------------------"

    @Pyro4.expose
    def getOrder(self):
        if(pendingQueue.not_empty):
            return pendingQueue.get()
        else:
            return 0

    @Pyro4.expose
    def getNumberOfOrders(self):
        return pendingQueue.qsize()

orderQueue=PendingQueue()
myIp = str(socket.gethostbyname(socket.gethostname()))
daemon = Pyro4.Daemon(myIp)                 # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(orderQueue)   		  # register the greeting object as a Pyro object
ns.register("lavic.queue.pendingOrders", uri)
print "Ready. Object uri =", uri      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls