"""
Shared Configuration Module
Centralized configuration for all crews
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml


class Config:
    """Global configuration manager."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / 'config'
        self.env_config = self._load_env_config()
        self.llm_config = self._load_llm_config()
        self.embedder_config = self._load_embedder_config()
    
    def _load_env_config(self) -> Dict:
        """Load environment configuration."""
        env_file = self.config_dir / 'env.yaml'
        if env_file.exists():
            with open(env_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_llm_config(self) -> Dict:
        """Load LLM configuration."""
        llm_file = self.config_dir / 'llm_config.yaml'
        if llm_file.exists():
            with open(llm_file, 'r') as f:
                return yaml.safe_load(f)
        return {
            'default_provider': 'openai',
            'default_model': 'gpt-4o',
            'default_temperature': 0.3
        }
    
    def _load_embedder_config(self) -> Dict:
        """Load embedder configuration."""
        embedder_file = self.config_dir / 'embedder_config.yaml'
        if embedder_file.exists():
            with open(embedder_file, 'r') as f:
                return yaml.safe_load(f)
        return {
            'provider': 'openai',
            'model': 'text-embedding-3-small'
        }
    
    def get_embedder_config(self) -> Dict:
        """Get embedder configuration for crews."""
        return {
            "provider": self.embedder_config.get('provider', 'openai'),
            "config": {
                "model": self.embedder_config.get('model', 'text-embedding-3-small')
            }
        }
    
    def get_storage_dir(self) -> Path:
        """Get storage directory for memory and knowledge."""
        storage_dir = os.getenv('CREWAI_STORAGE_DIR')
        if storage_dir:
            return Path(storage_dir)
        return self.base_dir / 'storage'


# Global config instance
config = Config()
