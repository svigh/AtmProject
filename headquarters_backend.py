from flask import Flask, request
from flask_restful import Resource, Api
import random
import requests

app = Flask(__name__)
masterKey = 123
decodeCheck = 1230

api = Api(app)

globalCacheUsers = [
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
	},
	{
		"pin": 1004,
		"card_num": 4,
		"balance": 10123
	}
]

class Atm(Resource):
	def get(self):	# Give users data
		return globalCacheUsers, 200

class Admin(Resource):
	def get(self, passKey):		# Give all users
		return globalCacheUsers, 200

	def post(self, passKey):	# Add a new user
		return globalCacheUsers, 200

	def delete(self, passKey): 	# Delete a user
		return globalCacheUsers, 200

api.add_resource(Atm, "/atm/users")
api.add_resource(Admin, "/admin/<int:passKey>")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="6000", debug=True)