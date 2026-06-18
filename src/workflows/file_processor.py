"""File processor for requirement files"""
import os
from pathlib import Path
from typing import List, Tuple
from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class RequirementFileProcessor:
    """Process requirement markdown files"""
    
    @staticmethod
    def get_requirement_files() -> List[Tuple[str, str]]:
        """
        Get all requirement files from the requirements folder
        
        Returns:
            List of tuples (filename, content)
        """
        requirements_path = Path(settings.REQUIREMENTS_PATH)
        
        if not requirements_path.exists():
            logger.warning(f"Requirements folder does not exist: {requirements_path}")
            return []
        
        files = []
        for file_path in requirements_path.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                files.append((file_path.name, content))
                logger.info(f"Loaded requirement file: {file_path.name}")
            except Exception as e:
                logger.error(f"Error reading file {file_path.name}: {str(e)}")
        
        return files
    
    @staticmethod
    def save_requirement(filename: str, content: str) -> bool:
        """Save requirement file"""
        try:
            requirements_path = Path(settings.REQUIREMENTS_PATH)
            requirements_path.mkdir(parents=True, exist_ok=True)
            
            file_path = requirements_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved requirement file: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving requirement file: {str(e)}")
            return False
