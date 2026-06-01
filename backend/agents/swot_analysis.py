from utils.openai_client import get_client


def perform_swot_analysis(state: dict) -> dict:
    client = get_client()
    customer_insights = state.get("customer_insights", "")
    market_insights = state.get("market_insights", "")
    feature_priorities = state.get("feature_priorities", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a SWOT Analysis Agent. Synthesize all prior analysis into a SWOT matrix:

STRENGTHS: Internal positives from customer satisfaction and product capabilities
WEAKNESSES: Internal gaps from pain points and competitive shortfalls
OPPORTUNITIES: External market trends and unmet needs to capitalize on
THREATS: External risks from competitors and market changes

For each quadrant provide 3-5 specific, evidence-based points and strategic implications.""",
            },
            {
                "role": "user",
                "content": f"""Perform a SWOT analysis based on:

Customer Insights:
{customer_insights[:1500]}

Market Insights:
{market_insights[:1500]}

Feature Priorities:
{feature_priorities[:1000]}

Create a detailed SWOT matrix with strategic implications for each quadrant.""",
            },
        ],
    )

    return {"swot_analysis": response.choices[0].message.content}
