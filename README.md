# Adidas-Order-Checker

Easier way to check multiple Adidas.com orders.

*Requires Python 2.7 and Requests

### Setup

1. Rename orderinfo_example.txt to orderinfo.txt and ordernumbers_example.txt to ordernumbers.txt
2. Edit main.py and change sleep_time if you'd like a delay between checking each order
3. Run main.py

### Order Checker

If you select this option it will check the status of all of the orders in orderinfo.txt

### Order Adder

If you select this option it will format the order numbers in ordernumbers.txt into the correct format in orderinfo.txt

Only select this option if you have multiple orders under the same email address

Otherwise, format orders into orderinfo.txt in the format listed in orderinfo_example.txt