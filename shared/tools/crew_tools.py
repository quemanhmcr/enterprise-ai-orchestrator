from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Type
import sys
import os

# Ensure the crews directory is in the path if not already
# This helps if running this file directly or from a different context
current_dir = os.path.dirname(os.path.abspath(__file__))
crews_dir = os.path.dirname(current_dir)
if crews_dir not in sys.path:
    sys.path.append(crews_dir)

class CrewToolInput(BaseModel):
    request: str = Field(..., description="The specific request or task description for the crew.")
    context: Optional[str] = Field(None, description="Additional context or background information.")

class BaseCrewTool(BaseTool):
    name: str = "Base Crew Tool"
    description: str = "Base tool for running a crew"
    args_schema: Type[BaseModel] = CrewToolInput

    def _run_crew(self, crew_module_name, crew_class_name, inputs: Dict[str, Any]):
        try:
            # Dynamic import
            module = __import__(crew_module_name, fromlist=[crew_class_name])
            crew_class = getattr(module, crew_class_name)
            
            # Instantiate the crew
            crew_instance = crew_class()
            
            # Check if it has a crew() method (CrewBase style) or if it is the crew itself
            if hasattr(crew_instance, 'crew'):
                crew = crew_instance.crew()
            else:
                crew = crew_instance
            
            # Run the crew
            return crew.kickoff(inputs=inputs)
        except ImportError as e:
            return f"Error importing crew {crew_class_name} from {crew_module_name}: {str(e)}"
        except Exception as e:
            return f"Error running crew {crew_class_name}: {str(e)}"

class MarketResearchCrewTool(BaseCrewTool):
    name: str = "Market Research Crew"
    description: str = "Delegate market research tasks. Useful for analyzing competitors, market trends, and consumer insights."

    def _run(self, request: str, context: str = None) -> str:
        inputs = {
            'market_segment': request,
            'time_period': 'Current and Future',
            'current_date': '2025-11-19',
            'geographic_scope': 'Global',
            'competitors': 'Key competitors',
            'target_demographics': 'General Audience',
            'forecast_horizon': '1 year'
        }
        return self._run_crew('market_research_crew.market_research_crew', 'MarketResearchCrew', inputs)

class ProductDevelopmentCrewTool(BaseCrewTool):
    name: str = "Product Development Crew"
    description: str = "Delegate product development tasks. Useful for product strategy, design, engineering, and QA."

    def _run(self, request: str, context: str = None) -> str:
        inputs = {
            'product_idea': request,
            'features': 'Key features based on request',
            'target_audience': 'General audience'
        }
        return self._run_crew('product_development_crew.product_development_crew', 'ProductDevelopmentCrew', inputs)

class SalesMarketingCrewTool(BaseCrewTool):
    name: str = "Sales & Marketing Crew"
    description: str = "Delegate sales and marketing tasks. Useful for campaigns, lead generation, and messaging."

    def _run(self, request: str, context: str = None) -> str:
        inputs = {
            'product_name': 'Enterprise Solution',
            'campaign_goal': request,
            'target_market': 'Global'
        }
        return self._run_crew('sales_marketing_crew.sales_marketing_crew', 'SalesMarketingCrew', inputs)

class OperationsCrewTool(BaseCrewTool):
    name: str = "Operations Crew"
    description: str = "Delegate operations tasks. Useful for logistics, supply chain, and process optimization."

    def _run(self, request: str, context: str = None) -> str:
        inputs = {
            'operation_area': request,
            'problem_statement': request
        }
        return self._run_crew('operations_crew.operations_crew', 'OperationsCrew', inputs)

class FinanceCrewTool(BaseCrewTool):
    name: str = "Finance Crew"
    description: str = "Delegate financial tasks. Useful for budgeting, forecasting, and financial analysis."

    def _run(self, request: str, context: str = None) -> str:
        inputs = {
            'financial_goal': request,
            'budget_constraints': 'Standard enterprise budget'
        }
        return self._run_crew('finance_crew.finance_crew', 'FinanceCrew', inputs)

class HRCrewTool(BaseCrewTool):
    name: str = "HR Crew"
    description: str = "Delegate HR tasks. Useful for recruitment, employee relations, and policy."

    def _run(self, request: str, context: str = None) -> str:
        try:
            # Import the specific run function for HR Crew
            from hr_crew.hr_crew import run_hr_query
            return run_hr_query(request)
        except ImportError as e:
            return f"Error importing HR Crew: {str(e)}"
        except Exception as e:
            return f"Error running HR Crew: {str(e)}"
