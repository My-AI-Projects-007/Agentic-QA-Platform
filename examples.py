"""
Example script demonstrating platform usage
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import AgenticQAPlatform
from src.config.logging_config import get_logger

logger = get_logger(__name__)


def example_process_all_requirements():
    """Example: Process all requirements from folder"""
    logger.info("Starting example: Process all requirements")
    
    platform = AgenticQAPlatform()
    results = platform.process_all_requirements()
    
    print("\n" + "="*60)
    print("PROCESSING RESULTS")
    print("="*60)
    
    for result in results:
        print(f"\nFile: {result['filename']}")
        print(f"Status: {result['status']}")
        print(f"Test Cases Generated: {result.get('test_cases_generated', 0)}")
        if result.get('errors'):
            print(f"Errors: {result['errors']}")
    
    return platform


def example_process_single_requirement(platform):
    """Example: Process a single requirement"""
    logger.info("Starting example: Process single requirement")
    
    requirement_text = """
    # Product Search Feature
    
    ## Overview
    Users should be able to search for products by keywords.
    
    ## Functional Requirements
    1. Search field should accept text input
    2. Search should filter products by title and description
    3. Results should be paginated with 10 items per page
    4. Users should be able to sort results by price, name, or relevance
    5. No results page should suggest similar searches
    
    ## Acceptance Criteria
    - User can enter search term
    - Results display matching products
    - Pagination works correctly
    - Sorting options are available
    - Empty results handled gracefully
    """
    
    result = platform.process_single_requirement(
        "product_search.md",
        requirement_text
    )
    
    print("\n" + "="*60)
    print("SINGLE REQUIREMENT PROCESSING")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Test Cases Generated: {result.get('test_cases_generated', 0)}")
    
    if result.get('test_cases'):
        print(f"\nGenerated Test Cases:")
        for test_case in result['test_cases'][:3]:  # Show first 3
            print(f"  - {test_case.get('test_id')}: {test_case.get('title')}")


def example_list_test_cases(platform):
    """Example: List all generated test cases"""
    logger.info("Starting example: List test cases")
    
    test_cases = platform.list_generated_test_cases()
    
    print("\n" + "="*60)
    print("ALL GENERATED TEST CASES")
    print("="*60)
    print(f"Total Test Cases: {len(test_cases)}\n")
    
    if test_cases:
        for tc in test_cases[:10]:  # Show first 10
            print(f"ID: {tc['test_id']}")
            print(f"  Title: {tc['title']}")
            print(f"  Requirement: {tc['requirement_id']}")
            print(f"  Priority: {tc['priority']}")
            print(f"  Status: {tc['status']}")
            print()


def main():
    """Run examples"""
    print("\n" + "="*60)
    print("AGENTIC QA PLATFORM - USAGE EXAMPLES")
    print("="*60 + "\n")
    
    try:
        # Example 1: Process all requirements
        platform = example_process_all_requirements()
        
        # Example 2: Process single requirement
        example_process_single_requirement(platform)
        
        # Example 3: List test cases
        example_list_test_cases(platform)
        
        print("\n" + "="*60)
        print("EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error running examples: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
