import Pyro4
import Queue
import json
import random
import sys
from time import sleep
from threading import Thread
from RequestProcessor import RequestProcessor

Pyro4.config.REQUIRE_EXPOSE = True

speed = {
	'slow' : 0.5,
	'normal' : 1,
	'fast' : 2
}

""" ***** Customer class ***** """
class Customer(object):

	def __init__(self, customer_name, speed, queue_to_join):
		print 'initializing customer ', customer_name
		self.customer_name = customer_name
		self.speed = speed
		self.queue_to_join = queue_to_join

		#set customer likings/preferences
		

	def speak(self, to_person, what):
		print 'speaking to ', to_person
		respont_to_person = Pyro4.Proxy(to_person)
		respont_to_person.listen('customer', self.customer_name, what)
		respont_to_person._pyroRelease()

	@Pyro4.expose
	def listen(self, from_person, name, message):
		#print "MESSSAGE RECEIVED"
		json_message = message #json.loads(message)
		message_type = json_message['messageType']
		json_message['fromName'] = name
		#print 'message', json_message
		self.request_queue.put(json_message)
		#print 'enqueued'

	def join_queue(self):
		print 'Customer joining the cashier queue ', self.customer_name
		self.queue_to_join.register(self.customer_name)

	def ativate_customer(self):
		def activate():
			"""register to the nameserver"""
			self.daemon=Pyro4.Daemon("192.168.0.39")
			ns=Pyro4.locateNS()#(host = "PYRO:Pyro.NameServer")
			uri=self.daemon.register(self)
			ns.register(self.customer_name, uri)
			
			"""Create queue and thread for listening to requests"""
			self.request_queue = Queue.Queue();
			self.request_processor = RequestProcessor(self, self.speed)
			self.request_processor.start()

			"""Join cashier queue"""
			self.join_queue();
			self.daemon.requestLoop()
			print 'SHUTTTING DOWN Daemon'
		self.active_thread = Thread(target=activate)
		self.active_thread.start()
		print 'customer activated'

	def shutdown_customer(self):
		self.request_processor.shutdown()
		Pyro4.locateNS().remove(self.customer_name)
		self.daemon.shutdown()
		print 'shutting down customer'

	def getOrderDetails(self):
		menuObj = Pyro4.Proxy("PYRONAME:lavic.menucard")
		menu = menuObj.getmenucard()
		menuObj._pyroRelease()
		num_of_items = random.randint(1,3)
		orderDetails = []
		#print 'numer of itesm', num_of_items
		for i in range(num_of_items):
			itemName = random.choice(menu['menu']).keys()[0]
			quantity = random.randint(1,3)
			this_order = {'itemName' : itemName , 'quantity':quantity }
			orderDetails.append(this_order)
		#print 'Customer order: ', orderDetails
		return orderDetails

	def checkIfMyOrder(self, token_num):
		#return True
		try:
			print 'my token ', self.reciept['order']['tokenNumber']
			print token_num
			if token_num == self.reciept['order']['tokenNumber']:
				print 'returning true'
				return True
		except:
			pass
		return False

	def set_receipt(self, reciept):
		print '@@@@@@@@@@saving reciept ', reciept
		self.reciept = reciept


""" ***** Customer class ends ***** """

def create_customer(customer_name, speed):
	try:
		queue_to_join = Pyro4.Proxy("PYRONAME:lavic.queue.customer")
	except:
		print 'no queue found'
		return
	print queue_to_join
	customer_name = "lavic.customer." + customer_name
	customer = Customer(customer_name, speed, queue_to_join)
	customer.ativate_customer()
	queue_to_join._pyroRelease()
	return customer

def generate_customers(frequency, max_customers, speed):
	count = 0
	while True:
		print 'running ',frequency, max_customers, speed
		if(max_customers == -1 or count < max_customers):
			count += 1 
			customer_name = 'customer'+str(count)
			cust = create_customer(customer_name, speed)
			sleep(int(frequency/speed))
		else:
			print 'Generator finished'
			break

if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print 'not enough arguments'
		sys.exit()
	print 'creating customer'
	# create_customer('customer1', 1)
	# print sys.argv[2]
	# print sys.argv[1]
	create_customer(sys.argv[2], sys.argv[1])
	#generate_customers(2,30,1)




	