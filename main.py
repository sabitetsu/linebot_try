from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 基本的にここにコードを書いていきます。
    print("メッセージ受付")
    message = event.message.text
    if message == "スタート" and quiz == "ぬる":
        print("開始！")
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="クイズ開始！")
            ])
        questions(event)
    elif message == "テスト":
        test(event)
    elif message == "クイズ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=quiz))
    elif quiz != "ぬる":
        resText = answers(quiz,message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resText))
        isEnd = check_end()
        if isEnd == "true":
            end_quiz(event)
        else:
            questions(event)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))
    print("テキスト送った")

sampleQuiz = ["客が来店した","客が退店する","注文を受ける","注文を通す","注文を持っていく"]
sampleAns = ["いらっしゃいませ","ありがとうございました","ご注文お伺いします","オーダー入ります","ご注文の品です"]
quiz = "ぬる"
quizNum = 0
resNum = 0

#def questions(rand):
#    sampleData = ["客が来店した","客が退店する","注文を受ける","注文を通す"]
#    return sampleData[rand]

def start_quiz():
    print("クイズスタート")
    #quiz = sampleQuiz[1]
    global quiz
    quiz = sampleQuiz[1]
    return quiz

def test(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message(
                profile.user_id,
                [
                    TextSendMessage(text="テストだよ"),
                    TextSendMessage(text="スコア：/5")
                ])

def questions(event):
    print("問題")
    global quiz
    quiz = sampleQuiz[quizNum]
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message(
                profile.user_id,
                TextSendMessage(text=quiz)
                )

def check_end():
    print("終わった？")
    global quizNum
    print(quizNum)
    if quizNum < 4:
        quizNum += 1
        print(quizNum)
        return "false"
    else:
        quizNum = 0
        return "true"


def end_quiz(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message(
                profile.user_id,
                [
                    TextSendMessage(text="クイズ終了"),
                    TextSendMessage(text="スコア："+ str(resNum) +"/5")
                ])

def answers(question,ans):
    print("答え合わせ")
    global resNum
    if question == sampleQuiz[0]:
        if ans == sampleAns[0]:
            res = "正解"
            resNum += 1
        else:
            res = "不正解"
    elif question == sampleQuiz[1]:
        if ans == sampleAns[1]:
            res = "正解"
            resNum += 1
        else:
            res = "不正解"
    elif question == sampleQuiz[2]:
        if ans == sampleAns[2]:
            res = "正解"
            resNum += 1
        else:
            res = "不正解"
    elif question == sampleQuiz[3]:
        if ans == sampleAns[3]:
            res = "正解"
            resNum += 1
        else:
            res = "不正解"
    elif question == sampleQuiz[4]:
        if ans == sampleAns[4]:
            res = "正解"
            resNum += 1
        else:
            res = "不正解"
    else:
        res = "よくわからない"
    global quiz
    quiz = "ぬる"
    print(quiz)
    return res


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

