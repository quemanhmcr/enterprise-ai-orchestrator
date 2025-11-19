"""
Operations Crew
Handles process optimization, supply chain, and quality management
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import os


@CrewBase
class OperationsCrew():
    """Operations Crew - Efficiency and Excellence"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        self.ops_knowledge = self._load_operations_knowledge()
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool()
        self.file_writer_tool = FileWriterTool()
    
    def _load_operations_knowledge(self):
        """Load operations management best practices."""
        knowledge_content = """
        # Operations Management Best Practices
        
        ## Lean Manufacturing
        - 8 Wastes (TIMWOODS): Transport, Inventory, Motion, Waiting, Overproduction, Over-processing, Defects, Skills
        - 5S: Sort, Set in order, Shine, Standardize, Sustain
        - Just-In-Time (JIT) production
        - Kanban system for workflow management
        
        ## Six Sigma
        - DMAIC: Define, Measure, Analyze, Improve, Control
        - Statistical process control (SPC)
        - Root cause analysis (5 Whys, Fishbone diagram)
        - Design for Six Sigma (DFSS)
        
        ## Supply Chain Management
        - Demand forecasting techniques
        - Economic Order Quantity (EOQ)
        - ABC analysis for inventory classification
        - Vendor-Managed Inventory (VMI)
        - Supply chain risk management (SCRM)
        
        ## Process Optimization
        - Value Stream Mapping (VSM)
        - Theory of Constraints (TOC)
        - Business Process Reengineering (BPR)
        - Continuous improvement (Kaizen)
        
        ## Quality Management
        - ISO 9001 quality management system
        - Total Quality Management (TQM)
        - Cost of Quality (Prevention, Appraisal, Internal Failure, External Failure)
        - Statistical Quality Control
        
        ## Key Metrics
        - Overall Equipment Effectiveness (OEE)
        - Cycle time and lead time
        - First Pass Yield (FPY)
        - On-Time In-Full (OTIF) delivery
        - Inventory turnover ratio
        - Cost per unit
        """
        
        return StringKnowledgeSource(
            content=knowledge_content,
            metadata={"source": "operations_playbook"}
        )
    
    @agent
    def chief_operations_officer(self) -> Agent:
        config = self.agents_config['chief_operations_officer']
        return Agent(
            config=config,
            # knowledge_sources=[self.ops_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def operations_manager(self) -> Agent:
        config = self.agents_config['operations_manager']
        return Agent(
            config=config,
            # knowledge_sources=[self.ops_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def supply_chain_analyst(self) -> Agent:
        config = self.agents_config['supply_chain_analyst']
        return Agent(
            config=config,
            # knowledge_sources=[self.ops_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def process_engineer(self) -> Agent:
        config = self.agents_config['process_engineer']
        return Agent(
            config=config,
            # knowledge_sources=[self.ops_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def quality_controller(self) -> Agent:
        config = self.agents_config['quality_controller']
        return Agent(
            config=config,
            # knowledge_sources=[self.ops_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @task
    def operations_optimization(self) -> Task:
        return Task(config=self.tasks_config['operations_optimization'])
    
    @task
    def supply_chain_management(self) -> Task:
        return Task(config=self.tasks_config['supply_chain_management'])
    
    @task
    def process_improvement(self) -> Task:
        return Task(config=self.tasks_config['process_improvement'])
    
    @task
    def quality_management(self) -> Task:
        return Task(config=self.tasks_config['quality_management'])
    
    @task
    def operations_synthesis(self) -> Task:
        return Task(config=self.tasks_config['operations_synthesis'])
    
    @crew
    def crew(self) -> Crew:
        """Creates the Operations Crew with HIERARCHICAL process.
        
        Manager LLM (COO-level thinking) sẽ:
        - Phân tích operational challenges và prioritize improvements
        - Assign process optimization tasks cho đúng specialists
        - Coordinate giữa supply chain, process engineering, quality
        - Review improvement plans và ensure feasibility
        - Make trade-off decisions giữa cost, quality, và speed
        - Drive continuous improvement culture
        """
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            # knowledge_sources=[self.ops_knowledge],
            planning=False,
            respect_context_window=True
        )
