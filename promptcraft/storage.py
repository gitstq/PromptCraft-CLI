"""
Prompt Storage & Version Management - Local persistence layer
Prompt存储与版本管理 - 本地持久化层
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PromptVersion:
    """Represents a version of a prompt"""
    id: str
    content: str
    created_at: str
    description: str
    tags: List[str]
    score: Optional[float] = None
    test_results: Optional[Dict] = None


@dataclass
class PromptProject:
    """Represents a prompt project with versions"""
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str
    versions: List[PromptVersion]
    current_version_id: Optional[str] = None


class PromptStorage:
    """
    Manages local storage of prompts and their versions
    管理Prompt及其版本的本地存储
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            storage_dir = os.path.expanduser("~/.promptcraft")
        
        self.storage_dir = Path(storage_dir)
        self.projects_dir = self.storage_dir / "projects"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{content}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def _get_project_path(self, project_id: str) -> Path:
        """Get path to project file"""
        return self.projects_dir / f"{project_id}.json"
    
    def create_project(self, name: str, description: str = "") -> PromptProject:
        """Create a new prompt project"""
        now = datetime.now().isoformat()
        project_id = self._generate_id(name)
        
        project = PromptProject(
            id=project_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            versions=[]
        )
        
        self._save_project(project)
        return project
    
    def _save_project(self, project: PromptProject):
        """Save project to disk"""
        project_path = self._get_project_path(project.id)
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(project), f, indent=2, ensure_ascii=False)
    
    def _load_project(self, project_id: str) -> Optional[PromptProject]:
        """Load project from disk"""
        project_path = self._get_project_path(project_id)
        if not project_path.exists():
            return None
        
        with open(project_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Convert version dicts to PromptVersion objects
        versions = [PromptVersion(**v) for v in data.get('versions', [])]
        data['versions'] = versions
        
        return PromptProject(**data)
    
    def add_version(self, project_id: str, content: str, description: str = "", 
                    tags: List[str] = None, score: Optional[float] = None) -> Optional[PromptVersion]:
        """Add a new version to a project"""
        project = self._load_project(project_id)
        if not project:
            return None
        
        if tags is None:
            tags = []
        
        version = PromptVersion(
            id=self._generate_id(content),
            content=content,
            created_at=datetime.now().isoformat(),
            description=description,
            tags=tags,
            score=score
        )
        
        project.versions.append(version)
        project.current_version_id = version.id
        project.updated_at = datetime.now().isoformat()
        
        self._save_project(project)
        return version
    
    def get_project(self, project_id: str) -> Optional[PromptProject]:
        """Get a project by ID"""
        return self._load_project(project_id)
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        projects = []
        for project_file in self.projects_dir.glob("*.json"):
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    projects.append({
                        "id": data["id"],
                        "name": data["name"],
                        "description": data["description"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "version_count": len(data.get("versions", []))
                    })
            except Exception:
                continue
        
        # Sort by updated_at descending
        projects.sort(key=lambda x: x["updated_at"], reverse=True)
        return projects
    
    def get_version(self, project_id: str, version_id: str) -> Optional[PromptVersion]:
        """Get a specific version"""
        project = self._load_project(project_id)
        if not project:
            return None
        
        for version in project.versions:
            if version.id == version_id:
                return version
        return None
    
    def get_current_version(self, project_id: str) -> Optional[PromptVersion]:
        """Get the current version of a project"""
        project = self._load_project(project_id)
        if not project or not project.current_version_id:
            return None
        
        return self.get_version(project_id, project.current_version_id)
    
    def set_current_version(self, project_id: str, version_id: str) -> bool:
        """Set the current version of a project"""
        project = self._load_project(project_id)
        if not project:
            return False
        
        # Verify version exists
        version_exists = any(v.id == version_id for v in project.versions)
        if not version_exists:
            return False
        
        project.current_version_id = version_id
        project.updated_at = datetime.now().isoformat()
        self._save_project(project)
        return True
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        project_path = self._get_project_path(project_id)
        if project_path.exists():
            project_path.unlink()
            return True
        return False
    
    def delete_version(self, project_id: str, version_id: str) -> bool:
        """Delete a version from a project"""
        project = self._load_project(project_id)
        if not project:
            return False
        
        project.versions = [v for v in project.versions if v.id != version_id]
        
        # Update current version if deleted
        if project.current_version_id == version_id:
            project.current_version_id = project.versions[-1].id if project.versions else None
        
        project.updated_at = datetime.now().isoformat()
        self._save_project(project)
        return True
    
    def search_projects(self, query: str) -> List[Dict[str, Any]]:
        """Search projects by name or description"""
        all_projects = self.list_projects()
        query_lower = query.lower()
        
        return [
            p for p in all_projects
            if query_lower in p["name"].lower() or query_lower in p["description"].lower()
        ]
    
    def export_project(self, project_id: str, format_type: str = "json") -> Optional[str]:
        """Export project to different formats"""
        project = self._load_project(project_id)
        if not project:
            return None
        
        if format_type == "json":
            return json.dumps(asdict(project), indent=2, ensure_ascii=False)
        
        elif format_type == "markdown":
            lines = [
                f"# {project.name}",
                f"\n{project.description}",
                f"\n## Versions ({len(project.versions)})",
            ]
            
            for i, version in enumerate(project.versions, 1):
                lines.extend([
                    f"\n### Version {i}",
                    f"- **ID**: {version.id}",
                    f"- **Created**: {version.created_at}",
                    f"- **Score**: {version.score or 'N/A'}",
                    f"- **Tags**: {', '.join(version.tags) if version.tags else 'None'}",
                    f"\n**Description**: {version.description}",
                    f"\n```\n{version.content}\n```"
                ])
            
            return '\n'.join(lines)
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        projects = self.list_projects()
        total_versions = sum(p["version_count"] for p in projects)
        
        return {
            "total_projects": len(projects),
            "total_versions": total_versions,
            "storage_dir": str(self.storage_dir),
            "avg_versions_per_project": total_versions / len(projects) if projects else 0
        }
