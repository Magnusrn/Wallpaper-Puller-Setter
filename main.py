import praw
import requests
import os
import time
import hashlib
import glob
from secrets import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from appscript import app, mactypes


def main(subreddit):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT)
    image_path = os.path.join(os.path.dirname(__file__), "wallpaper.jpg")

    for submission in reddit.subreddit(subreddit).top("day"):
        if submission.url.endswith(".jpg"):
            print("file found")
            file = requests.get(submission.url)
            remote_url = submission.url
            break
    print("hi")
    try:
        file
    except NameError:
        print("No .jpg images in the r/%s subreddit" % subreddit)
        quit()

    def md5Checksum(filePath, url):
        m = hashlib.md5()
        if url is None:
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

    def images_identical():  # compares local image to remote
        if md5Checksum(image_path, None) == md5Checksum(None, remote_url):
            print("images identical")
            return True
        return False

    if len(glob.glob(os.path.dirname(__file__) + "/*.jpg")) != 0:
        if not images_identical():
            print("Local image differs to remote, updating...")
        else:
            print("Local image is the same as remote.")
            return
    else:
        print("no file in folder")

    with open(image_path, "wb") as f:
        f.write(file.content)
        try:
            app('Finder').desktop_picture.set(mactypes.File(image_path))
        except Exception as e:
            print(e)


subreddit = "analog"  # default subreddit if no cl args given

# if len(sys.argv) == 2:
#     subreddit = sys.argv[-1]
# elif len(sys.argv)>2:
#     print("Incorrect syntax, Program accepts 0 or 1 arguments for subreddit.")
#     exit()

while True:
    try:
        main(subreddit.lower())
    except Exception as e:
        print(e)
    time.sleep(900)  # seconds
