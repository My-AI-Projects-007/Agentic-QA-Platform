"""Main application entry point"""
import asyncio
from typing import Optional
from src.config.logging_config import get_logger
from src.config.settings import settings
from src.database.config import init_db
from src.workflows.qa_workflow import QAWorkflow
from src.workflows.file_processor import RequirementFileProcessor

logger = get_logger(__name__)


class AgenticQAPlatform:
    """Main QA Platform application"""
    
    def __init__(self):
        """Initialize the platform"""
        logger.info("Initializing Agentic QA Platform")
        
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Initialize workflow
        self.workflow = QAWorkflow()
        logger.info("Workflow initialized")
    
    def process_single_requirement(self, filename: str, content: str) -> dict:
        """
        Process a single requirement file
        
        Args:
            filename: Name of the requirement file
            content: Content of the requirement
            
        Returns:
            Result dictionary with test cases and metadata
        """
        logger.info(f"Processing requirement: {filename}")
        
        try:
            result = self.workflow.run(content, filename)
            
            return {
                "status": "success",
                "filename": filename,
                "test_cases_generated": len(result.test_cases),
                "errors": result.errors,
                "messages": result.messages,
                "test_cases": [tc.dict() for tc in result.test_cases]
            }
        except Exception as e:
            logger.error(f"Error processing requirement: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "filename": filename,
                "error": str(e)
            }
    
    def process_all_requirements(self) -> list:
        """
        Process all requirements from the requirements folder
        
        Returns:
            List of results
        """
        logger.info("Processing all requirements")
        
        files = RequirementFileProcessor.get_requirement_files()
        logger.info(f"Found {len(files)} requirement files")
        
        results = []
        for filename, content in files:
            result = self.process_single_requirement(filename, content)
            results.append(result)
        
        # Print summary
        total_tests = sum(r.get("test_cases_generated", 0) for r in results)
        successful = len([r for r in results if r["status"] == "success"])
        
        logger.info(
            f"Processing complete: {successful}/{len(results)} successful, "
            f"{total_tests} total test cases generated"
        )
        
        return results
    
    def list_generated_test_cases(self) -> list:
        """List all generated test cases"""
        from src.database.config import SessionLocal
        from src.database.services import TestCaseService
        
        db = SessionLocal()
        try:
            test_cases = TestCaseService.list_all_test_cases(db)
            return [
                {
                    "id": tc.id,
                    "test_id": tc.test_id,
                    "title": tc.title,
                    "requirement_id": tc.requirement_id,
                    "status": tc.status.value,
                    "priority": tc.priority,
                }
                for tc in test_cases
            ]
        finally:
            db.close()


def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Target Website: {settings.TARGET_WEBSITE_URL}")
    logger.info("=" * 50)
    
    # Initialize platform
    platform = AgenticQAPlatform()
    
    # Process all requirements
    results = platform.process_all_requirements()
    
    # List generated test cases
    test_cases = platform.list_generated_test_cases()
    logger.info(f"Total test cases in database: {len(test_cases)}")
    
    return platform, results


if __name__ == "__main__":
    platform, results = main()
    logger.info("Platform initialization complete")
