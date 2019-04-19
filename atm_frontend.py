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
		for user in users:
			if pin == user["pin"]:
				if "card_num" in request.args:
					card_num = int(request.args["card_num"])
				else:
					return "No card number specified.", 404

				token = generate_access_token(pin, card_num)
				global verifiedUsers
				verifiedUsers[token] = (user["pin"], user["card_num"])
				print(verifiedUsers)
				packet = {"text": "Welcome", "token":token}

				return packet, 200
			else:
				if "card_num" in request.args:
					card_num = int(request.args["card_num"])
				else:
					return "No card number specified.", 404

				packet = {"text": "Burn", "token":""}
				return packet, 404

	def post(self, name):
		age = request.args.get("age")
		occupation = request.args.get("occupation")

		if age is None or occupation is None:
			return "Cannot pass empty arguments to new user", 400

		for user in users:
			if name == user["name"]:
				return "User {} already exists".format(name), 400

		user = {
			"name": name,
			"age": age,
			"occupation": occupation
		}
		users.append(user)
		return user, 201

	def put(self, token):
		if validToken(token):
			for user in users:
				if user["pin"] == verifiedUsers[token][0] and user["card_num"] == verifiedUsers[token][1]:
					subtract_amount = int(request.args["amount"])
					user["balance"] -= subtract_amount
					return user, 201

	def delete(self, name):
		global users
		users = [user for user in users if user["name"] != name]
		return "{} is deleted".format(name), 200


# @app.route('/verified/token')
# api.add_resource(User, "/user/")
api.add_resource(User, "/user/<int:token>")
# api.add_resource(User, resourceString)
app.run(host="0.0.0.0", debug=True)