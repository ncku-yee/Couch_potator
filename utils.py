import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage, TemplateSendMessage, ImagemapSendMessage
from linebot.models import URIImagemapAction, MessageTemplateAction, PostbackTemplateAction, URITemplateAction, MessageImagemapAction
from linebot.models importCarouselTemplate, , ImageCarouselTemplate, ButtonsTemplate,  ConfirmTemplate
from linebot.models import CarouselColumn, ImageCarouselColumn, BaseSize, ImagemapArea


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_image_url(reply_token, img_url):
    message = ImageSendMessage(
        original_content_url = img_url,
        preview_image_url = img_url
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_sticker(reply_token, package_id, sticker_id):
    message = StickerSendMessage(
        package_id = package_id,
        sticker_id = sticker_id
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_button_message(reply_token, title, text, image_url, message_label, message_text):
    actions = []
    for index in range(len(message_label)):
        actions.append(MessageTemplateAction(
            label = message_label[index],
            text = message_text[index]
        ))
    message = TemplateSendMessage(
        alt_text = "請輸入指令",
        template = ButtonsTemplate(
            thumbnail_image_url = image_url,
            title = title,
            text = text,
            actions = actions
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_carousel_uri_message(reply_token, message_title, message_image, message_text, message_uri):
    columns = []
    for index in range(len(message_image)):
        columns.append(CarouselColumn(
                thumbnail_image_url = message_image[index],
                title = message_title[index],
                text = message_text[index],
                actions = [
                    URITemplateAction(
                        label = "跳轉連結",
                        uri = message_uri[index]
                    )
                ]
            )
        )
    message = TemplateSendMessage(
        alt_text = "影片搜尋結果",
        template = CarouselTemplate(
        columns = columns
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_carousel_text_message(reply_token, message_title, message_image, message_text):
    columns = []
    for index in range(len(message_image)):
        columns.append(CarouselColumn(
                thumbnail_image_url = message_image[index],
                title = message_title[index],
                text = message_text[index],
                actions=[
                    MessageTemplateAction(
                        label = message_text[index],
                        text = message_text[index]
                    )
                ]
            )
        )
    message = TemplateSendMessage(
        alt_text = "漫畫搜尋結果",
        template = CarouselTemplate(
        columns = columns
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_carousel_image_message(reply_token, message_image, message_text):
    columns = []
    for index in range(len(message_image)):
        columns.append(ImageCarouselColumn(
                image_url = message_image[index],
                action = URITemplateAction(
                        label = message_text[index],
                        uri = message_image[index]
                    )
            )
        )
    message = TemplateSendMessage(
        alt_text = "漫畫內文",
        template = ImageCarouselTemplate(
        columns = columns
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_confirm_message(reply_token, confirm_text, next_episode):
    message = TemplateSendMessage(
        alt_text = '目錄 template',
        template = ConfirmTemplate(
            title = '確認',
            text = confirm_text,
            actions=[                              
                MessageTemplateAction(
                    label = next_episode,
                    text = next_episode,
                ),
                MessageTemplateAction(
                    label = "退出",
                    text = "退出"
                )
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"