from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

# Channel Access Token
channel_access_token = "YPXcebu/6k54mgrYRpbgQH+kgNyG7UEAUgLhRC7qqqZfsc+0CSKDiwnthHpV4JHX2GxEqPdchkFCzGBsuPc63t7oJD/RfliWSL60VfCzLo1kqQrVVAdCHjNthxqjWhQlVw2pdxA+48jWwz9jFPPWIAdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(channel_access_token)

# Channel Secret
channel_secret = "db0b224884da4516785b84c0fe6da1a1"
handler = WebhookHandler(channel_secret)


# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if "聯成" in user_message:
        location = LocationSendMessage(title='Lcclocation', address='Lcc', latitude=25.011189,
                                       longitude=121.514564)
        message = TextSendMessage(text=location)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
