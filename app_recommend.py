import json
import urllib.request
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def systems(id):
    dic1 = {"Ahhoro": 0,
            "記帳城市(免)": 0,
            "記帳城市(付)": 0,
            "MOZE3(免)": 0,
            "MOZE3(付)": 0,
            "CW money(免)": 0,
            "CW money(付)": 0,
            "天天記帳": 0,
            "碎碎念記帳": 0,
            "Money tracker": 0,
            "簡單記帳": 0,
            "記帳雞": 0,
            "卡那赫拉": 0,
            "理財幫手": 0
            }

    url = 'https://docs.google.com/spreadsheets/d/1IfDb9SmmOMtcOaGvBZDLDzKLMLUOpEUXdmuR4-GUCng/export?format=csv'
    webpage = urllib.request.urlopen(url)
    data = csv.DictReader(webpage.read().decode('utf-8-sig').splitlines())

    data_temp = []
    for item in data:
        temp = {}
        for key, value in item.items():
            temp[key] = value
        data_temp.append(temp)
    data = data_temp
    # print(data)
    result = {}  # 創建一個新的dict
    # print(result)
    for i in data:  # 把原本的data這個list一個一個丟進去這個dict中
        result[i['請填入記帳幫手提供您的ID！']] = i  # 把在data中ID這個key的value作為這次reuslt這個dict中的key
        del i['請填入記帳幫手提供您的ID！']
    # print(result[id])  #利用stu_id去尋找以上整理出來的dict中符合ID的dict
    with open('questionnaire_data.json', 'w', encoding='utf-8') as object:
        json.dump(result, object, ensure_ascii=False, indent=4)
    with open('questionnaire_data.json', 'r', encoding='utf-8') as object:
        q_d = json.load(object)

    if id == '':
        return "請輸入您的ID"

    elif q_d[id]['你的手機系統?'] == "Android":  # 第一題
        if q_d[id]["是否會介意付費的記帳程式"] == "YES":  # 第二題
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

            del dic1['記帳城市(付)']  # 因第二題刪
            del dic1['CW money(付)']  # 因第二題刪
            del dic1["MOZE3(免)"]  # 因第一題刪
            del dic1["MOZE3(付)"]  # 因第一題刪


        elif q_d[id]["是否會介意付費的記帳程式"] == "NO":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)


        return total(dic1)

    elif q_d[id]['你的手機系統?'] == "IOS":
        if q_d[id]["是否會介意付費的記帳程式"] == "YES":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

            del dic1['記帳城市(付)']  # 因第二題刪
            del dic1['MOZE3(付)']  # 因第二題刪
            del dic1['CW money(付)']  # 因第二題刪
            del dic1['理財幫手']  # 因第二題刪


        elif q_d[id]["是否會介意付費的記帳程式"] == "NO":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)


        return total(dic1)


