from utils.openai_client import get_client


def analyze_market_competitor(state: dict) -> dict:
    client = get_client()
    documents = state.get("documents", "")
    customer_insights = state.get("customer_insights", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a Market & Competitor Analysis Agent. Analyze the provided documents and identify:
1. Current market trends and dynamics
2. Competitor strengths and weaknesses
3. Market gaps and unmet customer needs
4. Positioning opportunities
5. Market size and growth indicators

Use clear sections and bullet points in your response.""",
            },
            {
                "role": "user",
                "content": f"""Analyze these documents for market and competitor insights.

Customer Insights (context):
{customer_insights[:1000]}

Documents:
{documents[:5000]}

Provide market trends, competitive analysis, and positioning opportunities.""",
            },
        ],
    )

    return {"market_insights": response.choices[0].message.content}
