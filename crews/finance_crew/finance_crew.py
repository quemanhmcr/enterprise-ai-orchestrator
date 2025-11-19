"""
Finance Crew
Handles financial planning, budgeting, analysis, and compliance
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import os


@CrewBase
class FinanceCrew():
    """Finance Crew - Financial Leadership"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        self.finance_knowledge = self._load_finance_knowledge()
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool()
        self.file_writer_tool = FileWriterTool()
    
    def _load_finance_knowledge(self):
        """Load financial management best practices."""
        knowledge_content = """
        # Financial Management Best Practices
        
        ## Financial Planning & Analysis
        - Three statement modeling (P&L, Balance Sheet, Cash Flow)
        - Scenario planning and sensitivity analysis
        - Driver-based forecasting
        - Rolling forecasts vs annual budgets
        
        ## Capital Allocation
        - Return on Invested Capital (ROIC)
        - Net Present Value (NPV) and IRR analysis
        - Capital efficiency metrics
        - Portfolio optimization
        
        ## Budgeting
        - Zero-based budgeting (ZBB)
        - Activity-based costing (ABC)
        - Variance analysis (price, volume, mix)
        - Reforecast frequency and triggers
        
        ## Financial Metrics
        - Rule of 40 (Growth Rate + Profit Margin ≥ 40%)
        - Cash conversion cycle
        - Days Sales Outstanding (DSO)
        - Burn rate and runway
        - Unit economics (CAC, LTV, payback period)
        
        ## Compliance & Controls
        - Sarbanes-Oxley (SOX) compliance
        - GAAP/IFRS accounting standards
        - COSO internal control framework
        - Audit committee best practices
        
        ## Risk Management
        - Enterprise Risk Management (ERM)
        - Foreign exchange hedging
        - Interest rate risk management
        - Scenario stress testing
        
        ## Financial Reporting
        - Management reporting (MIS)
        - Board reporting packages
        - Investor relations materials
        - KPI dashboards
        """
        
        return StringKnowledgeSource(
            content=knowledge_content,
            metadata={"source": "finance_playbook"}
        )
    
    @agent
    def cfo(self) -> Agent:
        config = self.agents_config['cfo']
        return Agent(
            config=config,
            # knowledge_sources=[self.finance_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def financial_analyst(self) -> Agent:
        config = self.agents_config['financial_analyst']
        return Agent(
            config=config,
            # knowledge_sources=[self.finance_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def budget_controller(self) -> Agent:
        config = self.agents_config['budget_controller']
        return Agent(
            config=config,
            # knowledge_sources=[self.finance_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def compliance_officer(self) -> Agent:
        config = self.agents_config['compliance_officer']
        return Agent(
            config=config,
            # knowledge_sources=[self.finance_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @task
    def financial_planning(self) -> Task:
        return Task(config=self.tasks_config['financial_planning'])
    
    @task
    def financial_analysis(self) -> Task:
        return Task(config=self.tasks_config['financial_analysis'])
    
    @task
    def budget_management(self) -> Task:
        return Task(config=self.tasks_config['budget_management'])
    
    @task
    def compliance_and_controls(self) -> Task:
        return Task(config=self.tasks_config['compliance_and_controls'])
    
    @task
    def finance_synthesis(self) -> Task:
        return Task(config=self.tasks_config['finance_synthesis'])
    
    @crew
    def crew(self) -> Crew:
        """Creates the Finance Crew with HIERARCHICAL process.
        
        Manager LLM (CFO-level thinking) sẽ:
        - Orchestrate financial planning và analysis
        - Assign financial modeling cho analysts
        - Coordinate budget planning, compliance, forecasting
        - Review financial plans và ensure accuracy
        - Make strategic financial recommendations
        - Ensure regulatory compliance và risk management
        """
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            # knowledge_sources=[self.finance_knowledge],  # Tạm tắt
            planning=False,  # Tắt planning
            respect_context_window=True
        )
