from utils.openai_client import get_client


def run_chat(message: str, history: list, context: str) -> str:
    client = get_client()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Product Strategy Assistant. Help product managers make "
                "data-driven decisions based on their uploaded documents and analysis results. "
                "Be specific and actionable. Refer back to earlier parts of the conversation "
                "when relevant — you have full memory of this session.\n\n"
                f"Context from documents and analysis:\n{context}"
            ),
        }
    ]

    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content
