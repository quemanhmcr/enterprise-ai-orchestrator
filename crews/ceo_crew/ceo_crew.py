from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Import the tools
try:
    from shared.tools.crew_tools import (
        FinanceCrewTool,
        HRCrewTool,
        MarketResearchCrewTool,
        OperationsCrewTool,
        ProductDevelopmentCrewTool,
        SalesMarketingCrewTool,
    )
except ImportError:
    # Fallback for direct execution or different path structure
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from shared.tools.crew_tools import (
        FinanceCrewTool,
        HRCrewTool,
        MarketResearchCrewTool,
        OperationsCrewTool,
        ProductDevelopmentCrewTool,
        SalesMarketingCrewTool,
    )

@CrewBase
class CeoCrew():
    """CEO Crew - Strategic Orchestration"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools
        self.market_research_tool = MarketResearchCrewTool()
        self.product_development_tool = ProductDevelopmentCrewTool()
        self.sales_marketing_tool = SalesMarketingCrewTool()
        self.operations_tool = OperationsCrewTool()
        self.finance_tool = FinanceCrewTool()
        self.hr_tool = HRCrewTool()

    @agent
    def ceo(self) -> Agent:
        return Agent(
            config=self.agents_config['ceo'],
            tools=[
                self.market_research_tool,
                self.product_development_tool,
                self.sales_marketing_tool,
                self.operations_tool,
                self.finance_tool,
                self.hr_tool
            ],
            verbose=True,
            allow_delegation=True
        )

    @task
    def manage_company_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['manage_company_strategy'],
            agent=self.ceo()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CEO Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

class CEOOrchestrationFlow:
    def kickoff(self, inputs=None):
        crew = CeoCrew().crew()
        return crew.kickoff(inputs=inputs)

def run_ceo_orchestration(request: str = None):
    print("Running CEO Orchestration...")
    inputs = {
        'request': request or 'Develop a strategy for Q1 2026 focusing on AI adoption.'
    }
    result = CeoCrew().crew().kickoff(inputs=inputs)
    print(result)
    return result

if __name__ == "__main__":
    run_ceo_orchestration()
