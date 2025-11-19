"""
Custom Guardrails for Task Validation
Reusable validation functions for all crews
"""

from typing import Tuple, Any
from crewai import TaskOutput
import re


def validate_word_count(min_words: int = 100, max_words: int = 5000):
    """Validate output word count."""
    def validator(result: TaskOutput) -> Tuple[bool, Any]:
        word_count = len(result.raw.split())
        
        if word_count < min_words:
            return (False, f"Content too short: {word_count} words. Minimum required: {min_words}")
        
        if word_count > max_words:
            return (False, f"Content too long: {word_count} words. Maximum allowed: {max_words}")
        
        return (True, result.raw)
    
    return validator


def validate_contains_sections(*required_sections: str):
    """Validate that output contains required sections."""
    def validator(result: TaskOutput) -> Tuple[bool, Any]:
        content = result.raw.lower()
        missing_sections = []
        
        for section in required_sections:
            # Check for section headers (markdown or plain text)
            section_pattern = f"(#{{{1,6}}}\\s*{section}|{section}\\s*:)"
            if not re.search(section_pattern, content, re.IGNORECASE):
                missing_sections.append(section)
        
        if missing_sections:
            return (False, f"Missing required sections: {', '.join(missing_sections)}")
        
        return (True, result.raw)
    
    return validator


def validate_has_data_sources(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate that output includes data sources or citations."""
    content = result.raw.lower()
    
    # Check for common citation patterns
    patterns = [
        r'\[.*?\]',  # Markdown links
        r'source:',  # Explicit source mentions
        r'according to',  # Attribution
        r'reference:',  # References
        r'http[s]?://',  # URLs
    ]
    
    has_sources = any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
    
    if not has_sources:
        return (False, "Output must include data sources, citations, or references")
    
    return (True, result.raw)


def validate_has_metrics(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate that output includes quantitative metrics."""
    content = result.raw
    
    # Check for numbers, percentages, or currency
    patterns = [
        r'\d+\.?\d*%',  # Percentages
        r'\$\d+',  # Currency
        r'\d{1,3}(,\d{3})*(\.\d+)?',  # Numbers with formatting
    ]
    
    has_metrics = any(re.search(pattern, content) for pattern in patterns)
    
    if not has_metrics:
        return (False, "Output must include quantitative metrics (numbers, percentages, or financial figures)")
    
    return (True, result.raw)


def validate_executive_summary_length(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate executive summary is concise (100-300 words)."""
    # Extract executive summary section
    content = result.raw.lower()
    
    # Try to find executive summary section
    summary_match = re.search(
        r'(?:#{1,6}\s*)?executive summary.*?(?=\n#{1,6}\s|\Z)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    
    if not summary_match:
        return (False, "Must include an 'Executive Summary' section")
    
    summary_text = summary_match.group(0)
    word_count = len(summary_text.split())
    
    if word_count < 100:
        return (False, f"Executive summary too short: {word_count} words. Minimum 100 words.")
    
    if word_count > 300:
        return (False, f"Executive summary too long: {word_count} words. Maximum 300 words.")
    
    return (True, result.raw)


def validate_json_format(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate output is valid JSON."""
    import json
    
    try:
        json.loads(result.raw)
        return (True, result.raw)
    except json.JSONDecodeError as e:
        return (False, f"Invalid JSON format: {str(e)}")


def validate_budget_compliance(max_budget: float):
    """Validate that financial figures don't exceed budget."""
    def validator(result: TaskOutput) -> Tuple[bool, Any]:
        content = result.raw
        
        # Extract all currency values
        currency_pattern = r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        amounts = [float(m.replace(',', '')) for m in re.findall(currency_pattern, content)]
        
        if not amounts:
            return (False, "Must include budget/cost estimates with dollar amounts")
        
        total = sum(amounts)
        
        if total > max_budget:
            return (False, f"Total budget ${total:,.2f} exceeds maximum allowed ${max_budget:,.2f}")
        
        return (True, result.raw)
    
    return validator


def validate_timeline_present(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate that output includes timeline or deadlines."""
    content = result.raw.lower()
    
    # Check for time-related keywords
    time_patterns = [
        r'q[1-4]\s+\d{4}',  # Q1 2025
        r'(january|february|march|april|may|june|july|august|september|october|november|december)',
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # Date formats
        r'(week|month|quarter|year)s?\s+\d+',
        r'timeline:',
        r'deadline:',
        r'by\s+\w+\s+\d+',
    ]
    
    has_timeline = any(re.search(pattern, content, re.IGNORECASE) for pattern in time_patterns)
    
    if not has_timeline:
        return (False, "Output must include timeline, deadlines, or time-based milestones")
    
    return (True, result.raw)


def validate_risk_assessment(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate that output includes risk assessment."""
    content = result.raw.lower()
    
    risk_keywords = [
        'risk',
        'threat',
        'challenge',
        'concern',
        'mitigation',
        'contingency'
    ]
    
    risk_mentions = sum(1 for keyword in risk_keywords if keyword in content)
    
    if risk_mentions < 2:
        return (False, "Output must include risk assessment with mitigation strategies")
    
    return (True, result.raw)


# Commonly used guardrail combinations
STANDARD_REPORT_GUARDRAILS = [
    validate_word_count(500, 3000),
    validate_has_data_sources,
    validate_has_metrics
]

EXECUTIVE_BRIEF_GUARDRAILS = [
    validate_executive_summary_length,
    validate_has_metrics,
    validate_timeline_present
]

STRATEGIC_PLAN_GUARDRAILS = [
    validate_word_count(1000, 5000),
    validate_contains_sections('executive summary', 'objectives', 'timeline'),
    validate_has_metrics,
    validate_timeline_present,
    validate_risk_assessment
]

FINANCIAL_REPORT_GUARDRAILS = [
    validate_has_metrics,
    validate_has_data_sources,
    validate_timeline_present
]
