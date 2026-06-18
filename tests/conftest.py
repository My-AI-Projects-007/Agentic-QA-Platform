"""
conftest.py - Pytest configuration and fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_env():
    """Setup test environment"""
    os.environ["ENV"] = "test"
    os.environ["DEBUG"] = "True"
    os.environ["OPENAI_API_KEY"] = "test-key"
    yield
    # Cleanup


@pytest.fixture
def sample_requirement():
    """Sample requirement text"""
    return """
    # User Login Feature
    
    ## Overview
    Users should be able to log in with email and password.
    
    ## Requirements
    1. Users can enter email and password
    2. System validates credentials
    3. User is redirected to dashboard on success
    4. Error message shown on failure
    """


@pytest.fixture
def sample_test_case():
    """Sample test case"""
    from src.models.schemas import TestCaseSchema, TestStep, PreconditionItem
    
    return TestCaseSchema(
        test_id="TC001",
        title="Valid User Login",
        description="Test successful login with correct credentials",
        preconditions=[
            PreconditionItem(item="User account exists"),
            PreconditionItem(item="User is not logged in"),
        ],
        steps=[
            TestStep(
                step_number=1,
                action="Navigate to login page",
                expected_result="Login form is displayed"
            ),
            TestStep(
                step_number=2,
                action="Enter valid email and password",
                expected_result="Credentials are entered"
            ),
            TestStep(
                step_number=3,
                action="Click login button",
                expected_result="Login request is submitted"
            ),
        ],
        expected_result="User is redirected to dashboard",
        priority="high"
    )


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
