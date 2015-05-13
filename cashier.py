import Pyro4
import json
import random
from threading import Thread
from time import sleep

Pyro4.config.REQUIRE_EXPOSE = True

bill={}
handling_customer = False
uri = ""
counter=0
class Cashier(object):
    @Pyro4.expose
    def listen(self,from_person,from_name,msg):
        respond_t = Thread(target = respond, args=(from_person, from_name, msg) )
        respond_t.start()
        return ""


def serve_customer():
    while True:
        customer_queue = Pyro4.Proxy("PYRONAME:lavic.queue.customer")
        next_customer= Pyro4.Proxy("PYRONAME:"+customer_queue.getNextCustomer())
        customer_queue._pyroRelease()
        global handling_customer
        print next_customer
        if not(next_customer is None):
            print next_customer.listen("Cashier" ,uri , get_greet_msg())
            handling_customer = True
            while handling_customer:
                sleep(1)
        else:
            print "its none"
        next_customer._pyroRelease()
        sleep(1)


def cashier_thread():
	cashier = Cashier()
	daemon = Pyro4.Daemon("192.168.0.20")
	global uri
	uri = daemon.register(cashier)
	print "Cashier on duty : ", uri
	daemon.requestLoop()


def getToken():
    global counter
    counter=counter+1
    return str(random.randrange(0, 101, 2))+str(counter)+str(random.randrange(0, 101, 2))


def calculate_bill(customer_order):
    global bill
    bill ={}
    order={}
    order['tokenNumber']=getToken()
    orderDetails=[]
    cost=0
    menu_card = Pyro4.Proxy("PYRONAME:lavic.menucard")
    for customer_order_item in customer_order['order']['orderDetails']:
            orderItem={}
            print "*******"+json.dumps(menu_card.getItem(customer_order_item['itemName']))
            orderItem['itemName']=customer_order_item['itemName']
            orderItem['unitCost']=menu_card.getItem(customer_order_item['itemName'])["price"]
            cost=cost+float(orderItem['unitCost'])
            orderItem['quantity']=customer_order_item['quantity']
            orderDetails.append(orderItem)
    menu_card._pyroRelease()
    order['orderDetails']=orderDetails
    order['cost']=cost
    order['tax']=0.10
    order['total']=cost * 0.10
    bill['order']=order
    return bill




def respond(from_person, from_name, msg):
    parsed_msg = msg
    if parsed_msg['messageType'] == "HELLO":
        respond_to_hello(from_person, from_name, msg)
    elif parsed_msg['messageType'] == "INTERACTION":
        respond_to_interaction(from_person,from_name,msg)
    elif parsed_msg['messageType'] == 'BBYE':
        respond_to_bye(from_person,from_name,msg)
    elif parsed_msg['messageType'] == 'ORDER_REQUEST':
        respond_to_order_request(from_person,from_name,msg)
    elif parsed_msg['messageType'] == 'PAYMENT_REQUEST':
        respond_to_payment_request(from_person,from_name,msg)




def respond_to_hello(from_person,from_name,msg):
    print from_person+" ["+from_name+"] : "+json.dumps(msg)
    customer = Pyro4.Proxy("PYRONAME:"+from_name)
    customer.listen("Cashier",uri,get_order_question_msg())
    customer._pyroRelease()

def respond_to_interaction(from_person,from_name,msg):
    print from_person+" ["+from_name+"] : "+json.dumps(msg)
    customer = Pyro4.Proxy("PYRONAME:"+from_name)
    customer.listen("Cashier",uri,get_order_question_msg())
    customer._pyroRelease()

def respond_to_order_request(from_person,from_name,msg):
    print from_person+" ["+from_name+"] : "+json.dumps(msg)
    customer = Pyro4.Proxy("PYRONAME:"+from_name)
    customer.listen("Cashier",uri,get_payment_request_msg(msg))
    customer._pyroRelease()

def respond_to_payment_request(from_person,from_name,msg):
    print from_person+" ["+from_name+"] : "+json.dumps(msg)
    customer = Pyro4.Proxy("PYRONAME:"+from_name)
    customer.listen("Cashier",uri,get_payment_made_msg())
    customer._pyroRelease()

def respond_to_bye(from_person,from_name,msg):
    global handling_customer
    handling_customer=False
    pending_request_queue = Pyro4.Proxy("PYRONAME:lavic.queue.pendingOrders")
    pending_request_queue.addOrder(get_order_incomplete_msg())
    print from_person+" ["+from_name+"] : "+json.dumps(msg)
    customer = Pyro4.Proxy("PYRONAME:"+from_name)
    customer.listen("Cashier",uri,get_bye_msg())
    customer._pyroRelease()





def get_greet_msg():
    msg={}
    msg['messageType']="HELLO"
    msg['message']="Hello, Welcome to Lavic. :) "
    return msg

def get_order_question_msg():
    msg={}
    msg['messageType']="ORDER_REQUEST"
    msg['message']="What would you like to have today ?"
    return msg



def get_order_incomplete_msg():
    msg={}
    msg['messageType']="ORDER_INCOMPLETE"
    msg['message']=''
    msg['order']=bill['order']
    return msg

def get_payment_request_msg(customer_order_msg):
    msg={}
    msg['messageType']="PAYMENT_REQUEST"
    msg['message']=''
    msg['order']=calculate_bill(customer_order_msg)
    return msg


def get_payment_made_msg():
    msg={}
    msg['messageType']="PAYMENT_MADE"
    msg['message']=' '
    msg['order']=bill['order']
    return msg

def get_bye_msg():
    msg={}
    msg['messageType']="BBYE"
    msg['message']="Thank you. Visit Us Again"
    return msg


if __name__ == "__main__":
    cash_t = Thread(target = cashier_thread)
    serve_customer_t = Thread(target = serve_customer)
    serve_customer_t.start()
    cash_t.start()
    serve_customer_t.join()
    cash_t.join()
    print "Lavik is closed now"








