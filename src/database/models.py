"""Database models for QA Platform"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from src.database.config import Base
import enum


class TestCaseStatus(str, enum.Enum):
    """Status of a test case"""
    DRAFT = "draft"
    READY = "ready"
    EXECUTED = "executed"
    PASSED = "passed"
    FAILED = "failed"


class Requirement(Base):
    """Requirement model"""
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    test_cases = relationship("TestCase", back_populates="requirement")

    def __repr__(self):
        return f"<Requirement(id={self.id}, filename={self.filename}, title={self.title})>"


class TestCase(Base):
    """Test case model"""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, index=True)
    test_id = Column(String(50), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    preconditions = Column(Text)  # JSON string
    steps = Column(Text)  # JSON string
    expected_result = Column(Text)
    status = Column(Enum(TestCaseStatus), default=TestCaseStatus.DRAFT)
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    requirement = relationship("Requirement", back_populates="test_cases")

    def __repr__(self):
        return f"<TestCase(id={self.id}, test_id={self.test_id}, title={self.title})>"


class TestExecution(Base):
    """Test execution log model"""
    __tablename__ = "test_executions"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, index=True)
    executed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))  # passed, failed, skipped
    duration_seconds = Column(Integer)
    error_message = Column(Text, nullable=True)
    logs = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TestExecution(id={self.id}, test_case_id={self.test_case_id}, status={self.status})>"