def functionality(number, dic1):  # 功能性
    if number == "5":
        dic1["CW money(免)"] += 1
        dic1["CW money(付)"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
    elif number == "4":
        dic1["CW money(免)"] += 1
        dic1["CW money(付)"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
        dic1["理財幫手"] += 1
        dic1["天天記帳"] += 1
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
    elif number == "3":
        dic1["CW money(免)"] += 1
        dic1["CW money(付)"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
        dic1["理財幫手"] += 1
        dic1["天天記帳"] += 1
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
        dic1["Ahhoro"] += 1
    elif number == "2":
        dic1["碎碎念記帳"] -= 1
        dic1["記帳雞"] -= 1


def conv(number, dic1):  # 易上手性
    if number == "5":
        dic1["簡單記帳"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
    elif number == "4":
        dic1["簡單記帳"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
        dic1["Ahhoro"] += 1
        dic1["理財幫手"] += 1
    elif number == "3":
        dic1["簡單記帳"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
        dic1["Ahhoro"] += 1
        dic1["理財幫手"] += 1
        dic1["天天記帳"] += 1
        dic1["記帳雞"] += 1
    elif number == "2":
        dic1["碎碎念記帳"] -= 1
        dic1["記帳城市(免)"] -= 1
        dic1["記帳城市(付)"] -= 1
        dic1["碎碎念記帳"] -= 1


def immediacy(number, dic1):  # 即時性
    if number == "5":
        dic1["CW money(免)"] += 1
        dic1["CW money(付)"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1


def beauty(number, dic1):  # 美觀
    if number == "5":
        dic1["卡那赫拉"] += 1
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
    elif number == "4":
        dic1["卡那赫拉"] += 1
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
        dic1["簡單記帳"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
    elif number == "3":
        dic1["卡那赫拉"] += 1
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
        dic1["簡單記帳"] += 1
        dic1["MOZE3(免)"] += 1
        dic1["MOZE3(付)"] += 1
        dic1["記帳雞"] += 1
        dic1["Ahhoro"] += 1
    elif number == "2":
        dic1["CW money(免)"] -= 1
        dic1["CW money(付)"] -= 1
        dic1["碎碎念記帳"] -= 1
        dic1["天天記帳"] -= 1


def fun(number, dic1):  # 趣味性
    if number == "5":
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
    elif number == "4":
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
        dic1["卡那赫拉"] += 1
    elif number == "3":
        dic1["記帳城市(免)"] += 1
        dic1["記帳城市(付)"] += 1
        dic1["卡那赫拉"] += 1
        dic1["記帳雞"] += 1
        dic1["碎碎念記帳"] += 1


def stop(reason, dic1):
    reasons = reason.replace(' ', '')
    reasons_list = reasons.split(",")
    for res in reasons_list:
        if res == "忘記花費":
            dic1["碎碎念記帳"] += 1
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["Money tracker"] += 1
        elif res == "忘記記帳":
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["天天記帳"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["簡單記帳"] += 1
            dic1["記帳城市(免)"] += 1
            dic1["記帳城市(付)"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["理財幫手"] += 1
        elif res == "忙碌":
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["Ahhoro"] += 1
            dic1["理財幫手"] += 1
        elif res == "懶惰":
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["Ahhoro"] += 1
            dic1["理財幫手"] += 1
        elif res == "記帳麻煩":
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["Ahhoro"] += 1
            dic1["理財幫手"] += 1
            dic1["記帳城市(免)"] += 1
            dic1["記帳城市(付)"] += 1


def habit(reason, dic1):
    reasons = reason.replace(' ', '')
    reasons_list = reasons.split(",")
    for res in reasons_list:
        if res == "時常會借還錢":
            dic1["MOZE3(付)"] += 1
            dic1["理財幫手"] += 1
        if res == "需要信用卡 or 帳單繳費提醒":
            dic1["MOZE3(付)"] += 1
        if res == "需要紀錄固定開銷":
            dic1["天天記帳"] += 1
            dic1["Ahhoro"] += 1
            dic1["簡單記帳"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
        if res == "多帳戶管理（錢包、銀行、信用卡等分別紀錄":
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["Ahhoro"] += 1
            dic1["理財幫手"] += 1
            dic1["記帳城市(免)"] += 1
            dic1["記帳城市(付)"] += 1
            dic1["天天記帳"] += 1
            dic1["Money tracker"] += 1
            dic1["碎碎念記帳"] += 1
        if res == "紀錄專案：紀錄特定事件所花的帳目（ex.旅行、週年慶）或 預算編製":
            dic1["MOZE3(免)"] += 1
            dic1["MOZE3(付)"] += 1
            dic1["天天記帳"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["Ahhoro"] += 1
            dic1["記帳城市(付)"] += 1
        if res == "需要紀錄不同貨幣":
            dic1["理財幫手"] += 1
            dic1["記帳城市(免)"] += 1
            dic1["記帳城市(付)"] += 1
            dic1["CW money(免)"] += 1
            dic1["CW money(付)"] += 1
            dic1["天天記帳"] += 1


def total(dic1):
    max(dic1.values())
    for key, value in dic1.items():
        if value == max(dic1.values()):
            return key


if __name__ == '__main__':
    print(systems(id='E44061296'))
    print(systems(id='F54091196'))