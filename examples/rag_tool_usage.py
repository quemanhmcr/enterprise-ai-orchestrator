"""
Example: Using Internal Document RAG Tool with CrewAI

This script demonstrates how to use the InternalDocRAGTool in your crews.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import CrewAI components
from crewai import LLM, Agent, Crew, Task  # noqa: E402

from shared.tools.internal_doc_rag_tool import create_internal_doc_rag_tool  # noqa: E402


def example_basic_usage():
    """Example 1: Basic standalone usage of RAG tool."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Standalone RAG Tool Usage")
    print("="*80 + "\n")

    # Create RAG tool instance
    rag_tool = create_internal_doc_rag_tool()

    # Query the documents
    queries = [
        "How many vacation days do employees get?",
        "What is the work from home policy?",
        "What are the health insurance benefits?",
    ]

    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-" * 80)
        result = rag_tool._run(query=query)
        print(result)
        print()


def example_with_agent():
    """Example 2: Using RAG tool with a CrewAI agent."""
    print("\n" + "="*80)
    print("EXAMPLE 2: RAG Tool with CrewAI Agent")
    print("="*80 + "\n")

    # Create RAG tool
    rag_tool = create_internal_doc_rag_tool()

    # Configure LLM
    llm = LLM(
        model=os.getenv("MODEL", "glm-4.6"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0.3
    )

    # Create HR assistant agent with RAG tool
    hr_assistant = Agent(
        role="HR Policy Assistant",
        goal="Answer employee questions about company policies and benefits",
        backstory="""You are an experienced HR assistant with deep knowledge
        of company policies. You help employees understand their benefits,
        vacation policies, and workplace guidelines. Always provide accurate
        information from official company documents.""",
        tools=[rag_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # Create task
    policy_question_task = Task(
        description="""An employee asks: "I've been working here for 4 years.
        How many vacation days am I entitled to, and can I work from home?"

        Use the Internal Document RAG tool to find accurate information from
        company policies and provide a clear, helpful answer.""",
        expected_output="""A clear answer containing:
        1. Number of vacation days based on years of service
        2. Work from home eligibility and guidelines
        3. Any relevant additional information""",
        agent=hr_assistant
    )

    # Create and run crew
    crew = Crew(
        agents=[hr_assistant],
        tasks=[policy_question_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*80)
    print("RESULT:")
    print("="*80)
    print(result)


def example_with_multiple_agents():
    """Example 3: Multiple agents using RAG tool for different purposes."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Multiple Agents with RAG Tool")
    print("="*80 + "\n")

    # Create RAG tool (shared by multiple agents)
    rag_tool = create_internal_doc_rag_tool()

    # Configure LLM
    llm = LLM(
        model=os.getenv("MODEL", "glm-4.6"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0.3
    )

    # Create specialized agents
    hr_specialist = Agent(
        role="HR Benefits Specialist",
        goal="Provide accurate information about employee benefits and policies",
        backstory="Expert in HR policies with 10+ years experience",
        tools=[rag_tool],
        llm=llm,
        verbose=True
    )

    finance_specialist = Agent(
        role="Finance Policy Specialist",
        goal="Explain financial policies and procedures to employees",
        backstory="Certified financial professional specializing in corporate policies",
        tools=[rag_tool],
        llm=llm,
        verbose=True
    )

    policy_writer = Agent(
        role="Policy Documentation Writer",
        goal="Create clear summaries of company policies",
        backstory="Professional technical writer with expertise in policy documentation",
        tools=[rag_tool],
        llm=llm,
        verbose=True
    )

    # Create tasks
    benefits_task = Task(
        description="Research and summarize all employee health insurance benefits",
        expected_output="Comprehensive summary of health insurance coverage and benefits",
        agent=hr_specialist
    )

    retirement_task = Task(
        description="Explain the company's retirement plan and 401(k) matching policy",
        expected_output="Clear explanation of retirement benefits with specific numbers",
        agent=finance_specialist
    )

    summary_task = Task(
        description="""Create a new employee welcome guide summarizing:
        1. Vacation policy highlights
        2. Health benefits overview
        3. Retirement plan basics
        Use information from the other specialists.""",
        expected_output="Concise welcome guide for new employees (200-300 words)",
        agent=policy_writer,
        context=[benefits_task, retirement_task]
    )

    # Create and run crew
    crew = Crew(
        agents=[hr_specialist, finance_specialist, policy_writer],
        tasks=[benefits_task, retirement_task, summary_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*80)
    print("FINAL RESULT - New Employee Welcome Guide:")
    print("="*80)
    print(result)


def example_add_custom_documents():
    """Example 4: Adding custom documents to the RAG index."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Adding Custom Documents")
    print("="*80 + "\n")

    # Create RAG tool
    rag_tool = create_internal_doc_rag_tool()

    # Example: Create a custom document
    custom_doc_path = Path("shared/documents/temp_policy.md")
    custom_doc_path.parent.mkdir(parents=True, exist_ok=True)

    custom_content = """
# Emergency Contact Policy

## Emergency Contacts

All employees must maintain updated emergency contact information:
- Primary emergency contact (name, relationship, phone)
- Secondary emergency contact
- Medical information (allergies, conditions)

## Update Frequency

- Review and update every 6 months
- Update immediately after any changes
- Available in employee self-service portal

## Contact: safety@company.com
"""

    with open(custom_doc_path, 'w') as f:
        f.write(custom_content)

    print(f"✓ Created custom document: {custom_doc_path}")

    # Add to index
    result = rag_tool.add_documents([str(custom_doc_path)])
    print(f"✓ {result}")

    # Query the new document
    query = "What is the emergency contact policy?"
    print(f"\n📝 Query: {query}")
    print("-" * 80)
    answer = rag_tool._run(query=query)
    print(answer)

    # Cleanup
    custom_doc_path.unlink()
    print("\n✓ Cleaned up temporary document")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "INTERNAL DOCUMENT RAG TOOL EXAMPLES" + " "*23 + "║")
    print("╚" + "="*78 + "╝")

    # Check if documents exist
    docs_dir = Path("shared/documents")
    sample_doc = docs_dir / "sample_company_policy.md"

    if not sample_doc.exists():
        print("\n⚠️  Sample document not found. Creating it now...")
        # The document should already exist from the setup

    # Run examples (comment out the ones you don't want to run)

    # Example 1: Basic usage
    example_basic_usage()

    # Example 2: With single agent
    # example_with_agent()

    # Example 3: With multiple agents
    # example_with_multiple_agents()

    # Example 4: Adding custom documents
    # example_add_custom_documents()

    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
