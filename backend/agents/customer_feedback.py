from utils.openai_client import get_client


def analyze_customer_feedback(state: dict) -> dict:
    client = get_client()
    documents = state.get("documents", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a Customer Feedback Analysis Agent. Analyze the provided documents and extract:
1. Key customer pain points and frustrations
2. Satisfaction drivers and positive feedback
3. Feature requests grouped by theme
4. Recurring patterns and sentiment trends
5. Actionable customer insights

Use clear sections and bullet points in your response.""",
            },
            {
                "role": "user",
                "content": f"Analyze the following product documents for customer feedback insights:\n\n{documents[:6000]}",
            },
        ],
    )

    return {"customer_insights": response.choices[0].message.content}
