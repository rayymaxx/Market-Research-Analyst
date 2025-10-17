"""
Advanced research prompts with comprehensive data collection frameworks
"""
from .base import BasePromptManager, FewShotExample, ChainOfThoughtMixin, RoleBasedMixin
from typing import Dict, List
import json

class ResearchPrompts(BasePromptManager, ChainOfThoughtMixin, RoleBasedMixin):
    """Advanced prompt manager for research-related chains"""
    
    def _load_prompts(self) -> Dict[str, str]:
        base_prompts = {
            "data_collection": self.DATA_COLLECTION,
            "company_research": self.COMPANY_RESEARCH,
            "industry_analysis": self.INDUSTRY_ANALYSIS,
        }
        
        # Enhance with advanced techniques
        enhanced_prompts = {}
        for name, prompt in base_prompts.items():
            enhanced_prompt = self.add_chain_of_thought_instructions(prompt)
            
            if name == "data_collection":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Market Intelligence Specialist",
                    ["Multi-source Data Collection", "Data Validation", "Competitive Intelligence"]
                )
            elif name == "company_research":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Company Intelligence Analyst", 
                    ["Business Profiling", "Financial Analysis", "Strategic Assessment"]
                )
            elif name == "industry_analysis":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Industry Research Specialist",
                    ["Market Sizing", "Value Chain Analysis", "Competitive Dynamics"]
                )
            
            enhanced_prompts[name] = enhanced_prompt
        
        return enhanced_prompts
    
    def _load_few_shot_examples(self) -> Dict[str, List[FewShotExample]]:
        return {
            "data_collection": self._get_data_collection_examples(),
            "company_research": self._get_company_research_examples(),
        }

    def _get_data_collection_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "research_topic": "AI-Powered Customer Service Platforms",
                    "primary_sources": ["Company websites", "Product documentation"],
                    "secondary_sources": ["Industry reports", "News articles"],
                    "data_requirements": ["Pricing", "Features", "Market share"]
                },
                output={
                    "competitor_data": {
                        "Intercom": {
                            "pricing": "$74/month per seat",
                            "key_features": ["AI chatbots", "Help center", "CRM integration"],
                            "market_position": "Market leader in conversational support"
                        }
                    },
                    "market_metrics": {
                        "market_size": "$12.5B (2023)",
                        "growth_rate": "24% CAGR",
                        "key_segments": ["SMB", "Enterprise", "E-commerce"]
                    }
                },
                explanation="Systematically gathered data from multiple sources: extracted pricing from company websites, features from product docs, market size from industry reports. Cross-verified information for accuracy."
            )
        ]

    # ===== CORE RESEARCH PROMPTS =====
    
    DATA_COLLECTION = """COMPREHENSIVE MARKET DATA COLLECTION FRAMEWORK

RESEARCH MISSION:
Topic: {research_topic}
Collection Date: {current_date}
Data Currency Requirement: All data must reflect current market conditions

DATA COLLECTION PRIORITIES (Ranked by Importance):

PRIORITY 1: COMPETITOR INTELLIGENCE
• Company Profiles: Size, founding year, leadership team
• Product Portfolio: Core offerings, features, technology stack
• Pricing Strategy: Price points, tiers, packaging, discounts
• Market Positioning: Target segments, value proposition, differentiation

PRIORITY 2: MARKET METRICS & ECONOMICS
• Market Sizing: Total addressable market, serviceable market
• Growth Rates: Historical growth, projected CAGR
• Segmentation: Customer segments, geographic coverage
• Key Performance Indicators: Industry-specific metrics

PRIORITY 3: CONSUMER & USER INSIGHTS
• Demographics: Target audience characteristics
• Behavior Patterns: Usage frequency, feature adoption
• Pain Points: Customer challenges, unmet needs
• Satisfaction Metrics: NPS, CSAT, retention rates

PRIORITY 4: INDUSTRY TRENDS & INNOVATION
• Technology Adoption: Emerging tech, innovation cycles
• Regulatory Landscape: Compliance requirements, policy changes
• Competitive Dynamics: Market concentration, entry barriers
• Investment Patterns: Funding rounds, M&A activity

DATA SOURCES STRATEGY:

PRIMARY SOURCES (Direct Observation):
{primary_sources}

SECONDARY SOURCES (Industry Analysis):
{secondary_sources}

TERTIARY SOURCES (Market Intelligence):
{tertiary_sources}

DATA VALIDATION PROTOCOL:
1. Cross-Verification: Confirm key facts from multiple independent sources
2. Timestamping: Record collection date for all data points
3. Source Attribution: Document provenance for traceability
4. Confidence Assessment: Rate data reliability (High/Medium/Low)

ETHICAL COLLECTION GUIDELINES:
✓ Respect copyright and terms of service
✓ Attribute all sources appropriately
✓ Avoid proprietary or confidential information
✓ Maintain data privacy and security

{format_instructions}

OUTPUT REQUIREMENTS:
Structured data collection with validated information, source attribution, and confidence assessments."""

    COMPANY_RESEARCH = """DEEP DIVE COMPANY INTELLIGENCE RESEARCH

RESEARCH SUBJECT:
Company: {company_name}
Industry Context: {industry_context}
Research Date: {current_date}

COMPREHENSIVE RESEARCH FRAMEWORK:

SECTION 1: COMPANY FUNDAMENTALS
• Corporate History & Evolution
• Mission, Vision & Values
• Leadership Team & Governance
• Organizational Structure & Culture

SECTION 2: PRODUCT & TECHNOLOGY
• Core Product/Service Portfolio
• Technology Stack & Architecture
• Feature Set & Capabilities
• Innovation Pipeline & Roadmap

SECTION 3: MARKET POSITION & STRATEGY
• Market Share & Competitive Positioning
• Target Customer Segments
• Geographic Footprint & Expansion
• Brand Equity & Perception

SECTION 4: FINANCIAL HEALTH
• Revenue Streams & Business Model
• Profitability & Margins
• Funding History & Valuation
• Financial Stability Indicators

SECTION 5: OPERATIONAL METRICS
• Customer Base & Growth Trajectory
• Operational Efficiency Measures
• Partnership & Alliance Network
• Risk Factors & Challenges

SECTION 6: STRATEGIC DIRECTION
• Growth Strategy & Initiatives
• M&A Activity & Partnerships
• Innovation Focus & R&D Investment
• Long-term Vision & Goals

DATA SOURCES UTILIZATION:
{data_sources}

RESEARCH METHODOLOGY:

1. FACT vs. PERCEPTION:
   - Differentiate between verified facts and market perceptions
   - Source all claims with appropriate evidence
   - Acknowledge information gaps and uncertainties

2. COMPETITIVE CONTEXT:
   - Position company relative to key competitors
   - Identify unique differentiators and advantages
   - Assess vulnerabilities and competitive gaps

3. STRATEGIC ASSESSMENT:
   - Evaluate strategic coherence and execution capability
   - Assess alignment with market trends and opportunities
   - Identify potential strategic risks and challenges

VALIDATION CHECKPOINTS:
✓ All financial data is sourced and dated
✓ Competitive claims are substantiated with evidence
✓ Strategic assessments are balanced and objective
✓ Information gaps are clearly identified

{format_instructions}

OUTPUT REQUIREMENTS:
Comprehensive company intelligence profile with verified facts, strategic assessment, and identified information gaps."""

    INDUSTRY_ANALYSIS = """COMPREHENSIVE INDUSTRY ANALYSIS FRAMEWORK

ANALYSIS SCOPE:
Industry: {industry_name}
Analysis Date: {current_date}
Geographic Focus: Global with regional specifics

INDUSTRY ANALYSIS DIMENSIONS:

DIMENSION 1: MARKET STRUCTURE & ECONOMICS
• Market Size & Growth Trajectory
• Market Segmentation & Characteristics
• Key Players & Market Concentration
• Profitability & Value Creation

DIMENSION 2: VALUE CHAIN ANALYSIS
• Key Activities & Processes
• Distribution Channels & Logistics
• Supplier & Partner Ecosystem
• Cost Structure & Profit Pools

DIMENSION 3: COMPETITIVE DYNAMICS
• Competitive Landscape & Rivalry
• Entry & Exit Barriers
• Substitution Threats
• Buyer & Supplier Power

DIMENSION 4: REGULATORY ENVIRONMENT
• Regulatory Framework & Compliance
• Policy Trends & Developments
• Standards & Certifications
• International Trade Considerations

DIMENSION 5: TECHNOLOGY LANDSCAPE
• Technology Adoption & Innovation
• R&D Investment & Focus Areas
• Disruption Potential & Timing
• Intellectual Property Landscape

DIMENSION 6: MACRO-ENVIRONMENTAL FACTORS
• Economic Conditions & Cycles
• Social & Demographic Trends
• Environmental & Sustainability Factors
• Political & Geopolitical Influences

ANALYSIS DATA INPUTS:
{industry_data}

ANALYTICAL FRAMEWORKS TO APPLY:

1. PORTER'S FIVE FORCES:
   - Assess competitive intensity and attractiveness
   - Evaluate threat of new entrants and substitutes
   - Analyze buyer and supplier power dynamics

2. PESTLE ANALYSIS:
   - Political, Economic, Social, Technological, Legal, Environmental factors
   - Identify macro-environmental opportunities and threats
   - Assess impact on industry structure and dynamics

3. INDUSTRY LIFE CYCLE:
   - Determine industry maturity stage
   - Assess growth potential and competitive evolution
   - Identify stage-appropriate strategies

QUANTITATIVE ASSESSMENT:
• Market Sizing: Provide TAM, SAM, SOM estimates with methodology
• Growth Projections: Historical and forecast growth rates
• Financial Metrics: Industry-average profitability, margins
• Performance Indicators: Key success factors and metrics

VALIDATION REQUIREMENTS:
✓ Market size estimates include methodology and assumptions
✓ Competitive analysis includes specific player examples
✓ Trend assessments are supported by data evidence
✓ Strategic implications are actionable and specific

{format_instructions}

OUTPUT REQUIREMENTS:
Comprehensive industry analysis with quantitative assessments, strategic frameworks, and actionable insights."""