"""
Enterprise Business System - Main Entry Point
Run the complete multi-crew orchestration system
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add crews directory to path
crews_path = Path(__file__).parent / 'crews'
sys.path.insert(0, str(crews_path))

from ceo_crew.ceo_crew import CEOOrchestrationFlow, run_ceo_orchestration


def print_banner():
    """Print welcome banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                   ENTERPRISE BUSINESS SYSTEM                                 ║
║                   Multi-Crew AI Orchestration                                ║
║                                                                              ║
║  Powered by CrewAI with Advanced Features:                                  ║
║  ✓ Memory System (4-tier)                                                   ║
║  ✓ Knowledge Sources (RAG)                                                  ║
║  ✓ Flows (Event-driven orchestration)                                       ║
║  ✓ Reasoning & Code Execution                                               ║
║  ✓ Hierarchical & Async Processes                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def print_system_architecture():
    """Print system architecture."""
    print("""
SYSTEM ARCHITECTURE:

┌─────────────────────────────────────────────────────────────────────────┐
│                         CEO ORCHESTRATION FLOW                          │
│                    (Hierarchical Process + Flow)                        │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │  Strategic Planning     │
                    │  (CEO Crew)             │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Market        │       │ Product       │       │ Sales &       │
│ Research      │       │ Development   │       │ Marketing     │
│ (Sequential)  │       │ (Sequential)  │       │ (Sequential)  │
└───────────────┘       └───────────────┘       └───────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
            ┌───────────────┐       ┌───────────────┐
            │ Operations    │       │ Finance       │
            │ (Sequential)  │       │ (Sequential)  │
            └───────────────┘       └───────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Results Synthesis       │
                    │ Executive Summary       │
                    └─────────────────────────┘

CREWS:
  1. CEO Crew (Hierarchical)
     - CEO (Reasoning enabled)
     - Chief Strategy Officer
     - Executive Assistant
     - Business Intelligence Analyst (Code execution)

  2. Market Research Crew (Sequential + Async tasks)
     - Market Research Lead
     - Competitive Analyst
     - Consumer Insights Specialist
     - Data Scientist

  3. Product Development Crew (Sequential + Async tasks)
     - Product Manager
     - UX Designer (Multimodal)
     - Engineering Lead (Code execution)
     - QA Specialist (Code execution)

  4. Sales & Marketing Crew (Sequential + Async tasks)
     - Sales Director
     - Marketing Strategist
     - Content Creator (Multimodal)
     - Customer Success Manager

  5. Operations Crew (Sequential + Async tasks)
     - Operations Manager
     - Supply Chain Analyst
     - Process Engineer (Code execution)
     - Quality Controller

  6. Finance Crew (Sequential + Async tasks)
     - CFO
     - Financial Analyst (Code execution)
     - Budget Controller
     - Compliance Officer

FEATURES:
  ✓ 4-Tier Memory System (Short-term, Long-term, Entity, Contextual)
  ✓ Knowledge Sources with RAG (PDF, CSV, JSON, Text)
  ✓ Guardrails for output quality validation
  ✓ Async execution for parallel processing
  ✓ Code execution in sandboxed environment
  ✓ Reasoning capabilities for complex decisions
  ✓ Flow-based orchestration with state management
    """)


async def run_full_orchestration(custom_input: str = None):
    """Run the complete enterprise business orchestration."""
    
    print_banner()
    print_system_architecture()
    
    print("\n" + "="*80)
    print("STARTING ENTERPRISE ORCHESTRATION")
    print("="*80 + "\n")
    
    if custom_input:
        print(f"Using custom input: {custom_input}")
        result = run_ceo_orchestration(request=custom_input)
        
        print("\n" + "="*80)
        print("ORCHESTRATION COMPLETE")
        print("="*80)
        print("\nFinal Result:")
        print(result)
        return result
    
    # Get user inputs
    print("Enter orchestration parameters (or press Enter for defaults):\n")
    
    quarter = input("Quarter [Q4 2025]: ").strip() or "Q4 2025"
    
    print("\nStrategic Goals (one per line, empty line to finish):")
    print("Default goals:")
    print("  1. Increase market share by 15%")
    print("  2. Launch 2 new AI products")
    print("  3. Improve operational efficiency by 20%")
    print("  4. Expand into APAC market")
    print("\nEnter custom goals (or just press Enter to use defaults):")
    
    custom_goals = []
    while True:
        goal = input(f"  Goal {len(custom_goals) + 1}: ").strip()
        if not goal:
            break
        custom_goals.append(goal)
    
    strategic_goals = custom_goals if custom_goals else [
        "Increase market share by 15%",
        "Launch 2 new AI products",
        "Improve operational efficiency by 20%",
        "Expand into APAC market"
    ]
    
    budget_input = input("\nBudget [$10,000,000]: ").strip()
    budget = float(budget_input.replace(',', '').replace('$', '')) if budget_input else 10000000.0
    
    print("\n" + "="*80)
    print("ORCHESTRATION CONFIGURATION")
    print("="*80)
    print(f"Quarter: {quarter}")
    print(f"Budget: ${budget:,.2f}")
    print(f"Strategic Goals ({len(strategic_goals)}):")
    for i, goal in enumerate(strategic_goals, 1):
        print(f"  {i}. {goal}")
    print("="*80 + "\n")
    
    confirm = input("Start orchestration? [Y/n]: ").strip().lower()
    if confirm and confirm != 'y':
        print("Orchestration cancelled.")
        return
    
    # Construct request from inputs
    request = f"""
    Develop a comprehensive business strategy for {quarter}.
    Budget: ${budget:,.2f}
    
    Strategic Goals:
    {chr(10).join(f'- {g}' for g in strategic_goals)}
    """
    
    # Run orchestration
    result = run_ceo_orchestration(request=request)
    
    print("\n" + "="*80)
    print("ORCHESTRATION COMPLETE")
    print("="*80)
    print("\nFinal Result:")
    print(result)
    
    return result


