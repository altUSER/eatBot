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
    vk.method('messages.send', {'user_id':id,'message':s,'random_id':(int(time.strftime('%H')) + int(time.strftime('%M')) + int(time.strftime('%S')))})

def cfg_set(sect, set, val):
	conf_file = open('class.conf', 'w') #имя конфиг файла

	conf.set(str(sect), str(set), str(val))

	conf.write(conf_file)
	conf_file.close()

def save(event):
	if os.path.isdir('save'):
		fname=str(time.strftime('%Y_%m_%d'))
		os.system('cp class.conf save/' + fname)
		write_msg(admin_id, '[AUTO INFO]Сохранение БД, файл сохранен как save/' + fname)
		return('Сохранение БД, файл сохранен как ' + fname)
	else:
		return('Ошибка! Директория save/ не обнаружена.')

def list(conf):
	eat_y = 'Едят:\n'
	y_count = 0
	eat_n = '\nНе едят:\n'
	n_check ='\nНе отметились:\n'
	for id in conf.sections():
		if conf.get(id, 'eat') == 'y':
			y_count += 1
			eat_y += conf.get(id, 'name') + '\n'
		if conf.get(id, 'eat') == 'n':
			eat_n += conf.get(id, 'name') + '\n'
		if conf.get(id, 'eat') == '-':
			n_check += conf.get(id, 'name') + '\n'

	return(eat_y + 'Всего: ' + str(y_count) + '\n' + eat_n + '\n' + n_check)

def geteatlist(conf):

	now = datetime.datetime.now() #переменная для вывода времени

	longpoll = vk_api.longpoll.VkLongPoll(vk)
	for event in longpoll.listen(): #ловля сообщений
		time.sleep(0.5)

		if event.type == VkEventType.MESSAGE_NEW: 
			msg = event.text
			inp = msg.lower().split()

			if (len(inp) != 0):
				if (inp[0] == 'eat'):

					if inp[1] == 'y' and len(inp) == 2 and (str(event.peer_id) in conf.sections()): #отметка на акк отправляющего
						old_v = conf.get(str(event.peer_id), 'eat')
						conf.set(str(event.peer_id), 'eat', 'y')
						write_msg(event.peer_id, old_v + ' заменено на y')
					if inp[1] == 'n' and len(inp) == 2 and (str(event.peer_id) in conf.sections()):
						old_v = conf.get(str(event.peer_id), 'eat')
						conf.set(str(event.peer_id), 'eat', 'n')
						write_msg(event.peer_id, old_v + ' заменено на n')

					if inp[1] == 'list' and len(inp) == 2: #вывод всех данных

						write_msg(event.peer_id, list(conf))

					if inp[1] == 'save' and len(inp) == 2: #сохранение значений
						write_msg(event.peer_id, save(event))

					if inp[1] == 'archive' and len(inp) == 3:

						if inp[2] == 'list':
							outp = ''
							c = 0
							for n in os.listdir('save'):
								outp += n + '(' + str(c) + ')' + '\n'
								c += 1
							write_msg(event.peer_id, outp)
						else:
							try:
								cfg = cp.RawConfigParser()
								cfg.read('save/' + os.listdir('save')[int(inp[2])]) #имя конфиг файла
								outp = 'Архив на ' + os.listdir('save')[int(inp[2])] + ':\n' + list(cfg)
							except Exception as e:
								outp = 'Ошибка ' + str(e)
							write_msg(event.peer_id, outp)

					if inp[1] == 'am' and len(inp) == 4: #отметка другого человека
						try:
							num = int(inp[2])
							if num > 0 and num < 25:
								id = conf.sections()[num - 1]

							if inp[3] == 'y':
								old_v = conf.get(id, 'eat')
								cfg_set(id, 'eat', 'y')
								write_msg(event.peer_id, old_v + ' заменено на y')

							if inp[3] == 'n':
								old_v = conf.get(id, 'eat')
								cfg_set(id, 'eat', 'n')
								write_msg(event.peer_id, old_v + ' заменено на n')
						except:
							write_msg(event.peer_id, 'Не а')

while True:
	try:
		vk = vk_api.VkApi(login = login, password = password) #переменные из vars
		conf = cp.RawConfigParser()
		print('Login...')
		vk.auth()
		print('Done')

		conf = cp.RawConfigParser()
		conf.read('class.conf') #имя конфиг файла

		geteatlist(conf)

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		print('Fatal error! ' + str(e) + ' Restart after 10 sec.')
		time.sleep(10)
