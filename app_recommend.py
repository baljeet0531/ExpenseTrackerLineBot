import json
import urllib.request
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def run_new_json():

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
        # 把在data中ID這個key的value作為這次reuslt這個dict中的key
        result[i['請填入記帳幫手提供您的ID！']] = i
        del i['請填入記帳幫手提供您的ID！']
    # print(result[id])  #利用stu_id去尋找以上整理出來的dict中符合ID的dict
    with open('questionnaire_data.json', 'w', encoding='utf-8') as object:
        json.dump(result, object, ensure_ascii=False, indent=4)
    return True


user_recommend = {}


def judgement(id):
    dic1 = {"Ahorro": 0,
            "記帳城市(免費版)": 0,
            "記帳城市(付費版)": 0,
            "MOZE3.0(免費版)": 0,
            "MOZE3.0(付費版)": 0,
            "CW money(免費版)": 0,
            "CW money(付費版)": 0,
            "天天記帳": 0,
            "碎碎念記帳": 0,
            "Spendee Budget & Money Tracker": 0,
            "簡單記帳": 0,
            "記帳雞": 0,
            "卡娜赫拉家計簿": 0,
            "理財幫手 AndroMoney": 0
            }

    with open('questionnaire_data.json', 'r', encoding='utf-8') as object:
        q_d = json.load(object)
    if q_d[id]['你的手機系統?'] == "Android":  # 第一題
        if q_d[id]["是否會介意付費的記帳程式"] == "YES":  # 第二題
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

            del dic1['記帳城市(付費版)']  # 因第二題刪
            del dic1['CW money(付費版)']  # 因第二題刪
            del dic1["MOZE3.0(免費版)"]  # 因第一題刪
            del dic1["MOZE3.0(付費版)"]  # 因第一題刪

        elif q_d[id]["是否會介意付費的記帳程式"] == "NO":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

    elif q_d[id]['你的手機系統?'] == "IOS":
        if q_d[id]["是否會介意付費的記帳程式"] == "YES":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

            del dic1['記帳城市(付費版)']  # 因第二題刪
            del dic1['MOZE3.0(付費版)']  # 因第二題刪
            del dic1['CW money(付費版)']  # 因第二題刪
            del dic1['理財幫手 AndroMoney']  # 因第二題刪

        elif q_d[id]["是否會介意付費的記帳程式"] == "NO":
            functionality(q_d[id]["功能性"], dic1)
            conv(q_d[id]["易上手性"], dic1)
            immediacy(q_d[id]["即時性"], dic1)
            beauty(q_d[id]["美觀"], dic1)
            fun(q_d[id]["趣味性"], dic1)
            stop(q_d[id]["停止記帳的原因"], dic1)
            habit(q_d[id]["金錢的使用習慣"], dic1)

    user_recommend[id] = dic1
    with open('user_recommend_data.json', 'w', encoding='utf-8') as object:
        json.dump(user_recommend, object, ensure_ascii=False, indent=4)
    return total(dic1)

