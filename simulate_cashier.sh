echo 'Enter the number of customers'
read customers
for i in `seq 1 $customers`
do
	osascript -e 'tell application "Terminal" to do script "/Users/omkargudekar/Desktop/customer.py 1 '+$i+'"'
done  


