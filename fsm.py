from transitions.extensions import GraphMachine

from utils import send_text_message, send_sticker, send_image_url, send_button_message, send_carousel_uri_message, send_carousel_text_message, send_carousel_image_message, send_confirm_message

import re
import requests
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup as bs
import random

class TocMachine(GraphMachine):
    # Some variables that shared by all funciton
    # requests object
    session_requests = None
    # Store the information of recommand comic
    recommand_comic_list = None
    recommand_comic_url_list = None
    # Record every state whether it is success or fail
    search_result = None
    # Store the comic name from the search result
    match_comic_name = None
    # Store the comic url from the search result
    match_comic_url = None
    # Store the comic image from the search result
    match_comic_image = None
    # The episode list and description URL for corresponding comic
    search_url = None
    # The episode list of the specific comic 
    comic_episode_list = None
    # The url of episode list of the specific comic 
    comic_episode_url_list = None
    # Record current episode
    current_episode = None
    # Record the total page of episode
    total_page = None
    # Record the current page of episode
    current_page = None
    # The src of the image
    current_page_url = None
    # Flag to record that whether find the comic in csv(True = Not found)
    comic_not_found = None
    # Flag to record that whether can match your choice to the search result(True = Not match)
    comic_select_not_found = None
    # Flag to record that whether find the episode in comic_episode_list(True = Not found)
    episode_not_found = None
    # Flag to record that whether the current page is tha last page(True = Last page)
    end_of_page = None
    # Flag to record that whether find the animate in seraching page
    animate_not_found = None
    # Flag to record that whether find the youtube in seraching page
    yt_not_found = None
    # Flag to record that whether the state is from select_yt to search_yt
    yt_loop = None
    # Flag to record that whether the state is from select_animate to search_animate
    animate_loop = None

    # List for send_carousel_uri_message function 
    message_image = None
    message_uri = None
    message_text = None
    message_title = None

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.session_requests = requests.session()
        # Initialize the flag
        self.comic_not_found = False
        self.episode_not_found = False
        self.end_of_page = False
        self.animate_not_found = False
        self.yt_not_found = False
        self.yt_loop = False
        self.animate_loop = False
        self.comic_select_not_found = False

    # For user state
    def is_going_to_user(self, event):
        text = event.message.text
        return text == "返回" or text == "退出" or text.lower() == "quit" or text.lower() == "exit"

    def on_enter_user(self, event):
        print("I'm entering user")
        reply_token = event.reply_token
        if not self.end_of_page:
                message_label = ["看漫畫", "看動漫", "youtube", "FSM"]
                message_text = ["看漫畫", "看動漫", "youtube", "FSM"]
                send_button_message(event.reply_token, "指令集", \
                    "請點選以下指令，以繼續動作\n隨時都可輸入\"退出\"回到本頁面", "https://i.imgur.com/HYZkYHr.jpg", message_label, message_text)
        else:
            
            send_text_message(reply_token, "已經是最新一集的最後一頁囉\udbc0\udc83\n請再次重新輸入指令\udbc0\udc96\n如果忘記有哪些指令可輸入\"指令集\"\udbc0\udc8d")
        # Back to user state, need to initialize the flag
        self.comic_not_found = False
        self.episode_not_found = False
        self.end_of_page = False
        self.animate_not_found = False
        self.yt_not_found = False
        self.yt_loop = False
        self.animate_loop = False
        self.comic_select_not_found = False

    def on_exit_user(self, event=None):
        print("Leaving user") 

    # For search_comic state
    def is_going_to_search_comic(self, event):
        text = event.message.text
        return text == "看漫畫"

    def on_enter_search_comic(self, event):
        print("I'm entering search_comic")
        reply_token = event.reply_token
        if not self.comic_not_found:
            url = "http://8comic.se/"
            res = requests.get(url)
            soup = bs(res.text,'html.parser')
            comic_list = []
            url_list = []
            self.recommand_comic_list = []
            self.recommand_comic_url_list = []
            for entry in soup.find('div', class_='carousel-clip').select('a'):
                m = re.search("http://8comic.se/(\d*)/$",entry['href'])
                if(m):
                    if entry.find('img') != None:
                        comic_list.append(entry.find('img')['alt'])
                    else:
                        url_list.append(entry['href'])
            random_sample = random.sample([index for index in range(len(url_list))], 4)
            for random_index in random_sample:
                self.recommand_comic_list.append(comic_list[random_index])
                self.recommand_comic_url_list.append(url_list[random_index])
            send_button_message(event.reply_token, "請輸入漫畫名稱", \
                    "以下4部漫畫為系統推薦\n隨時都可輸入\"退出\"回到本頁面", "https://i.imgur.com/HYZkYHr.jpg", self.recommand_comic_list, self.recommand_comic_list)
        else:
            send_text_message(reply_token, "\udbc0\udc92沒有此漫畫\udbc0\udc92\n請重新輸入漫畫名稱\udbc0\udc8a\n\udbc0\udc9d或是輸入退出\udbc0\udc9d")
            self.comic_not_found = False

    def on_exit_search_comic(self, event):
        print("Go to select_episode")

    # For select_match state
    def is_going_to_select_match(self, event):
        text = event.message.text
        # First to check if user select comic from recommand list
        if text in self.recommand_comic_list:
            self.search_result = "The comic is in recommand list"
            self.match_comic_name = [text[:20]]
            self.match_comic_url = [self.recommand_comic_url_list[self.recommand_comic_list.index(text)]]
            result = self.session_requests.get(self.recommand_comic_url_list[self.recommand_comic_list.index(text)])
            soup = bs(result.text, 'html.parser')
            preview_image = soup.find('img')['src']
            preview_image = re.sub(r"http:", "https:", preview_image)
            self.match_comic_image = [preview_image]
            self.message_title = ["選擇推薦漫畫"]
        else:
            url = "http://8comic.se/搜尋結果/?w=" + text
            result = self.session_requests.get(url)
            soup = bs(result.text, 'html.parser')
            search_title = None
            search_url = None
            self.search_result = ''
            self.match_comic_name = []
            self.match_comic_url = []
            self.match_comic_image = []
            self.message_title = []
            index = 0
            for entry in soup.select('a'):
                m = re.search("^/(\d*)/$",entry['href'])
                if(m):
                    # At most list 9 matches(left 1 for error message)
                    if index == 9:
                        break
                    search_title = entry.text
                    search_url = entry['href']
                    self.match_comic_name.append(search_title[:20])
                    self.match_comic_url.append("http://8comic.se/" + search_url)
                    self.search_result += ("{}. {}\n".format(index+1, search_title))
                    # Get preview image for searching result
                    result = self.session_requests.get("http://8comic.se/" + search_url)
                    soup = bs(result.text, 'html.parser')
                    preview_image = soup.find('img')['src']
                    preview_image = re.sub(r"http:", "https:", preview_image)
                    self.match_comic_image.append(preview_image)
                    self.message_title.append("搜尋結果{}".format(index + 1))
                    index += 1
        return True
        
    def on_enter_select_match(self, event):
        print("I'm entering select_match")
        reply_token = event.reply_token
        if not self.search_result:
            self.comic_not_found = True
            self.back_search(event)
        else:
            if not self.comic_select_not_found:
                send_carousel_text_message(reply_token, self.message_title, self.match_comic_image, self.match_comic_name)
            else:
                send_carousel_text_message(reply_token, \
                    ["選擇失敗(請重新選擇)"] + self.message_title, \
                    ["https://i.imgur.com/3xofosk.jpg"] + self.match_comic_image, \
                    ["退出"] + self.match_comic_name)
                self.comic_select_not_found = False

    def on_exit_select_match(self, event=None):
        print("Leaving select_match")

    # For select_episode state
    def is_going_to_select_episode(self, event):
        text = event.message.text
        if text in self.match_comic_name:
            self.search_url = self.match_comic_url[self.match_comic_name.index(text)]
        else:
            self.search_url = ""
        return True
        
    def on_enter_select_episode(self, event):
        print("I'm entering select_episode")
        reply_token = event.reply_token
        if not self.search_url:
            self.comic_select_not_found = True
            self.back_match(event)
        else:
            result = self.session_requests.get(self.search_url)
            soup = bs(result.text, 'html.parser')
            episode_object = soup.select('tr')
            self.comic_episode_list = []
            self.comic_episode_url_list = []
            # Store the search list into comic_episode_list and comic_episode_url_list
            for episode in episode_object:
                for information in episode.find_all('a'):
                    self.comic_episode_url_list.append(information['href'])
                    self.comic_episode_list.append(information.text)
            reply_message = "{} ~ {}\n".format(self.comic_episode_list[0], self.comic_episode_list[-1])
            if self.comic_episode_list[0].find("卷") != -1:
                for index in range(len(self.comic_episode_list)):
                    if self.comic_episode_list[index].find("卷") != -1:
                        continue
                    else:
                        reply_message = "{} ~ {}\n{} ~ {}\n"\
                            .format(self.comic_episode_list[0], self.comic_episode_list[index-1], self.comic_episode_list[index], self.comic_episode_list[-1])
                        break 
            reply_message += "輸入你要的集數可以觀看該回漫畫"
            newest_episodes = self.comic_episode_list[-4:]
            if not self.episode_not_found:
                send_button_message(reply_token, "以下為搜尋集數", reply_message, self.match_comic_image[self.match_comic_url.index(self.search_url)], newest_episodes, newest_episodes)
            else:
                send_button_message(reply_token, "沒有該集漫畫(請重新輸入)", reply_message, self.match_comic_image[self.match_comic_url.index(self.search_url)], newest_episodes, newest_episodes)
                self.episode_not_found = False

    def on_exit_select_episode(self, event=None):
        print("Leaving select_episode")

    # For view_comic state
    def is_going_to_view_comic(self, event):
        text = event.message.text
        # Check if the current state is in next_page
        if self.state == "next_page" and text not in self.comic_episode_list:
            return False
        if text in self.comic_episode_list:
            self.current_episode = text
            self.current_page_url = self.comic_episode_url_list[self.comic_episode_list.index(text)]
            # Get all content of websie
            result_episode = self.session_requests.get(self.current_page_url)
            soup_episode = bs(result_episode.text, 'html.parser')
            # Get the src of the first page and information about total page 
            self.current_page_url = soup_episode.find(id="caonima")['src']
            page_info = soup_episode.find(id="infotxtb").text
            self.total_page = int(re.search("共(\d*)頁]$", page_info).group(1))
            self.current_page = int(re.search("第(\d*)頁", page_info).group(1))
            # Generate the url of the first page
            self.current_page_url = re.sub(r"http:", "https:", self.current_page_url)
            self.current_page_url = re.sub(r"(\d*).jpg", "{:0>3d}.jpg".format(self.current_page), self.current_page_url) 
        else:
            self.current_page_url = ""
        return True       

    def on_enter_view_comic(self, event):
        print("I'm entering view_comic")
        reply_token = event.reply_token
        # The select episode is invalid
        if not self.current_page_url:
            self.episode_not_found = True
            self.back_select(event)
        else:
            current_page_url_list = []
            current_page_list = []
            for i in range(10):
                if self.current_page > self.total_page:
                    send_carousel_image_message(reply_token, current_page_url_list, current_page_list)
                    return
                else:
                    self.current_page_url = re.sub(r"(\d*).jpg", "{:0>3d}.jpg".format(self.current_page), self.current_page_url) 
                    current_page_url_list.append(self.current_page_url)
                    current_page_list.append("第{:0>3d}頁".format(self.current_page))
                    self.current_page += 1
            send_carousel_image_message(reply_token, current_page_url_list, current_page_list)

    def on_exit_view_comic(self, event=None):
        print("Leaving view_comic")  

    # For next_page state
    def is_going_to_next_page(self, event):
        text = event.message.text
        return text == "下一頁" or text.lower() == "next" or text.lower() == "n"

    def on_enter_next_page(self, event):
        print("I'm entering next_page")
        reply_token = event.reply_token
        # Check if the current page link is not last page,
        # then back to initial state and return
        if self.current_page > self.total_page:
            print("Already reach the last page.")
            # You have not already ready read the lastest episode
            if self.current_episode != self.comic_episode_list[-1]:
                index = self.comic_episode_list.index(self.current_episode)
                # Next episode does not exist
                if index + 1 == len(self.comic_episode_list):
                    send_button_message(reply_token, "已經是最後一頁囉!!", "請選擇繼續觀看下(上)一話或是退出", \
                        self.match_comic_image[self.match_comic_url.index(self.search_url)],\
                        [self.comic_episode_list[index - 1], "退出"], \
                        [self.comic_episode_list[index - 1], "退出"])
                # Last episode does not exist
                elif index - 1 < 0:
                    send_button_message(reply_token, "已經是最後一頁囉!!", "請選擇繼續觀看下(上)一話或是退出", \
                        self.match_comic_image[self.match_comic_url.index(self.search_url)],\
                        [self.comic_episode_list[index + 1], "退出"], \
                        [self.comic_episode_list[index + 1], "退出"])
                else:
                    send_button_message(reply_token, "已經是最後一頁囉!!", "請選擇繼續觀看下(上)一話或是退出", \
                        self.match_comic_image[self.match_comic_url.index(self.search_url)],\
                        [self.comic_episode_list[index - 1], self.comic_episode_list[index + 1], "退出"], \
                        [self.comic_episode_list[index - 1], self.comic_episode_list[index + 1], "退出"])
            else: 
                self.end_of_page = True
                self.back_user(event)
        else:
            # Update the next_page URL
            self.current_page_url = re.sub(r"(\d*).jpg", "{:0>3d}.jpg".format(self.current_page), self.current_page_url) 
            self.on_enter_view_comic(event)

    def on_exit_next_page(self, event=None):
        print("Leaving next_page") 

    # For show_fsm state
    def is_going_to_show_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_show_fsm(self, event):
        print("I'm entering show_fsm")
        reply_token = event.reply_token
        send_image_url(reply_token, "https://comic-animate-yt.herokuapp.com/show-fsm")

    def on_exit_show_fsm(self, event=None):
        print("Leaving show_fsm") 

    # For search_animate state
    def is_going_to_search_animate(self, event):
        text = event.message.text
        return text == "看動漫" or text.lower() == "animate"

    def on_enter_search_animate(self, event):
        print("I'm entering search_animate")
        reply_token = event.reply_token
        if self.animate_loop:
            self.animate_loop = False
            return True
        if not self.animate_not_found:
            send_text_message(reply_token, "\uDBC0\uDC84請輸入動漫名稱\uDBC0\uDC84")
        else:
            send_text_message(reply_token, "\udbc0\udc92找不到此動漫\udbc0\udc92\n請重新輸入動漫名稱\udbc0\udc8a\n\udbc0\udc9d或是輸入退出\udbc0\udc9d")
            self.animate_not_found = False

    def on_exit_search_animate(self, event):
        print("Leaving search_animate")

    # For select_animate state
    def is_going_to_select_animate(self, event):
        text = event.message.text
        # Headers for this search website
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookies": "savelist=%E6%B5%B7%E8%B3%8A%E7%8E%8B%24%24%24%24%24%24wrw65165",
            "Host": "www.99kubo.tv",
            "Pragma": "no-cache",
            "Referer": "http://www.99kubo.tv/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        url = "http://www.99kubo.tv/index.php?s=home-vod-innersearch&q=" + text
        result = self.session_requests.get(url, headers=headers)
        soup = bs(result.text, 'html.parser')
        self.search_result = ''
        self.message_title = [] 
        self.message_image = []
        self.message_text = [] 
        self.message_uri = []
        time_list = []
        match_count = 0
        for entry in soup.select('cite'):
            # Max match results
            if match_count == 10:
                break
            time_list.append(entry.text)
            match_count += 1
        match_count = 0
        for entry in soup.select('a'):
            m = re.search("/vod-read-id-(\d*).html",entry['href'])
            if m:
                # At most list 10 matches
                if match_count == 10:
                    break
                if entry.find('img') == None:
                    title = entry.text.split('-')[0]
                    self.message_text.append(title[:60])
                    self.message_uri.append("http://www.99kubo.tv" + entry['href'])
                    match_count += 1
                    # Get preview image
                else:
                    self.message_image.append(entry.find('img')['src'])
        for index in range(len(self.message_uri)):
            self.message_title.append("搜尋結果{}".format(index + 1))
            self.search_result += ("標題: {}\n{}\n{}\n".format(self.message_text[index], time_list[index], self.message_uri[index]))
        return True
        
    def on_enter_select_animate(self, event):
        print("I'm entering select_animate")
        reply_token = event.reply_token
        # If search result is empty string
        if not self.search_result:
            self.animate_not_found = True
        else:
            send_carousel_uri_message(reply_token, self.message_title, self.message_image, self.message_text, self.message_uri)
            self.animate_loop = True
        self.back_animate(event)

    def on_exit_select_animate(self, event=None):
        print("Leaving select_animate")

    # For serach_yt state
    def is_going_to_search_yt(self, event):
        text = event.message.text
        return text.lower() == "youtube" or text.lower() == "yt"

    def on_enter_search_yt(self, event):
        print("I'm entering search_yt")
        reply_token = event.reply_token
        # If state transition is from select_yt to here
        if self.yt_loop:
            self.yt_loop = False
            return True
        if not self.yt_not_found:
            url = "https://www.youtube.com/feed/trending?gl=TW&hl=zh-TW"
            result = self.session_requests.get(url)
            soup = bs(result.text, 'html.parser')
            last = None
            time = None
            title = None
            self.message_title = ["搜尋Youtube"]
            self.message_text = ["請輸入關鍵字，以下為熱門影片"]
            self.message_uri = ["https://www.youtube.com/feed/trending?gl=TW&hl=zh-TW"]
            self.message_image = ["https://i.imgur.com/mv789PL.png"]
            match_count = 0
            for entry in soup.select('a'):
                m = re.search("v=(.*)",entry['href'])
                if m:
                    # Get the hash value for the video
                    target = m.group(1)
                    # Filter the playlist of searching result
                    if re.search("list",target):
                        continue
                    # At most list 10 matches
                    if match_count == 9:
                        break
                    # Get the preview image for the video
                    if entry.find('img') != None:
                        if re.match("(.*).gif", entry.find('img')['src']):
                            self.message_image.append(entry.find('img')['data-thumb'])
                        else:
                            self.message_image.append(entry.find('img')['src'])
                    # Get the time for the video
                    if re.match(r"(\s*)(\d*):(\d*)", entry.text):
                        time = entry.text.split('\n')[2]
                        continue
                    last = target
                    # Get the title for the video
                    title = entry.text
                    match_count += 1
                    self.message_uri.append("https://www.youtube.com/watch?v=" + target)
                    self.message_text.append(title[:60])
                    self.message_title.append("熱門排行{}".format(match_count))
            send_carousel_uri_message(reply_token, self.message_title, self.message_image, self.message_text, self.message_uri)
        else:
            send_text_message(reply_token, "\udbc0\udc92找不到視頻\udbc0\udc92\n請重新輸入關鍵字\udbc0\udc8a\n\udbc0\udc9d或是輸入退出\udbc0\udc9d")
            self.yt_not_found = False

    def on_exit_search_yt(self, event):
        print("Leaving search_yt")

    # For select_yt state
    def is_going_to_select_yt(self, event):
        text = event.message.text
        url = "https://www.youtube.com/results?search_query=" + text
        result = self.session_requests.get(url)
        soup = bs(result.text, 'html.parser')
        last = None
        time = None
        title = None
        self.search_result = ''
        self.message_title = []
        self.message_text = []
        self.message_uri = []
        self.message_image = []
        match_count = 0
        for entry in soup.select('a'):
            m = re.search("v=(.*)",entry['href'])
            if m:
                # Get the hash value for the video
                target = m.group(1)
                # Filter the playlist of searching result
                if re.search("list",target):
                    continue
                # At most list 10 matches
                if match_count == 10:
                    break
                # Get the preview image for the video
                if entry.find('img') != None:
                    if re.match("(.*).gif", entry.find('img')['src']):
                        self.message_image.append(entry.find('img')['data-thumb'])
                    else:
                        self.message_image.append(entry.find('img')['src'])
                # Get the time for the video
                if re.match(r"(\s*)(\d*):(\d*)", entry.text):
                    time = entry.text.split('\n')[2]
                    continue
                last = target
                # Get the title for the video
                title = entry.text
                match_count += 1
                self.message_uri.append("https://www.youtube.com/watch?v=" + target)
                self.message_text.append(title[:60])
                self.message_title.append("搜尋結果{}".format(match_count))
                self.search_result += ("標題:{}({})\nhttps://www.youtube.com/watch?v={}\n".format(title, time, target))
        return True
        
    def on_enter_select_yt(self, event):
        print("I'm entering select_yt")
        reply_token = event.reply_token
        # If search result is empty string
        if not self.search_result:
            self.yt_not_found = True
        else:
            send_carousel_uri_message(reply_token, self.message_title, self.message_image, self.message_text, self.message_uri)
            self.yt_loop = True
        self.back_yt(event)

    def on_exit_select_yt(self, event):
        print("Leaving select_yt")
