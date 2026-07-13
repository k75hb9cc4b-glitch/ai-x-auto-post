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

# X API v2（ツイート投稿）
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET,
)

# X API v1.1（画像アップロード）
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

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        ),
        "Referer": "https://www.dmm.co.jp/",
    }

    try:

        print(f"画像取得: {url}")

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        fd, path = tempfile.mkstemp(suffix=".jpg")

        with os.fdopen(fd, "wb") as f:
            f.write(response.content)

        return path

    except Exception as e:

        print("画像取得失敗:", e)

        return None


def post_to_x(text, image_urls=None):

    media_ids = []

    if image_urls:

        for url in image_urls:

            path = download_image(url)

            if not path:
                continue

            try:

                media = api.media_upload(filename=path)

                media_ids.append(media.media_id)

                print("画像アップロード成功")

            except Exception as e:

                print("画像アップロード失敗:", e)

            finally:

                if os.path.exists(path):
                    os.remove(path)

    try:

        if media_ids:

            client.create_tweet(
                text=text,
                media_ids=media_ids,
            )

        else:

            client.create_tweet(
                text=text,
            )

        print("投稿成功")

    except Exception as e:

        print("投稿失敗:", e)

        raise
