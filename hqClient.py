import requests
from requests.auth import HTTPDigestAuth
import json

url = 'http://127.0.0.1:6000'

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
			req = requests.get(url + "/admin/" + input("Insert key: "))

			if req.status_code == 200:
				responseDict = json.loads(req.content) # unpack b' format to dictionary

				idx = 0
				for user in responseDict:
					idx+=1
					print("User ", idx, user)
			if req.status_code == 408:
				print(req.text)
			else:
				print("Untreated fail")


		if option == "2":	# Add user
			req = requests.post(url + "/admin/" + input("Insert key: "), params={"card_num": input("Card number to add "), "pin": input("Pin number to add "), "balance" : input("Starting balance of the account ")})

			if req.status_code == 200:		# SUCCESS
				print("\nUser added with success")
			else:
				if req.status_code == 412:	# Already exists
					print(req.text)
				if req.status_code == 408:	# Invalid passKey
					print(req.text)
				else:
					print("\nCouldn't add user, untreated error code")

		if option == "3":	# Delete user
			req = requests.delete(url + "/admin/" + input("Insert key: "), params={"card_num": input("Card number to delete "), "pin": input("Pin number to delete ")})

			if req.status_code == 200:		# SUCCESS
				print("\nUser deleted with success")
			else:
				if req.status_code == 412:	# Doesn't exist
					print(req.text)

				if req.status_code == 408:	# Invalid passKey
					print(req.text)
				else:
					print("\nCouldn't add user, untreated error code")

		if option == "4":	# Exit
			break

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print("\nProgram terminated")
		exit(0)
