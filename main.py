from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

# Token
channel_access_token = "EP8rVpoA5OuSJ+KdvzijoN8HjLQdOpMBuUnxI0sNpI6WNXsgYHVo7goD6a1rbn+KOjnDD+ibrDNXvyj4MFdcoNXVyu2PdGj1cwZ7lBm/uyEcx3n+fLWxwg39xFlTN2aD6p0UkGuP/8kOHQ5LifhL3AdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(channel_access_token)
channel_secret = "0473c95b3ad046e263f9b2eb400ba5e2"
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
    if ["MENU", "menu", "Menu", "目錄"] in user_message:
        menu = """
        目前指令有: 
        貓咪、圖片
        影片、地圖
        """
        message = TextSendMessage(text=menu)
    # 使用者輸入包含"貓咪"，訊息為文字訊息
    if "貓咪" in user_message:
        message = TextSendMessage(text="給我罐頭 !")
    # 使用者輸入包含"圖片"，訊息為圖片訊息
    if "圖片" in user_message:
        # preview_image_url預覽縮圖、original_content_url實際開啟圖
        message = ImageSendMessage(original_content_url="https://i.imgur.com/qTQOkol.jpg",
                                   preview_image_url="https://i.imgur.com/qTQOkol.jpg")
    # 使用者輸入包含"影片"，訊息為影片訊息
    if "影片" in user_message:
        # preview_image_url影片預覽縮圖、original_content_url實際開啟影片
        message = VideoSendMessage(original_content_url="https://i.imgur.com/nwide3z.mp4",
                                   preview_image_url="https://i.imgur.com/qTQOkol.jpg")
    # 使用者輸入包含"地圖"，訊息為google地圖
    if "地圖" in user_message:
        message = LocationSendMessage(title="猴硐貓村",
                                      address="224新北市瑞芳區侯硐",
                                      latitude=25.088678,
                                      longitude=121.827537)
    # 使用者輸入包含"喵"，訊息為回傳使用者輸入內容
    if"喵" in user_message:
        message = TextSendMessage(text=user_message)
    # 回傳訊息內容
    line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
