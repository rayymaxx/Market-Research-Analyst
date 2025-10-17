from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Any, Dict
from .tools import create_all_tools

@CrewBase
class MarketResearchCrew():
    """Market Research Analyst Crew"""
    
    def __init__(self):
        super().__init__()
        self.tools = create_all_tools()

    @agent
    def seniorResearchDirector(self) -> Agent:
        return Agent(
            config=self.agents_config['seniorResearchDirector'],
            verbose=True
        )

    @agent
    def digitalIntelligenceGatherer(self) -> Agent:
        return Agent(
            config=self.agents_config['digitalIntelligenceGatherer'],
            tools=self.tools,  # All tools for data collection
            verbose=True
        )

    @agent
    def quantitativeInsightsSpecialist(self) -> Agent:
        return Agent(
            config=self.agents_config['quantitativeInsightsSpecialist'],
            verbose=True
        )

    @agent
    def strategicCommunicationsExpert(self) -> Agent:
        return Agent(
            config=self.agents_config['strategicCommunicationsExpert'],
            verbose=True
        )

    @task
    def research_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_planning_task'],
            agent=self.seniorResearchDirector()
        )

    @task
    def competitor_data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitor_data_collection_task'],
            agent=self.digitalIntelligenceGatherer(),
            context=[self.research_planning_task()]
        )

    @task
    def market_trends_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_trends_collection_task'],
            agent=self.digitalIntelligenceGatherer(),
            context=[self.research_planning_task()]
        )

    @task
    def swot_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['swot_analysis_task'],
            agent=self.quantitativeInsightsSpecialist(),
            context=[
                self.competitor_data_collection_task(),
                self.market_trends_collection_task()
            ]
        )

    @task
    def competitive_benchmarking_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitive_benchmarking_task'],
            agent=self.quantitativeInsightsSpecialist(),
            context=[self.competitor_data_collection_task()]
        )

    @task
    def quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance_task'],
            agent=self.seniorResearchDirector(),
            context=[
                self.competitor_data_collection_task(),
                self.market_trends_collection_task(),
                self.swot_analysis_task(),
                self.competitive_benchmarking_task()
            ]
        )

    @task
    def executive_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['executive_summary_task'],
            agent=self.strategicCommunicationsExpert(),
            context=[
                self.swot_analysis_task(),
                self.competitive_benchmarking_task()
            ]
        )

    @task
    def comprehensive_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['comprehensive_report_task'],
            agent=self.strategicCommunicationsExpert(),
            output_file='research_report.md',
            context=[
                self.executive_summary_task(),
                self.quality_assurance_task()
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Market Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically populated by @agent decorators
            tasks=self.tasks,    # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True,
            memory=False
        )