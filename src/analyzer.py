from openai import OpenAI

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.secret import mysecret

client = OpenAI(
    api_key= mysecret #  This is the default and can be omitted
)

def CallGPT(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )
    try:
        return chat_completion.choices[0].message.content
    except:
        return ""

if __name__ == "__main__":
    user_prompt = "What are the benefits of using ChatGPT?"
    reply = CallGPT(user_prompt)
    print(f"ChatGPT: {reply}")