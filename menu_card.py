__author__ = 'dhavalkolapkar'
import json
import Pyro4
import socket

Pyro4.config.REQUIRE_EXPOSE = True

class MenuCard(object):

    def __init__(self):
        self.menu_card =json.loads(open("/Users/omkargudekar/Desktop/laviktest/xyz.json").read())

    @Pyro4.expose
    def getmenucard(self):
        return self.menu_card

    @Pyro4.expose
    def getItem(self, lookup):
       for key, value in self.menu_card.items():
           #print key
           for v in value:
               # print v
                for innerKey,innerValue in v.items():
                    if lookup in innerKey:
                        return innerValue;

menuCard=MenuCard()
myIp = str(socket.gethostbyname(socket.gethostname()))
#print("My IP Address: " + myIp)
daemon=Pyro4.Daemon(myIp) #make a Pyro daemon
ns=Pyro4.locateNS()
uri=daemon.register(menuCard) #register the greeting object as a Pyro object
ns.register("lavic.menucard", uri)
#print("Ready. uri =" + str(uri)) #print the uri so we can use it in the client later
print "Menucard service started!"
daemon.requestLoop() # start the even