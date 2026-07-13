import random

from app.sheets import get_random_product, mark_posted
from app.prompts import SYSTEM_PROMPT
from app.openai_client import generate_post
from app.x_client import post_to_x


def main():

    print("=" * 50)
    print("🤖 AI X Auto Poster")
    print("=" * 50)

    product = get_random_product()

    if not product:
        print("投稿する作品がありません")
        return

    print(f"作品名 : {product.get('作品名')}")
    print(f"ジャンル : {product.get('ジャンル')}")
    print(f"サークル : {product.get('サークル')}")

    url = (
        product.get("アフィリエイトURL")
        or product.get("作品URL")
    )

    prompt = f"""
{SYSTEM_PROMPT}

作品名:
{product.get("作品名")}

ジャンル:
{product.get("ジャンル")}

サークル:
{product.get("サークル")}

タグ:
{product.get("タグ")}

あらすじ:
{product.get("あらすじ")}

作品URL:
{url}
"""

    print("🧠 AI文章生成中...")

    post = generate_post(prompt)

    call_to_action = random.choice([
        "👇作品はこちら",
        "👇サンプルはこちら",
        "👇気になる人はこちら",
        "👇詳細はこちら",
        "👇チェックしてみて",
    ])

    warning = random.choice([
        "🔞18歳未満閲覧禁止",
        "※18歳未満閲覧禁止",
        "18歳未満は閲覧できません",
    ])

    post = f"""{post}

{call_to_action}
{url}

{warning}
#PR
"""

    image_urls = [
        product.get("画像URL1"),
        product.get("画像URL2"),
        product.get("画像URL3"),
        product.get("画像URL4"),
    ]

    print(f"📷 画像枚数 : {len([x for x in image_urls if x])}")

    print("🚀 Xへ投稿中...")

    tweet_id = post_to_x(
        post,
        image_urls,
    )

    print("📝 スプレッドシート更新中...")

    mark_posted(
        product["_row"],
        tweet_id,
    )

    print("=" * 50)
    print("✅ 投稿完了")
    print(f"TweetID : {tweet_id}")
    print("=" * 50)


if __name__ == "__main__":
    main()
