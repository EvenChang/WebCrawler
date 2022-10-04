#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyPtt import PTT
import sys, time, os, datetime
ptt_bot = PTT.API()
evenId = '******'
evenPassword = '************'
logFile = "pttTitle.txt"

def getCurrentTime():
    datetime_dt = datetime.datetime.today()# 獲得當地時間
    datetime_str = datetime_dt.strftime("%H:%M:%S")  # 格式化日期
    return datetime_str

def writeToLogFile(content):
    text_file = open(logFile, "a+")
    text_file.write(content + "\n")
    text_file.close()

try:
    ptt_bot.login(evenId, evenPassword)
except PTT.exceptions.LoginError:
    ptt_bot.log('登入失敗')
    sys.exit()
except PTT.exceptions.WrongIDorPassword:
    ptt_bot.log('帳號密碼錯誤')
    sys.exit()
except PTT.exceptions.LoginTooOften:
    ptt_bot.log('請稍等一下再登入')
    sys.exit()
ptt_bot.log('登入成功')

if ptt_bot.unregistered_user:
    print('未註冊使用者')

    if ptt_bot.process_picks != 0:
        print('註冊單處理順位 {ptt_bot.process_picks}')

if ptt_bot.registered_user:
    print('已註冊使用者')

# call ptt_bot other api

tmpString = "even"
#authorSet = {"YingLinga", "TccReD"}
authorSet = {"drgon"}
# TccReD
lines = []

count = 0
while True:
    try:
        for author in authorSet:
            index = ptt_bot.get_newest_index(
                PTT.data_type.index_type.BBS,
                board='money',
                search_type=PTT.data_type.post_search_type.AUTHOR,
                search_condition=author,
                )
            post_info = ptt_bot.get_post(
                board='money',
                post_index=index,
                search_type=PTT.data_type.post_search_type.AUTHOR, search_condition=author)

            with open(logFile) as file:
                lines = [line.strip() for line in file]

            if post_info.title not in lines:
                os.system("osascript -e 'Tell     application \"System Events\" to display dialog \""+ post_info.title +     "\"'")
                writeToLogFile(post_info.title)
                print(post_info.title)

            count += 1
            print(count, getCurrentTime(), author, lines)
    except:
        os.system("./bin/python pttRealTime.py")
    # time.sleep(1)

ptt_bot.logout()

