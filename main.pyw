import praw
import requests
import ctypes
import os
import time
import hashlib
import sys
import glob
from secrets import CLIENT_ID,CLIENT_SECRET,USER_AGENT

#lots of code needed removed for .pyw as it doesn't work with print statements(not sure why this is...)

def main(subreddit):
    reddit = praw.Reddit(
    client_id= CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT)
    
    image_path = os.path.dirname(__file__) + "\\wallpaper.jpg"
        
    for submission in reddit.subreddit(subreddit).top("day"):
        if submission.url.endswith(".jpg"):
            file = requests.get(submission.url)
            remote_url = submission.url
            break
    try: 
        file
    except NameError:
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
        if md5Checksum(image_path,None)==md5Checksum(None,remote_url): 
            return True
        return False
    
    if (len(glob.glob(os.path.dirname(__file__) + "\*.jpg"))!=0):
        if images_identical():
            return
        
    with open(image_path,"wb") as f:
        f.write(file.content)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 1) #idk how but this sets the wallpaper, glob just pulls any image from /images folder as the name would differ depending on time
  
subreddit = "analog" #default subreddit if no cl args given

if len(sys.argv) == 2:
    subreddit = sys.argv[-1]
elif len(sys.argv)>2:
    exit()
    
while True:
    main(subreddit.lower())
    time.sleep(3600) #sleep 1 hour 
