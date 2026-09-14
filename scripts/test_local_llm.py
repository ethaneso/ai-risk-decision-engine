from ollama import chat


def main():
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


if __name__ == "__main__":
    main()