async def run_individual_crew(crew_name: str, custom_input: str = None):
    """Run a single crew for testing."""
    
    print_banner()
    
    print(f"\n{'='*80}")
    print(f"RUNNING {crew_name.upper()} CREW")
    print(f"{'='*80}\n")
    
    if crew_name == "ceo":
        from ceo_crew.ceo_crew import CeoCrew
        
        inputs = {
            'request': custom_input or 'Develop a strategy for Q1 2026 focusing on AI adoption.'
        }
        
        crew = CeoCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    elif crew_name == "market_research":
        from market_research_crew.market_research_crew import MarketResearchCrew
        import datetime
        
        inputs = {
            'market_segment': custom_input or 'Enterprise AI Solutions',
            'time_period': 'Q4 2025',
            'current_date': datetime.datetime.now().strftime('%B %d, %Y'),
            'geographic_scope': 'Global',
            'competitors': 'Top 5 AI/ML companies',
            'target_demographics': 'Enterprise Decision Makers',
            'forecast_horizon': '12 months'
        }
        
        crew = MarketResearchCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    elif crew_name == "product_development":
        from product_development_crew.product_development_crew import ProductDevelopmentCrew
        
        inputs = {
            'quarter': 'Q4 2025',
            'strategic_goals': custom_input or 'Launch 2 new AI products, Improve UX'
        }
        
        crew = ProductDevelopmentCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    elif crew_name == "sales_marketing":
        from sales_marketing_crew.sales_marketing_crew import SalesMarketingCrew
        
        inputs = {
            'quarter': 'Q4 2025',
            'revenue_target': 3000000,
            'campaign_goal': custom_input or 'Boost brand awareness'
        }
        
        crew = SalesMarketingCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    elif crew_name == "operations":
        from operations_crew.operations_crew import OperationsCrew
        
        inputs = {
            'quarter': 'Q4 2025',
            'focus_area': custom_input or 'Supply Chain Optimization'
        }
        
        crew = OperationsCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    elif crew_name == "finance":
        from finance_crew.finance_crew import FinanceCrew
        
        inputs = {
            'quarter': 'Q4 2025',
            'revenue_target': 3000000,
            'ebitda_margin': 25,
            'fcf_target': 1500000,
            'focus_area': custom_input or 'Cost reduction'
        }
        
        crew = FinanceCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
    else:
        print(f"Unknown crew: {crew_name}")
        return
    
    print("\n" + "="*80)
    print(f"{crew_name.upper()} CREW COMPLETED")
    print("="*80)
    print(result)
    
    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Enterprise Business System - Multi-Crew AI Orchestration")
    
    # Create mutually exclusive group for commands
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--orchestrate", action="store_true", help="Run the full CEO orchestration flow")
    group.add_argument("--crew", type=str, help="Run a single crew (ceo, market_research, product_development, sales_marketing, operations, finance)")
    
    # Add input argument
    parser.add_argument("--input", type=str, help="Custom input/goal/request for the crew or orchestration")
    
    args = parser.parse_args()
    
    if args.crew:
        crew_name = args.crew.lower()
        asyncio.run(run_individual_crew(crew_name, args.input))
    elif args.orchestrate:
        # For now, run_full_orchestration doesn't take arguments but prompts user. 
        # We can modify it later to accept args.input if needed, but for now let's keep the interactive mode
        # or pass it if we modify run_full_orchestration.
        # Let's modify run_full_orchestration to take an optional input to skip prompts if provided.
        asyncio.run(run_full_orchestration(args.input))
    else:
        # Default behavior if no args provided
        asyncio.run(run_full_orchestration())


if __name__ == "__main__":
    main()
