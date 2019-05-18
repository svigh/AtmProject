#!/usr/bin/python3
import requests
import json

url = 'http://0.0.0.0:6000'
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'		# No Color

def main():
	while(1):
		print("Options:\n \
		1) Get list of all users\n \
		2) Add new user\n \
		3) Delete existing user\n \
		4) Exit\n \
		")
		option = input("Choose option ")

		if option == "1":	# Get users
			try:
				passKey = input("Insert passKey(10): ")
				if passKey.isdigit():
					req = requests.get(url + "/admin/" + passKey)
				else:
					print(RED+"Only numbers allowed"+NC)
					continue
			except requests.RequestException as e:
				print(RED, e, "\n", NC)
				print(RED+"Couldn't connect to HQ server, is it open? (0.0.0.0:6000 - default)"+NC)
				continue

			if req.status_code == 200:
				responseDict = json.loads(req.content) # unpack b' format to dictionary

				idx = 0
				for user in responseDict:
					idx+=1
					print(GREEN, "User ", idx, user, NC)
			else:
				if req.status_code // 100 == 4: # Invalid passKey
					print(RED+req.text+NC)
				else:
					print(RED+"Untreated fail"+NC)

		if option == "2":	# Add user
			try:
				passKey = input("Insert passKey(10): ")
				if passKey.isdigit():
					card_num = input("Card number to add: ")
					if card_num.isdigit():
						pin = input("Pin number to add: ")
						if pin.isdigit():
							balance = input("Starting balance of the account: ")
							if balance.isdigit():
								req = requests.post(url + "/admin/" + passKey, params={"card_num": card_num, "pin": pin, "balance": balance})
							else:
								print(RED+"Only numbers allowed"+NC)
								continue
						else:
							print(RED+"Only numbers allowed"+NC)
							continue
					else:
						print(RED+"Only numbers allowed"+NC)
						continue
				else:
					print(RED+"Only numbers allowed"+NC)
					continue

			except requests.RequestException as e:
				print(RED, e, "\n", NC)
				print(RED+"Couldn't connect to HQ server, is it open? (0.0.0.0:6000 - default)"+NC)
				continue
			if req.status_code == 200:		# SUCCESS
				print(GREEN+"\nUser added with success"+NC)
			else:
				if req.status_code // 100 == 4:	# Already exists (412) or invalid passKey (408)
					print(RED+req.text+NC)
				else:
					print(RED+"\nCouldn't add user, untreated error code"+NC)

		if option == "3":	# Delete user
			try:
				passKey = input("Insert passKey(10): ")
				if passKey.isdigit():
					card_num = input("Card number to delete: ")
					if card_num.isdigit():
						pin = input("Pin number to delete: ")
						if pin.isdigit():
							req = requests.delete(url + "/admin/" + passKey, params={"card_num": card_num, "pin": pin})
						else:
							print(RED+"Only numbers allowed"+NC)
							continue
					else:
						print(RED+"Only numbers allowed"+NC)
						continue
				else:
					print(RED+"Only numbers allowed"+NC)
					continue

			except requests.RequestException as e:
				print(RED, e, "\n", NC)
				print(RED+"Couldn't connect to HQ server, is it open? (0.0.0.0:6000 - default)"+NC)
				continue
			if req.status_code == 200:		# SUCCESS
				print(GREEN+"\nUser deleted with success"+NC)
			else:
				if req.status_code // 100 == 4:	# Doesn't exist (412) or invalid passKey (408)
					print(RED+req.text+NC)
				else:
					print(RED+"\nCouldn't delete user, untreated error code"+NC)

		if option == "4":	# Exit
			print(GREEN+"Graceful exit"+NC)
			break

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print(CYAN+"\nProgram terminated"+NC)
		exit(0)
