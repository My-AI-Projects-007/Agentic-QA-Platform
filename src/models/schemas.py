"""Pydantic models and schemas for API and data validation"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TestStep(BaseModel):
    """Single step in a test case"""
    step_number: int
    action: str
    expected_result: str


class PreconditionItem(BaseModel):
    """Precondition for test case"""
    item: str


class TestCaseSchema(BaseModel):
    """Schema for generated test case"""
    test_id: str = Field(..., description="Unique test case ID")
    title: str = Field(..., description="Test case title")
    description: str = Field(..., description="Detailed description")
    preconditions: List[PreconditionItem] = Field(default_factory=list)
    steps: List[TestStep] = Field(..., description="List of test steps")
    expected_result: str = Field(..., description="Expected result")
    priority: str = Field(default="medium", description="Priority: low, medium, high, critical")


class RequirementSchema(BaseModel):
    """Schema for parsed requirement"""
    filename: str
    title: str
    content: str
    test_cases: List[TestCaseSchema]


class TestCaseResponse(BaseModel):
    """Response model for test case"""
    id: int
    requirement_id: int
    test_id: str
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


class TestExecutionLog(BaseModel):
    """Log entry for test execution"""
    test_case_id: int
    executed_at: datetime
    status: str
    duration_seconds: int
    error_message: Optional[str] = None


class AgentState(BaseModel):
    """State for LangGraph agent workflow"""
    requirement_content: str
    filename: str
    test_cases: List[TestCaseSchema] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    messages: List[Dict[str, Any]] = Field(default_factory=list)


class WorkflowConfig(BaseModel):
    """Configuration for workflow"""
    max_iterations: int = 10
    timeout_seconds: int = 300
    model_name: str = "gpt-4"
    temperature: float = 0.7
