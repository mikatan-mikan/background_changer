from json import load
from os import path
from time import sleep
from datetime import datetime
#デスクトップ背景の設定用import
from ctypes import windll

from random import randint


#appdata = r"%LOCALAPPDATA%\MG_mikan\background_changer"
appdata = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')

def read_json():
    global json_file,json_list
    json_file = load(open(f"{appdata}\\config.json"))
    # print(json_file)
    #json_list = [[[],[]],[],[]]#時間、分、パス
    json_list = []#時間ごとにリストを作り中に詰める([[時間,分,データ数,"rand"],データ1のpath,データnのpath]):pathとrand or 時間経過変更を判定できる設計
    for i in range(len(json_file)):
        tmp_hour = int(json_file[i][0]['time'][:-3])
        tmp_min = int(json_file[i][0]['time'][-2:])
        tmp_list = [[tmp_hour,tmp_min,len(json_file[i]),json_file[-1][0]["mode"]]]
        for j in range(len(json_file[i])):
            tmp_list.append(json_file[i][j]['path'])
            #フラグは不要...なはず
            # if len(json_file[j]) != 1:
            #     json_list[2].append([True,len(json_file[j])])#同じ時刻が存在しているフラグ
            # else:
            #     json_list[2].append([False,1])
        json_list.append(tmp_list)

read_json()
print(json_list)

now_count = -1
for i in range(len(json_list)):#実行時点で既に時間が過ぎているものをスキップしたい
    if datetime.now().hour >= json_list[i][0][0] and datetime.now().minute >= json_list[i][0][1]:
        now_count = i
        # print(now_count)

old_day = -1
rand_num_pic = 0
choice_num_pic = 1

while True:
    now_hour = int(datetime.now().strftime("%H"))
    now_min = int(datetime.now().strftime("%M"))
    now_day = int(datetime.now().strftime("%D").split("/")[1])
    if now_day != old_day:
        now_count = -1
    json_file_new = load(open(f"{appdata}\\config.json"))
    if json_file[-1][0]["path"] != json_file_new[-1][0]["path"]:#uuidが変わったら
        read_json()#ファイルリロード
        now_count = -1
    if (json_list[now_count + 1][0][0] <= now_hour and json_list[now_count + 1][0][1] <= now_min) or json_list[now_count + 1][0][0] < now_hour:#現在の表示している画像+1番目の画像の表示時刻を超えているなら
        # print("run",now_count)
        old_day = now_day
        now_count += 1
        if json_list[now_count + 1][0][3] == "rand":
            choice_num_pic = (randint(1,json_list[now_count][0][2]))#rand_num_pic
        elif json_list[now_count + 1][0][3] == "change":
            choice_num_pic = 1#rand_num_pic
        for i in range(24):#24枚分走査する
            if (json_list[now_count + 1][0][0] <= now_hour and json_list[now_count + 1][0][1] <= now_min) or json_list[now_count + 1][0][0] < now_hour:#先の一枚の描写時間なら　
                now_count += 1
            else:#違うならその画像で固定
                break
    # 
    elif json_list[now_count][0][3] == "change" and json_list[now_count][0][2] > 1: # changeが指定されていた時
        print(json_list)                           
        sleep(60)
        # isReturn = True if choice_num_pic == 1 else False
        choice_num_pic += 1                             #次の画像を選択
        if choice_num_pic > json_list[now_count][0][2]: #ただし、もし次が存在しないなら
            choice_num_pic = 1                          #最初に戻す
            #もし、一枚しかなければ
            if json_list[now_count][0][2] == 1:
                continue
            # if isReturn:                                #もし前回と同じ画像なら
            #     continue                                #背景を変える必要がないのでcontinue
    else:
        sleep(60)
        continue
    #from PIL import Image
    #Image.open(json_list[now_count][choice_num_pic]).show()
    # print(json_list[now_count][choice_num_pic],now_count,json_list[now_count][0][2])
    #再起動後も維持する
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02
    windll.user32.SystemParametersInfoW(20, 0, json_list[now_count][choice_num_pic], SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)