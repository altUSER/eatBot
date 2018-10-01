#coding: utf-8

import vk_api, vk_api.longpoll
from vk_api.longpoll import VkEventType
import datetime
from vars import * #данные для входа
import ConfigParser as cp

def write_msg(id, s):
    vk.method('messages.send', {'user_id':id,'message':s})

def geteatlist(conf):

	now = datetime.datetime.now() #переменная для вывода времени

	longpoll = vk_api.longpoll.VkLongPoll(vk)
	for event in longpoll.listen(): #ловля сообщений

		if event.type == VkEventType.MESSAGE_NEW: 
			msg = event.text
			inp = msg.split()


			if inp[0] == 'eat':

				conf_file = open('class.conf', 'w') #имя конфиг файла

				if inp[1] == 'y':
					old_v = conf.get(str(event.peer_id), 'eat')
					conf.set(str(event.peer_id), 'eat', 'y')
					write_msg(event.peer_id, old_v + ' заменено на y')
				if inp[1] == 'n':
					old_v = conf.get(str(event.peer_id), 'eat')
                                        conf.set(str(event.peer_id), 'eat', 'n')
                                        write_msg(event.peer_id, old_v + ' заменено на n')


				conf.write(conf_file)
				conf_file.close()


vk = vk_api.VkApi(login = login, password = password) #переменные из vars
conf = cp.RawConfigParser()
print('Login...')
vk.auth()
print('Done')

conf = cp.RawConfigParser()
conf.read('class.conf') #имя конфиг файла

geteatlist(conf)
