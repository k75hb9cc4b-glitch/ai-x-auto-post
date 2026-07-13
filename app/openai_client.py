from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_post(prompt):

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=1.2,

        max_tokens=120,

        presence_penalty=0.8,

        frequency_penalty=0.8,

        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
    )

    post = response.choices[0].message.content.strip()

    # AIが余計なカギ括弧を付けることがあるので除去
    post = post.replace('"', "")
    post = post.replace("「", "")
    post = post.replace("」", "")

    return post
