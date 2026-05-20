"""
Configuration management for PromptCraft CLI
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager"""
    
    DEFAULT_CONFIG = {
        'data_dir': '~/.promptcraft',
        'default_format': 'json',
        'editor': None,  # Use system default
        'colors': True,
        'pagination': 20,
        'auto_backup': True,
        'backup_count': 10,
        'optimization': {
            'max_length': 4000,
            'preserve_structure': True,
            'add_examples': True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        config_dir = os.path.expanduser('~/.config')
        if not os.path.exists(config_dir):
            config_dir = os.path.expanduser('~')
        return os.path.join(config_dir, 'promptcraft.json')
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        config = self.DEFAULT_CONFIG.copy()
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config: {e}")
        
        # Expand data directory path
        config['data_dir'] = os.path.expanduser(config['data_dir'])
        
        return config
    
    def save(self) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error: Failed to save config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    @property
    def data_dir(self) -> str:
        """Get data directory"""
        return self.config['data_dir']
    
    @property
    def prompts_dir(self) -> str:
        """Get prompts storage directory"""
        return os.path.join(self.data_dir, 'prompts')
    
    @property
    def versions_dir(self) -> str:
        """Get versions storage directory"""
        return os.path.join(self.data_dir, 'versions')
    
    @property
    def templates_dir(self) -> str:
        """Get templates storage directory"""
        return os.path.join(self.data_dir, 'templates')
    
    def ensure_directories(self) -> None:
        """Ensure all data directories exist"""
        for directory in [self.data_dir, self.prompts_dir, self.versions_dir, self.templates_dir]:
            os.makedirs(directory, exist_ok=True)
