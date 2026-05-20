"""
Project initialization and management
"""

import os
import json
from pathlib import Path
from typing import Optional


class Project:
    """PromptCraft project manager"""
    
    PROJECT_FILE = '.promptcraft.json'
    
    def __init__(self, path: str = '.'):
        """Initialize project"""
        self.path = Path(path).resolve()
        self.project_file = self.path / self.PROJECT_FILE
    
    def initialize(self, name: Optional[str] = None) -> bool:
        """Initialize a new PromptCraft project"""
        try:
            # Create project directory if it doesn't exist
            self.path.mkdir(parents=True, exist_ok=True)
            
            # Create project configuration
            project_config = {
                'name': name or self.path.name,
                'version': '1.0.0',
                'created_at': self._get_timestamp(),
                'settings': {
                    'default_category': 'general',
                    'auto_version': True,
                    'backup_enabled': True
                }
            }
            
            # Save project file
            with open(self.project_file, 'w', encoding='utf-8') as f:
                json.dump(project_config, f, indent=2)
            
            # Create directories
            (self.path / 'prompts').mkdir(exist_ok=True)
            (self.path / 'templates').mkdir(exist_ok=True)
            (self.path / 'exports').mkdir(exist_ok=True)
            
            # Create .gitignore
            gitignore_content = """# PromptCraft
exports/
*.backup
.promptcraft.local.json
"""
            with open(self.path / '.gitignore', 'w') as f:
                f.write(gitignore_content)
            
            return True
        
        except (OSError, IOError) as e:
            print(f"Error: Failed to initialize project: {e}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if directory is a PromptCraft project"""
        return self.project_file.exists()
    
    def get_config(self) -> Optional[dict]:
        """Get project configuration"""
        if not self.is_initialized():
            return None
        
        try:
            with open(self.project_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def update_config(self, updates: dict) -> bool:
        """Update project configuration"""
        config = self.get_config()
        if not config:
            return False
        
        config.update(updates)
        
        try:
            with open(self.project_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError:
            return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
