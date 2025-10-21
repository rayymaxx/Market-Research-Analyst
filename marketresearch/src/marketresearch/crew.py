# src/marketresearch/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Any, Dict
from .tools import create_all_tools
from .rag_chain_factory import RAGEnhancedChainFactory
from .config.gemini_config import get_crewai_gemini_llm
from langchain.memory import ConversationBufferMemory
import json
import time

@CrewBase
class MarketResearchCrew():
    """Market Research Analyst Crew with RAG-Enhanced Chains"""
    
    def __init__(self):
        super(MarketResearchCrew, self).__init__()
        # Initialize RAG-enhanced chain factory
        self.chain_factory = RAGEnhancedChainFactory("./knowledge")
        print("✅ RAG-Enhanced Chain Factory Initialized")
        
        # Add crew-wide memory for better context retention
        self.crew_memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="crew_history"
        )
        
        # Track task outputs for better context passing
        self.task_outputs = {}
        self.research_progress = {
            "completed_tasks": [],
            "current_phase": "planning",
            "key_insights": [],
            "data_quality_score": 0
        }
        
        print("✅ Crew Memory System Initialized")

    def _get_llm_for_agent(self, agent_role: str):
        """Get appropriate LLM for each agent using your multi-model system"""
        task_type_mapping = {
            "seniorResearchDirector": "executive_summary",
            "digitalIntelligenceGatherer": "data_collection", 
            "quantitativeInsightsSpecialist": "swot_analysis",
            "strategicCommunicationsExpert": "research_report"
        }
        
        task_type = task_type_mapping.get(agent_role, "general")
        return get_crewai_gemini_llm(task_type)
    
    def _create_all_tools_with_chains(self):
        """Create all tools including chain tools"""
        base_tools = create_all_tools()
        
        # Import and create chain tools
        from .tools.chain_tools import (
            SWOTAnalysisTool, 
            CompanyResearchChainTool, 
            MarketTrendsTool,
            CompetitiveBenchmarkingTool
        )
        
        chain_tools = [
            SWOTAnalysisTool(),
            CompanyResearchChainTool(),
            MarketTrendsTool(),
            CompetitiveBenchmarkingTool(),
        ]
        
        all_tools = base_tools + chain_tools
        
        print(f"🔧 Loaded {len(all_tools)} tools total:")
        for tool in all_tools:
            print(f"   - {tool.name}")
        
        return all_tools

    @agent
    def seniorResearchDirector(self) -> Agent:
        return Agent(
            config=self.agents_config['seniorResearchDirector'],
            llm=self._get_llm_for_agent("seniorResearchDirector"),
            verbose=True
        )

    @agent
    def digitalIntelligenceGatherer(self) -> Agent:
        # Use all tools for data gatherer
        all_tools = self._create_all_tools_with_chains()
        
        return Agent(
            config=self.agents_config['digitalIntelligenceGatherer'],
            tools=all_tools,
            llm=self._get_llm_for_agent("digitalIntelligenceGatherer"),
            verbose=True
        )

    @agent
    def quantitativeInsightsSpecialist(self) -> Agent:
        # Use all tools for insights specialist
        all_tools = self._create_all_tools_with_chains()
        
        return Agent(
            config=self.agents_config['quantitativeInsightsSpecialist'],
            tools=all_tools,
            llm=self._get_llm_for_agent("quantitativeInsightsSpecialist"),
            verbose=True
        )

    @agent
    def strategicCommunicationsExpert(self) -> Agent:
        # Use all tools for communications expert
        all_tools = self._create_all_tools_with_chains()
        
        return Agent(
            config=self.agents_config['strategicCommunicationsExpert'],
            tools=all_tools,
            llm=self._get_llm_for_agent("strategicCommunicationsExpert"),
            verbose=True
        )

    @task
    def comprehensive_data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['comprehensive_data_collection_task'],
            agent=self.digitalIntelligenceGatherer(),
            description="""Conduct comprehensive market research including:
            1. Research planning and strategy
            2. Competitor data collection and analysis
            3. Market trends identification and analysis
            4. Industry landscape mapping
            
            Use all available tools to gather comprehensive data in a single task.
            Focus on efficiency and thoroughness to minimize API calls."""
        )

    @task
    def comprehensive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['comprehensive_analysis_task'],
            agent=self.quantitativeInsightsSpecialist(),
            context=[self.comprehensive_data_collection_task()],
            description="""Perform comprehensive analysis including:
            1. SWOT analysis using collected data
            2. Competitive benchmarking and scoring
            3. Quality assurance of all findings
            4. Strategic insights generation
            
            Combine multiple analytical frameworks into one comprehensive analysis."""
        )

    @task
    def final_comprehensive_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_comprehensive_report_task'],
            agent=self.strategicCommunicationsExpert(),
            output_file='research_report.pdf',
            context=[self.comprehensive_data_collection_task(), self.comprehensive_analysis_task()],
            description="""Create the final comprehensive market research report including:
            1. Executive summary with key findings
            2. Detailed market analysis and trends
            3. Competitive landscape and benchmarking
            4. SWOT analysis and strategic recommendations
            5. Quality-assured conclusions and next steps
            
            Integrate all previous work into one comprehensive, professional report."""
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Market Research Crew with all tasks"""
        return Crew(
            agents=self.agents,  # Automatically populated by @agent decorators
            tasks=self.tasks,    # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable CrewAI's built-in memory (conflicts with our custom memory)
            max_iter=1,   # Single iteration to prevent quota issues
            max_execution_time=3600  # 60 minutes timeout for fewer but longer tasks
        )
    
    def kickoff_with_rag(self, inputs: dict):
        """Enhanced kickoff with memory and context tracking"""
        from .utils.cache import research_cache
        
        # Check cache first
        cache_key = f"{inputs['research_topic']}_{inputs['research_request']}"
        cached_result = research_cache.get(cache_key)
        if cached_result:
            print(f"📋 Using cached result for: {inputs['research_topic']}")
            return cached_result
        
        print("🚀 Starting RAG-Enhanced Market Research...")
        stats = self.chain_factory.rag_pipeline.get_knowledge_stats()
        print(f"📚 Knowledge Base: {stats['total_documents']} documents loaded")
        
        # Load previous research context if available
        memory_context = self.crew_memory.load_memory_variables({})
        if memory_context.get('crew_history'):
            print(f"🧠 Previous research context loaded: {len(memory_context['crew_history'])} interactions")
            # Convert LangChain messages to strings for CrewAI compatibility
            history_text = "\n".join([str(msg.content) if hasattr(msg, 'content') else str(msg) for msg in memory_context['crew_history']])
            inputs['previous_research'] = history_text
        
        # Show which models we're using
        print("🤖 Agent Model Assignment:")
        agents = [
            "seniorResearchDirector",
            "digitalIntelligenceGatherer", 
            "quantitativeInsightsSpecialist",
            "strategicCommunicationsExpert"
        ]
        
        for agent_name in agents:
            agent = getattr(self, agent_name)()
            model_name = agent.llm.model
            print(f"   - {agent_name}: {model_name}")
        
        # Add research progress tracking to inputs
        inputs['research_progress'] = self.research_progress
        inputs['chain_factory_summary'] = self.chain_factory.get_research_summary()
        
        print("📈 Research Progress Tracking Enabled")
        
        try:
            # Execute the crew with enhanced context
            result = self.crew().kickoff(inputs=inputs)
            
            # Convert result to PDF if it's markdown
            if isinstance(result, str) and result.strip():
                from .utils.pdf_converter import convert_md_to_pdf
                research_id = inputs.get('research_id', inputs['research_topic'].replace(' ', '_'))
                pdf_path = f"research_report_{research_id}.pdf"
                try:
                    convert_md_to_pdf(str(result), pdf_path)
                    print(f"📄 PDF report generated: {pdf_path}")
                except Exception as pdf_error:
                    print(f"⚠️ PDF conversion failed: {pdf_error}")
            
            # Save successful research session to memory
            self.crew_memory.save_context(
                {"research_topic": inputs['research_topic']},
                {"research_result": f"Completed research on {inputs['research_topic']} successfully"}
            )
            
            # Update research progress
            self.research_progress['completed_tasks'] = ['all']
            self.research_progress['current_phase'] = 'completed'
            
            # Cache the result
            research_cache.set(cache_key, result)
            print(f"📋 Research result cached for future use")
            
            print("✅ Research session saved to memory")
            return result
            
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            # Save failed attempt to memory for learning
            self.crew_memory.save_context(
                {"research_topic": inputs['research_topic']},
                {"research_error": f"Research failed: {str(e)}"}
            )
            raise
    
    def get_memory_summary(self):
        """Get summary of crew memory and research progress"""
        return {
            "crew_memory": len(self.crew_memory.chat_memory.messages) if hasattr(self.crew_memory, 'chat_memory') else 0,
            "chain_factory_memory": self.chain_factory.get_research_summary(),
            "research_progress": self.research_progress,
            "task_outputs_count": len(self.task_outputs)
        }