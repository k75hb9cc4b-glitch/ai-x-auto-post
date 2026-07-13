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

# API v2
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET,
)

# API v1.1（画像アップロード）
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
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        ),
        "Referer": "https://www.dmm.co.jp/",
    }

    try:

        print(f"画像取得開始: {url}")

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        fd, path = tempfile.mkstemp(suffix=".jpg")

        with os.fdopen(fd, "wb") as f:
            f.write(response.content)

        print("画像取得成功")

        return path

    except Exception as e:

        print(f"画像取得失敗: {e}")

        return None


def post_to_x(text, image_urls=None):

    media_ids = []

    if image_urls:

        for url in image_urls:

            if not url:
                continue

            path = download_image(url)

            if path is None:
                continue

            try:

                media = api.media_upload(filename=path)

                media_ids.append(media.media_id)

                print(f"画像アップロード成功 media_id={media.media_id}")

            except Exception as e:

                print(f"画像アップロード失敗: {e}")

            finally:

                if os.path.exists(path):
                    os.remove(path)

    print(f"アップロード画像数: {len(media_ids)}")

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
