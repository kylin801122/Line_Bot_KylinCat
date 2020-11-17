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
    # 回傳google地圖
    if "聯成" in user_message:
        message = LocationSendMessage(title="聯成電腦",
                                      address="234新北市永和區永和路二段59號4樓",
                                      latitude=25.011189,
                                      longitude=121.514564)
        line_bot_api.reply_message(event.reply_token, message)
    # 回傳特定訊息
    if "貓咪" in user_message:
        message = TextSendMessage(text="給我罐頭 !")
        line_bot_api.reply_message(event.reply_token, message)
    # 回傳圖片訊息
    if "圖片" in user_message:
        # preview_image_url預覽縮圖、original_content_url實際開啟圖
        message = ImageSendMessage(original_content_url='https://cdn.hk01.com/di/media/images/564720/org/7a5b31ccd89a2360794c1ef6bf54393f.jpg/0ws2YFTJcguqJ5hF1Hp3V8ELwZfAP_rMiLU2UYi1NlE?v=w1920',
                                   preview_image_url='https://storage.googleapis.com/www-cw-com-tw/article/201810/article-5bd182cf13ebb.jpg')
        line_bot_api.reply_message(event.reply_token, message)
    # 回傳影片訊息
    if "影片" in user_message:
        message = VideoSendMessage(original_content_url='https://video-previews.elements.envatousercontent.com/h264-video-previews/4103404.mp4',
                                   preview_image_url='https://cdn.hk01.com/di/media/images/564720/org/7a5b31ccd89a2360794c1ef6bf54393f.jpg/0ws2YFTJcguqJ5hF1Hp3V8ELwZfAP_rMiLU2UYi1NlE?v=w1920')
        line_bot_api.reply_message(event.reply_token, message)
    # 回傳使用者輸入內容
    if"喵" in user_message:
        message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
