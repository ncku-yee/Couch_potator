# Couch_potator

## Brief description of this LINE chat-bot

#### Feature 1(Browse comic book)
We provide more than a hundreds of comic books.<br/>
You can search comic you would like to browse through our LINE chat-bot.<br/>
After searching, if we can find the match comic, we will show the episode list.<br/>
You can choose the specific episode, and we will show the content on the screen.<br/>
<br/>
#### Feature 2(Browse animate)_(Currently, only success to run on ngrok.)_
You can search any animates you would like to browse through our LINE chat-bot.<br/>
After searching, we will show you the most relative result, and gives you the URL.<br/>
You can click the URL, and enjoy your video.<br/>
<br/>
#### Feature 3(Youtube)
You can search any videos you would like to browse through our LINE chat-bot.<br/>
After searching, we will show you the most relative result, and gives you the URL.<br/>
You can click the URL, and enjoy your video.<br/>
<br/>
#### Feature 4(FSM)
By the way, you can also type [```fsm```/```FSM```] to get the image of **finite state machine**.

## Finite State Machine
![image](https://comic-animate-yt.herokuapp.com/show-fsm)

## Set up
The environment of this application is shown below.

* [Python](https://www.python.org/downloads/) **(Version == 3.6)**
* Pipenv
* HTTPS Server **(We use [ngrok](https://ngrok.com/download))**
* A LINE bot **(You should create a account by yourself)**

You can follow the intruction we provide.

#### For Windows:
Step1.<br/>
In ```Pipfile.lock```, we have already generated the virtual environment for python.<br/>
You can just type ```pipenv shell``` on your terminal.<br/>
If you want to create a specific virtual environment.<br/>
**You must follow the below instrucitons.**<br/>

```
pip install pipenv

pipenv --python 3.6

pipenv install -r requirement.txt

pipenv shell
```

\* ```pipenv install -r requirement.txt``` will get the packages in ```requirement.txt```, so if you want to install other packages, you must add the packages name in ```requirement.txt``` before ```pipenv install -r requirement.txt```.<br/>
\* If you have problem for installing ```pygraphviz```, you can take the below as reference.<br/> 

* Go to ```/Graphviz2.38``` ,then installing ```graphviz-2.38.exe``` and extracting ```graphviz-2.38_x64.tar```.
* Copy the whole files in ```graphviz-2.38_x64.tar``` into the directory where you install your ```graphviz-2.38```.
* Add the path ```your path to graphviz-2.28/bin``` as your system environment .
* Final, type ```pipenv install pygraphviz-1.5-cp36-cp36m-win_amd64.whl``` on your terminal.

Step2.<br/>
1. Go to [LINE Developers](https://developers.line.biz/zh-hant/) website.<br/>
2. Logon with your LINE account.<br/>
3. Create a provider.<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/create_provider.jpg)
4. Click **Create a Messaging API channel** and fill in some information about your chat-bot.<br/>
5. Issue your **Channel secret** and copy.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/issue_secret.jpg)
6. Issue your **Channel access token** and copy.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/issue_token.jpg)
7. Enabled your **Webhook URL**

Step3.<br/>
1. You should generate a file called ```.env```.<br/>
2. Set ```LINE_CHANNEL_SECRET``` with the **Channel secret** you copy in Step2.<br/>
3. Set ```LINE_CHANNEL_ACCESS_TOKEN``` with the **Channel access token** you copy in Step2.<br/>
4. Set ```port=8000```.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/example_env.jpg)

Step4.<br/>
1. Installing [ngrok](https://ngrok.com/download).
2. Open your ngrok and it will open a terminal automatically.
3. Type the following instruciton ```ngrok http 8000```.
4. If successfully implements, it would like the image below.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/ngrok_instruction.jpg)

Step5.<br/>
1. You can check the request status by open the [URL](http://127.0.0.1:4040) on browser in ngrok **Web Interface**.<br/>
2. You should copy the URL(Begining with _https://_) **Forwarding** in ngrok to section **Webhook URL** in [LINE Developers](https://developers.line.biz/zh-hant/), and add ```/{route}```<br/>
For example. ```https://fb1557fe.ngrok.io/webhook```<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/webhook.jpg)
\***!!Watch out!!** You **MUST** enabled **Webhook URL**<br/>

Step6.<br/>
1. On your terminal, type the instruction ```python app.py```
2. Besure you have set your ```.env```  file already.
3. If successfully executes the ```app.py```, it would like the image below.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/executed_successfully.jpg)<br/>
\* If you don't set ```LINE_CHANNEL_SECRET```, it would like the image below.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/secret_not_set.jpg)<br/>
\* If you don't set ```LINE_CHANNEL_ACCESS_TOKEN```, it would like the image below.
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/token_not_set.jpg)<br/>