'''
在功能性、易上手性、美感、即時性、趣味性的運算邏輯上，依照使用者填寫不同的重視程度（導致number有1至5的差別）會給予此11個APP不同大小的分數範圍。
若number為5，則APP的分數範圍為1~11（因為總共有11個APP）；若number為4，則APP的分數範圍為1~9；若number為3，則APP的分數範圍為1~7，以此類推。
'''
def functionality(number, dic1):  # 功能性
    '''
    功能性我們依照以下各個APP具備的記帳功能數量去做比較，分出功能數量多到少的APP有8個等第。
    功能數量最少者為1分，每提升一等第加10/7分。
    不同number對應的等第加分就不同。
    '''
    if number == "5":
        dic1["CW money(付費版)"] += 1 + 7 * 10 / 7
        dic1["CW money(免費版)"] += 1 + 6 * 10 / 7
        dic1["MOZE3.0(付費版)"] += 1 + 6 * 10 / 7
        dic1["MOZE3.0(免費版)"] += 1 + 5 * 10 / 7
        dic1["記帳城市(付費版)"] += 1 + 4 * 10 / 7
        dic1["理財幫手 AndroMoney"] += 1 + 4 * 10 / 7
        dic1["天天記帳"] += 1 + 4 * 10 / 7
        dic1["記帳城市(免費版)"] += 1 + 3 * 10 / 7
        dic1["Ahorro"] += 1 + 3 * 10 / 7
        dic1["簡單記帳"] += 1 + 2 * 10 / 7
        dic1["記帳雞"] += 1 + 2 * 10 / 7
        dic1["卡娜赫拉家計簿"] += 1 + 1 * 10 / 7
        dic1["碎碎念記帳"] += 1 + 1 * 10 / 7
        dic1["Spendee Budget & Money Tracker"] += 1
    elif number == "4":
        dic1["CW money(付費版)"] += 9
        dic1["CW money(免費版)"] += 1 + 6 * 8 / 7
        dic1["MOZE3.0(付費版)"] += 1 + 6 * 8 / 7
        dic1["MOZE3.0(免費版)"] += 1 + 5 * 8 / 7
        dic1["記帳城市(付費版)"] += 1 + 4 * 8 / 7
        dic1["理財幫手 AndroMoney"] += 1 + 4 * 8 / 7
        dic1["天天記帳"] += 1 + 4 * 8 / 7
        dic1["記帳城市(免費版)"] += 1 + 3 * 8 / 7
        dic1["Ahorro"] += 1 + 3 * 8 / 7
        dic1["簡單記帳"] += 1 + 2 * 8 / 7
        dic1["記帳雞"] += 1 + 2 * 8 / 7
        dic1["卡娜赫拉家計簿"] += 1 + 1 * 8 / 7
        dic1["碎碎念記帳"] += 1 + 1 * 8 / 7
        dic1["Spendee Budget & Money Tracker"] += 1
    elif number == "3":
        dic1["CW money(付費版)"] += 7
        dic1["CW money(免費版)"] += 1 + 6 * 6 / 7
        dic1["MOZE3.0(付費版)"] += 1 + 6 * 6 / 7
        dic1["MOZE3.0(免費版)"] += 1 + 5 * 6 / 7
        dic1["記帳城市(付費版)"] += 1 + 4 * 6 / 7
        dic1["理財幫手 AndroMoney"] += 1 + 4 * 6 / 7
        dic1["天天記帳"] += 1 + 4 * 6 / 7
        dic1["記帳城市(免費版)"] += 1 + 3 * 6 / 7
        dic1["Ahorro"] += 1 + 3 * 6 / 7
        dic1["簡單記帳"] += 1 + 2 * 6 / 7
        dic1["記帳雞"] += 1 + 2 * 6 / 7
        dic1["卡娜赫拉家計簿"] += 1 + 1 * 6 / 7
        dic1["碎碎念記帳"] += 1 + 1 * 6 / 7
        dic1["Spendee Budget & Money Tracker"] += 1
    elif number == "2":
        dic1["CW money(付費版)"] += 5
        dic1["CW money(免費版)"] += 1 + 6 * 4 / 7
        dic1["MOZE3.0(付費版)"] += 1 + 6 * 4 / 7
        dic1["MOZE3.0(免費版)"] += 1 + 5 * 4 / 7
        dic1["記帳城市(付費版)"] += 1 + 4 * 4 / 7
        dic1["理財幫手 AndroMoney"] += 1 + 4 * 4 / 7
        dic1["天天記帳"] += 1 + 4 * 4 / 7
        dic1["記帳城市(免費版)"] += 1 + 3 * 4 / 7
        dic1["Ahorro"] += 1 + 3 * 4 / 7
        dic1["簡單記帳"] += 1 + 2 * 4 / 7
        dic1["記帳雞"] += 1 + 2 * 4 / 7
        dic1["卡娜赫拉家計簿"] += 1 + 1 * 4 / 7
        dic1["碎碎念記帳"] += 1 + 1 * 4 / 7
        dic1["Spendee Budget & Money Tracker"] += 1
    elif number == "1":
        dic1["CW money(付費版)"] += 3
        dic1["CW money(免費版)"] += 1 + 6 * 2 / 7
        dic1["MOZE3.0(付費版)"] += 1 + 6 * 2 / 7
        dic1["MOZE3.0(免費版)"] += 1 + 5 * 2 / 7
        dic1["記帳城市(付費版)"] += 1 + 4 * 2 / 7
        dic1["理財幫手 AndroMoney"] += 1 + 4 * 2 / 7
        dic1["天天記帳"] += 1 + 4 * 2 / 7
        dic1["記帳城市(免費版)"] += 1 + 3 * 2 / 7
        dic1["Ahorro"] += 1 + 3 * 2 / 7
        dic1["簡單記帳"] += 1 + 2 * 2 / 7
        dic1["記帳雞"] += 1 + 2 * 2 / 7
        dic1["卡娜赫拉家計簿"] += 1 + 1 * 2 / 7
        dic1["碎碎念記帳"] += 1 + 1 * 2 / 7
        dic1["Spendee Budget & Money Tracker"] += 1


