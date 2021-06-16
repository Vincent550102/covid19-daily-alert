from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    TemplateSendMessage
)
from random import randint
from time import sleep
import datetime
import configparser,json
from DataBase.DataBase import DATABASE
from crawler import crawler
import psycopg2
app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

def push_mess(uid, mess):
    line_bot_api.push_message(
        uid,
        TextMessage(text=mess)
    )

def reply_mess(event, mess):
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=mess)
    )

def alert_all(db):
    checked_num = crawler()
    data = db.Select()
    for uid in data:
        push_mess(uid[0], "早安你好，昨天整天的 COVID19 確診者共有: {} 人。".format(checked_num))

def external():
    db = DATABASE()
    alert_all(db)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    mess = event.message.text
    uid = event.source.user_id
    db = DATABASE()
    if mess=="OK":
        db.Insert(uid)
        reply_mess(event, "這是昨天的確診數，之後每天早上 7:00 將會為您更新昨天的確診數歐~")
        alert_all(db)
    elif mess=="test":
        alert_all(db)
    elif mess=="debug":
        print(datetime.datetime.now().ctime())
        print(db.Select())
    else:
        reply_mess(event, "不明命令 code:404")
    db.Close()
if __name__ == "__main__":
    app.run()
