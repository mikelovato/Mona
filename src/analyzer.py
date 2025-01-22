from openai import OpenAI

client = OpenAI(
    api_key="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"  # This is the default and can be omitted
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

if __name__ == "__main__":
    user_prompt = "What are the benefits of using ChatGPT?"
    reply = CallGPT(user_prompt)
    print(f"ChatGPT: {reply}")