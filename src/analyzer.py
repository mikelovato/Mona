from openai import OpenAI

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.constants import mysecret

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
    if 'choices' in chat_completion:
        return chat_completion
    else:
        return {}  

if __name__ == "__main__":
    user_prompt = "What are the benefits of using ChatGPT?"
    reply = CallGPT(user_prompt)
    print(f"ChatGPT: {reply}")