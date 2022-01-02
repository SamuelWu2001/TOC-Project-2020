from transitions import Machine

from utils import send_text_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from utils import send_text_message, send_button_message,send_image_message,send_carousel_message,send_carousel_message_leader,send_carousel_message_movie,send_carousel_message_video,send_carousel_message_briefinfo,send_text_button_update
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

moviedict = {}
movieurl = ''

class TocMachine(Machine):
    def __init__(self, **machine_configs):
        self.machine = Machine(model=self, **machine_configs)

    def is_going_to_welcome(self, event):
        if event.message.text!='預告片' and event.message.text!='劇情簡介':
            return True
        else:
            return False
    
    def is_going_to_update(self, event):
        return event.message.text == "更新資料"

    def is_going_to_commingsoon(self, event):
        return event.message.text == "即將上映"

    def is_going_to_nowshowing(self, event):
        return event.message.text == "熱映電影"

    def is_going_to_leaderboard(self, event):
        return event.message.text == "排行榜"

    def is_going_to_movie(self, event):
        global moviedict,movieurl
        movieurl = moviedict.get(event.message.text,None)
        if movieurl==None:
            return False
        else:
            return True
    def is_going_to_video(self, event):
        return event.message.text == "預告片"

    def is_going_to_briefinfo(self, event):
        return event.message.text == "劇情簡介"

    def on_enter_welcome(self, event):
        print("I'm entering welcome")
        title = '歡迎光臨威秀影城'
        text = '您可以直接輸入電影名稱或是由下方功能列表輔助篩選'
        btn = [
            MessageTemplateAction(
                label = '即將上映',
                text ='即將上映'
            ),
            MessageTemplateAction(
                label = '熱映電影',
                text = '熱映電影'
            ),
            MessageTemplateAction(
                label = '排行榜',
                text = '排行榜'
            ),
            MessageTemplateAction(
                label = '更新資料',
                text = '更新資料'
            ),
        ]
        url = 'https://play-lh.googleusercontent.com/2Qb6GILluUbL2-nQS36YtXox9UJpfmhF5emtiHXNNYMyN3ku8cunfCkntesWO-BQMQ'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_update(self,event):
        global moviedict
        ua = UserAgent()
        moviedict = {}
        for i in range(1,3):
            response = requests.get("https://www.vscinemas.com.tw/vsweb/film/coming.aspx?p="+str(i),headers={'User-Agent':ua.random})
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                for movie in soup.find('ul',{'class':'movieList'}).find_all('li'):
                    url = 'https://www.vscinemas.com.tw/vsweb/film/'+movie.find('h2').find('a').get('href')
                    title = movie.find('h2').find('a').text
                    moviedict[title]=url
            except:
                continue
        for i in range(1,6):
            response = requests.get("https://www.vscinemas.com.tw/vsweb/film/index.aspx?p="+str(i),headers={'User-Agent':ua.random})
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                for movie in soup.find('ul',{'class':'movieList'}).find_all('li'):
                    movieurl = 'https://www.vscinemas.com.tw/vsweb/film/'+movie.find('h2').find('a').get('href')
                    title = movie.find('h2').find('a').text
                    moviedict[title]=movieurl
            except:
                continue
        send_text_button_update(event.reply_token,'資料更新完畢')

    def on_enter_commingsoon(self, event):
        ua = UserAgent()
        response = requests.get("https://www.vscinemas.com.tw/vsweb/film/coming.aspx",headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        movielist = []
        for movie in soup.find('ul',{'class':'movieList'}).find_all('li'):
            title = movie.find('a').find('img').get('title')
            imgurl = 'https://www.vscinemas.com.tw/vsweb'+movie.find('a').find('img').get('src')[2:]
            time = movie.find('time').text
            movielist.append((title,imgurl,time))
        send_carousel_message(event.reply_token, movielist)

    def on_enter_nowshowing(self, event):
        ua = UserAgent()
        response = requests.get("https://www.vscinemas.com.tw/vsweb/film/index.aspx",headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        movielist = []
        for movie in soup.find('ul',{'class':'movieList'}).find_all('li'):
            title = movie.find('a').find('img').get('title')
            imgurl = 'https://www.vscinemas.com.tw/vsweb'+movie.find('a').find('img').get('src')[2:]
            time = movie.find('time').text
            movielist.append((title,imgurl,time))
        send_carousel_message(event.reply_token, movielist)

    def on_enter_leaderboard(self, event):
        ua = UserAgent()
        index=1
        response = requests.get("https://www.vscinemas.com.tw/vsweb/film/hot.aspx",headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.find('section',{'class':"hotArea"})
        imgurl = 'https://www.vscinemas.com.tw/vsweb' + text.find('figure').find('a').find('img').get('src')[2:]
        title = soup.find('section',{'class':"hotInfo"}).find('div',{'class':"info"}).find('h1').find('a').text
        name = soup.find('section',{'class':"hotInfo"}).find('div',{'class':"info"}).find('h2').text
        movielist = [(title,imgurl,name,index)]

        for movie in soup.find('ul',{'class':'hotList'}).find_all('li'):
            index+=1
            imgurl = 'https://www.vscinemas.com.tw/vsweb'+movie.find('figure').find('a').find('img').get('src')[2:]
            title = movie.find('section',{'class':'infoArea'}).find('h2').find('a').text
            name = movie.find('section',{'class':'infoArea'}).find('h3').text
            movielist.append((title,imgurl,name,index))
        send_carousel_message_leader(event.reply_token,movielist)

    def on_enter_movie(self, event):
        global movieurl
        ua = UserAgent()
        response = requests.get(movieurl,headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('div',{'class':'infoArea'}).find('table')
        info = table.findNext('td').text + table.findNext('td').findNext('td').find('p').text +'\n'+ table.findNext('td').findNext('td').findNext('td').text+ table.findNext('td').findNext('td').findNext('td').findNext('td').find('p').text+'\n'+ table.findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').text+ table.findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').text+'\n'+ table.findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').text+ table.findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').text
        imgurl = 'https://www.vscinemas.com.tw/vsweb'+soup.find('div',{'class':'movieMain'}).find('figure').find('img').get('src')[2:]
        send_carousel_message_movie(event.reply_token, info,imgurl,event.message.text)

    def on_enter_video(self, event):
        global movieurl,moviedict
        title = [k for k,v in moviedict.items() if v==movieurl]
        title = title[0]
        ua = UserAgent()
        response = requests.get(movieurl,headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        videourl = soup.find('div',{'class':'slidesArea'}).find('div').find('iframe').get('src')
        imgurl = 'https://www.vscinemas.com.tw/vsweb'+soup.find('div',{'class':'movieMain'}).find('figure').find('img').get('src')[2:]
        print(videourl,imgurl)
        send_carousel_message_video(event.reply_token,videourl,imgurl,title)


    def on_enter_briefinfo(self, event):
        global movieurl,moviedict
        title = [k for k,v in moviedict.items() if v==movieurl]
        title = title[0]
        ua = UserAgent()
        response = requests.get(movieurl,headers={'User-Agent':ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        infotext = ''
        for info in soup.find('div',{'class':'bbsArticle'}).find_all('p'):
            infotext += info.text
        send_carousel_message_briefinfo(event.reply_token,infotext,"劇情簡介:",title)

    def on_exit_welcome(self,x):
        print("Leaving welcome")

    def on_exit_nowshowing(self,x):
        print("Leaving welcome")

    def on_exit_commingsoon(self,x):
        print("Leaving theater")

    def on_exit_leaderboard(self,x):
        print("Leaving theater")

    def on_exit_movie(self,x):
        print("Leaving theater")
        
    def on_exit_video(self,x):
        print("Leaving theater")
