"""Database service layer for test case and requirement management"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Requirement, TestCase, TestCaseStatus, TestExecution
from src.models.schemas import TestCaseSchema
import json
from datetime import datetime


class RequirementService:
    """Service for requirement operations"""
    
    @staticmethod
    def create_requirement(
        db: Session, filename: str, title: str, content: str
    ) -> Requirement:
        """Create a new requirement"""
        requirement = Requirement(filename=filename, title=title, content=content)
        db.add(requirement)
        db.commit()
        db.refresh(requirement)
        return requirement
    
    @staticmethod
    def get_requirement(db: Session, requirement_id: int) -> Optional[Requirement]:
        """Get requirement by ID"""
        return db.query(Requirement).filter(Requirement.id == requirement_id).first()
    
    @staticmethod
    def get_requirement_by_filename(db: Session, filename: str) -> Optional[Requirement]:
        """Get requirement by filename"""
        return db.query(Requirement).filter(Requirement.filename == filename).first()
    
    @staticmethod
    def list_requirements(db: Session) -> List[Requirement]:
        """List all requirements"""
        return db.query(Requirement).all()


class TestCaseService:
    """Service for test case operations"""
    
    @staticmethod
    def create_test_case(
        db: Session,
        requirement_id: int,
        test_case_schema: TestCaseSchema,
    ) -> TestCase:
        """Create a new test case from schema"""
        test_case = TestCase(
            requirement_id=requirement_id,
            test_id=test_case_schema.test_id,
            title=test_case_schema.title,
            description=test_case_schema.description,
            preconditions=json.dumps(
                [pc.dict() for pc in test_case_schema.preconditions]
            ),
            steps=json.dumps([step.dict() for step in test_case_schema.steps]),
            expected_result=test_case_schema.expected_result,
            priority=test_case_schema.priority,
            status=TestCaseStatus.DRAFT,
        )
        db.add(test_case)
        db.commit()
        db.refresh(test_case)
        return test_case
    
    @staticmethod
    def get_test_case(db: Session, test_case_id: int) -> Optional[TestCase]:
        """Get test case by ID"""
        return db.query(TestCase).filter(TestCase.id == test_case_id).first()
    
    @staticmethod
    def list_test_cases_by_requirement(
        db: Session, requirement_id: int
    ) -> List[TestCase]:
        """List test cases for a requirement"""
        return db.query(TestCase).filter(
            TestCase.requirement_id == requirement_id
        ).all()
    
    @staticmethod
    def update_test_case_status(
        db: Session, test_case_id: int, status: TestCaseStatus
    ) -> Optional[TestCase]:
        """Update test case status"""
        test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        if test_case:
            test_case.status = status
            test_case.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(test_case)
        return test_case
    
    @staticmethod
    def list_all_test_cases(db: Session) -> List[TestCase]:
        """List all test cases"""
        return db.query(TestCase).all()


class TestExecutionService:
    """Service for test execution tracking"""
    
    @staticmethod
    def log_execution(
        db: Session,
        test_case_id: int,
        status: str,
        duration_seconds: int,
        error_message: Optional[str] = None,
        logs: Optional[str] = None,
    ) -> TestExecution:
        """Log test execution"""
        execution = TestExecution(
            test_case_id=test_case_id,
            status=status,
            duration_seconds=duration_seconds,
            error_message=error_message,
            logs=logs,
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution
    
    @staticmethod
    def get_executions_by_test_case(
        db: Session, test_case_id: int, limit: int = 10
    ) -> List[TestExecution]:
        """Get recent executions for a test case"""
        return db.query(TestExecution).filter(
            TestExecution.test_case_id == test_case_id
        ).order_by(TestExecution.executed_at.desc()).limit(limit).all()
