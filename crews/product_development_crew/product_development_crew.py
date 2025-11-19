"""
Product Development Crew
Handles product strategy, UX design, engineering, and QA
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import yaml
import os
from pathlib import Path


@CrewBase
class ProductDevelopmentCrew():
    """Product Development Crew - Engineering and Innovation"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool()
        self.file_writer_tool = FileWriterTool()
        # Load knowledge sources
        self.product_knowledge = self._load_product_knowledge()
    
    def _load_product_knowledge(self):
        """Load product development best practices and guidelines."""
        knowledge_content = """
        # Product Development Best Practices
        
        ## Agile Methodology
        - Sprint planning and backlog refinement
        - Daily standups and retrospectives
        - Continuous integration and delivery
        - Iterative development with user feedback
        
        ## Technical Excellence
        - Clean code principles (SOLID, DRY, KISS)
        - Test-driven development (TDD)
        - Code reviews and pair programming
        - Documentation and knowledge sharing
        
        ## Design Thinking
        - User-centered design approach
        - Empathy mapping and persona development
        - Rapid prototyping and iteration
        - Usability testing and validation
        
        ## Quality Assurance
        - Shift-left testing strategy
        - Automated testing pyramid (unit > integration > E2E)
        - Performance testing and optimization
        - Security testing and compliance
        
        ## Product Management
        - RICE prioritization framework
        - OKR (Objectives and Key Results)
        - A/B testing and experimentation
        - Data-driven decision making
        """
        
        return StringKnowledgeSource(
            content=knowledge_content,
            metadata={"source": "product_development_guidelines"}
        )
    
    @agent
    def chief_product_officer(self) -> Agent:
        config = self.agents_config['chief_product_officer']
        return Agent(
            config=config,
            # knowledge_sources=[self.product_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def product_manager(self) -> Agent:
        config = self.agents_config['product_manager']
        return Agent(
            config=config,
            # knowledge_sources=[self.product_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def ux_designer(self) -> Agent:
        config = self.agents_config['ux_designer']
        return Agent(
            config=config,
            # knowledge_sources=[self.product_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def engineering_lead(self) -> Agent:
        config = self.agents_config['engineering_lead']
        return Agent(
            config=config,
            # knowledge_sources=[self.product_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @agent
    def qa_specialist(self) -> Agent:
        config = self.agents_config['qa_specialist']
        return Agent(
            config=config,
            # knowledge_sources=[self.product_knowledge],
            tools=[self.search_tool, self.file_read_tool, self.file_writer_tool],
            verbose=True
        )
    
    @task
    def product_roadmap_planning(self) -> Task:
        return Task(config=self.tasks_config['product_roadmap_planning'])
    
    @task
    def ux_design_planning(self) -> Task:
        return Task(config=self.tasks_config['ux_design_planning'])
    
    @task
    def technical_architecture(self) -> Task:
        return Task(config=self.tasks_config['technical_architecture'])
    
    @task
    def quality_assurance_strategy(self) -> Task:
        return Task(config=self.tasks_config['quality_assurance_strategy'])
    
    @task
    def product_development_synthesis(self) -> Task:
        return Task(config=self.tasks_config['product_development_synthesis'])
    
    @crew
    def crew(self) -> Crew:
        """Creates the Product Development Crew with HIERARCHICAL process.
        
        Manager LLM (CPO-level thinking) sẽ:
        - Phân tích product requirements và chia thành sub-tasks
        - Assign tasks cho đúng specialists (UX, Engineering, QA, Security, etc.)
        - Review designs, code architecture, test plans
        - Ensure cross-functional collaboration và quality
        - Make go/no-go decisions dựa trên technical feasibility và business value
        """
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            # knowledge_sources=[self.product_knowledge],
            planning=False,
            respect_context_window=True
        )
