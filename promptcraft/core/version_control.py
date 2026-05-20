"""
Version control functionality for prompts
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

from promptcraft.core.config import Config


class VersionControl:
    """Version control system for prompts"""
    
    def __init__(self, config: Config):
        """Initialize version control"""
        self.config = config
        self.config.ensure_directories()
    
    def _get_version_path(self, prompt_id: str) -> str:
        """Get storage path for prompt versions"""
        return os.path.join(self.config.versions_dir, f"{prompt_id}.json")
    
    def _generate_version_hash(self, content: str) -> str:
        """Generate hash for version content"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def create_version(
        self,
        prompt_id: str,
        content: str,
        message: str = "",
        author: Optional[str] = None
    ) -> str:
        """Create a new version for a prompt"""
        version_path = self._get_version_path(prompt_id)
        
        # Load existing versions
        versions = self._load_versions(prompt_id)
        
        # Generate version number
        version_number = len(versions) + 1
        version_id = f"v{version_number}"
        
        # Create version data
        version_data = {
            'id': version_id,
            'number': version_number,
            'hash': self._generate_version_hash(content),
            'content': content,
            'message': message,
            'author': author or os.environ.get('USER', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'size': len(content)
        }
        
        versions.append(version_data)
        
        # Save versions
        try:
            with open(version_path, 'w', encoding='utf-8') as f:
                json.dump(versions, f, indent=2, ensure_ascii=False)
            return version_id
        except IOError as e:
            print(f"Error: Failed to save version: {e}")
            return ""
    
    def _load_versions(self, prompt_id: str) -> List[Dict[str, Any]]:
        """Load all versions for a prompt"""
        version_path = self._get_version_path(prompt_id)
        
        if not os.path.exists(version_path):
            return []
        
        try:
            with open(version_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_version(self, prompt_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """Get specific version of a prompt"""
        versions = self._load_versions(prompt_id)
        
        for version in versions:
            if version['id'] == version_id or str(version['number']) == version_id.lstrip('v'):
                return version
        
        return None
    
    def get_version_history(
        self,
        prompt_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get version history for a prompt"""
        versions = self._load_versions(prompt_id)
        
        # Sort by version number (newest first)
        versions.sort(key=lambda x: x['number'], reverse=True)
        
        return versions[:limit]
    
    def compare_versions(
        self,
        prompt_id: str,
        version1: str,
        version2: str
    ) -> Optional[Dict[str, Any]]:
        """Compare two versions of a prompt"""
        v1_data = self.get_version(prompt_id, version1)
        v2_data = self.get_version(prompt_id, version2)
        
        if not v1_data or not v2_data:
            return None
        
        return {
            'version1': v1_data,
            'version2': v2_data,
            'diff': self._compute_diff(v1_data['content'], v2_data['content'])
        }
    
    def _compute_diff(self, content1: str, content2: str) -> List[Dict[str, Any]]:
        """Compute diff between two content strings"""
        try:
            import difflib
            
            lines1 = content1.splitlines(keepends=True)
            lines2 = content2.splitlines(keepends=True)
            
            diff = list(difflib.unified_diff(
                lines1, lines2,
                lineterm='',
                n=3
            ))
            
            return diff
        except Exception:
            # Fallback to simple comparison
            return []
    
    def rollback(self, prompt_id: str, version_id: str) -> Optional[str]:
        """Rollback to a specific version"""
        version = self.get_version(prompt_id, version_id)
        if not version:
            return None
        
        return version['content']
    
    def delete_versions(self, prompt_id: str) -> bool:
        """Delete all versions for a prompt"""
        version_path = self._get_version_path(prompt_id)
        
        try:
            if os.path.exists(version_path):
                os.remove(version_path)
            return True
        except IOError as e:
            print(f"Error: Failed to delete versions: {e}")
            return False
    
    def get_version_stats(self, prompt_id: str) -> Dict[str, Any]:
        """Get version statistics for a prompt"""
        versions = self._load_versions(prompt_id)
        
        if not versions:
            return {
                'total_versions': 0,
                'first_version': None,
                'latest_version': None,
                'total_size_change': 0
            }
        
        first = versions[0]
        latest = versions[-1]
        
        size_changes = [v['size'] for v in versions]
        total_change = size_changes[-1] - size_changes[0] if len(size_changes) > 1 else 0
        
        return {
            'total_versions': len(versions),
            'first_version': first['timestamp'],
            'latest_version': latest['timestamp'],
            'total_size_change': total_change,
            'average_version_size': sum(size_changes) / len(size_changes)
        }
    
    def find_similar_versions(
        self,
        prompt_id: str,
        content: str,
        threshold: float = 0.9
    ) -> List[Dict[str, Any]]:
        """Find versions similar to given content"""
        versions = self._load_versions(prompt_id)
        similar = []
        
        for version in versions:
            similarity = self._calculate_similarity(content, version['content'])
            if similarity >= threshold:
                similar.append({
                    'version': version,
                    'similarity': similarity
                })
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two contents (0-1)"""
        try:
            import difflib
            return difflib.SequenceMatcher(None, content1, content2).ratio()
        except Exception:
            # Simple fallback
            if content1 == content2:
                return 1.0
            return 0.0
