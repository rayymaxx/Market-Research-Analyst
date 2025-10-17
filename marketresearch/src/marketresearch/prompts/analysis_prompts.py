"""
Advanced prompt templates for analysis chains with few-shot, chain-of-thought, and role-based prompting
"""
from .base import BasePromptManager, FewShotExample, ChainOfThoughtMixin, RoleBasedMixin
from typing import Dict, List
import json

class AnalysisPrompts(BasePromptManager, ChainOfThoughtMixin, RoleBasedMixin):
    """Advanced prompt manager for analysis-related chains"""
    
    def _load_prompts(self) -> Dict[str, str]:
        base_prompts = {
            "swot_analysis": self.SWOT_ANALYSIS,
            "competitive_benchmarking": self.COMPETITIVE_BENCHMARKING,
            "market_trends": self.MARKET_TRENDS_ANALYSIS,
        }
        
        # Enhance prompts with advanced techniques
        enhanced_prompts = {}
        for name, prompt in base_prompts.items():
            # Add chain of thought
            enhanced_prompt = self.add_chain_of_thought_instructions(prompt)
            # Add role context
            if name == "swot_analysis":
                enhanced_prompt = self.add_role_context(enhanced_prompt, 
                    "Senior Strategic Analyst", 
                    ["SWOT Analysis", "Business Strategy", "Competitive Intelligence"]
                )
            elif name == "competitive_benchmarking":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Competitive Intelligence Specialist",
                    ["Quantitative Analysis", "Market Positioning", "Strategic Benchmarking"]
                )
            elif name == "market_trends":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Market Trends Analyst",
                    ["Pattern Recognition", "Forecasting", "Industry Analysis"]
                )
            
            enhanced_prompts[name] = enhanced_prompt
        
        return enhanced_prompts
    
    def _load_few_shot_examples(self) -> Dict[str, List[FewShotExample]]:
        return {
            "swot_analysis": self._get_swot_examples(),
            "competitive_benchmarking": self._get_benchmarking_examples(),
            "market_trends": self._get_trends_examples(),
        }
    
    def _get_swot_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "research_topic": "Electric Vehicle Charging Network",
                    "competitor_data": {
                        "competitors": ["ChargePoint", "EVgo", "Tesla Supercharger"],
                        "market_share": {"ChargePoint": "35%", "EVgo": "25%", "Tesla": "40%"}
                    },
                    "market_data": {
                        "growth_rate": "28% CAGR",
                        "market_size": "$15.2B (2023)",
                        "key_trends": ["Government incentives", "Fleet electrification"]
                    }
                },
                output={
                    "strengths": [
                        {
                            "description": "Largest charging network with 35% market share",
                            "evidence": "Market share data shows 35% penetration across North America",
                            "impact": "HIGH",
                            "confidence": 0.95
                        }
                    ],
                    "weaknesses": [
                        {
                            "description": "Limited fast-charging infrastructure compared to Tesla",
                            "evidence": "Only 15% of stations are DC fast chargers vs Tesla's 40%",
                            "impact": "MEDIUM", 
                            "confidence": 0.85
                        }
                    ],
                    "opportunities": [
                        {
                            "description": "Expand into fleet charging for commercial vehicles",
                            "evidence": "Fleet electrification trend growing at 45% annually",
                            "impact": "HIGH",
                            "confidence": 0.80
                        }
                    ],
                    "threats": [
                        {
                            "description": "Increasing competition from automotive OEMs building proprietary networks",
                            "evidence": "3 major automakers announced proprietary charging networks in 2023",
                            "impact": "MEDIUM",
                            "confidence": 0.75
                        }
                    ]
                },
                explanation="Analyzed market share data to identify strength in network size. Compared charging technology mix to identify weakness in fast-charging. Identified fleet electrification trend as opportunity. Noted competitive threat from automotive OEM vertical integration."
            )
        ]
    
    def _get_benchmarking_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "research_topic": "Cloud Storage Providers",
                    "competitors": [
                        {"name": "Dropbox", "features": ["File sync", "Collaboration"], "price": "$12/user"},
                        {"name": "Google Drive", "features": ["Integration", "Storage"], "price": "$6/user"}
                    ]
                },
                output={
                    "competitors": [
                        {
                            "name": "Dropbox",
                            "product_score": 8.5,
                            "pricing_score": 6.0,
                            "market_presence_score": 9.0,
                            "customer_focus_score": 8.0,
                            "overall_score": 8.1,
                            "strengths": ["Superior collaboration features", "Strong brand recognition"],
                            "weaknesses": ["Higher pricing", "Limited storage tiers"]
                        }
                    ],
                    "key_findings": [
                        "Google Drive leads on price-value proposition",
                        "Dropbox maintains advantage in collaboration features"
                    ]
                },
                explanation="Applied weighted scoring framework: 40% product features, 25% pricing, 20% market presence, 15% customer focus. Calculated weighted averages. Compared relative strengths and weaknesses across dimensions."
            )
        ]

    # ===== CORE PROMPT TEMPLATES =====
    
    SWOT_ANALYSIS = """CRITICAL BUSINESS ANALYSIS: COMPREHENSIVE SWOT ANALYSIS

ANALYSIS CONTEXT:
Research Topic: {research_topic}
Analysis Date: {current_date}
Data Currency: All data should reflect current market conditions as of {current_date}

DATA INPUTS:
• Competitor Intelligence: {competitor_data}
• Market Trends & Metrics: {market_data}  
• Company/Product Context: {company_data}
• Additional Research: {context_data}

ANALYTICAL FRAMEWORK REQUIREMENTS:

1. EVIDENCE-BASED ASSESSMENT:
   - Every SWOT item MUST cite specific data points
   - Use quantitative metrics where available (market share %, growth rates, etc.)
   - Include source references for all evidence

2. IMPACT ASSESSMENT SCALE:
   HIGH: Strategic significance, major business impact, affects core operations
   MEDIUM: Operational significance, moderate business impact  
   LOW: Tactical significance, minor business impact

3. CONFIDENCE SCORING:
   0.9-1.0: High confidence (multiple verified sources)
   0.7-0.8: Medium confidence (reliable single source)
   0.5-0.6: Low confidence (estimates/industry averages)

4. STRATEGIC PRIORITIZATION:
   - Focus on factors with HIGH impact and HIGH confidence
   - Balance coverage across all four SWOT categories
   - Prioritize actionable insights over comprehensive lists

VALIDATION CHECKS:
✓ Each item has specific evidence, not generic statements
✓ Impact and confidence scores are justified by data
✓ No contradictory items within the same category  
✓ Strategic implications are clearly articulated

{format_instructions}

FINAL OUTPUT REQUIREMENTS:
Provide a structured SWOT analysis with evidence-based items, impact assessments, and confidence scores."""

    COMPETITIVE_BENCHMARKING = """QUANTITATIVE COMPETITIVE BENCHMARKING ANALYSIS

BENCHMARKING CONTEXT:
Market Segment: {research_topic}
Analysis Date: {current_date}
Competitor Set: {competitors}

SCORING METHODOLOGY (Weighted Framework):

DIMENSION 1: PRODUCT FEATURES (40% Weight)
• Technology Stack & Innovation
• Feature Completeness & Depth  
• User Experience & Design
• Integration Capabilities
• Customization & Flexibility

DIMENSION 2: PRICING STRATEGY (25% Weight)  
• Price Points & Tiering
• Value Proposition & ROI
• Packaging & Bundling
• Flexibility & Contract Terms

DIMENSION 3: MARKET PRESENCE (20% Weight)
• Brand Recognition & Reputation
• Market Share & Leadership
• Geographic Coverage
• Partnership Ecosystem

DIMENSION 4: CUSTOMER FOCUS (15% Weight)
• Customer Support Quality
• Satisfaction & Retention Rates
• Community Engagement
• Feedback Implementation

SCORING SCALE (0-10):
10: Market leader, best-in-class
8-9: Strong performer, competitive advantage  
6-7: Average performer, parity with market
4-5: Below average, competitive disadvantage
0-3: Significant gaps, non-competitive

CALCULATION PROCESS:
1. Score each dimension independently (0-10)
2. Apply dimension weights
3. Calculate weighted overall score
4. Provide specific rationale for each score

ADDITIONAL CONTEXT:
{context_data}

VALIDATION REQUIREMENTS:
✓ Consistent scoring methodology applied to all competitors
✓ Specific examples provided for each score rationale
✓ Weighted calculations are mathematically correct
✓ Key competitive gaps and advantages are highlighted

{format_instructions}

OUTPUT REQUIREMENTS:
Complete competitive benchmarking with scored dimensions, weighted overall scores, and strategic insights."""

    MARKET_TRENDS_ANALYSIS = """COMPREHENSIVE MARKET TRENDS ANALYSIS & FORECASTING

ANALYSIS SCOPE:
Industry: {research_topic}
Current Date: {current_date}
Forecast Horizon: Short-term (1-2 years), Medium-term (3-5 years)

TREND ANALYSIS FRAMEWORK:

CATEGORY 1: TECHNOLOGY & INNOVATION TRENDS
• Emerging Technologies & Adoption Curves
• R&D Investment Patterns
• Disruption Potential & Timing
• Standards & Interoperability

CATEGORY 2: CONSUMER & BEHAVIORAL TRENDS  
• Usage Patterns & Engagement Metrics
• Expectation Evolution & Demands
• Adoption Barriers & Drivers
• Demographic Shifts

CATEGORY 3: REGULATORY & COMPLIANCE TRENDS
• Current Regulatory Landscape
• Proposed Legislation & Timelines
• Compliance Requirements & Costs
• International Standards Alignment

CATEGORY 4: ECONOMIC & MARKET DYNAMICS
• Market Sizing & Growth Projections
• Investment & Funding Patterns
• Competitive Landscape Evolution
• Macroeconomic Influences

ANALYSIS DATA INPUTS:
{market_data}

TREND ASSESSMENT CRITERIA:

IMPACT LEVEL:
HIGH: Transformative, creates new markets or destroys existing ones
MEDIUM: Significant, changes competitive dynamics
LOW: Incremental, affects operational efficiency

CONFIDENCE LEVEL:
HIGH (0.8-1.0): Multiple data sources, clear evidence patterns
MEDIUM (0.6-0.8): Strong indicators, some uncertainty
LOW (0.4-0.6): Early signals, requires validation

TIMING ESTIMATION:
IMMINENT (0-12 months): Clear signals, early adoption
NEAR-TERM (1-3 years): Emerging patterns, pilot deployments
LONG-TERM (3-5 years): Early research, concept development

VALIDATION CHECKS:
✓ Each trend has specific evidence and data points
✓ Impact, confidence, and timing assessments are justified
✓ Interdependencies between trends are identified
✓ Contradictory signals are acknowledged and resolved

{format_instructions}

OUTPUT REQUIREMENTS:
Comprehensive market trends analysis with categorized trends, impact assessments, and strategic implications."""