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

作品URL:
{url}
"""

    # OpenAIには送る（動作確認のため）
    post = generate_post(prompt)

    print(post)

    # ★ここをURLだけ投稿するように変更
    post_to_x(url)

    mark_posted(product["_row"])

    print("投稿成功")


if __name__ == "__main__":
    main()