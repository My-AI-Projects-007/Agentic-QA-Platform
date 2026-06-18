"""Test suite for QA Workflow"""
import pytest
from src.workflows.qa_workflow import QAWorkflow
from src.models.schemas import AgentState


@pytest.fixture
def workflow():
    """Create a QAWorkflow instance"""
    return QAWorkflow()


@pytest.fixture
def sample_requirement_text():
    """Sample requirement text for testing"""
    return """
    Login Feature
    
    Users should be able to log in with email and password.
    The system should validate the email format.
    Password must be at least 8 characters.
    """


def test_workflow_initialization(workflow):
    """Test workflow initialization"""
    assert workflow is not None
    assert workflow.requirement_agent is not None
    assert workflow.analyzer is not None


def test_validate_test_case():
    """Test test case validation"""
    from src.models.schemas import TestCaseSchema, TestStep
    
    # Valid test case
    valid_case = TestCaseSchema(
        test_id="TC001",
        title="Valid Test",
        description="Description",
        steps=[TestStep(step_number=1, action="Action", expected_result="Result")],
        expected_result="Result"
    )
    
    assert QAWorkflow._validate_test_case(valid_case) is True
    
    # Invalid test case (no test_id)
    invalid_case = TestCaseSchema(
        test_id="",
        title="Invalid Test",
        description="Description",
        steps=[TestStep(step_number=1, action="Action", expected_result="Result")],
        expected_result="Result"
    )
    
    assert QAWorkflow._validate_test_case(invalid_case) is False


def test_initial_state_creation():
    """Test AgentState initialization"""
    state = AgentState(
        requirement_content="Test requirement",
        filename="test.md"
    )
    
    assert state.requirement_content == "Test requirement"
    assert state.filename == "test.md"
    assert len(state.test_cases) == 0
    assert len(state.errors) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
