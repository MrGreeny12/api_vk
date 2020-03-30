
import request from requests
import pprint

APP_ID = 7298778
AUTH_URL = 'https://oauth.vk.com/authorize'
params = {
	'client_id' : APP_ID,
	'display' : 'page',
	'scope' : '',
	'responce_type' : 'token',
	'v' : 5.103
}

TOKEN = '17b9af7e4d876c6b82d33196845d88b2b6664aecc69e7546c46d356be0bffd83d3d410502fe1dc66f2e91'
user_id = 192091799 #внести айди того, кого хочешь посмотреть

class User:
	def __init__(self, token, user_id):
		self.token = token
		self.user_id = user_id

	def get_params(self):
		return {
			'user_id' : self.user_id,
			'order' : 'name',
			'list_id' : '',
			'count' : 1000,
			'offset' : '5',
			'fields' : '',
			'name_case' : 'ins',
			'ref' : '',
			'access_token' : TOKEN,
			'v': 5.103
		}

	def get_friends_list(self, kwargs=None):
		params = self.get_params
		responce = request.get(
			'https://api.vk.com/method/friends.get',
			params
		)

		return responce.json()

	# def set_friends_list(self):
	# 	pass


anonim = User(TOKEN, user_id)
friends_list = anonim.get_friends_list()
print(friends_list)