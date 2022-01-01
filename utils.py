import os

from linebot import LineBotApi, WebhookParser
from linebot.models import CarouselTemplate ,CarouselColumn ,MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage,FlexSendMessage

from moviecard import moviecard,briefinfocard,videocard,updatecard

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_text_button_update(reply_token, title):
    line_bot_api = LineBotApi(channel_access_token)
    t = updatecard
    t['body']['contents'][0]['text'] = title
    line_bot_api.reply_message(reply_token, FlexSendMessage('moviecard',t))

    return "OK"

def send_carousel_message(reply_token, movielist):
    line_bot_api = LineBotApi(channel_access_token)
    col = []
    for i in range(len(movielist)):
        c = CarouselColumn(
            thumbnail_image_url = movielist[i][1],
            text = '上映日期 : ' + movielist[i][2],
            actions=[
                MessageTemplateAction(
                    label = movielist[i][0][0:19],
                    text = movielist[i][0],
                )
            ]
        )
        col.append(c)
        if i>=9:
            break
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=col,image_size='contain'
        ),
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_carousel_message_leader(reply_token, movielist):
    line_bot_api = LineBotApi(channel_access_token)
    col = []
    for i in range(len(movielist)):
        c = CarouselColumn(
            thumbnail_image_url = movielist[i][1],
            title = '本週排名 : ' + str(movielist[i][3]),
            text = movielist[i][2],
            actions=[
                MessageTemplateAction(
                    label = movielist[i][0][0:19],
                    text = movielist[i][0],
                )
            ]
        )
        col.append(c)
        if i>=9:
            break
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=col,image_size='contain'
        ),
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_carousel_message_movie(reply_token, info,imgurl,moviename):
    line_bot_api = LineBotApi(channel_access_token)
    t = moviecard
    t['hero']['url'] = imgurl
    t['body']['contents'][0]['text'] = moviename
    t['body']['contents'][1]['contents'][0]['text'] = info
    t['footer']['contents'][0]['action']['label'] = '預告片'
    t['footer']['contents'][0]['action']['text'] = '預告片'
    t['footer']['contents'][1]['action']['label'] = '劇情簡介'
    t['footer']['contents'][1]['action']['text'] = '劇情簡介'
    t['footer']['contents'][2]['action']['label'] = '返回首頁'
    t['footer']['contents'][2]['action']['text'] = '返回首頁'
    line_bot_api.reply_message(reply_token, FlexSendMessage('moviecard',t))

    return "OK"

def send_carousel_message_video(reply_token, videourl,imgurl,back):
    line_bot_api = LineBotApi(channel_access_token)
    t = videocard
    t['hero']['url'] = imgurl
    t['footer']['contents'][0]['action']['uri'] = videourl
    t['footer']['contents'][1]['action']['text'] = back
    line_bot_api.reply_message(reply_token, FlexSendMessage('moviecard',t))

    return "OK"

def send_carousel_message_briefinfo(reply_token, info,title,back):
    line_bot_api = LineBotApi(channel_access_token)
    t = briefinfocard
    t['body']['contents'][0]['text'] = title
    t['body']['contents'][1]['text'] = '\n'+info[0:299]
    t['footer']['contents'][0]['action']['text'] = back
    line_bot_api.reply_message(reply_token, FlexSendMessage('moviecard',t))

    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
