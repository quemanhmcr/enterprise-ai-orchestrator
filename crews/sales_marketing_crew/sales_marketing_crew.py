"""
Sales & Marketing Crew
Handles revenue generation, brand building, and customer success
"""


from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool, SerperDevTool


@CrewBase
class SalesMarketingCrew():
    """Sales & Marketing Crew - Revenue and Growth"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool()
        self.file_writer_tool = FileWriterTool()

        # Load knowledge
        self.gtm_knowledge = self._load_gtm_knowledge()

    def _load_gtm_knowledge(self):
        """Load go-to-market best practices."""
        knowledge_content = """
        # Go-to-Market Best Practices

        ## Sales Methodology
        - MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion)
        - SPIN Selling (Situation, Problem, Implication, Need-Payoff)
        - Challenger Sale approach
        - Account-Based Selling (ABS)

        ## Marketing Frameworks
        - AARRR (Acquisition, Activation, Retention, Revenue, Referral)
        - 4Ps (Product, Price, Place, Promotion)
        - STP (Segmentation, Targeting, Positioning)
        - Growth hacking and experimentation

        ## Content Marketing
        - Buyer's journey content mapping (Awareness, Consideration, Decision)
        - Pillar content and topic clusters
        - SEO best practices (on-page, technical, off-page)
        - Content distribution and amplification

        ## Customer Success
        - Customer health scoring
        - Red-Yellow-Green account classification
        - Net Revenue Retention (NRR) optimization
        - Voice of Customer (VoC) programs

        ## Key Metrics
        - CAC (Customer Acquisition Cost)
        - LTV (Lifetime Value)
        - LTV:CAC ratio (target 3:1)
        - Magic Number (sales efficiency)
        - Pipeline coverage (3x-4x)
        - Win rate and sales cycle length
        """

        return StringKnowledgeSource(
            content=knowledge_content,
            metadata={"source": "gtm_playbook"}
        )

    @agent
    def chief_revenue_officer(self) -> Agent:
        config = self.agents_config['chief_revenue_officer']
        return Agent(
            config=config,
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            # knowledge_sources=[self.gtm_knowledge],
            verbose=True
        )

    @agent
    def sales_director(self) -> Agent:
        config = self.agents_config['sales_director']
        return Agent(
            config=config,
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            # knowledge_sources=[self.gtm_knowledge],
            verbose=True
        )

    @agent
    def marketing_strategist(self) -> Agent:
        config = self.agents_config['marketing_strategist']
        return Agent(
            config=config,
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            # knowledge_sources=[self.gtm_knowledge],
            verbose=True
        )

    @agent
    def content_creator(self) -> Agent:
        config = self.agents_config['content_creator']
        return Agent(
            config=config,
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            # knowledge_sources=[self.gtm_knowledge],
            verbose=True
        )

    @agent
    def customer_success_manager(self) -> Agent:
        config = self.agents_config['customer_success_manager']
        return Agent(
            config=config,
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            # knowledge_sources=[self.gtm_knowledge],
            verbose=True
        )

    @task
    def sales_strategy_planning(self) -> Task:
        return Task(config=self.tasks_config['sales_strategy_planning'])

    @task
    def marketing_campaign_planning(self) -> Task:
        return Task(config=self.tasks_config['marketing_campaign_planning'])

    @task
    def content_strategy_execution(self) -> Task:
        return Task(config=self.tasks_config['content_strategy_execution'])

    @task
    def customer_success_planning(self) -> Task:
        return Task(config=self.tasks_config['customer_success_planning'])

    @task
    def sales_marketing_synthesis(self) -> Task:
        return Task(config=self.tasks_config['sales_marketing_synthesis'])

    @crew
    def crew(self) -> Crew:
        """Creates the Sales & Marketing Crew with HIERARCHICAL process.

        Manager LLM (CRO-level thinking) sẽ:
        - Orchestrate GTM strategy across sales, marketing, và customer success
        - Assign campaign planning cho Marketing team
        - Coordinate sales plays và account strategies
        - Ensure alignment giữa marketing pipeline và sales capacity
        - Review content, campaigns, sales materials
        - Make budget allocation decisions
        - Track metrics và adjust strategy based on performance
        """

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            # knowledge_sources=[self.gtm_knowledge],  # Tạm tắt knowledge
            planning=False,  # Tắt planning vì conflict với custom model
            respect_context_window=True
        )
