"""
Utility functions for the QA Platform
"""
from datetime import datetime
import json
from typing import Dict, Any, List


def format_test_case_for_report(test_case: Dict[str, Any]) -> str:
    """Format test case for reporting"""
    lines = [
        f"Test ID: {test_case.get('test_id')}",
        f"Title: {test_case.get('title')}",
        f"Description: {test_case.get('description')}",
        f"Priority: {test_case.get('priority')}",
        f"Status: {test_case.get('status')}",
    ]
    
    if test_case.get('preconditions'):
        lines.append("Preconditions:")
        for pc in test_case['preconditions']:
            lines.append(f"  - {pc.get('item')}")
    
    if test_case.get('steps'):
        lines.append("Steps:")
        for step in test_case['steps']:
            lines.append(f"  {step.get('step_number')}. {step.get('action')}")
            lines.append(f"     Expected: {step.get('expected_result')}")
    
    lines.append(f"Expected Result: {test_case.get('expected_result')}")
    
    return "\n".join(lines)


def generate_test_report(test_cases: List[Dict[str, Any]]) -> str:
    """Generate a comprehensive test report"""
    report_lines = [
        "="*70,
        "TEST CASE REPORT",
        "="*70,
        f"Generated: {datetime.now().isoformat()}",
        f"Total Test Cases: {len(test_cases)}",
        "",
    ]
    
    # Group by priority
    by_priority = {}
    for tc in test_cases:
        priority = tc.get('priority', 'medium')
        if priority not in by_priority:
            by_priority[priority] = []
        by_priority[priority].append(tc)
    
    # Summary by priority
    report_lines.append("SUMMARY BY PRIORITY:")
    for priority in ['critical', 'high', 'medium', 'low']:
        count = len(by_priority.get(priority, []))
        report_lines.append(f"  {priority.upper()}: {count}")
    
    report_lines.append("")
    report_lines.append("="*70)
    report_lines.append("TEST CASES")
    report_lines.append("="*70)
    report_lines.append("")
    
    # Detailed test cases
    for i, tc in enumerate(test_cases, 1):
        report_lines.append(f"[{i}]")
        report_lines.append(format_test_case_for_report(tc))
        report_lines.append("")
    
    return "\n".join(report_lines)


def save_report(report_content: str, filename: str = None) -> str:
    """Save report to file"""
    from pathlib import Path
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.txt"
    
    report_path = Path("reports") / filename
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    return str(report_path)


def parse_test_case_json(json_str: str) -> Dict[str, Any]:
    """Parse test case from JSON string"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")


def dict_to_json(data: Dict[str, Any]) -> str:
    """Convert dictionary to JSON string"""
    return json.dumps(data, indent=2, default=str)
