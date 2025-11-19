"""
HR Crew - Human Resources Assistant
Sử dụng RAG tool để trả lời câu hỏi về company policies
"""

import os

from crewai import LLM, Agent, Crew, Task
from dotenv import load_dotenv

from shared.tools.internal_doc_rag_tool import create_internal_doc_rag_tool

# Load environment
load_dotenv()


def create_hr_crew():
    """Tạo HR Crew với RAG tool."""

    # Tạo RAG tool
    rag_tool = create_internal_doc_rag_tool()

    # Configure LLM cho agents
    llm = LLM(
        model=os.getenv("MODEL", "glm-4.6"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0.3,
        stream=True  # Enable streaming
    )

    # HR Policy Expert Agent
    hr_expert = Agent(
        role="HR Policy Expert",
        goal="Answer employee questions about company policies, benefits, and procedures",
        backstory="""You are an experienced HR professional with deep knowledge
        of company policies. You use the Internal Document RAG tool to search
        through official company documents and provide accurate, helpful answers
        to employee questions. You always cite specific policies when answering.""",
        tools=[rag_tool],  # Sử dụng RAG tool
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # Employee Relations Specialist
    relations_specialist = Agent(
        role="Employee Relations Specialist",
        goal="Ensure employees understand their rights and benefits clearly",
        backstory="""You specialize in explaining complex HR policies in simple terms.
        You work with the HR Policy Expert to help employees understand their benefits,
        leave policies, and workplace guidelines. You make sure information is
        communicated clearly and compassionately.""",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    return hr_expert, relations_specialist, rag_tool


def run_hr_query(question: str):
    """Chạy HR crew để trả lời câu hỏi employee."""

    print("\n" + "="*80)
    print("HR CREW - Employee Question Answering")
    print("="*80)
    print(f"\n📋 Employee Question: {question}\n")

    # Tạo crew
    hr_expert, relations_specialist, rag_tool = create_hr_crew()

    # Task 1: Research policy
    research_task = Task(
        description=f"""An employee asks: "{question}"

        Use the Internal Document RAG tool to search company policies and find
        accurate information to answer this question. Be specific and cite the
        relevant policies.""",
        expected_output="""A detailed answer including:
        1. Direct answer to the question
        2. Specific policy details (numbers, dates, conditions)
        3. Any relevant additional information
        4. Citations from company documents""",
        agent=hr_expert
    )

    # Task 2: Format response
    format_task = Task(
        description="""Take the policy information found by the HR Policy Expert
        and format it into a clear, friendly response for the employee.

        Make sure the answer is:
        - Easy to understand
        - Well-structured
        - Includes all important details
        - Professional but friendly in tone""",
        expected_output="""A well-formatted employee response with:
        - Clear sections
        - Bullet points for key information
        - Friendly, professional tone
        - Next steps if applicable""",
        agent=relations_specialist,
        context=[research_task]
    )

    # Create and run crew
    crew = Crew(
        agents=[hr_expert, relations_specialist],
        tasks=[research_task, format_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*80)
    print("📄 FINAL HR RESPONSE:")
    print("="*80)
    print(result)
    print("\n")

    return result


if __name__ == "__main__":
    # Test với nhiều câu hỏi
    test_questions = [
        "I've been working here for 4 years. How many vacation days do I get and can I work from home?",
        "What health insurance benefits does the company provide?",
        "Can I carry over my unused vacation days to next year?",
        "What is the 401k matching policy?",
    ]

    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "HR CREW WITH RAG TOOL - DEMO" + " "*29 + "║")
    print("╚" + "="*78 + "╝")

    for i, question in enumerate(test_questions, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST {i}/{len(test_questions)}")
        print(f"{'='*80}")

        result = run_hr_query(question)

        if i < len(test_questions):
            input("\n⏸️  Press Enter to continue to next question...")
