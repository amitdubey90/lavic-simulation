import Pyro4
import threading
import time
import json
import sys
import socket

Pyro4.config.REQUIRE_EXPOSE = True

class Server(object):

    def __init__(self, name):
        #threading.Thread.__init__(self)
        print("======================================================")
        print("")
        print("               NEW SERVER " + str(name).upper())
        print("")
        print("======================================================")
        print("Hi, my name is " + str(name) +". I'm starting my work")
        try:
            self.orders = Pyro4.Proxy("PYRONAME:lavic.server")
            self.ns=Pyro4.locateNS()
        except:
            print("Some problem connecting to queue. Exiting...")
            exit()
        self.order_json = None
        self.address = None

    def run(self):
        print("Time to work!")
        def loopFun():
            server_name = 'harsh'
            while True:
                try:
                    parsed_json = self.orders.get_order()
                    if parsed_json is not None:
                        message_type = parsed_json['messageType']
                        if message_type == "ORDER_COMPLETE":
                            print("Hey, this is " + serverName + " giving away the order")
                            token_number = parsed_json['order']['tokenNumber']
                            print("--------------------------------------")
                            print("    Announcing token "+ str(token_number) +"      |")
                            print("--------------------------------------")
                            parsed_json['messageType'] = "ORDER_PREPARED"
                            self.order_json = parsed_json
                            self._broadcast_customers()
                    time.sleep(6)
                except:
                    print("Some problem getting json")
        t = threading.Thread(target=loopFun)
        t.start()
        print("Worker thread started")


    @Pyro4.expose
    def take_order(self):
        print("===========================================================")
        print("    Hey! Thanks. Please take your order.Have a good day!")
        print("===========================================================")
        response_json = self.order_json
        self.order_json = None
        return response_json

    def activate(self):
        def act():
            myIp = str(socket.gethostbyname(socket.gethostname()))
            daemon=Pyro4.Daemon(myIp)                 # make a Pyro daemon
            ns=Pyro4.locateNS()
            uri=daemon.register(server)
            server.set_my_pyro(uri)
            ns.register("lavic.server.announcer2", uri)
            print("I'm ready at the counter. My Address =" + str(uri))
            daemon.requestLoop()
        t = threading.Thread(target=act)
        t.start()
        print 'server activated'


    def _broadcast_customers(self):
        count = 0
        customer_list = self.ns.list("lavic.customer.")
        shout_limit = 3
        print("BROADCASTING")
        for count in range(0, shout_limit):
            if not self.order_json is None:
                print("Announcing..." + str(count + 1))
                for customer in customer_list:
                    pyro_address = customer_list[customer]
                    print(str(customer) + " : " + pyro_address)
                    try:
                        customer_obj = Pyro4.Proxy(pyro_address)
                        customer_obj.listen("server", str(self.address), self.order_json )
                    except:
                        print("Some problem connecting to customers :" + str(customer))
            else:
                self.order_json = None
                return
            time.sleep(1)
        print ("No takers! Disposing order. Sorry.")

    def set_my_pyro(self, address):
        self.address = address



if __name__ == "__main__":

    serverName = str(sys.argv[1])
    if serverName == "":
        serverName = "John"
    if not serverName == "":
        server = Server(str(sys.argv[1]))
    else:
        server = Server("John")
    server.activate()
    server.run()

    #server.join()
    print 'starting daemon'