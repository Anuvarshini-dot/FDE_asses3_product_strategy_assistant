from utils.openai_client import get_client


def generate_executive_report(state: dict) -> dict:
    client = get_client()
    customer_insights = state.get("customer_insights", "")
    market_insights = state.get("market_insights", "")
    feature_priorities = state.get("feature_priorities", "")
    swot_analysis = state.get("swot_analysis", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an Executive Report Agent. Synthesize all analysis into a C-suite ready summary:

1. Situation Overview (2-3 sentences)
2. Top 3 Strategic Opportunities
3. Critical Risks to Address
4. Recommended Strategic Priorities (ranked)
5. Immediate Next Steps (30/60/90 day plan)
6. Expected Business Impact

Write concisely for senior leadership. Use data-driven language and quantify impact where possible.""",
            },
            {
                "role": "user",
                "content": f"""Create an executive strategy report from all analyses:

Customer Insights:
{customer_insights[:1500]}

Market & Competitor Analysis:
{market_insights[:1500]}

Feature Priorities:
{feature_priorities[:1500]}

SWOT Analysis:
{swot_analysis[:1500]}

Generate a comprehensive executive summary with ranked priorities and a 30/60/90 day action plan.""",
            },
        ],
    )

    return {"executive_summary": response.choices[0].message.content}
