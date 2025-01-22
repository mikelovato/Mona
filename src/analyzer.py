from openai import OpenAI

client = OpenAI(
    api_key="-----"  # This is the default and can be omitted
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