def conv(number, dic1):  # 易上手性，透過表單調查出的介面清楚分數來當作評判標準。

    if number == "5":
        dic1["簡單記帳"] += 1 + 10 * 1
        dic1["MOZE3.0(免費版)"] += 1 + 9 * 1
        dic1["MOZE3.0(付費版)"] += 1 + 9 * 1
        dic1["Ahorro"] += 1 + 8 * 1
        dic1["理財幫手 AndroMoney"] += 1 + 7 * 1
        dic1["天天記帳"] += 1 + 6 * 1
        dic1["記帳雞"] += 1 + 5 * 1
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 1
        dic1["CW money(免費版)"] += 1 + 3 * 1
        dic1["CW money(付費版)"] += 1 + 3 * 1
        dic1["卡娜赫拉家計簿"] += 1 + 2 * 1
        dic1["記帳城市(免費版)"] += 1 + 1 * 1
        dic1["記帳城市(付費版)"] += 1 + 1 * 1
        dic1["碎碎念記帳"] += 1
    elif number == "4":
        dic1["簡單記帳"] += 1 + 10 * 0.8
        dic1["MOZE3.0(免費版)"] += 1 + 9 * 0.8
        dic1["MOZE3.0(付費版)"] += 1 + 9 * 0.8
        dic1["Ahorro"] += 1 + 8 * 0.8
        dic1["理財幫手 AndroMoney"] += 1 + 7 * 0.8
        dic1["天天記帳"] += 1 + 6 * 0.8
        dic1["記帳雞"] += 1 + 5 * 0.8
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.8
        dic1["CW money(免費版)"] += 1 + 3 * 0.8
        dic1["CW money(付費版)"] += 1 + 3 * 0.8
        dic1["卡娜赫拉家計簿"] += 1 + 2 * 0.8
        dic1["記帳城市(免費版)"] += 1 + 1 * 0.8
        dic1["記帳城市(付費版)"] += 1 + 1 * 0.8
        dic1["碎碎念記帳"] += 1
    elif number == "3":
        dic1["簡單記帳"] += 1 + 10 * 0.6
        dic1["MOZE3.0(免費版)"] += 1 + 9 * 0.6
        dic1["MOZE3.0(付費版)"] += 1 + 9 * 0.6
        dic1["Ahorro"] += 1 + 8 * 0.6
        dic1["理財幫手 AndroMoney"] += 1 + 7 * 0.6
        dic1["天天記帳"] += 1 + 6 * 0.6
        dic1["記帳雞"] += 1 + 5 * 0.6
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.6
        dic1["CW money(免費版)"] += 1 + 3 * 0.6
        dic1["CW money(付費版)"] += 1 + 3 * 0.6
        dic1["卡娜赫拉家計簿"] += 1 + 2 * 0.6
        dic1["記帳城市(免費版)"] += 1 + 1 * 0.6
        dic1["記帳城市(付費版)"] += 1 + 1 * 0.6
        dic1["碎碎念記帳"] += 1
    elif number == "2":
        dic1["簡單記帳"] += 1 + 10 * 0.4
        dic1["MOZE3.0(免費版)"] += 1 + 9 * 0.4
        dic1["MOZE3.0(付費版)"] += 1 + 9 * 0.4
        dic1["Ahorro"] += 1 + 8 * 0.4
        dic1["理財幫手 AndroMoney"] += 1 + 7 * 0.4
        dic1["天天記帳"] += 1 + 6 * 0.4
        dic1["記帳雞"] += 1 + 5 * 0.4
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.4
        dic1["CW money(免費版)"] += 1 + 3 * 0.4
        dic1["CW money(付費版)"] += 1 + 3 * 0.4
        dic1["卡娜赫拉家計簿"] += 1 + 2 * 0.4
        dic1["記帳城市(免費版)"] += 1 + 1 * 0.4
        dic1["記帳城市(付費版)"] += 1 + 1 * 0.4
        dic1["碎碎念記帳"] += 1
    elif number == "1":
        dic1["簡單記帳"] += 1 + 10 * 0.2
        dic1["MOZE3.0(免費版)"] += 1 + 9 * 0.2
        dic1["MOZE3.0(付費版)"] += 1 + 9 * 0.2
        dic1["Ahorro"] += 1 + 8 * 0.2
        dic1["理財幫手 AndroMoney"] += 1 + 7 * 0.2
        dic1["天天記帳"] += 1 + 6 * 0.2
        dic1["記帳雞"] += 1 + 5 * 0.2
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.2
        dic1["CW money(免費版)"] += 1 + 3 * 0.2
        dic1["CW money(付費版)"] += 1 + 3 * 0.2
        dic1["卡娜赫拉家計簿"] += 1 + 2 * 0.2
        dic1["記帳城市(免費版)"] += 1 + 1 * 0.2
        dic1["記帳城市(付費版)"] += 1 + 1 * 0.2
        dic1["碎碎念記帳"] += 1


