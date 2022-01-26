import praw
import requests
import ctypes
import os
import time
import hashlib
from secrets import CLIENT_ID,CLIENT_SECRET,USER_AGENT

def main(subreddit):
    reddit = praw.Reddit(
    client_id= CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT)
    current_image_path = "images\\image.jpg"
    
    for submission in reddit.subreddit(subreddit).top():
        if submission.url.endswith(".jpg"):
            file = requests.get(submission.url)
            remote_url = submission.url
            break
    try: 
        file
    except NameError:
        print("No .jpg images in the r/%s subreddit" %(subreddit))
        quit()
        
    def md5Checksum(filePath,url):
        m = hashlib.md5()
        if url==None:
            with open(filePath, 'rb') as fh:
                m = hashlib.md5()
                while True:
                    data = fh.read(8192)
                    if not data:
                        break
                    m.update(data)
                return m.hexdigest()
        else:
            r = requests.get(url)
            for data in r.iter_content(8192):
                m.update(data)
            return m.hexdigest()
        
    def images_identical(): #compares local image to remote
        if md5Checksum(current_image_path,None)==md5Checksum(None,remote_url): 
            return True
        return False
        
    if os.path.exists(current_image_path):
        if not images_identical():
            os.makedirs("images\\" + time.strftime("/%Y/%m/%d"), exist_ok=True) #make directory for current day
            os.rename(current_image_path, "images\\%s\\%s.jpg" % (time.strftime("/%Y/%m/%d"),time.strftime("%H%M%S"))) #create file name within folder with current current time. 
            
    with open(current_image_path,"wb") as f:
        f.write(file.content)
        filepath = os.getcwd() + "\\" + current_image_path
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 1) #idk how but this sets the wallpaper
       
while True:
    mins =60
    main("analog")
    time.sleep(60*mins)