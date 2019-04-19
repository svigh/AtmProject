import requests
from requests.auth import HTTPDigestAuth
import json

url = 'http://127.0.0.1:5000'

def getToken(responseDict):
	return int(responseDict["token"]) if responseDict["token"] is not "" else -1

def main():
	while(1):
		print("Please insert info.")
		req = requests.get(url + "/user/", params={"pin":input("Insert PIN"), "card_num":input("Insert card num")})
		print(req.url)
		print(req.status_code)
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		print(responseDict)
		print(getToken(responseDict))

if __name__ == "__main__":
	main()
