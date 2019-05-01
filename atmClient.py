import requests
from requests.auth import HTTPDigestAuth
import json

url = 'http://127.0.0.1:5000'
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'		# No Color

def main():
	while(1):
		def getToken(responseDict):
			return int(responseDict["token"]) if responseDict["token"] is not "" else -1

		def getBalance(responseDict):
			return int(responseDict["balance"]) if responseDict["balance"] and responseDict["balance"] is not "" else -1

		print("\nPlease insert info")
		req = requests.get(url + "/user/0", params={"card_num":input("Insert card num: "), "pin":input("Insert PIN: ")})
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		if req.status_code == 411:
			print(RED+"That card number/pin combo doesn't exist, please retry."+NC)
			continue

		token = getToken(responseDict)
		balance = getBalance(responseDict)
		while req.status_code == 200 or req.status_code == 201:
			try:
				print(GREEN+"Available balance: {}".format(balance)+NC)
				req = requests.put(url + "/user/" + str(token), params={"amount":input("\nInsert amount to subtract (Ctrl+D to go back)")})
				responseDict = json.loads(req.content) # unpack b' format to dictionary
				balance = getBalance(responseDict)
			except EOFError:
				break

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print(CYAN+"\nProgram terminated"+NC)
		exit(0)
