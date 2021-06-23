# -*- coding: utf-8 -*-
import Linebot_function as lf  # import自己寫的linebot功能
from threading import Timer
from bs4 import BeautifulSoup
import app_recommend
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import requests
import os
import json
import configparser
from linebot.models import *
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import Flask, request, abort, send_file

# import XXXX 時如果有error，請google python install XXXX，通常在terminal下 pip install XXXX 指令就可以安裝了
#
# line bot api reference: https://github.com/line/line-bot-sdk-python

app = Flask(__name__, static_folder='/')  # 建立 Flask 物件

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))

# 如果重開ngrok，記得在這裡以及line channel後台更新網址
ngrok_url = 'https://0e665e4ca977.ngrok.io'


# 載入richmenu
def richmenu():
    try:
        channel_access_token = config.get('line-bot', 'channel-access-token')

        line_bot_api = LineBotApi(channel_access_token)

        headers = {"Authorization": "Bearer " +
                   channel_access_token, "Content-Type": "application/json"}
        body = json.load(
            open('./richmenu/richmenu.json', 'r', encoding='utf-8'))
        req = requests.request(
            'POST', "https://api.line.me/v2/bot/richmenu", headers=headers, data=json.dumps(body).encode('utf-8'))
        a = req.text[15:56]
        with open("./richmenu/richmenu.png", 'rb') as f:
            line_bot_api.set_rich_menu_image(a, "image/jpeg", f)
        req = requests.request(
            'POST', 'https://api.line.me/v2/bot/user/all/richmenu/' + a, headers=headers)
    except:
        pass


@app.route("/callback", methods=['POST'])  # 路由
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 收到語音訊息__記帳


@handler.add(MessageEvent, message=AudioMessage)
def handle_message(event):
    print(event)
    a = lf.return_alert_data()[event.source.user_id]["audio"]
    print(a)
    if event.source.type == 'user':
        a = int(a)+1
        lf.enter_alert_audio_data(event.source.user_id, str(a))
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="記得記帳"))


