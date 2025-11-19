"""
Market Research Crew - Competitive Intelligence and Market Analysis
Sequential process with async competitive and consumer insights gathering
"""

from pathlib import Path
from typing import Dict, List

# RAG-based tools (PDFSearchTool, CSVSearchTool, JSONSearchTool) require qdrant_client
# GithubSearchTool and YoutubeVideoSearchTool may need additional API keys
# from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
import yaml
from crewai import Agent, Crew, Process, Task
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriterTool, SerperDevTool


class MarketResearchCrew:
    """Market Research Crew for market intelligence and competitive analysis."""

    def __init__(self):
        self.agents_config = self._load_config('agents.yaml')
        self.tasks_config = self._load_config('tasks.yaml')
        self.tools = self._setup_tools()
        self.knowledge_sources = self._setup_knowledge()

    def _load_config(self, filename: str) -> Dict:
        """Load YAML configuration file."""
        config_path = Path(__file__).parent / 'config' / filename
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _setup_tools(self) -> Dict:
        """Initialize crew tools - only non-RAG tools to avoid qdrant_client dependency."""
        return {
            # Search Tool
            'SerperDevTool': SerperDevTool(),

            # File Tools (non-RAG)
            'FileReadTool': FileReadTool(),
            'DirectoryReadTool': DirectoryReadTool(),
            'FileWriterTool': FileWriterTool()
        }

    def _setup_knowledge(self) -> List:
        """Setup crew-level knowledge sources."""
        # Temporarily disabled - CSV knowledge source requires additional setup
        sources = []

        # knowledge_path = Path(__file__).parent.parent.parent / 'shared' / 'knowledge'
        # # Market data CSV files
        # csv_files = list(knowledge_path.glob('market_data*.csv'))
        # if csv_files:
        #     sources.append(CSVKnowledgeSource(
        #         file_paths=[str(f) for f in csv_files]
        #     ))

        return sources

    def _get_tools(self, tool_names: List[str]) -> List:
        """Get tool instances by name."""
        return [self.tools[name] for name in tool_names if name in self.tools]

    def _create_agent(self, agent_name: str) -> Agent:
        """Create an agent from configuration."""
        config = self.agents_config[agent_name]

        # Get tools for this agent
        agent_tools = []
        if 'tools' in config:
            agent_tools = self._get_tools(config['tools'])

        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=agent_tools,
            reasoning=config.get('reasoning', False),
            max_reasoning_attempts=config.get('max_reasoning_attempts', 3),
            allow_delegation=config.get('allow_delegation', False),
            allow_code_execution=config.get('allow_code_execution', False),
            code_execution_mode=config.get('code_execution_mode', 'safe'),
            max_execution_time=config.get('max_execution_time', 180),
            verbose=config.get('verbose', True),
            inject_date=config.get('inject_date', False),
            max_iter=config.get('max_iter', 25),
            max_rpm=config.get('max_rpm', 20)
        )

    def _create_task(self, task_name: str, agents: Dict[str, Agent]) -> Task:
        """Create a task from configuration."""
        config = self.tasks_config[task_name]

        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=agents[config['agent']],
            async_execution=config.get('async_execution', False),
            guardrails=config.get('guardrails', []),
            guardrail_max_retries=config.get('guardrail_max_retries', 2),
            output_file=config.get('output_file')
        )

    def crew(self) -> Crew:
        """Create and configure the market research crew."""

        # Create agents - using agents defined in agents.yaml
        agents = {
            'market_research_lead': self._create_agent('market_research_director'),
            'competitive_analyst': self._create_agent('competitive_intelligence_analyst'),
            'consumer_insights_specialist': self._create_agent('customer_insights_researcher'),
            'data_scientist': self._create_agent('data_scientist_market_analytics')
        }

        # Create tasks
        tasks = {
            'market_landscape_analysis': self._create_task('market_landscape_analysis', agents),
            'competitive_intelligence': self._create_task('competitive_intelligence', agents),
            'consumer_insights': self._create_task('consumer_insights', agents),
            'predictive_analysis': self._create_task('predictive_analysis', agents),
            'market_research_synthesis': self._create_task('market_research_synthesis', agents)
        }

        # Set up task contexts
        tasks['predictive_analysis'].context = [
            tasks['market_landscape_analysis'],
            tasks['competitive_intelligence'],
            tasks['consumer_insights']
        ]
        tasks['market_research_synthesis'].context = [
            tasks['market_landscape_analysis'],
            tasks['competitive_intelligence'],
            tasks['consumer_insights'],
            tasks['predictive_analysis']
        ]

        return Crew(
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            process=Process.sequential,
            memory=False,
            knowledge_sources=self.knowledge_sources if self.knowledge_sources else None,
            verbose=True,
            max_rpm=80
        )


def run():
    """Run the market research crew."""
    import datetime

    inputs = {
        'market_segment': 'Enterprise AI Solutions',
        'time_period': 'Q4 2025',
        'current_date': datetime.datetime.now().strftime('%B %d, %Y'),
        'geographic_scope': 'North America and Europe',
        'competitors': ['OpenAI', 'Anthropic', 'Google AI', 'Microsoft Azure AI', 'AWS Bedrock'],
        'target_demographics': 'Enterprise CTOs, VPs of Engineering, Data Science Teams',
        'forecast_horizon': '18 months'
    }

    market_crew = MarketResearchCrew()
    result = market_crew.crew().kickoff(inputs=inputs)

    print("\n" + "="*80)
    print("MARKET RESEARCH CREW EXECUTION COMPLETED")
    print("="*80)
    print(result)

    return result


if __name__ == "__main__":
    run()
