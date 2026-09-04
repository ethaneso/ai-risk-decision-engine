from ollama import chat


response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Explain prompt injection in one paragraph.",
        }
    ],
)

print(response.message.content)