import json
import time
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler

def setting_flex_message():
    # create flex_message json file from https://developers.line.biz/flex-simulator/
    flex_message = json.load(
        open('./flex_message/group_feature.json', 'r', encoding='utf-8'))
    return flex_message
def setting_alert_message():
    flex_message = json.load(
        open('./flex_message/alert.json', 'r', encoding='utf-8'))
    return flex_message
def setting_check_message():
    template_message = json.load(
        open('./template_message/check.json', 'r', encoding='utf-8'))
    return template_message
def setting_recommend_message():
    recommend_message = json.load(
        open('./flex_message/recommend.json', 'r', encoding='utf-8'))
    return recommend_message

def alert_data(user_id):
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data = json.load(f, strict=False)
    if user_id not in data:
        data[user_id]= {
            "time":"tm",
            "audio":"0"
        }
    with open('./alert_data.json', "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4)
def enter_alert_time_data(tm,user_id):
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data= json.load(f, strict=False)
    data[user_id]["time"]= tm
    with open('./alert_data.json', "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4)

def enter_alert_audio_data(user_id,aud):
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data= json.load(f, strict=False)
    data[user_id]["audio"] = aud
    with open('./alert_data.json', "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4)

def get_alert_time_user():
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data= json.load(f, strict=False)
    now = time.ctime().split(" ")[3][:5]
    user=[]
    user2=[]
    for i in data:
        if data[i]["time"]==now:
            user.append(i)
            if data[i]["audio"]!="0":
               user2.append(i)
    return user,user2
def get_audio_user():
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data = json.load(f, strict=False)
    user=[]
    for i in data:
        if data[i]["audio"] != "0":
           user.append(i)

    return user

def return_alert_data():
    with open("./alert_data.json", "r", encoding='utf-8-sig', errors='ignore') as f:
        data= json.load(f, strict=False)
    return data




if __name__ == "__main__":
    print(get_audio_user())






