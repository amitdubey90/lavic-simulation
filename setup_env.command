osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/name_server.py" '
sleep 5
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/customer_queue.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/order_queue.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/pending_order_queue.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/menu_card.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/chef.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/cashier.py" '
sleep 2
osascript -e 'tell application "Terminal" to do script "python /Users/omkargudekar/Desktop/laviktest/cashier.py" '