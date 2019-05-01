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
			# print(req.url)
			# print(req.status_code)
			responseDict = json.loads(req.content) # unpack b' format to dictionary
			idx = 0
			for user in responseDict:
				idx+=1
				print("User ", idx, user)

		if option == "2":	# Add user
			req = requests.post(url + "/admin/" + input("Insert key: "), params={"card_num": input("Card number to add "), "pin": input("Pin number to add "), "balance" : input("Starting balance of the account ")})
			if req.status_code == 200:
				print("\nUser added with success")
			else:
				if req.status_code == 412:
					print("\nCouldn't add user, it already exists")
				else:
					print("\nCouldn't add user, untreated error code")

		if option == "3":	# Delete user
			req = requests.delete(url + "/admin/" + input("Insert key: "), params={"card_num": input("Card number to delete "), "pin": input("Pin number to delete ")})
			if req.status_code == 200:
				print("\nUser deleted with success")
			else:
				if req.status_code == 412:
					print("\nCouldn't delete user, it doesn't exist")
				else:
					print("\nCouldn't add user, untreated error code")

		if option == "4":	# Exit
			break

		# while req.status_code == 200 or req.status_code == 201:
		# 	try:
		# 		req = requests.put(url + "/user/" + str(token), params={"amount":input("Insert amount to subtract (Ctrl+D to go back)")})
		# 	except EOFError:
		# 		break
		# 	print(req.url)
		# 	print(req.status_code)
		# 	print(req.content)

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print("\nProgram terminated")
		exit(0)
