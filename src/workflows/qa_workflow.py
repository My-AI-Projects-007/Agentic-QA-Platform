"""Workflow orchestration using LangGraph"""
from typing import Any, Dict, List, Annotated
from langgraph.graph import StateGraph, END
from src.models.schemas import AgentState, TestCaseSchema
from src.agents.requirement_agent import RequirementAgent, RequirementAnalyzer
from src.database.services import RequirementService, TestCaseService
from src.database.config import SessionLocal
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class QAWorkflow:
    """Main QA Platform workflow using LangGraph"""
    
    def __init__(self):
        """Initialize the QA workflow"""
        self.requirement_agent = RequirementAgent()
        self.analyzer = RequirementAnalyzer()
        self.graph = self._build_graph()
        logger.info("QA Workflow initialized")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph"""
        workflow = StateGraph(AgentState)
        
        # Define nodes
        workflow.add_node("parse_requirement", self._parse_requirement_node)
        workflow.add_node("extract_scenarios", self._extract_scenarios_node)
        workflow.add_node("generate_test_cases", self._generate_test_cases_node)
        workflow.add_node("save_to_database", self._save_to_database_node)
        workflow.add_node("validate_output", self._validate_output_node)
        
        # Define edges
        workflow.add_edge("parse_requirement", "extract_scenarios")
        workflow.add_edge("extract_scenarios", "generate_test_cases")
        workflow.add_edge("generate_test_cases", "validate_output")
        workflow.add_edge("validate_output", "save_to_database")
        workflow.add_edge("save_to_database", END)
        
        # Set entry point
        workflow.set_entry_point("parse_requirement")
        
        return workflow.compile()
    
    def _parse_requirement_node(self, state: AgentState) -> AgentState:
        """Parse and analyze the requirement"""
        logger.info(f"Parsing requirement: {state.filename}")
        
        try:
            metadata = self.requirement_agent.parse_requirement_metadata(
                state.requirement_content
            )
            state.messages.append({
                "node": "parse_requirement",
                "status": "success",
                "metadata": metadata
            })
            return state
        except Exception as e:
            logger.error(f"Error in parse_requirement: {str(e)}")
            state.errors.append(f"Parsing error: {str(e)}")
            return state
    
    def _extract_scenarios_node(self, state: AgentState) -> AgentState:
        """Extract scenarios from requirement"""
        logger.info("Extracting scenarios")
        
        try:
            scenarios = self.analyzer.extract_scenarios(state.requirement_content)
            criteria = self.analyzer.extract_acceptance_criteria(
                state.requirement_content
            )
            
            state.messages.append({
                "node": "extract_scenarios",
                "status": "success",
                "scenarios_count": len(scenarios),
                "criteria_count": len(criteria)
            })
            return state
        except Exception as e:
            logger.error(f"Error in extract_scenarios: {str(e)}")
            state.errors.append(f"Scenario extraction error: {str(e)}")
            return state
    
    def _generate_test_cases_node(self, state: AgentState) -> AgentState:
        """Generate test cases using the Requirement Agent"""
        logger.info("Generating test cases")
        
        try:
            test_cases = self.requirement_agent.generate_test_cases(
                state.requirement_content
            )
            
            # Ensure proper parsing
            if isinstance(test_cases, dict) and 'test_cases' in test_cases:
                test_cases = test_cases['test_cases']
            
            # Convert dicts to TestCaseSchema if needed
            parsed_cases: List[TestCaseSchema] = []
            for case in test_cases:
                if isinstance(case, dict):
                    try:
                        parsed_cases.append(TestCaseSchema(**case))
                    except Exception as e:
                        logger.warning(f"Failed to parse test case: {str(e)}")
                        continue
                elif isinstance(case, TestCaseSchema):
                    parsed_cases.append(case)
            
            state.test_cases = parsed_cases
            state.messages.append({
                "node": "generate_test_cases",
                "status": "success",
                "test_cases_generated": len(parsed_cases)
            })
            
            logger.info(f"Generated {len(parsed_cases)} test cases")
            return state
            
        except Exception as e:
            logger.error(f"Error in generate_test_cases: {str(e)}", exc_info=True)
            state.errors.append(f"Test case generation error: {str(e)}")
            return state
    
    def _validate_output_node(self, state: AgentState) -> AgentState:
        """Validate generated test cases"""
        logger.info("Validating test cases")
        
        try:
            if not state.test_cases:
                state.errors.append("No test cases generated")
                return state
            
            valid_cases = []
            for case in state.test_cases:
                if self._validate_test_case(case):
                    valid_cases.append(case)
                else:
                    state.errors.append(f"Invalid test case: {case.test_id}")
            
            state.test_cases = valid_cases
            state.messages.append({
                "node": "validate_output",
                "status": "success",
                "valid_cases": len(valid_cases),
                "invalid_cases": len(state.test_cases) - len(valid_cases)
            })
            
            return state
            
        except Exception as e:
            logger.error(f"Error in validate_output: {str(e)}")
            state.errors.append(f"Validation error: {str(e)}")
            return state
    
    def _save_to_database_node(self, state: AgentState) -> AgentState:
        """Save requirement and test cases to database"""
        logger.info(f"Saving {len(state.test_cases)} test cases to database")
        
        db = SessionLocal()
        try:
            # Create/get requirement
            requirement = RequirementService.get_requirement_by_filename(
                db, state.filename
            )
            
            if not requirement:
                requirement = RequirementService.create_requirement(
                    db,
                    filename=state.filename,
                    title=state.filename.replace('_', ' ').replace('.md', ''),
                    content=state.requirement_content
                )
            
            # Save test cases
            saved_count = 0
            for test_case in state.test_cases:
                try:
                    TestCaseService.create_test_case(db, requirement.id, test_case)
                    saved_count += 1
                except Exception as e:
                    logger.warning(f"Failed to save test case {test_case.test_id}: {str(e)}")
            
            state.messages.append({
                "node": "save_to_database",
                "status": "success",
                "requirement_id": requirement.id,
                "test_cases_saved": saved_count
            })
            
            logger.info(f"Saved {saved_count} test cases for requirement {requirement.id}")
            return state
            
        except Exception as e:
            logger.error(f"Error in save_to_database: {str(e)}", exc_info=True)
            state.errors.append(f"Database save error: {str(e)}")
            return state
        finally:
            db.close()
    
    @staticmethod
    def _validate_test_case(test_case: TestCaseSchema) -> bool:
        """Validate a test case"""
        if not test_case.test_id or not test_case.title:
            return False
        if not test_case.steps or len(test_case.steps) == 0:
            return False
        return True
    
    def run(self, requirement_content: str, filename: str) -> AgentState:
        """
        Run the workflow for a requirement
        
        Args:
            requirement_content: The requirement text
            filename: The source filename
            
        Returns:
            Final workflow state with results
        """
        logger.info(f"Running workflow for {filename}")
        
        initial_state = AgentState(
            requirement_content=requirement_content,
            filename=filename,
        )
        
        result = self.graph.invoke(initial_state)
        
        logger.info(
            f"Workflow completed: {len(result.test_cases)} test cases, "
            f"{len(result.errors)} errors"
        )
        
        return result