## Usage
The initial state is set to ```user```.<br/>
Every time ```user``` state is triggered to ```advance``` to another state, you can type ```退出``` / ```返回``` / ```exit``` / ```quit``` to go back to ```user``` state.
1. For ```user``` state is tiggered to ```search_comic``` state.<br/>
    * Input: "看漫畫"
        * Reply: "(hello)請輸入漫畫名稱(hello)"
    * Input: "看影片"
        * Reply: "(sad)沒有這個指令(sad)"<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/user_state.jpg)<br/>

2. For ```user``` state is tiggered to ```search_animate``` state.<br/>
    * Input: "看動漫"
        * Reply: "(hello)請輸入動漫名稱(hello)"
    * Input: "看影片"
        * Reply: "(sad)沒有這個指令(sad)"<br/>
    * **For example:**<br/>   
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/search_animate.jpg)<br/>

3. For ```search_animate``` state is tiggered to ```select_animate``` state.<br/>
    * **Important: Can not run on Heroku(Reason is not found currently, but it still can run on ngrok.)**
    * Input: Any keywords is OK(e.g. **海賊王**)
        * Reply: "(love)搜尋結果:(love)<br/>
		海賊王(第912集):<br/>
		https://ani.gimy.tv/vod-play-id-32-src-1-num-1.html<br/>
		海賊王/航海王(更新至912集):<br/>
		https://ani.gimy.tv/vod-play-id-3342-src-1-num-1.html<br/>
		海賊王劇場版10：強者天下(HD):<br/>
		https://ani.gimy.tv/vod-play-id-3856-src-1-num-1.html<br/>
		海賊王：狂熱行動(HC):<br/>
		https://ani.gimy.tv/vod-play-id-5931-src-1-num-1.html<br/>
		海賊王劇場版1：黃金島冒險(HD1280高清中字版):<br/>
		https://ani.gimy.tv/vod-play-id-3859-src-1-num-1.html<br/>
		海賊王劇場版3：珍獸島的喬巴王國(HD1280高清中字版):<br/>
		https://ani.gimy.tv/vod-play-id-3864-src-1-num-1.html..."<br/>
		or<br/>
		"(blue)找不到此動漫(blue)<br/>
		請重新輸入動漫名稱(james wink)<br/>
		(aww)或是輸入退出(aww)"
	* **Will back to ```search_animate``` state.**<br/>
    * **For example:**<br/>   
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/result_animate.jpg)<br/>

4. For ```user``` state is tiggered to ```search_yt``` state.<br/>
    * Input: "YT" or "youtube"
        * Reply: "(hello)請輸入關鍵字(hello)"
    * Input: "看影片"
        * Reply: "(sad)沒有這個指令(sad)"<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/search_yt.jpg)<br/>

5. For ```search_yt``` state is tiggered to ```select_yt``` state.<br/>
    * Input: Any keywords is OK(e.g. **太陽**)
        * Reply: "(love)搜尋結果:(love)<br/>
		標題:邱振哲PikA 【 太陽 】 Official Music Video(4:24)<br/>
		https://www.youtube.com/watch?v=7vlVjfMl_Nk<br/>
		標題:曲肖冰 - 太陽『我只想做你的太陽，在你的心裡呀，在你的心底呀。』【動態歌詞Lyrics】(4:18)<br/>
		https://www.youtube.com/watch?v=UpiATw00vx8<br/>
		標題:中國好聲音2019【第一期】 馬杰雪-太陽(4:22<br/>
		https://www.youtube.com/watch?v=nrkuOHH51v0<br/>
		標題:【太阳兽】新家开箱，居家爱用物分享(12:18)<br/>
		https://www.youtube.com/watch?v=_dc3tIdzAns<br/>
		標題:马杰雪 - 太阳(Live)『就算不能在你身旁 也要奋力为你而发光 ♪』【動態歌詞】(4:30)<br/>
		https://www.youtube.com/watch?v=RISGV-s4Og4 ..."<br/>
		or<br/>
		"(blue)找不到視頻(blue)<br/>
		請重新輸入關鍵字(james wink)<br/>
		(aww)或是輸入退出(aww)"
	 * **Will back to ```search_yt``` state.**<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/result_yt.jpg)<br/>

