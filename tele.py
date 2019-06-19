#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import ex

def replyShelterData(user, loc_param, loc_param2):
    print(user, loc_param, loc_param2)
    res_list = ex.getData(loc_param, loc_param2)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r+msg)+1 > ex.MAX_MSG_LENGTH:
            ex.sendMessage(user, msg)
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        ex.sendMessage(user, msg)
    else:
        ex.sendMessage(user, '해당하는 데이터가 없습니다.')

def save(user, loc_param):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        ex.sendMessage(user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        ex.sendMessage(user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        ex.sendMessage(user, row)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        ex.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('지역') and len(args)>1:
        print('try to 지역', args[1], args[2])
        replyShelterData(chat_id, args[1], args[2])
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1], args[2])
        save(chat_id, args[1], args[2])
    elif text.startswith('확인'):
        print('try to 확인')
        check(chat_id)
    else:
        ex.sendMessage(chat_id, '모르는 명령어입니다.\n지역 [(시, 도) (구, 군)], 저장 [(시, 도) (구, 군)], 확인 중 하나의 명령을 입력하세요.')

bot = telepot.Bot(ex.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)