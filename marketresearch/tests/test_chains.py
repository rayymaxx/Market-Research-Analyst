"""
Test all LCEL chains
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from marketresearch.src.marketresearch.chains import ChainFactory

def test_chains():
    """Test all chains"""
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1
    )
    
    # Create chain factory
    factory = ChainFactory(llm)
    
    # Test SWOT Analysis
    print("🧪 Testing SWOT Analysis Chain...")
    swot_chain = factory.get_chain("swot_analysis")
    swot_result = swot_chain.analyze(
        research_topic="Electric Vehicle Market",
        current_date="2024-01-15",
        competitor_data={"Tesla": "Market leader"},
        market_data={"growth": "28% CAGR"}
    )
    print(f"✅ SWOT Analysis Complete: {len(swot_result.strengths)} strengths identified")
    
    # Test Industry Analysis
    print("🧪 Testing Industry Analysis Chain...")
    industry_chain = factory.get_chain("industry_analysis")
    industry_result = industry_chain.analyze_industry(
        research_topic="EV Market",
        industry_data={"size": "$15B", "growth": "28% CAGR"}
    )
    print(f"✅ Industry Analysis Complete: Market size {industry_result.market_size}")
    
    # Test Company Research
    print("🧪 Testing Company Research Chain...")
    company_chain = factory.get_chain("company_research")
    company_result = company_chain.research_company(
        research_topic="EV Market",
        company_name="Tesla"
    )
    print(f"✅ Company Research Complete: {company_result.company_name} analyzed")
    
    # Test Recommendations
    print("🧪 Testing Recommendations Chain...")
    rec_chain = factory.get_chain("strategic_recommendations")
    rec_result = rec_chain.generate_recommendations(
        research_topic="EV Market",
        business_context="Growing competition in electric vehicles",
        analysis_insights={"market_growth": "28%", "competitive_intensity": "High"}
    )
    print(f"✅ Recommendations Complete: {len(rec_result.immediate_actions)} immediate actions")
    
    # Test Executive Summary
    print("🧪 Testing Executive Summary Chain...")
    summary_chain = factory.get_chain("executive_summary")
    summary_result = summary_chain.generate_summary(
        research_topic="EV Market",
        analysis_results={"market_size": "$15B", "growth": "28%"},
        target_audience="executives"
    )
    print(f"✅ Executive Summary Complete: {len(summary_result.key_insights)} insights")
    
    print("🎉 All chains working perfectly!")

if __name__ == "__main__":
    test_chains()