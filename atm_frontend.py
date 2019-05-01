from flask import Flask, request
from flask_restful import Resource, Api
import random
import requests
import json

app = Flask(__name__)

api = Api(app)

HQ_SERVER = 'http://127.0.0.1:6000/atm/users'

def generate_access_token(pin, card_num):
	random.seed(card_num)
	return random.randint(0,pin)

localCacheUsers = [
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
		"card_num": 12,
		"pin": 1112,
		"balance": 120
	},
	{
		"card_num": 3,
		"pin": 1003,
		"balance": 10
	}
]

verifiedUsers = {}

def validToken(token):
	if token in verifiedUsers:
		return 1
	return 0

class User(Resource):
	def get(self, token):	# Connect account to perform operations
		update_local_user_cache()
		card_num = int(request.args["card_num"])
		pin = int(request.args["pin"])

		def credentials_exist_locally():
			for user in localCacheUsers:
				if pin == user["pin"] and card_num == user["card_num"]:
					token = generate_access_token(pin, card_num)
					global verifiedUsers
					verifiedUsers[token] = (user["pin"], user["card_num"])
					return {"local_response": 1, "token": token, "balance": user["balance"]}
			return {"local_response": 0, "token": 0}

		local_creds = credentials_exist_locally()

		if local_creds["local_response"]:
			packet = {"text": "SUCCES", "token":local_creds["token"], "balance":local_creds["balance"]}
			return packet, 200
		else:
			print("Local cache might be mismatched with HQ.\nUpdating cache...")
			update_local_user_cache()
			local_creds = credentials_exist_locally()
			if local_creds["local_response"]:
				packet = {"text": "SUCCES", "token":local_creds["token"], "balance":local_creds["balance"]}
				return packet, 200
			else:
				packet = {"text": "FAIL: Wrong pin for given card number or account not existent", "token":"", "balance": -1}
				return packet, 420

	def put(self, token):  # Do operation on connected account
		if validToken(token):
			for user in localCacheUsers:
				if user["pin"] == verifiedUsers[token][0] and user["card_num"] == verifiedUsers[token][1]:
					subtract_amount = int(request.args["amount"])
					if subtract_amount > user["balance"]:
						return "Not enough funds", 411
					else:
						user["balance"] -= subtract_amount
						requests.put(url=HQ_SERVER, params={"card_num": user["card_num"], "pin": user["pin"], "balance": user["balance"]})	# Update master database
					return user, 200
			return "Information mismatch, token exists, card number and pin dont match", 420
		return str(token) + "token not found", 420

def update_local_user_cache():

	def get_users_from_HQ(_url = HQ_SERVER):
		responseDict = {}
		req = requests.get(url=_url)
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		return responseDict
	updated_user_dict = get_users_from_HQ()

	def merge_user_bases(users_to_integrate):
		global localCacheUsers

		for local_user in localCacheUsers:		# Update users balances from master database
			for user in users_to_integrate:
				if user["card_num"] == local_user["card_num"] and user["pin"] == local_user["pin"]:
					local_user["balance"] = user["balance"]


		local_card_nums = [v for local_user in localCacheUsers for (k,v) in local_user.items() if k == "card_num"]
		local_pin_nums = [v for local_user in localCacheUsers for (k,v) in local_user.items() if k == "pin"]

		for user in users_to_integrate:			# Fetch new users
			if user["card_num"] in local_card_nums and user["pin"] in local_pin_nums and local_card_nums.index(user["card_num"]) == local_pin_nums.index(user["pin"]):
				continue
			localCacheUsers.append(user)

		global_card_nums = [v for user in users_to_integrate for (k,v) in user.items() if k == "card_num"]
		global_pin_nums = [v for user in users_to_integrate for (k,v) in user.items() if k == "pin"]

		for local_user in localCacheUsers:		# Fetch deleted users
			if local_user["card_num"] not in global_card_nums and local_user["pin"] not in global_pin_nums:
				del localCacheUsers[localCacheUsers.index(local_user)]

	merge_user_bases(updated_user_dict)

api.add_resource(User, "/user/<int:token>")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)