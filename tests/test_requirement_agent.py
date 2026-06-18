"""Test suite for Requirement Agent"""
import pytest
from src.agents.requirement_agent import RequirementAgent, RequirementAnalyzer
from src.models.schemas import TestCaseSchema


@pytest.fixture
def agent():
    """Create a RequirementAgent instance"""
    return RequirementAgent(model_name="gpt-4", temperature=0.7)


@pytest.fixture
def sample_requirement():
    """Sample requirement for testing"""
    return """
    User Login Feature
    
    ## Requirement
    Users should be able to log in with email and password.
    The login form should validate email format.
    
    ## Scenarios
    - User logs in with correct credentials
    - User logs in with incorrect password
    - User logs in with non-existent email
    
    ## Acceptance Criteria
    - User can log in with valid credentials
    - Error message displayed for invalid credentials
    - Session is created after successful login
    """


def test_requirement_agent_initialization(agent):
    """Test agent initialization"""
    assert agent is not None
    assert agent.model_name == "gpt-4"
    assert agent.temperature == 0.7


def test_requirement_analyzer_extract_scenarios(sample_requirement):
    """Test scenario extraction"""
    analyzer = RequirementAnalyzer()
    scenarios = analyzer.extract_scenarios(sample_requirement)
    assert len(scenarios) > 0


def test_requirement_analyzer_extract_criteria(sample_requirement):
    """Test acceptance criteria extraction"""
    analyzer = RequirementAnalyzer()
    criteria = analyzer.extract_acceptance_criteria(sample_requirement)
    assert len(criteria) > 0


def test_test_case_schema_validation():
    """Test TestCaseSchema validation"""
    from src.models.schemas import TestStep, PreconditionItem
    
    test_case = TestCaseSchema(
        test_id="TC001",
        title="Valid Test Case",
        description="Test description",
        steps=[
            TestStep(step_number=1, action="Click login", expected_result="Login page displayed"),
            TestStep(step_number=2, action="Enter credentials", expected_result="Credentials entered"),
        ],
        expected_result="User logged in successfully",
        priority="high"
    )
    
    assert test_case.test_id == "TC001"
    assert len(test_case.steps) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
