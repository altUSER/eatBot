#coding: utf-8

import vk_api, vk_api.longpoll
from vk_api.longpoll import VkEventType
import datetime
from vars import * #данные для входа

def getname(event): #получение имени чата и пользователя
	id = event.peer_id
	if str(id)[0] == '1': #если сообщение из лс
		usr = vk.method('users.get', {'user_ids':id})
		outp = usr[0]['first_name'].encode('utf-8') + '_' + usr[0]['last_name'].encode('utf-8')
	if str(id)[0] == '2': #если сообщение из чата
		chat = vk.method('messages.getChat', {'chat_id':id - 2000000000})
		usr = vk.method('users.get', {'user_ids':event.user_id})
		outp = chat['title'] + ' | ' + usr[0]['first_name'] + '_' + usr[0]['last_name']
	return outp

def geteatlist():

	now = datetime.datetime.now() #переменная для вывода времени

	longpoll = vk_api.longpoll.VkLongPoll(vk)
	for event in longpoll.listen(): #ловля сообщений

		if event.type == VkEventType.MESSAGE_NEW: 
			msg = event.text
			inp = msg.split()


			if inp[0] == 'eat':

				if inp[1] == '+':
					print getname(event) + ' True'
				if inp[1] == '-':
					print getname(event) + ' False'



vk = vk_api.VkApi(login = login, password = password) #переменные из vars
print('Login...')
vk.auth()
print('Done')

geteatlist()
