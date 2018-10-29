#coding: utf-8

import vk_api, vk_api.longpoll
from vk_api.longpoll import VkEventType
import datetime
from vars import * #данные для входа
import ConfigParser as cp
import os
import time

##настройки
admin_id = 160946239

def write_msg(id, s):
    vk.method('messages.send', {'user_id':id,'message':s})

def rst(event):
	if os.path.isdir('log'):
		fname=str(time.strftime('%Y_%b_%d_%H:%M:%S')) + '.conf'
		os.system('cp class.conf log/' + fname)
		write_msg(admin_id, '[AUTO INFO]Произведен сброс, файл сохранен как log/' + fname)
		for id in conf.sections():
			conf.set(str(id), 'eat', '-')
		return('Произведен сброс, файл сохранен как log/' + fname)
	else:
		return('Ошибка! Директория log/ не обнаружена.')

def geteatlist(conf):

	now = datetime.datetime.now() #переменная для вывода времени

	longpoll = vk_api.longpoll.VkLongPoll(vk)
	for event in longpoll.listen(): #ловля сообщений
		time.sleep(0.5)

		if event.type == VkEventType.MESSAGE_NEW: 
			msg = event.text
			inp = msg.split()

			if (len(inp) != 0):
				if (inp[0] == 'eat') or (inp[0] == 'Eat'):

					conf_file = open('class.conf', 'w') #имя конфиг файла

					if inp[1] == 'y':	#отметка на акк отправляющего
						old_v = conf.get(str(event.peer_id), 'eat')
						conf.set(str(event.peer_id), 'eat', 'y')
						write_msg(event.peer_id, old_v + ' заменено на y')
					if inp[1] == 'n':
						old_v = conf.get(str(event.peer_id), 'eat')
						conf.set(str(event.peer_id), 'eat', 'n')
						write_msg(event.peer_id, old_v + ' заменено на n')

					if inp[1] == 'list': #вывод всех данных
						eat_y = 'Едят:\n'
						y_count = 0
						eat_n = '\nНе едят:\n'
						ncheck = '\nНе отметелись:\n'
						for id in conf.sections():
							if conf.get(id, 'eat') == '-':
								ncheck += conf.get(id, 'name') + '\n'
							if conf.get(id, 'eat') == 'y':
								y_count += 1
								eat_y += conf.get(id, 'name') + '\n'
							if conf.get(id, 'eat') == 'n':
								eat_n += conf.get(id, 'name') + '\n'

						write_msg(event.peer_id, eat_y + 'Всего: ' + str(y_count) + '\n' + eat_n + ncheck)

					if inp[1] == 'reset': #сброс значений
						write_msg(event.peer_id, rst(event))

					if inp[1] == 'am': #отметка другого человека
						num = inp[2]
						id = conf.sections()[int(num) - 1]

						if inp[3] == 'y':
							old_v = conf.get(id, 'eat')
							conf.set(id, 'eat', 'y')
							write_msg(event.peer_id, old_v + ' заменено на y')

						if inp[3] == 'n':
							old_v = conf.get(id, 'eat')
							conf.set(id, 'eat', 'n')
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

