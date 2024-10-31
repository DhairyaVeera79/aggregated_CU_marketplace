from openai import OpenAI

client = OpenAI()  

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "give me code in python to find prime numbers below 1000"}
    ]
)

print(response.choices[0].message.content)