def immediacy(number, dic1):  # 即時性，我們針對有「widget記帳功能」的APP定義為最有即時性，因此有其功能則會加分。
    if number == "5":
        dic1["CW money(免費版)"] += 11
        dic1["CW money(付費版)"] += 11
        dic1["MOZE3.0(付費版)"] += 11
    if number == "4":
        dic1["CW money(免費版)"] += 9
        dic1["CW money(付費版)"] += 9
        dic1["MOZE3.0(付費版)"] += 9
    if number == "3":
        dic1["CW money(免費版)"] += 7
        dic1["CW money(付費版)"] += 7
        dic1["MOZE3.0(付費版)"] += 7
    if number == "2":
        dic1["CW money(免費版)"] += 5
        dic1["CW money(付費版)"] += 5
        dic1["MOZE3.0(付費版)"] += 5
    if number == "1":
        dic1["CW money(免費版)"] += 3
        dic1["CW money(付費版)"] += 3
        dic1["MOZE3.0(付費版)"] += 3


def beauty(number, dic1):  # 美觀
    if number == "5":
        dic1["記帳城市(免費版)"] += 1 + 10 * 1
        dic1["記帳城市(付費版)"] += 1 + 10 * 1
        dic1["卡娜赫拉家計簿"] += 1 + 9 * 1
        dic1["簡單記帳"] += 1 + 8 * 1
        dic1["MOZE3.0(免費版)"] += 1 + 7 * 1
        dic1["MOZE3.0(付費版)"] += 1 + 7 * 1
        dic1["記帳雞"] += 1 + 6 * 1
        dic1["Ahorro"] += 1 + 5 * 1
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 1
        dic1["理財幫手 AndroMoney"] += 1 + 3 * 1
        dic1["天天記帳"] += 1 + 2 * 1
        dic1["碎碎念記帳"] += 1 + 1 * 1
        dic1["CW money(免費版)"] += 1
        dic1["CW money(付費版)"] += 1
    elif number == "4":
        dic1["記帳城市(免費版)"] += 1 + 10 * 0.8
        dic1["記帳城市(付費版)"] += 1 + 10 * 0.8
        dic1["卡娜赫拉家計簿"] += 1 + 9 * 0.8
        dic1["簡單記帳"] += 1 + 8 * 0.8
        dic1["MOZE3.0(免費版)"] += 1 + 7 * 0.8
        dic1["MOZE3.0(付費版)"] += 1 + 7 * 0.8
        dic1["記帳雞"] += 1 + 6 * 0.8
        dic1["Ahorro"] += 1 + 5 * 0.8
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.8
        dic1["理財幫手 AndroMoney"] += 1 + 3 * 0.8
        dic1["天天記帳"] += 1 + 2 * 0.8
        dic1["碎碎念記帳"] += 1 + 1 * 0.8
        dic1["CW money(免費版)"] += 1
        dic1["CW money(付費版)"] += 1
    elif number == "3":
        dic1["記帳城市(免費版)"] += 1 + 10 * 0.6
        dic1["記帳城市(付費版)"] += 1 + 10 * 0.6
        dic1["卡娜赫拉家計簿"] += 1 + 9 * 0.6
        dic1["簡單記帳"] += 1 + 8 * 0.6
        dic1["MOZE3.0(免費版)"] += 1 + 7 * 0.6
        dic1["MOZE3.0(付費版)"] += 1 + 7 * 0.6
        dic1["記帳雞"] += 1 + 6 * 0.6
        dic1["Ahorro"] += 1 + 5 * 0.6
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.6
        dic1["理財幫手 AndroMoney"] += 1 + 3 * 0.6
        dic1["天天記帳"] += 1 + 2 * 0.6
        dic1["碎碎念記帳"] += 1 + 1 * 0.6
        dic1["CW money(免費版)"] += 1
        dic1["CW money(付費版)"] += 1
    elif number == "2":
        dic1["記帳城市(免費版)"] += 1 + 10 * 0.4
        dic1["記帳城市(付費版)"] += 1 + 10 * 0.4
        dic1["卡娜赫拉家計簿"] += 1 + 9 * 0.4
        dic1["簡單記帳"] += 1 + 8 * 0.4
        dic1["MOZE3.0(免費版)"] += 1 + 7 * 0.4
        dic1["MOZE3.0(付費版)"] += 1 + 7 * 0.4
        dic1["記帳雞"] += 1 + 6 * 0.4
        dic1["Ahorro"] += 1 + 5 * 0.4
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.4
        dic1["理財幫手 AndroMoney"] += 1 + 3 * 0.4
        dic1["天天記帳"] += 1 + 2 * 0.4
        dic1["碎碎念記帳"] += 1 + 1 * 0.4
        dic1["CW money(免費版)"] += 1
        dic1["CW money(付費版)"] += 1
    elif number == "1":
        dic1["記帳城市(免費版)"] += 1 + 10 * 0.2
        dic1["記帳城市(付費版)"] += 1 + 10 * 0.2
        dic1["卡娜赫拉家計簿"] += 1 + 9 * 0.2
        dic1["簡單記帳"] += 1 + 8 * 0.2
        dic1["MOZE3.0(免費版)"] += 1 + 7 * 0.2
        dic1["MOZE3.0(付費版)"] += 1 + 7 * 0.2
        dic1["記帳雞"] += 1 + 6 * 0.2
        dic1["Ahorro"] += 1 + 5 * 0.2
        dic1["Spendee Budget & Money Tracker"] += 1 + 4 * 0.2
        dic1["理財幫手 AndroMoney"] += 1 + 3 * 0.2
        dic1["天天記帳"] += 1 + 2 * 0.2
        dic1["碎碎念記帳"] += 1 + 1 * 0.2
        dic1["CW money(免費版)"] += 1
        dic1["CW money(付費版)"] += 1


