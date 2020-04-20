from pprint import pprint
from urllib.parse import urlencode

import requests

def auth():
    APP_ID = 7382587
    AUTH_URL = 'https://oauth.vk.com/authorize'
    oparams = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'friends',
        'response_type': 'token',
        'v': 5.52
    }
    print('?'.join((AUTH_URL, urlencode(oparams))))

TOKEN = '7dc66e04ac0f5a03d8508c0daa3fd7b348391c8d84af0de6e34437ee6d8ba0cd9017fae46a7cde8e703ea'

class User:
    '''
    Класс принимает на входе: token, id пользователя
    '''
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def __and__(self, other_user):
        '''
        other_user - это другой экземпляр класса user
        производит сравнение списков id двух экземпляров класса
        :param other_user: экземпляр класса, с которым нужно сравнить
        :return: список id общих друзей
        '''
        self.other_user_fr_list = other_user.friends_get()['response']['items']
        self.friends_list = self.friends_get()['response']['items']
        self.common_list = []
        for i in self.other_user_fr_list:
            for j in self.friends_list:
                if i == j:
                    self.common_list.append(i)
                    break
        users = []
        for id_user in self.common_list:
            user = User(self.token, id_user)
            users.append(id_user)
        return users

    def __str__(self):
        self.profile_domain = self.user_get()['response'][0]['domain']
        return ('https://vk.com/' + self.profile_domain)

    def get_params(self):
        return {
            'access_token': self.token,
            'user_id': self.user_id,
            'order': 'hints',
            'count': '200',
            # 'fields': 'first_name, last_name',
            'name_case': 'nom',
            'v': 5.52
        }

    def friends_get(self):
        '''
        принимают параметры запроса
        :return: словарь с данными по методу friends.get vk
        '''
        params = self.get_params()
        responce = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        return responce.json()

    def user_get(self):
        '''
        внутренний запрос класса, получает с сервера vk данные через метод users.get
        :return: данные с сервера в виде словаря
        '''
        params_2 = {
            'access_token': self.token,
            'user_id': self.user_id,
            'fields': 'domain',
            'v': 5.52
        }
        params = self.get_params()
        responce_2 = requests.get(
            'https://api.vk.com/method/users.get',
            params_2
        )
        return responce_2.json()

# auth()
user1 = User(TOKEN, 192091799)
user2 = User(TOKEN, 320118571)
pprint(user1&user2)
print(user1)