6. For ```user``` state is tiggered to ```show_fsm``` state.<br/>
    * Input: "fsm"
        * Reply: ![image](https://comic-animate-yt.herokuapp.com/show-fsm)<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/show_fsm.jpg)<br/>

7. For ```search_comic``` state is tiggered to ```select_match``` state.<br/>
    * Input: "海賊王"
        * Reply: "(sparkling eyes)以下為搜尋結果:(sparkling eyes)<br/>
		 1. 特別篇 海賊王X龍珠<br/>
		 2. 海賊王<br/>
		請選擇其中一個漫畫繼續觀賞"
    * Input: "漫畫"
        * Reply: "(blue)沒有此漫畫(blue)<br/>
                  請重新輸入漫畫名稱(james wink)<br/>
                  (aww)或是輸入退出(aww)"
        * **Will back to ```search_comic``` state.**<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/search_comic.jpg)<br/>

8. For ```select_match``` state is tiggered to ```select_episode``` state.<br/>
    * Input: "海賊王"
        * Reply: "(sparkling eyes)以下為搜尋集數:(sparkling eyes)<br/>
		第001卷 ~ 第068卷<br/>
		第679話 ~ 第964話<br/>
		輸入你要的集數可以觀看該回漫畫(cony kiss)"
    * Input: "海賊"
        * Reply: "(tongue out)輸入錯誤漫畫(tongue out)<br/>
		請再次從以下結果中選擇其中一個漫畫:(hmph)<br/>
		 1. 特別篇 海賊王X龍珠<br/>
		 2. 海賊王"
        * **Will back to ```select_match``` state.**<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/select_match.jpg)<br/>

9. For ```select_episode``` state is tiggered to ```view_comic``` state.<br/>
    * Input: "第964話"
        * Reply: ![image](https://pic.8comic.se/wp-content/uploads/a04cj84wj6uq04/1152/964/001.jpg)
    * Input: "第999話"
        * Reply: "(blue)沒有此回漫畫(blue)<br/>
                  請重新輸入集數(james wink)"
        * **Will back to ```select_episode``` state.**<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/select_comic.jpg)<br/>

10. For ```view_comic``` state is tiggered to ```next_page``` state.<br/>
    * Input: "N" / "n" / "Next" / "下一頁"
        * Reply: ![iamge](https://pic.8comic.se/wp-content/uploads/a04cj84wj6uq04/1152/964/002.jpg)
    * Input: "上一頁"
        * Reply: "(sad)沒有這個指令(sad)"<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/view_state.jpg)<br/>

11. In any state, you can type ```退出``` / ```返回``` / ```exit``` / ```quit``` to go back to ```user``` state.<br/>
    * Input: "退出" / "返回" / "exit" / "quit"
        * Reply: "(sparkling eyes)請輸入指令(sparkling eyes)"<br/>
    * **For example:**<br/>
![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/exit.jpg)<br/>

## Deploy on Heroku
Now, my LINE chat-bot is deployed on heroku.<br/>
**URL:** https://dashboard.heroku.com/apps/comic-animate-yt/deploy/heroku-git

### Heroku CLI installation

**For Windows:** https://devcenter.heroku.com/articles/heroku-cli<br/>
**For Ubuntu 16+:** Type the instruction on your terminal `sudo snap install --classic heroku`<br/>

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

   `heroku login`<br/>
   The broswer will open the login page.<br/>
   ![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/login_page.jpg)<br/>
   After login successgully, it would like the image below.<br/>
   ![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/login_success.jpg)<br/>

### Upload project to Heroku

1. Add local project to Heroku project<br/>
	`heroku git:remote -a {HEROKU_APP_NAME}`<br/>
   
2. Upload project<br/>
	```
	git add .
	git commit -m "YOUR COMMIT"
	git push -f heroku master
	```
   
3. Set Environment - Line Messaging API Secret Keys<br/>
	```
	heroku config:set LINE_CHANNEL_SECRET={your_line_channel_secret}
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN={your_line_channel_access_token}
	```
   
4. Your Project is now running on Heroku!<br/>

	URL you need to copy to WebhookURL in LINE Developers: `https://{HEROKU_APP_NAME}.herokuapp.com/{route}`<br/>
   \* `{route}` may be `webhook` or `callback`<br/>
	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`<br/>

5. If you fail to install `pygraphviz` when pushing project, try the following instructions<br/>
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
   	git push -f heroku master
	```
   
6. If you want to use the `{route} = show_fsm`, type the following instruciton<br/>
   ```
   heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-graphviz
   ```
   **Verify after you add the buildpack:**<br/>
   ```
   heroku run dot -V
   ```
   **You can open your browser and type the URL:** `https://{HEROKU_APP_NAME}.herokuapp.com/show_fsm`<br/>
   The image of finite state machine will show on your browser.<br/> 
   ![image](https://github.com/ncku-yee/Couch_potator/blob/master/img/heroku_fsm.jpg)<br/>
