from flask import Flask, request
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
import random

app = Flask(__name__)

api = Api(app)
ma = Marshmallow(app)

def generate_access_token(pin, card_num):
	random.seed(card_num)
	return random.randint(0,pin)

users = [
	{
		"name": "John",
		"age": 32,
		"occupation": "student"
	},
	{
		"name": "Mark",
		"age": 12,
		"occupation": "engineer"
	},
	{
		"name": "DonaldTrump",
		"age": 60,
		"occupation": "idiot"
	}
]

class User(Resource):
	def get(self):
		pin = int(request.args["pin"])
		if pin == 1234:
			if "card_num" in request.args:
				card_num = int(request.args["card_num"])
			else:
				return "No card number specified.", 404

			token = generate_access_token(pin, card_num)
			packet = {"text": "Welcome", "token":token}
			return packet, 200
		else:
			if "card_num" in request.args:
				card_num = int(request.args["card_num"])
			else:
				return "No card number specified.", 404

			# token = generate_access_token(pin, card_num)
			packet = {"text": "Burn", "token":""}
			return packet, 404
		# if name == "all":
		# 	return users, 200

		# for user in users:
		# 	if name == user["name"]:
		# 		return user, 200
		# return "User not found", 404

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

	def put(self, name):
		age = request.args.get("age")
		occupation = request.args.get("occupation")

		for user in users:
			if name == user["name"]:
				user["age"] = age
				user["occupation"] = occupation
				return user, 200

		user = {
			"name":name,
			"age":age,
			"occupation":occupation
		}
		users.append(user)
		return user, 201

	def delete(self, name):
		global users
		users = [user for user in users if user["name"] != name]
		return "{} is deleted".format(name), 200


# if __name__ == "__main__":



@app.route('/verify')
def index():
	pin = int(request.args["pin"])

	if pin == 1234:
		card_num = int(request.args["card_num"])
		token = generate_access_token(pin, card_num)
		packet = {"text": "Welcome", "token":token}
		return packet, 200
	else:
		card_num = int(request.args["card_num"])
		token = generate_access_token(pin, card_num)
		packet = {"text": "Burn", "token":""}
		return packet, 404

# @app.route('/verified/token')
api.add_resource(User, "/user/")
app.run(host="0.0.0.0", debug=True)