def fun(number, dic1):  # 趣味性
    '''
    依照我們表單所統計得到的資料：
    投票總人數中有一半的人認為小遊戲（記帳城市）可以增進記帳趣味性，
    而互動功能（記帳雞、碎碎念記帳）、小故事（卡娜赫拉家計簿）則有1/4的人認為可以增進趣味性，
    因此我們將記帳程式設為各number中的滿分，而記帳雞、碎碎念記帳、卡娜赫拉家計簿則是滿分的一半做計算。
    '''
    if number == "5":
        dic1["記帳城市(免費版)"] += 11
        dic1["記帳城市(付費版)"] += 11
        dic1["卡娜赫拉家計簿"] += 11/2
        dic1["記帳雞"] += 11/2
        dic1["碎碎念記帳"] += 11/2
    elif number == "4":
        dic1["記帳城市(免費版)"] += 9
        dic1["記帳城市(付費版)"] += 9
        dic1["卡娜赫拉家計簿"] += 9/2
        dic1["記帳雞"] += 9/2
        dic1["碎碎念記帳"] += 9/2
    elif number == "3":
        dic1["記帳城市(免費版)"] += 7
        dic1["記帳城市(付費版)"] += 7
        dic1["卡娜赫拉家計簿"] += 7/2
        dic1["記帳雞"] += 7/2
        dic1["碎碎念記帳"] += 7/2
    elif number == "2":
        dic1["記帳城市(免費版)"] += 5
        dic1["記帳城市(付費版)"] += 5
        dic1["卡娜赫拉家計簿"] += 5/2
        dic1["記帳雞"] += 5/2
        dic1["碎碎念記帳"] += 5/2
    elif number == "1":
        dic1["記帳城市(免費版)"] += 3
        dic1["記帳城市(付費版)"] += 3
        dic1["卡娜赫拉家計簿"] += 3/2
        dic1["記帳雞"] += 3/2
        dic1["碎碎念記帳"] += 3/2


