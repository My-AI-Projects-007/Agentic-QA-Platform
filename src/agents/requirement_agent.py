"""Requirement Agent - Parses requirements and generates test cases"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.models.schemas import TestCaseSchema, AgentState
from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class RequirementAgent:
    """Agent for processing requirements and generating test cases"""
    
    def __init__(self, model_name: str = None, temperature: float = None):
        """Initialize the Requirement Agent"""
        self.model_name = model_name or settings.MODEL_NAME
        self.temperature = temperature if temperature is not None else settings.TEMPERATURE
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY,
        )
        
        # Output parser
        self.parser = JsonOutputParser(pydantic_object=TestCaseSchema)
        
        logger.info(
            f"RequirementAgent initialized with model: {self.model_name}, "
            f"temperature: {self.temperature}"
        )
    
    def generate_test_cases(self, requirement_content: str) -> List[TestCaseSchema]:
        """
        Generate test cases from requirement content
        
        Args:
            requirement_content: The requirement text to parse
            
        Returns:
            List of generated test cases
        """
        logger.info("Starting test case generation from requirement")
        
        prompt = PromptTemplate(
            template=self._get_test_generation_prompt(),
            input_variables=["requirement"],
            output_parser=self.parser,
        )
        
        # Create chain
        chain = prompt | self.llm | self.parser
        
        try:
            # Generate test cases
            result = chain.invoke({"requirement": requirement_content})
            
            # Ensure result is a list
            if isinstance(result, TestCaseSchema):
                test_cases = [result]
            elif isinstance(result, list):
                test_cases = result
            else:
                test_cases = []
            
            logger.info(f"Generated {len(test_cases)} test cases")
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}", exc_info=True)
            return []
    
    def parse_requirement_metadata(self, requirement_content: str) -> Dict[str, Any]:
        """
        Extract metadata (title, scope, etc.) from requirement
        
        Args:
            requirement_content: The requirement text
            
        Returns:
            Dictionary with metadata
        """
        logger.info("Parsing requirement metadata")
        
        prompt = PromptTemplate(
            template=self._get_metadata_extraction_prompt(),
            input_variables=["requirement"],
        )
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"requirement": requirement_content})
            logger.info("Successfully extracted metadata")
            return {"metadata": response}
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}", exc_info=True)
            return {}
    
    @staticmethod
    def _get_test_generation_prompt() -> str:
        """Get the prompt template for test case generation"""
        return """You are an expert QA engineer. Your task is to generate comprehensive test cases from a software requirement.

Requirement:
{requirement}

Generate test cases in JSON format. Each test case must have:
- test_id: A unique identifier (e.g., TC001, TC002)
- title: Short descriptive title
- description: Detailed description
- preconditions: List of items that must be true before test execution
- steps: Array of steps with step_number, action, and expected_result
- expected_result: Overall expected outcome
- priority: One of low, medium, high, critical

Return an array of test cases. Ensure the JSON is valid and parseable.

Format your response as a valid JSON array of test case objects:
[
  {{
    "test_id": "TC001",
    "title": "...",
    "description": "...",
    "preconditions": [...]
    "steps": [...]
    "expected_result": "...",
    "priority": "medium"
  }}
]

Generate test cases now:"""
    
    @staticmethod
    def _get_metadata_extraction_prompt() -> str:
        """Get the prompt template for metadata extraction"""
        return """Extract metadata from the following requirement:

{requirement}

Provide:
1. Title: Main title/name of the feature
2. Scope: What is covered
3. Type: Functional, Non-Functional, UI, API, etc.
4. Related components: What parts of the system are affected

Be concise and structured."""


class RequirementAnalyzer:
    """Analyzer for requirement documents"""
    
    @staticmethod
    def extract_scenarios(requirement_content: str) -> List[str]:
        """Extract user scenarios from requirement"""
        # Simple pattern matching - can be enhanced with ML
        scenarios = []
        lines = requirement_content.split('\n')
        
        for line in lines:
            if 'scenario' in line.lower() or 'user' in line.lower():
                scenarios.append(line.strip())
        
        return scenarios
    
    @staticmethod
    def extract_acceptance_criteria(requirement_content: str) -> List[str]:
        """Extract acceptance criteria from requirement"""
        criteria = []
        lines = requirement_content.split('\n')
        
        in_criteria = False
        for line in lines:
            if 'acceptance' in line.lower() or 'criteria' in line.lower():
                in_criteria = True
                continue
            
            if in_criteria and line.strip().startswith('-'):
                criteria.append(line.strip())
        
        return criteria
