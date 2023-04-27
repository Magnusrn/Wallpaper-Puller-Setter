import praw
import requests
import os
import time
import subprocess
import Quartz

import hashlib
import glob
from secrets import CLIENT_ID, CLIENT_SECRET, USER_AGENT


def main(subreddit):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT)

    for submission in reddit.subreddit(subreddit).top(time_filter="day"):
        if submission.url.endswith(".jpg"):
            file = requests.get(submission.url)
            remote_url = submission.url
            break
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

    #
    # def images_identical():  # compares local image to remote
    #     if md5Checksum(image_path, None) == md5Checksum(None, remote_url):
    #         print("images identical")
    #         return True
    #     return False
    #
    # if len(glob.glob(os.path.dirname(__file__) + "/*.jpg")) != 0:
    #     if not images_identical():
    #         print("Local image differs to remote, updating...")
    #     else:
    #         print("Local image is the same as remote.")
    #         return
    # else:
    #     print()()("no file in folder")

    def set_desktop_background():
        list_of_files = glob.glob(os.path.dirname(__file__) + "/images/*.jpg")
        latest_image = max(list_of_files, key=os.path.getctime)
        # what the fuck is this apostrophe nightmare
        script = f"""osascript -e 'tell application "Finder" to set desktop picture to POSIX file "{latest_image}"'"""
        subprocess.Popen(script, shell=True)

    image_hash = md5Checksum(None, remote_url)
    image_path = os.path.join(os.path.dirname(__file__), "images", f"{image_hash}.jpg")
    with open(image_path, "wb") as f:
        f.write(file.content)
        try:
            print("setting desktop wallpaper")
            set_desktop_background()
        except Exception as e:
            print(e)


subreddit = "analog"  # default subreddit if no cl args given


def isScreenLocked():
    return 'CGSSessionScreenIsLocked' in Quartz.CGSessionCopyCurrentDictionary().keys()


# if len(sys.argv) == 2:
#     subreddit = sys.argv[-1]
# elif len(sys.argv)>2:
#     print("Incorrect syntax, Program accepts 0 or 1 arguments for subreddit.")
#     exit()

while True:
    # for some reason if you try to set wallpaper while screen is locked
    # it bugs out and any subsequent settings even if locked in are prevented
    while isScreenLocked():
        print("screen is locked")
        time.sleep(10)
    try:
        main(subreddit.lower())
    except Exception as e:
        print(e)
    time.sleep(60)  # seconds
