import os
import tempfile
import requests
import tweepy

from app.config import (
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET,
)

client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET,
)

auth = tweepy.OAuth1UserHandler(
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET,
)

api = tweepy.API(auth)


def download_image(url):

    if not url:
        return None

    try:

        r = requests.get(url, timeout=20)

        if r.status_code != 200:
            return None

        fd, path = tempfile.mkstemp(suffix=".jpg")

        with os.fdopen(fd, "wb") as f:
            f.write(r.content)

        return path

    except Exception as e:

        print("画像取得失敗:", e)

        return None


def post_to_x(text, image_urls=None):

    media_ids = []

    if image_urls:

        for url in image_urls:

            if not url:
                continue

            path = download_image(url)

            if not path:
                continue

            try:

                media = api.media_upload(path)

                media_ids.append(media.media_id)

            finally:

                if os.path.exists(path):
                    os.remove(path)

    client.create_tweet(
        text=text,
        media_ids=media_ids if media_ids else None,
    )

    print("投稿成功")
