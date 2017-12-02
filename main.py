import requests
import re
from time import sleep

sleep_time = 0 #Delay between checking each order

def smart_sleep(b):
	for a in xrange (b, 0, -1):
		print 'Sleeping for {} seconds...\r'.format(str(a)), 
		sleep(1)
	print 'Sleeping for {} seconds complete!\n'.format(str(b))

def find_between(soup, first, last):
	try:
	    start = soup.index( first ) + len( first )
	    end = soup.index( last, start )
	    return soup[start:end]
	except ValueError:
	    return ''

def order_checker():
	with open('orderinfo.txt', 'r') as myfile:
		info = myfile.read().split('\n')

	emails = [information.split(':')[0] for information in info if information != '']	
	order_numbers = [information.split(':')[1] for information in info if information != '']

	orders_processing = []
	orders_confirmed = []
	orders_shipped = []
	orders_delivered = []
	failed_orders = []

	print 'Checking {} orders...\n'.format(len(order_numbers))

	for order_number in order_numbers:
		session = requests.Session()

		headers = {
		    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		    'Connection': 'keep-alive',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'en-US,en;q=0.9',
		    'Upgrade-Insecure-Requests': '1',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
		}

		response = session.get('https://www.adidas.com/us/order-tracker', headers=headers)

		form_actions = re.findall(r'<form action="(.*?)"', response.content)
		request_link = [form_action for form_action in form_actions if 'order-tracker' in form_action][0]

		headers = {
		    'Origin': 'https://www.adidas.com',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'en-US,en;q=0.9',
		    'Upgrade-Insecure-Requests': '1',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		    'Cache-Control': 'max-age=0',
		    'Referer': 'https://www.adidas.com/us/order-tracker',
		    'Connection': 'keep-alive',
		}

		data = [
		  ('dwfrm_ordersignup_orderNo', '{}'.format(order_number)),
		  ('dwfrm_ordersignup_email', '{}'.format(emails[order_numbers.index(order_number)])),
		  ('dwfrm_ordersignup_signup', 'Track order'),
		]

		response = session.post(request_link, headers=headers, data=data)
		if response.status_code == 200:
			item = find_between(response.content, '<span class="name">', '</span>').replace('\n', '').title()
			size = find_between(response.content, '<span class="label">Size: </span>\n<span class="value">', '</span>').replace('\n', '').replace(' ', '').replace('-', '.5')
			try:
				content = response.content[response.content.index("<div class='order-step selected'"):]
				order_status = find_between(content, '<div class="order-step-content-wrp">', '</div>')
				if 'Order processing' in order_status:
					order_status = 'Order processing'
					orders_processing.append(order_number)
				elif 'Order confirmed, waiting to be packed' in order_status:
					order_status = 'Order confirmed, waiting to be packed'
					orders_confirmed.append(order_number)
				elif 'Shipped' in order_status:
					order_status = 'Shipped'
					orders_shipped.append(order_number)
				elif 'Delivered' in order_status:
					order_status = 'Delivered'
					orders_delivered.append(order_number)
				else:
					failed_orders.append(order_number)
					print '[Order #{}] Error retrieving order order status\n'.format(order_number)
				print '[Order #{}] {} - {}\n{}\n'.format(order_number, item, size, order_status)
			except:
				print order_number, emails[order_numbers.index(order_number)]
				failed_orders.append(order_number)
				print '[Order #{}] Error retrieving order order status\n'.format(order_number)
		else:
			print order_number, emails[order_numbers.index(order_number)]
			failed_orders.append(order_number)
			print '[Order #{}] Error retrieving order order status\n'.format(order_number)
		
		if sleep_time != 0:
			smart_sleep(sleep_time)

	print 'Order checking complete\n\n{} orders processing\n{} orders confirmed\n{} orders shipped\n{} orders delivered\n{} orders failed to check\n'.format(len(orders_processing), len(orders_confirmed), len(orders_shipped), len(orders_delivered), len(failed_orders))

	if orders_processing != []:
		orders_processing = ['{}:{}'.format(emails[order_numbers.index(order_number)], order_number) for order_number in orders_processing]
		orders_processing = '\n'.join(orders_processing)
	else:
		orders_processing = 'None'
	if orders_confirmed != []:
		orders_confirmed = ['{}:{}'.format(emails[order_numbers.index(order_number)], order_number) for order_number in orders_confirmed]
		orders_confirmed = '\n'.join(orders_confirmed)
	else:
		orders_confirmed = 'None'
	if orders_shipped != []:
		orders_shipped = ['{}:{}'.format(emails[order_numbers.index(order_number)], order_number) for order_number in orders_shipped]
		orders_shipped = '\n'.join(orders_shipped)
	else:
		orders_shipped = 'None'
	if orders_delivered != []:
		orders_delivered = ['{}:{}'.format(emails[order_numbers.index(order_number)], order_number) for order_number in orders_delivered]
		orders_delivered = '\n'.join(orders_delivered)
	else:
		failed_orders = 'None'
	if failed_orders != []:
		failed_orders = ['{}:{}'.format(emails[order_numbers.index(order_number)], order_number) for order_number in failed_orders]
		failed_orders = '\n'.join(failed_orders)
	else:
		failed_orders = 'None'

	results = 'Orders Processing\n\n{}\n\nOrders Confirmed\n\n{}\n\nOrders Shipped\n\n{}\n\nOrders Delivered\n\n{}\n\nOrders Failed to Check\n\n{}'.format(orders_processing, orders_confirmed, orders_shipped, orders_delivered, failed_orders)

	with open('results.txt', 'w') as myfile:
		myfile.write(results)

	print 'Results saved to text file'

def order_adder():
	with open('ordernumbers.txt', 'r') as myfile:
		order_numbers = myfile.read().split('\n')
	email = raw_input('Email Address: ')
	overwrite = raw_input('Overwrite current order info (y/n): ').lower()
	info = ['{}:{}'.format(email, order_number) for order_number in order_numbers]
	if overwrite == 'y':
		with open('orderinfo.txt', 'w') as myfile:
			for information in info:
				myfile.write('{}\n'.format(information))
	elif overwrite == 'n':
		try:
			with open('orderinfo.txt', 'a') as myfile:
				for information in info:
					myfile.write('{}\n'.format(information))
		except:
			with open('orderinfo.txt', 'w') as myfile:
				for information in info:
					myfile.write('{}\n'.format(information))
	else:
		print '\nYou did not choose a valid option, try again\n'
		order_adder()
	print '\n{} orders added\n'.format(len(info))

def decision():
	choice = str(raw_input('Select an option by entering the corresponding number.\n\nOrder Checker (1) | Order Adder (2) | Quit (3)\nChoice: '))
	print ''
	if choice == '1':
		order_checker()
	elif choice == '2':
		order_adder()
	elif choice == '3':
		quit()
	else:
		print 'You did not choose a valid option, try again.\n'
		decision()

print '\nAdidas Order Checker by @DefNotAvg\n'

while True:
	decision()
	raw_input('Task complete. Click enter to run again.')