# 收到message event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)  # 看event長怎樣
    text = event.message.text

    if text == "記帳推薦":
        recommend_message = lf.setting_recommend_message()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="記帳推薦",
                contents=recommend_message))
    elif text == "記帳推薦!":
        muilt_reply = []
        muilt_reply.append(TextSendMessage
                           (text="以下為您的ID以及推薦你適合記帳程式的連結。\n進入連結後請在第一題填入我們提供的ID進行，謝謝！"))
        muilt_reply.append(TextSendMessage(text=event.source.user_id))
        muilt_reply.append(TextSendMessage(text='https://forms.gle/9i3bmXM6QXJv3gpV8'))
        line_bot_api.reply_message(
            event.reply_token, muilt_reply)

    elif text == "推薦結果":
        app_recommend.run_new_json()   #此步驟是先讓問卷json檔有新的資料
        with open('questionnaire_data.json', 'r', encoding='utf-8') as object:
            q_d = json.load(object)

        if event.source.user_id in q_d:
            app = app_recommend.judgement(event.source.user_id)
            system = q_d[event.source.user_id]["你的手機系統?"]
            with open('app_download_url.json', 'r', encoding='utf-8') as object:
                a_d_u = json.load(object)
            muilt_reply = []
            muilt_reply.append(TextSendMessage(text="我會推薦你用「" + app + "」去紀錄帳目"))
            muilt_reply.append(TextSendMessage(text=a_d_u[system][app]))
            line_bot_api.reply_message(
                event.reply_token, muilt_reply)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請點選「記帳推薦」進行分析後再來看結果噢"))
    elif text == "想換記帳程式":
        with open('user_recommend_data.json', 'r', encoding='utf-8') as object:
            u_r_d = json.load(object)
        del u_r_d[event.source.user_id][app_recommend.total(event.source.user_id)]
        with open('questionnaire_data.json', 'r', encoding='utf-8') as object:
            q_d = json.load(object)
        app = app_recommend.total(u_r_d)
        system = q_d[event.source.user_id]["你的手機系統?"]
        with open('app_download_url.json', 'r', encoding='utf-8') as object:
            a_d_u = json.load(object)
        muilt_reply = []
        muilt_reply.append(TextSendMessage(text="試試「" + app + "」去紀錄帳目如何？"))
        muilt_reply.append(TextSendMessage(text=a_d_u[system][app]))
        line_bot_api.reply_message(
            event.reply_token, muilt_reply)

    elif text == "記帳提醒":
        flex_message = lf.setting_alert_message()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="記帳提醒",
                contents=flex_message)
        )
        lf.alert_data(event.source.user_id)

    elif text == "網址":  # liff網址
        response = "https://liff.line.me/1656056998-RP6bYLXr"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=response))

    elif text == "我又沒有唸書":
        # send image_message
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(
                original_content_url=ngrok_url + "/image/can_not_read.jpg",
                preview_image_url=ngrok_url + "/image/can_not_read.jpg"
            )
        )
        return
    elif text == "功能":
        if event.source.type == 'group':  # 群組功能
            group_id = event.source.group_id
            user_id = event.source.user_id
            profile = line_bot_api.get_profile(user_id)
            user_name = profile.display_name

            # set flex message
            flex_message = lf.setting_flex_message()
            # set action uri of flex message
            flex_message["footer"]["contents"][0]["action"]["uri"] = ngrok_url + \
                '/webpage/index.html?groupId=' + group_id + \
                '&userId=' + user_id + '&userName=' + user_name
            # send flex message to user
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='群組功能',
                    contents=flex_message)
            )

            # web
            ##
            # soup = BeautifulSoup(
            #     ngrok_url + '/webpage/index.html?groupId=' + event.source.group_id, 'html.parser')
            # member_select = soup.find(id="member-select")

            # new_option = soup.new_tag("option", value=member_name)
            # member_select.append
            return

        elif event.source.type == 'user':  # 個人功能
            response = "個人功能"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=response))

    elif text == "已經記了":
        lf.enter_alert_audio_data(event.source.user_id, "0")
    elif text=="取消提醒":
        lf.cancel_alert(event.source.user_id)
    else:
        return

# 收到Postback event


@ handler.add(PostbackEvent)
def handle_postback(event):
    print(event)
    postback = event.postback.data
    time = event.postback.params

    if postback == "time":
        reply = "設定成功!將於每日"+time["time"]+"提醒你記帳!"
        lf.enter_alert_time_data(
            user_id=event.source.user_id, tm=time["time"],)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply))


# 收到join event
@ handler.add(JoinEvent)
def handle_join(event):
    print(event)
    # reply image message
    line_bot_api.reply_message(
        event.reply_token, ImageSendMessage(
            original_content_url=ngrok_url + "/image/hi.jpg",
            preview_image_url=ngrok_url + "/image/hi.jpg"
        )
    )


def alert():
    while lf.get_alert_time_user():

        alert_id, audio_id = lf.get_alert_time_user()
        # print(user_id)

        try:
            for i in alert_id:
                flex_message = lf.setting_check_message()
                line_bot_api.push_message(i, FlexSendMessage(
                    alt_text='記得每天記帳喲~',
                    contents=flex_message))
                # break
            # break
            for i in audio_id:

                mess = "你還有{}筆語音還沒紀錄".format(
                    lf.return_alert_data()[i]["audio"])
                line_bot_api.push_message(i, TemplateSendMessage(
                                          alt_text=mess,
                                          template=ConfirmTemplate(
                                              text=mess,
                                              actions=[
                                                  MessageAction(
                                                      label='已經記了',
                                                      text='已經記了'
                                                  ),
                                                  MessageAction(
                                                      label='等等再說',
                                                      text='等等再說'
                                                  )
                                              ]
                                          )
                                          ))
                break
            break
        except:
            pass


if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    sched = BackgroundScheduler()
    sched.add_job(alert, 'cron', second=0)
    sched.start()





if __name__ == "__main__":
    richmenu()
    app.run(debug=True)
