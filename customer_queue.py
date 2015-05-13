import Pyro4
import Queue

Pyro4.config.REQUIRE_EXPOSE = True

queue = Queue.Queue()

class CustomerQueue(object):

    @Pyro4.expose
    def register(self, name):
        print name
        queue.put(name)

    @Pyro4.expose
    def getNextCustomer(self):
        return queue.get()

custQueue=CustomerQueue()
daemon=Pyro4.Daemon("192.168.0.20")                 # make a Pyro daemon
ns=Pyro4.locateNS()
uri=daemon.register(custQueue)   		  # register the greeting object as a Pyro object
ns.register("lavic.queue.customer", uri)
print "Ready. Object uri =", uri      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
