import os
import re
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

from tools.tools import Tools
import Actions

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("^画像\s")
def message_hello(message, say):
    tools = Tools()

    match = re.search("^画像\s(.+)", message['blocks'][0]['elements'][0]['elements'][0]['text'])
    image_name = match.group(1)
    imageList = tools.getImageUrl(image_name)

    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    #say(f"Hey there <@{message['user']}>!")

    say(imageList[0])

# 'hello' を含むメッセージをリッスンします
@app.message("hello")
def message_hello(message, say):
#    Act = Actions.Actions()
#
#    print (Act.test(message))
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> clicked the button")


# アプリを起動します
if __name__ == "__main__":
    # handler = SlackRequestHandler(app)

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    # flask_app = Flask(__name__)
    # flask_app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

