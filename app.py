from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('Kvk8dM0IO2bXNzsqCIs3PMfGzaLMZDlhySSCodRIZgXK0otS8m01r4C7eAx6VBbVquFNy+mFmBnVWKtKXf82UMayJZQ8WNXnD/xnEodP6crpqwyHeeZzSpfC9SOvc1SaRLbLck1xlt8yltYBTA8y3gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ea244f552168d152418896215d9b262d')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "感謝您的回復，本功能尚在開發中，敬請期待!!"

    if "給我貼圖" in msg:
        sticker_message = StickerSendMessage(
            package_id='11539',
            sticker_id='52114131'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ["hi", "Hi"]:
        r = "嗨"
    elif msg == "功能":
        r = "功能列表正在開發中"
    elif msg == "你是誰":
         r ="我是一個正在學習的機器人"
    elif "預約" in msg:
        r = "目前預約人數眾多，請稍待回復"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()