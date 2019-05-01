import requests
from requests.auth import HTTPDigestAuth
import json

url = 'http://127.0.0.1:5000'

def main():
	while(1):
		def getToken(responseDict):
			return int(responseDict["token"]) if responseDict["token"] is not "" else -1

		def getBalance(responseDict):
			return int(responseDict["balance"]) if responseDict["balance"] is not "" else -1

		print("Please insert info.")
		req = requests.get(url + "/user/0", params={"card_num":input("Insert card num: "), "pin":input("Insert PIN: ")})
		# print(req.url)
		# print(req.status_code)
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		# print(responseDict)

		token = getToken(responseDict)
		balance = getBalance(responseDict)
		while req.status_code == 200 or req.status_code == 201:
			try:
				print("Available balance: {}".format(balance))
				req = requests.put(url + "/user/" + str(token), params={"amount":input("Insert amount to subtract (Ctrl+D to go back)")})
			except EOFError:
				break
			print(req.url)
			print(req.status_code)
			print(req.content)

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print("\nProgram terminated")
		exit(0)
