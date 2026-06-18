"""Test suite for database operations"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.config import Base
from src.database.models import Requirement, TestCase, TestCaseStatus
from src.database.services import RequirementService, TestCaseService
from src.models.schemas import TestCaseSchema, TestStep, PreconditionItem


@pytest.fixture
def test_db():
    """Create an in-memory test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    
    db = SessionLocal()
    yield db
    db.close()


def test_create_requirement(test_db):
    """Test creating a requirement"""
    requirement = RequirementService.create_requirement(
        test_db,
        filename="test_req.md",
        title="Test Requirement",
        content="Test content"
    )
    
    assert requirement.id is not None
    assert requirement.filename == "test_req.md"
    assert requirement.title == "Test Requirement"


def test_get_requirement(test_db):
    """Test retrieving a requirement"""
    # Create
    requirement = RequirementService.create_requirement(
        test_db,
        filename="test.md",
        title="Test",
        content="Content"
    )
    
    # Retrieve
    retrieved = RequirementService.get_requirement(test_db, requirement.id)
    assert retrieved.id == requirement.id


def test_create_test_case(test_db):
    """Test creating a test case"""
    # Create requirement first
    requirement = RequirementService.create_requirement(
        test_db,
        filename="req.md",
        title="Requirement",
        content="Content"
    )
    
    # Create test case
    test_case_schema = TestCaseSchema(
        test_id="TC001",
        title="Test Case",
        description="Description",
        steps=[
            TestStep(step_number=1, action="Action", expected_result="Result")
        ],
        expected_result="Final result",
        priority="high"
    )
    
    test_case = TestCaseService.create_test_case(
        test_db, requirement.id, test_case_schema
    )
    
    assert test_case.id is not None
    assert test_case.test_id == "TC001"
    assert test_case.requirement_id == requirement.id


def test_list_test_cases_by_requirement(test_db):
    """Test listing test cases for a requirement"""
    # Setup
    requirement = RequirementService.create_requirement(
        test_db, "req.md", "Req", "Content"
    )
    
    # Create multiple test cases
    for i in range(3):
        schema = TestCaseSchema(
            test_id=f"TC{i:03d}",
            title=f"Test Case {i}",
            description="Description",
            steps=[TestStep(step_number=1, action="Action", expected_result="Result")],
            expected_result="Result",
            priority="medium"
        )
        TestCaseService.create_test_case(test_db, requirement.id, schema)
    
    # List
    test_cases = TestCaseService.list_test_cases_by_requirement(test_db, requirement.id)
    assert len(test_cases) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
