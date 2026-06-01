from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.customer_feedback import analyze_customer_feedback
from agents.market_competitor import analyze_market_competitor
from agents.feature_prioritization import prioritize_features
from agents.swot_analysis import perform_swot_analysis
from agents.executive_report import generate_executive_report


class AnalysisState(TypedDict):
    documents: str
    customer_insights: str
    market_insights: str
    feature_priorities: str
    swot_analysis: str
    executive_summary: str


def build_workflow():
    graph = StateGraph(AnalysisState)

    graph.add_node("customer_feedback", analyze_customer_feedback)
    graph.add_node("market_competitor", analyze_market_competitor)
    graph.add_node("feature_prioritization", prioritize_features)
    graph.add_node("swot_analysis", perform_swot_analysis)
    graph.add_node("executive_report", generate_executive_report)

    graph.set_entry_point("customer_feedback")
    graph.add_edge("customer_feedback", "market_competitor")
    graph.add_edge("market_competitor", "feature_prioritization")
    graph.add_edge("feature_prioritization", "swot_analysis")
    graph.add_edge("swot_analysis", "executive_report")
    graph.add_edge("executive_report", END)

    return graph.compile()
