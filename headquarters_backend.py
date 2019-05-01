from flask import Flask, request
from flask_restful import Resource, Api
import random
import requests

app = Flask(__name__)

def valid_passKey(passKey):
	masterKey = 1234
	decodeCheck = 12340
	if passKey != 0 and passKey is not None:
		return decodeCheck // passKey == masterKey

api = Api(app)

globalCacheUsers = [
	{
		"card_num": 1,
		"pin": 1001,
		"balance": 1000
	},
	{
		"card_num": 2,
		"pin": 1002,
		"balance": 12400
	},
	{
		"card_num": 3,
		"pin": 1003,
		"balance": 102
	},
	{
		"card_num": 6,
		"pin": 1006,
		"balance": 666
	},
	{
		"card_num": 5,
		"pin": 1005,
		"balance": 555
	},
	{
		"card_num": 4,
		"pin": 1004,
		"balance": 10123
	}
]

class Atm(Resource):
	def get(self):	# Give users data
		return globalCacheUsers, 200
	def put(self):	# Get update balance after transaction
		pin = int(request.args["pin"])
		card_num = int(request.args["card_num"])
		balance = int(request.args["balance"])
		for user in globalCacheUsers:
			if user["card_num"] == card_num and user["pin"] == pin:
				user["balance"] = balance


class Admin(Resource):
	def get(self, passKey):		# Give all users
		if valid_passKey(passKey):
			return globalCacheUsers, 200
		return "ACCESS DENIED: wrong key", 408

	def post(self, passKey):	# Add a new user
		if valid_passKey(passKey):
			global globalCacheUsers
			newUser = {}
			card_num = int(request.args["card_num"])
			pin = int(request.args["pin"])
			balance = int(request.args["balance"])


			local_card_nums = [v for local_user in globalCacheUsers for (k,v) in local_user.items() if k == "card_num"]
			local_pin_nums = [v for local_user in globalCacheUsers for (k,v) in local_user.items() if k == "pin"]

			if card_num in local_card_nums and pin in local_pin_nums and local_card_nums.index(card_num) == local_pin_nums.index(pin):
				return "\nUser already exists", 412
			else:
				newUser["card_num"] = card_num
				newUser["pin"] = pin
				newUser["balance"] = balance
				globalCacheUsers.append(newUser)

			for user in globalCacheUsers:
				print(user)
			return globalCacheUsers, 200
		return "ACCESS DENIED: wrong key", 408

	def delete(self, passKey): 	# Delete a user
		if valid_passKey(passKey):
			global globalCacheUsers
			card_num = int(request.args["card_num"])
			pin = int(request.args["pin"])

			local_card_nums = [v for local_user in globalCacheUsers for (k,v) in local_user.items() if k == "card_num"]
			local_pin_nums = [v for local_user in globalCacheUsers for (k,v) in local_user.items() if k == "pin"]

			if card_num not in local_card_nums or pin not in local_pin_nums:
				return "\nUser doesn't exist", 412
			else:
				for user in globalCacheUsers:
					if user["card_num"] == card_num and user["pin"] == pin:
						del globalCacheUsers[globalCacheUsers.index(user)]
						return globalCacheUsers, 200
		else:
			return "ACCESS DENIED: wrong key", 408

api.add_resource(Atm, "/atm/users")
api.add_resource(Admin, "/admin/<int:passKey>")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="6000", debug=True)