from app.sheets import get_random_product, mark_posted
from app.prompts import SYSTEM_PROMPT
from app.openai_client import generate_post
from app.x_client import post_to_x


def main():

    product = get_random_product()

    if not product:
        print("商品がありません")
        return

    url = (
        product.get("アフィリエイトURL")
        if product.get("アフィリエイトURL")
        else product.get("作品URL")
    )

    prompt = f"""
{SYSTEM_PROMPT}

作品名:
{product.get("作品名")}

ジャンル:
{product.get("ジャンル")}

作品URL:
{url}
"""

    print("AI文章生成中...")

    post = generate_post(prompt)

    post = f"""{post}

👇作品はこちら
{url}

🔞18歳未満閲覧禁止
#PR
"""

    image_urls = [
        product.get("画像URL1"),
        product.get("画像URL2"),
        product.get("画像URL3"),
        product.get("画像URL4"),
    ]

    print("Xへ投稿中...")

    post_to_x(post, image_urls)

    mark_posted(product["_row"])

    print("投稿成功！")


if __name__ == "__main__":
    main()
