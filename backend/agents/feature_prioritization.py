from utils.openai_client import get_client


def prioritize_features(state: dict) -> dict:
    client = get_client()
    customer_insights = state.get("customer_insights", "")
    market_insights = state.get("market_insights", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a Feature Prioritization Agent. Based on customer and market analysis:
1. Extract and list all potential product features
2. Score each feature using RICE (Reach, Impact, Confidence, Effort)
3. Categorize as Must-Have, Should-Have, or Nice-to-Have
4. Recommend a phased implementation roadmap (Q1-Q4)
5. Highlight quick wins vs strategic investments

Use tables and bullet points to structure your response.""",
            },
            {
                "role": "user",
                "content": f"""Prioritize product features based on this analysis:

Customer Insights:
{customer_insights[:2000]}

Market Insights:
{market_insights[:2000]}

Provide a prioritized feature list with RICE scores and a phased roadmap.""",
            },
        ],
    )

    return {"feature_priorities": response.choices[0].message.content}
