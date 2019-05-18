#!/usr/bin/python3
import requests
import json

url = 'http://0.0.0.0:5000'
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'		# No Color

def main():
	while(1):
		def getToken(responseDict):
			return int(responseDict["token"]) if responseDict["token"] is not "" else -1

		def getBalance(responseDict):
			return int(responseDict["balance"]) if responseDict["balance"] >=0 and responseDict["balance"] is not "" else -1

		print("\nPlease insert info")
		try:
			card_num = input("Insert card num: ")
			if card_num.isdigit():
				pin = input("Insert PIN: ")
				if pin.isdigit():
					req = requests.get(url + "/user/0", params={"card_num":card_num, "pin": pin})
				else:
					print(RED+"Only numbers allowed"+NC)
					continue
			else:
				print(RED+"Only numbers allowed"+NC)
				continue
		except requests.RequestException as e:
			print(RED, e, "\n", NC)
			print(RED+"Couldn't connect to ATM server, is it open? (0.0.0.0:5000 - default)"+NC)
			continue
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		if req.status_code == 420:
			print(RED+"That card number/pin combo doesn't exist, please retry"+NC)
			continue

		token = getToken(responseDict)
		balance = getBalance(responseDict)
		while req.status_code != 420:
			try:
				print(GREEN+"Available balance: {}".format(balance)+NC)
				try:
					amount = input("\nInsert amount to subtract (Ctrl+D to go back): ")
					if amount.isdigit():
						req = requests.put(url + "/user/" + str(token), params={"amount": amount})
					else:
						print(RED+"Only numbers allowed"+NC)
				except requests.RequestException as e:
					print(RED, e, "\n", NC)
					print(RED+"Couldn't connect to ATM server, is it open? (0.0.0.0:5000 - default)"+NC)
					break
				if req.status_code == 200:
					responseDict = json.loads(req.content) # unpack b' format to dictionary
					balance = getBalance(responseDict)
				else:
					if req.status_code // 100 == 4: # Minor error, insufficient funds (411)
						print(RED+req.text+NC)
					else:
						print(RED+"Untreated error"+NC)
			except EOFError:
				break

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print(CYAN+"\nProgram terminated"+NC)
		exit(0)
