"""
Advanced prompt templates for reporting chains with executive-level precision
"""
from .base import BasePromptManager, FewShotExample, ChainOfThoughtMixin, RoleBasedMixin
from typing import Dict, List
import json

class ReportingPrompts(BasePromptManager, ChainOfThoughtMixin, RoleBasedMixin):
    """Advanced prompt manager for reporting-related chains"""
    
    def _load_prompts(self) -> Dict[str, str]:
        base_prompts = {
            "executive_summary": self.EXECUTIVE_SUMMARY,
            "research_report": self.RESEARCH_REPORT,
            "strategic_recommendations": self.STRATEGIC_RECOMMENDATIONS,
            "presentation_deck": self.PRESENTATION_DECK,
        }
        
        # Enhance with advanced techniques
        enhanced_prompts = {}
        for name, prompt in base_prompts.items():
            enhanced_prompt = self.add_chain_of_thought_instructions(prompt)
            
            if name == "executive_summary":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Chief Strategy Officer",
                    ["Executive Communication", "Strategic Synthesis", "Decision Support"]
                )
            elif name == "research_report":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Senior Research Director",
                    ["Comprehensive Analysis", "Business Writing", "Stakeholder Management"]
                )
            elif name == "strategic_recommendations":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Management Consultant",
                    ["Strategic Planning", "Implementation Roadmapping", "ROI Analysis"]
                )
            elif name == "presentation_deck":
                enhanced_prompt = self.add_role_context(enhanced_prompt,
                    "Presentation Specialist",
                    ["Visual Storytelling", "Executive Communication", "Investor Relations"]
                )
            
            enhanced_prompts[name] = enhanced_prompt
        
        return enhanced_prompts
    
    def _load_few_shot_examples(self) -> Dict[str, List[FewShotExample]]:
        return {
            "executive_summary": self._get_executive_summary_examples(),
            "strategic_recommendations": self._get_recommendations_examples(),
            "research_report": self._get_research_report_examples(),
        }
    
    def _get_executive_summary_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "research_topic": "AI-Powered Customer Service Market",
                    "target_audience": "C-level executives",
                    "analysis_results": {
                        "market_size": "$15.2B growing at 24% CAGR",
                        "key_competitors": ["Intercom", "Zendesk", "Freshdesk"],
                        "major_findings": [
                            "AI automation can reduce support costs by 30%",
                            "Customer satisfaction increases by 25% with AI features"
                        ]
                    }
                },
                output={
                    "market_overview": "The AI-powered customer service market is experiencing rapid growth, projected to reach $15.2B by 2025 with 24% CAGR, driven by increasing demand for automated support solutions.",
                    "key_insights": [
                        "AI automation demonstrates 30% cost reduction in customer support operations",
                        "Platforms with AI features show 25% higher customer satisfaction scores",
                        "Market consolidation expected as larger players acquire AI startups"
                    ],
                    "strategic_recommendations": [
                        {
                            "priority": "immediate",
                            "action": "Pilot AI chatbot implementation for tier-1 support",
                            "timeline": "3 months",
                            "resources": "AI development team, $150K budget",
                            "expected_outcome": "20% reduction in support ticket volume"
                        }
                    ],
                    "risk_assessment": [
                        {
                            "risk": "Data privacy concerns with AI training data",
                            "probability": "medium",
                            "impact": "high", 
                            "mitigation": "Implement data anonymization and compliance protocols"
                        }
                    ],
                    "success_metrics": [
                        "Customer satisfaction score (CSAT)",
                        "First contact resolution rate", 
                        "Support cost per ticket",
                        "AI feature adoption rate"
                    ]
                },
                explanation="Synthesized market size and growth data into concise overview. Extracted most impactful findings as key insights. Prioritized recommendations by business impact and feasibility. Identified high-probability risks with specific mitigations."
            )
        ]
    
    def _get_recommendations_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "business_context": "SaaS company facing increased competition",
                    "analysis_insights": {
                        "competitive_gap": "Lacking AI features compared to market leaders",
                        "market_opportunity": "Untapped SMB segment seeking affordable solutions",
                        "customer_feedback": "Requests for better mobile experience"
                    }
                },
                output={
                    "immediate_actions": [
                        {
                            "action": "Launch mobile app development project",
                            "rationale": "Addresses direct customer feedback and competitive gap",
                            "owner": "Product Team",
                            "timeline": "4 months",
                            "resources": "$200K budget, 3 developers",
                            "expected_outcome": "15% increase in mobile user engagement",
                            "success_metrics": ["Mobile app downloads", "Mobile usage rate"]
                        }
                    ],
                    "short_term_initiatives": [
                        {
                            "action": "Develop AI-powered feature roadmap",
                            "rationale": "Closes competitive gap with market leaders",
                            "owner": "CTO Office",
                            "timeline": "6 months", 
                            "resources": "$500K R&D budget",
                            "expected_outcome": "Competitive parity in AI capabilities",
                            "success_metrics": ["AI feature adoption", "Customer retention"]
                        }
                    ],
                    "long_term_strategies": [
                        {
                            "action": "Expand into SMB segment with tailored pricing",
                            "rationale": "Captures underserved market opportunity",
                            "owner": "Business Development",
                            "timeline": "12 months",
                            "resources": "$1M market development fund",
                            "expected_outcome": "20% revenue growth from new segment",
                            "success_metrics": ["SMB customer acquisition", "Segment revenue"]
                        }
                    ]
                },
                explanation="Categorized recommendations by timeframe: immediate (quick wins), short-term (strategic projects), long-term (market expansion). Each recommendation includes specific ownership, resources, and measurable outcomes."
            )
        ]

    def _get_research_report_examples(self) -> List[FewShotExample]:
        return [
            FewShotExample(
                input={
                    "research_topic": "Electric Vehicle Charging Infrastructure",
                    "analysis_data": {
                        "market_analysis": "Market growing at 28% CAGR to $25B by 2028",
                        "competitive_landscape": "Tesla leads with 40% market share",
                        "technology_trends": "Ultra-fast charging becoming standard"
                    }
                },
                output={
                    "executive_summary": "The EV charging market presents significant growth opportunities with 28% CAGR, though competitive intensity is increasing as technology standards evolve.",
                    "methodology": "Combined primary research with 200 industry surveys and secondary analysis of market reports from Grand View Research and McKinsey.",
                    "market_overview": "Global EV charging infrastructure market valued at $15.2B in 2023, projected to reach $25B by 2028, driven by government incentives and automotive OEM commitments.",
                    "competitive_analysis": "Tesla maintains leadership with 40% market share through proprietary network, while ChargePoint and EVgo compete on interoperability and partnerships.",
                    "strategic_recommendations": [
                        "Focus on interoperability standards to capture multi-brand EV users",
                        "Develop ultra-fast charging capabilities to meet future vehicle requirements",
                        "Form strategic partnerships with automotive OEMs and utilities"
                    ],
                    "implementation_roadmap": {
                        "phase_1": "Technology assessment and partner identification (3 months)",
                        "phase_2": "Pilot deployment and standards development (6 months)", 
                        "phase_3": "Full-scale rollout and market expansion (12 months)"
                    }
                },
                explanation="Structured comprehensive report with logical flow from executive summary to implementation. Balanced quantitative data with strategic insights. Provided actionable roadmap with clear phases and timelines."
            )
        ]

    # ===== CORE REPORTING PROMPT TEMPLATES =====
    
    EXECUTIVE_SUMMARY = """EXECUTIVE-LEVEL STRATEGIC SUMMARY

AUDIENCE & CONTEXT:
Primary Audience: {target_audience}
Report Topic: {research_topic}
Current Date: {current_date}
Decision Timeframe: Strategic planning cycle

CONTENT ARCHITECTURE REQUIREMENTS:

1. SITUATION OVERVIEW (2-3 Sentences Maximum):
   - Current market state and key dynamics
   - Major developments or changes since last analysis
   - Immediate business context and implications

2. KEY FINDINGS (3-5 Data-Driven Insights):
   - Each insight MUST include specific quantitative data
   - Focus on findings with strategic business impact
   - Prioritize by relevance to audience decision-making
   - Include comparative analysis where applicable

3. STRATEGIC IMPLICATIONS:
   - What findings mean for the organization
   - Potential impact on competitive positioning
   - Implications for resource allocation and priorities
   - Timing considerations for action

4. RECOMMENDED ACTIONS (Prioritized):
   IMMEDIATE (0-3 months): Quick wins, urgent responses
   SHORT-TERM (3-6 months): Strategic initiatives, capability building  
   LONG-TERM (6-12+ months): Transformational moves, major investments

5. RISK ASSESSMENT:
   - High-probability, high-impact risks only
   - Specific mitigation strategies for each risk
   - Monitoring indicators and trigger points

ANALYSIS INPUTS TO SYNTHESIZE:
{analysis_results}

WRITING STANDARDS:

TONE & STYLE:
- Professional, concise, action-oriented
- Data-driven with specific metrics
- Focus on business impact and ROI
- Avoid technical jargon unless audience-specific

LENGTH CONSTRAINT:
- Maximum 300 words for entire summary
- Each section proportionally balanced
- Bullet points preferred over paragraphs
- White space for readability

DATA INTEGRATION:
✓ All claims supported by analysis data
✓ Quantitative metrics used wherever possible
✓ Comparative context provided (vs. competitors, industry averages)
✓ Confidence levels indicated for projections

VALIDATION CHECKLIST:
□ Executive can make decision based solely on this summary
□ Each recommendation has clear ownership and timeline
□ Risks have specific mitigation strategies
□ Success metrics are measurable and relevant

{format_instructions}

FINAL OUTPUT:
Professional executive summary ready for C-level decision making."""

    RESEARCH_REPORT = """COMPREHENSIVE RESEARCH REPORT DEVELOPMENT

REPORT SPECIFICATIONS:
Title: Market Analysis: {research_topic}
Publication Date: {current_date}
Intended Audience: {target_audience}
Report Length: 8-12 pages (equivalent content density)

STRUCTURED REPORT OUTLINE:

SECTION 1: EXECUTIVE SUMMARY (1 page)
- Situation overview and key findings
- Strategic implications and recommendations
- Risk assessment and mitigation strategies

SECTION 2: METHODOLOGY & DATA SOURCES
- Research approach and framework
- Data collection methods and sources
- Analytical techniques applied
- Limitations and assumptions

SECTION 3: MARKET OVERVIEW & COMPETITIVE LANDSCAPE
- Market sizing and growth projections
- Key market segments and characteristics
- Competitive positioning and dynamics
- Market attractiveness assessment

SECTION 4: DETAILED ANALYSIS FINDINGS
- Technology and innovation trends
- Consumer behavior and preferences
- Regulatory and compliance landscape
- Economic and financial analysis

SECTION 5: STRATEGIC IMPLICATIONS
- Opportunities for growth and expansion
- Threats and competitive challenges
- Strategic options and alternatives
- Timing and sequencing considerations

SECTION 6: RECOMMENDATIONS & IMPLEMENTATION
- Prioritized strategic recommendations
- Implementation roadmap with phases
- Resource requirements and budget estimates
- Success metrics and monitoring framework

SECTION 7: APPENDICES & SUPPORTING MATERIALS
- Detailed data tables and charts
- Competitor profiles and analysis
- Regulatory documentation
- Technical specifications

ANALYSIS DATA INPUTS:
{analysis_data}

WRITING & FORMATTING STANDARDS:

PROFESSIONAL STANDARDS:
- Third-person, objective tone throughout
- Consistent terminology and definitions
- Logical flow between sections
- Balanced analysis of pros and cons

DATA PRESENTATION:
- Charts and graphs for quantitative data
- Tables for comparative analysis
- Bullet points for key findings
- Executive summaries for each major section

CITATION & REFERENCING:
- All data sources properly attributed
- External research appropriately cited
- Proprietary data clearly identified
- Timestamps for all market data

QUALITY ASSURANCE CHECKPOINTS:
✓ All recommendations are actionable and specific
✓ Data visualizations support key messages
✓ Risk factors are adequately addressed
✓ Implementation plan is realistic and resourced

VALIDATION REQUIREMENTS:
□ Methodology is transparent and replicable
□ Findings are supported by multiple data sources
□ Recommendations address identified opportunities
□ Report structure facilitates executive review

{format_instructions}

OUTPUT REQUIREMENTS:
Comprehensive, professional-grade research report suitable for strategic planning and investment decisions."""

    STRATEGIC_RECOMMENDATIONS = """STRATEGIC RECOMMENDATION ENGINE

BUSINESS CONTEXT ANALYSIS:
Current Situation: {business_context}
Decision Date: {current_date}
Strategic Timeframe: {timeframe}

RECOMMENDATION FRAMEWORK & CRITERIA:

PRIORITIZATION MATRIX:
IMPACT ASSESSMENT:
HIGH: Transformative effect on competitive position or revenue (>20% impact)
MEDIUM: Significant operational improvement (5-20% impact)  
LOW: Incremental efficiency gains (<5% impact)

FEASIBILITY ASSESSMENT:
HIGH: Existing capabilities, minimal investment, short timeline
MEDIUM: Some new capabilities required, moderate investment
LOW: Major capability gaps, significant investment, long timeline

RECOMMENDATION CATEGORIZATION:

IMMEDIATE ACTIONS (0-3 Months):
- Quick wins with high impact and high feasibility
- Address urgent competitive threats or opportunities
- Require minimal investment and existing capabilities
- Deliver measurable results within current quarter

SHORT-TERM INITIATIVES (3-6 Months):
- Strategic projects requiring some investment
- Build new capabilities or address gaps
- Moderate risk with clear ROI within 12 months
- Align with current strategic priorities

LONG-TERM STRATEGIES (6-12+ Months):
- Transformational moves with major investment
- Create sustainable competitive advantages
- Higher risk with longer payback periods
- Position for future market leadership

ANALYSIS INSIGHTS TO INFORM RECOMMENDATIONS:
{analysis_insights}

RECOMMENDATION SPECIFICATION REQUIREMENTS:

FOR EACH RECOMMENDATION:

1. ACTION STATEMENT:
   - Specific, measurable, and time-bound
   - Clear scope and deliverables
   - Alignment with strategic objectives

2. BUSINESS RATIONALE:
   - Problem or opportunity being addressed
   - Expected business impact and benefits
   - Strategic importance and urgency

3. IMPLEMENTATION DETAILS:
   - Primary owner and supporting teams
   - Detailed timeline with key milestones
   - Resource requirements (budget, personnel, technology)
   - Dependencies and prerequisites

4. SUCCESS MEASUREMENT:
   - Key performance indicators (KPIs)
   - Target metrics and improvement goals
   - Monitoring frequency and reporting
   - Success criteria and evaluation methods

5. RISK ASSESSMENT:
   - Implementation risks and mitigation
   - Market and competitive risks
   - Contingency plans and alternatives

VALIDATION CHECKLIST:
✓ Each recommendation has clear ownership and accountability
✓ Resource requirements are realistic and available
✓ Timeline accounts for dependencies and constraints
✓ Success metrics are measurable and relevant
✓ Risks are identified with specific mitigation strategies

{format_instructions}

OUTPUT REQUIREMENTS:
Prioritized strategic recommendations with detailed implementation plans, resource requirements, and success metrics."""

    PRESENTATION_DECK = """EXECUTIVE PRESENTATION DECK CREATION

PRESENTATION CONTEXT:
Topic: {presentation_topic}
Target Audience: {target_audience}
Presentation Date: {current_date}
Duration: 30-45 minutes including Q&A

SLIDE DECK ARCHITECTURE:

SLIDE 1: TITLE SLIDE
- Presentation title and subtitle
- Presenter name and position
- Date and occasion
- Company logo and branding

SLIDE 2: AGENDA & EXECUTIVE SUMMARY
- Presentation structure and flow
- Key messages and takeaways
- Time allocation for each section

SLIDE 3-4: MARKET OVERVIEW
- Market size and growth trajectory
- Key trends and drivers
- Competitive landscape overview
- Market attractiveness assessment

SLIDE 5-6: COMPETITIVE ANALYSIS
- Competitor positioning map
- Strengths and weaknesses analysis
- Market share and growth comparisons
- Competitive threats and opportunities

SLIDE 7-8: KEY FINDINGS & INSIGHTS
- 3-5 most important data points
- Visualizations of key metrics
- Comparative analysis charts
- Trend identification graphics

SLIDE 9-10: STRATEGIC RECOMMENDATIONS
- Prioritized action plan
- Implementation roadmap
- Resource requirements
- Expected outcomes and benefits

SLIDE 11: IMPLEMENTATION PLAN
- Timeline with key milestones
- Responsibility assignment
- Success metrics and targets
- Risk mitigation strategies

SLIDE 12: Q&A & NEXT STEPS
- Anticipated questions and answers
- Immediate next actions
- Follow-up timeline
- Contact information

CONTENT INPUTS FOR SLIDE DEVELOPMENT:
{content_data}

DESIGN & DELIVERY STANDARDS:

VISUAL DESIGN PRINCIPLES:
- Consistent branding and color scheme
- High-contrast, readable fonts
- Minimal text, maximum visual impact
- Professional graphics and charts

CONTENT GUIDELINES:
- One key message per slide
- Maximum 5 bullet points per slide
- Data-driven with specific metrics
- Action-oriented language

SPEAKER NOTES REQUIREMENTS:
- Key talking points for each slide
- Data sources and methodology notes
- Anticipated audience questions
- Transition statements between slides

AUDIENCE ENGAGEMENT:
- Interactive elements where appropriate
- Storytelling approach to data presentation
- Clear call-to-action on final slide
- Memorable closing statement

QUALITY ASSURANCE CHECKLIST:
✓ Each slide has clear purpose and key message
✓ Visualizations effectively communicate data insights
✓ Flow is logical and builds toward recommendations
✓ Content is appropriate for audience expertise level
✓ Timing allows for audience interaction and questions

{format_instructions}

OUTPUT REQUIREMENTS:
Complete presentation deck with slides, speaker notes, and visual design guidance ready for executive delivery."""