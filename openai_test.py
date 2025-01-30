import os

from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="o1-mini",  # Use "gpt-3.5-turbo" if you want a cheaper model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Test the chatbot
user_input = "Hello, who won the last Champions League in the 2023-2024 season?"
reply = chat_with_openai(user_input)
print("OpenAI:", reply)