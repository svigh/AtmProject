from flask import Flask, request
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import random

app = Flask(__name__)

api = Api(app)
ma = Marshmallow(app)
resourceString = ""

def generate_access_token(pin, card_num):
	random.seed(card_num)
	return random.randint(0,pin)

users = [
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
	def get(self, token):
		pin = int(request.args["pin"])
		card_num = int(request.args["card_num"])

		for user in users:
			print(user)
			if pin == user["pin"] and card_num == user["card_num"]:
				token = generate_access_token(pin, card_num)
				global verifiedUsers
				verifiedUsers[token] = (user["pin"], user["card_num"])
				print(verifiedUsers)
				packet = {"text": "Welcome", "token":token}
				return packet, 200

		packet = {"text": "Wrong pin for given card number", "token":""}
		return packet, 404

	def put(self, token):
		if validToken(token):
			for user in users:
				if user["pin"] == verifiedUsers[token][0] and user["card_num"] == verifiedUsers[token][1]:
					subtract_amount = int(request.args["amount"])
					if subtract_amount > user["balance"]:
						return "Not enough funds", 404
					else:
						user["balance"] -= subtract_amount
					return user, 201
			return "Information mismatch, token exists, card number and pin dont match", 404
		return token + "token not found", 404

	def delete(self, name):
		global users
		users = [user for user in users if user["name"] != name]
		return "{} is deleted".format(name), 200

api.add_resource(User, "/user/<int:token>")

app.run(host="0.0.0.0", debug=True)