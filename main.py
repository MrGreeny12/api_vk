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

TOKEN = '198bade3d62e3d604091a7fdc7a48844055d697d3b3aa41c2973d0261a27678319cdfbee5c2e4e9293ccd'

class User:
    '''
    Класс принимает на входе: token, id пользователя
    '''
    def __init__(self, token, id_vk):
        self.token = token
        self.id_vk = id_vk

    def get_params(self):
        return {
            'access_token': self.token,
            'user_id': self.id_vk,
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

    def common_friends(self, other_user):
        '''
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
        return self.common_list

    def user_get(self):
        '''
        внутренний запрос класса, получает с сервера vk данные через метод users.get
        :return: данные с сервера в виде словаря
        '''
        params_2 = {
            'access_token': self.token,
            'user_id': self.id_vk,
            'fields': 'domain',
            'v': 5.52
        }
        params = self.get_params()
        responce_2 = requests.get(
            'https://api.vk.com/method/users.get',
            params_2
        )
        return responce_2.json()

    def profile_link(self):
        '''

        :return: генерирует ссылку на профиль в вк для экземпляра класса
        '''
        self.profile_domain = self.user_get()['response'][0]['domain']
        print(f'https://vk.com/{self.profile_domain}')

        # потом придумать, как из списка id - сделать список экземпляров класса

# через перебор циклом, определять id - в виде нового usera
def main():
    '''
    функция принимает название пользователей и возвращает список общих друзей
    '''
    command = input('Введите объекты поиска (например: user1 & user2, не забывая о пробелах):')
    user_1, operator, user_2 = command.split()
    if operator == '&':
        search = f'{user_1}.common_friends({user_2})'
        print(type(search))
        pprint(search.json())
    else:
        print(f'Вы ввели {operator} вместо &. Повторите попытку')



# auth()
user1 = User(TOKEN, 192091799)
user2 = User(TOKEN, 320118571)
print(type(user1))
friends_list_1 = user1.friends_get()
friends_list_2 = user2.friends_get()
# user2.profile_link()
# pprint(friends_list_1)
# pprint(friends_list_2)
common_list_1 = user1.common_friends(user2)
# pprint(common_list_1)
# print(user1)
# main()
