from flask import Flask, request
from flask_restful import Resource, Api
import random
import requests
import json

app = Flask(__name__)

api = Api(app)

def generate_access_token(pin, card_num):
	random.seed(card_num)
	return random.randint(0,pin)

localCacheUsers = [
	{
		"pin": 1001,
		"card_num": 1,
		"balance": 1000
	},
	{
		"pin": 1002,
		"card_num": 2,
		"balance": 12400
	},
	{
		"pin": 1003,
		"card_num": 3,
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
		pin = int(request.args["pin"])
		card_num = int(request.args["card_num"])

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
				packet = {"text": "FAIL: Wrong pin for given card number or account not existent", "token":""}
				return packet, 404

	def put(self, token):  # Do operation on connected account
		if validToken(token):
			for user in localCacheUsers:
				if user["pin"] == verifiedUsers[token][0] and user["card_num"] == verifiedUsers[token][1]:
					subtract_amount = int(request.args["amount"])
					if subtract_amount > user["balance"]:
						return "Not enough funds", 404
					else:
						user["balance"] -= subtract_amount
					return user, 201
			return "Information mismatch, token exists, card number and pin dont match", 404
		return token + "token not found", 404

def update_local_user_cache():
	def get_users_from_HQ(_url = 'http://127.0.0.1:6000/atm/users'):
		responseDict = {}
		req = requests.get(url=_url)
		print(req.url)
		print(req.status_code)
		responseDict = json.loads(req.content) # unpack b' format to dictionary
		print(responseDict)
		return responseDict
	updated_user_dict = get_users_from_HQ()

	def merge_user_bases(users_to_integrate):
		for user in users_to_integrate:
			if user in localCacheUsers:
				pass
			else:
				localCacheUsers.append(user)
	merge_user_bases(updated_user_dict)

api.add_resource(User, "/user/<int:token>")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)