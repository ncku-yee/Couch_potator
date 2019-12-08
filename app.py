import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_sticker, send_image_url, send_button_message, send_carousel_uri_message, send_carousel_image_message

load_dotenv()

machine = TocMachine(
    states=["user", "search_comic", "select_match", "select_episode", "view_comic", "next_page", "show_fsm", \
            "search_animate", "select_animate", "search_yt", "select_yt"],
    transitions=[
        # Every state backs to user state has the highest priority. 
        {
            "trigger": "advance",
            "source": ["search_comic", "view_comic", "select_match", "select_episode", "next_page", "search_animate", "search_yt"],
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "show_fsm",
            "conditions": "is_going_to_show_fsm",
        },
        {
            "trigger": "advance",
            "source": "show_fsm",
            "dest": "user",
            "conditions": "is_going_to_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search_animate",
            "conditions": "is_going_to_search_animate",
        },        
        {
            "trigger": "advance",
            "source": "search_animate",
            "dest": "select_animate",
            "conditions": "is_going_to_select_animate",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search_yt",
            "conditions": "is_going_to_search_yt",
        }, 
        {
            "trigger": "advance",
            "source": "search_yt",
            "dest": "select_yt",
            "conditions": "is_going_to_select_yt",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search_comic",
            "conditions": "is_going_to_search_comic",
        },
        {
            "trigger": "advance",
            "source": "search_comic",
            "dest": "select_match",
            "conditions": "is_going_to_select_match",
        },
        {
            "trigger": "advance",
            "source": "select_match",
            "dest": "select_episode",
            "conditions": "is_going_to_select_episode",
        },
        {
            "trigger": "advance",
            "source": "select_episode",
            "dest": "view_comic",
            "conditions": "is_going_to_view_comic",
        },

        {
            "trigger": "advance",
            "source": "view_comic",
            "dest": "next_page",
            "conditions": "is_going_to_next_page",
        },
        {
            "trigger": "advance",
            "source": "next_page",
            "dest": "next_page",
            "conditions": "is_going_to_next_page",
        },
        {
           "trigger": "advance",
            "source": "next_page",
            "dest": "view_comic",
            "conditions": "is_going_to_view_comic",
        }, 
        {
           "trigger": "advance",
            "source": "view_comic",
            "dest": "view_comic",
            "conditions": "is_going_to_view_comic",
        }, 
        {"trigger": "back_user", "source": "next_page", "dest": "user"},
        {"trigger": "back_search", "source": "select_match", "dest": "search_comic"},
        {"trigger": "back_match", "source": "select_episode", "dest": "select_match"},
        {"trigger": "back_select", "source": "view_comic", "dest": "select_episode"},
        {"trigger": "back_animate", "source": "select_animate", "dest": "search_animate"},
        {"trigger": "back_yt", "source": "select_yt", "dest": "search_yt"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    # app.logger.info(f"Signature: {signature}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        response = machine.advance(event)
        if response == False:
            if machine.state == "user":
                message_label = ["看漫畫", "看動漫", "youtube", "FSM"]
                message_text = ["看漫畫", "看動漫", "youtube", "FSM"]
                send_button_message(event.reply_token, "指令集", \
                    "請點選以下指令，以繼續動作\n隨時都可輸入\"退出\"回到本頁面", "https://i.imgur.com/HYZkYHr.jpg", message_label, message_text)
            elif machine.state == "show_fsm":
                send_text_message(event.reply_token, "\udbc0\udc7c請輸入\"退出\"以繼續操作\udbc0\udc7c")
            elif machine.state == "next_page":
                send_button_message(event.reply_token, "無此指令", \
                    "請選擇以下指令以繼續觀賞", "https://i.imgur.com/HYZkYHr.jpg", ["下一頁", "退出"], ["下一頁", "退出"])
            # if machine.state == "show_fsm" or "search_animate" or "search_yt" or "search_comic" or "select_episode" or "select_match":


    return "OK"

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