def stop(reason, dic1):
    reasons = reason.replace(' ', '')
    reasons_list = reasons.split(",")
    for res in reasons_list:
        if res == "忘記花費":  # 用定位、錄音、拍照去回想（依功能多寡去做加分）
            dic1["碎碎念記帳"] += 1  # 可拍照
            dic1["CW money(免費版)"] += 2  # 可錄音、拍照
            dic1["CW money(付費版)"] += 2
            dic1["Spendee Budget & Money Tracker"] += 1  # 可定位
            dic1["記帳雞"] += 2  # 可錄音、拍照
        elif res == "忘記記帳":  # 用定時提醒去解決，所以有「定時提醒」功能者都會再多加一分
            dic1["CW money(免費版)"] += 1
            dic1["CW money(付費版)"] += 1
            dic1["天天記帳"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["簡單記帳"] += 1
            dic1["記帳城市(免費版)"] += 1
            dic1["記帳城市(付費版)"] += 1
            dic1["MOZE3.0(免費版)"] += 1
            dic1["MOZE3.0(付費版)"] += 1
            dic1["理財幫手 AndroMoney"] += 1
        elif res == "忙碌":  # 減少記帳時間：利用widget記帳、掃電子發票、常用分類快速選取解決
            dic1["CW money(免費版)"] += 3  # 三功能皆有
            dic1["CW money(付費版)"] += 3  # 三功能皆有
            dic1["碎碎念記帳"] += 1  # 可掃電子發票
            dic1["MOZE3.0(免費版)"] += 1  # 常用分類快速選取
            dic1["MOZE3.0(付費版)"] += 3  # 三功能皆有
            dic1["Ahorro"] += 1  # 可掃電子發票
            dic1["理財幫手 AndroMoney"] += 1  # 可掃電子發票
            dic1["簡單記帳"] += 1  # 常用分類快速選取
            dic1["記帳城市(免費版)"] += 1  # 常用分類快速選取
            dic1["記帳城市(付費版)"] += 1  # 常用分類快速選取
        elif res == "懶惰":
            dic1["CW money(免費版)"] += 3  # 三功能皆有
            dic1["CW money(付費版)"] += 3  # 三功能皆有
            dic1["碎碎念記帳"] += 1  # 可掃電子發票
            dic1["MOZE3.0(免費版)"] += 1  # 常用分類快速選取
            dic1["MOZE3.0(付費版)"] += 3  # 三功能皆有
            dic1["Ahorro"] += 1  # 可掃電子發票
            dic1["理財幫手 AndroMoney"] += 1  # 可掃電子發票
            dic1["簡單記帳"] += 1  # 常用分類快速選取
            dic1["記帳城市(免費版)"] += 1  # 常用分類快速選取
            dic1["記帳城市(付費版)"] += 1  # 常用分類快速選取
        elif res == "記帳麻煩":
            dic1["CW money(免費版)"] += 3  # 三功能皆有
            dic1["CW money(付費版)"] += 3  # 三功能皆有
            dic1["碎碎念記帳"] += 1  # 可掃電子發票
            dic1["MOZE3.0(免費版)"] += 1  # 常用分類快速選取
            dic1["MOZE3.0(付費版)"] += 3  # 三功能皆有
            dic1["Ahorro"] += 1  # 可掃電子發票
            dic1["理財幫手 AndroMoney"] += 1  # 可掃電子發票
            dic1["簡單記帳"] += 1  # 常用分類快速選取
            dic1["記帳城市(免費版)"] += 1  # 常用分類快速選取
            dic1["記帳城市(付費版)"] += 1  # 常用分類快速選取


def habit(reason, dic1):
    reasons = reason.replace(' ', '')
    reasons_list = reasons.split(",")
    for res in reasons_list:
        if res == "時常會借還錢":  # 有提醒借還錢功能者加一分
            dic1["MOZE3.0(付費版)"] += 1
            dic1["理財幫手 AndroMoney"] += 1
        if res == "需要信用卡 or 帳單繳費提醒":  # 有此功能者加一分
            dic1["MOZE3.0(付費版)"] += 1
        if res == "需要紀錄固定開銷":  # 有「設定固定開銷」功能者加一分
            dic1["天天記帳"] += 1
            dic1["Ahorro"] += 1
            dic1["簡單記帳"] += 1
            dic1["MOZE3.0(免費版)"] += 1
            dic1["MOZE3.0(付費版)"] += 1
            dic1["CW money(免費版)"] += 1
            dic1["CW money(付費版)"] += 1
        if res == "多帳戶管理（錢包、銀行、信用卡等分別紀錄）":  # 有多帳本功能者加一分
            dic1["CW money(免費版)"] += 1
            dic1["CW money(付費版)"] += 1
            dic1["MOZE3.0(免費版)"] += 1
            dic1["MOZE3.0(付費版)"] += 1
            dic1["Ahorro"] += 1
            dic1["理財幫手 AndroMoney"] += 1
            dic1["記帳城市(免費版)"] += 1
            dic1["記帳城市(付費版)"] += 1
            dic1["天天記帳"] += 1
            dic1["Spendee Budget & Money Tracker"] += 1
            dic1["碎碎念記帳"] += 1
        if res == "紀錄專案：紀錄特定事件所花的帳目（ex.旅行、週年慶）或 預算編製":
            # 有專案功能 or 編制預算功能者加一分
            dic1["MOZE3.0(免費版)"] += 1
            dic1["MOZE3.0(付費版)"] += 1
            dic1["天天記帳"] += 1
            dic1["碎碎念記帳"] += 1
            dic1["Ahorro"] += 1
            dic1["記帳城市(付費版)"] += 1
            dic1["CW money(免費版)"] += 1
            dic1["CW money(付費版)"] += 1
        if res == "需要紀錄不同貨幣":  # 有可用不同貨幣記帳or匯率轉換功能者加一分  
            dic1["理財幫手 AndroMoney"] += 1
            dic1["記帳城市(免費版)"] += 1
            dic1["記帳城市(付費版)"] += 1
            dic1["CW money(免費版)"] += 1
            dic1["CW money(付費版)"] += 1
            dic1["天天記帳"] += 1


def total(dic1):
    max(dic1.values())
    for key, value in dic1.items():
        if value == max(dic1.values()):
            return key


if __name__ == '__main__':
    print(run_new_json())
    print(judgement(id='U4068c37804d834081ea24fe8d4521ab9'))
    print(judgement(id='F54091196'))
