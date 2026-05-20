"""
Prompt management functionality
"""

import os
import json
import hashlib
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from promptcraft.core.config import Config
from promptcraft.core.version_control import VersionControl


class PromptManager:
    """Manager for prompt CRUD operations"""
    
    def __init__(self, config: Config):
        """Initialize prompt manager"""
        self.config = config
        self.config.ensure_directories()
        self.vc = VersionControl(config)
    
    def _generate_id(self, name: str) -> str:
        """Generate unique prompt ID"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{name}_{timestamp}_{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _get_prompt_path(self, prompt_id: str) -> str:
        """Get storage path for a prompt"""
        return os.path.join(self.config.prompts_dir, f"{prompt_id}.json")
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '-', text).strip('-')
        return text[:50]
    
    def add_prompt(
        self,
        name: str,
        content: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None
    ) -> Optional[str]:
        """Add a new prompt"""
        prompt_id = self._generate_id(name)
        slug = self._slugify(name)
        
        prompt_data = {
            'id': prompt_id,
            'slug': slug,
            'name': name,
            'content': content,
            'category': category or 'general',
            'tags': tags or [],
            'description': description or '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': 1,
            'usage_count': 0,
            'metadata': {
                'word_count': len(content.split()),
                'char_count': len(content),
                'line_count': len(content.split('\n'))
            }
        }
        
        try:
            prompt_path = self._get_prompt_path(prompt_id)
            with open(prompt_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            # Create initial version
            self.vc.create_version(prompt_id, content, "Initial version")
            
            return prompt_id
        except IOError as e:
            print(f"Error: Failed to save prompt: {e}")
            return None
    
    def get_prompt(self, identifier: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get prompt by ID, slug, or name"""
        # Try to find by ID first
        prompt_path = self._get_prompt_path(identifier)
        if os.path.exists(prompt_path):
            try:
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    prompt = json.load(f)
                    
                    # If version specified, get that version's content
                    if version:
                        version_data = self.vc.get_version(identifier, version)
                        if version_data:
                            prompt['content'] = version_data['content']
                            prompt['version'] = version
                    
                    return prompt
            except (json.JSONDecodeError, IOError):
                return None
        
        # Search by slug or name
        prompts = self.list_prompts()
        for prompt in prompts:
            if prompt['slug'] == identifier or prompt['name'].lower() == identifier.lower():
                if version:
                    version_data = self.vc.get_version(prompt['id'], version)
                    if version_data:
                        prompt['content'] = version_data['content']
                        prompt['version'] = version
                return prompt
        
        return None
    
    def update_prompt(
        self,
        identifier: str,
        content: str,
        message: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Update an existing prompt"""
        prompt = self.get_prompt(identifier)
        if not prompt:
            return False
        
        prompt_id = prompt['id']
        
        # Update fields
        prompt['content'] = content
        prompt['updated_at'] = datetime.now().isoformat()
        prompt['version'] += 1
        
        # Update optional fields
        for key, value in kwargs.items():
            if value is not None:
                prompt[key] = value
        
        # Update metadata
        prompt['metadata'] = {
            'word_count': len(content.split()),
            'char_count': len(content),
            'line_count': len(content.split('\n'))
        }
        
        try:
            # Save updated prompt
            prompt_path = self._get_prompt_path(prompt_id)
            with open(prompt_path, 'w', encoding='utf-8') as f:
                json.dump(prompt, f, indent=2, ensure_ascii=False)
            
            # Create new version
            version_message = message or f"Update version {prompt['version']}"
            self.vc.create_version(prompt_id, content, version_message)
            
            return True
        except IOError as e:
            print(f"Error: Failed to update prompt: {e}")
            return False
    
    def delete_prompt(self, identifier: str) -> bool:
        """Delete a prompt"""
        prompt = self.get_prompt(identifier)
        if not prompt:
            return False
        
        prompt_id = prompt['id']
        
        try:
            # Delete prompt file
            prompt_path = self._get_prompt_path(prompt_id)
            if os.path.exists(prompt_path):
                os.remove(prompt_path)
            
            # Delete version history
            self.vc.delete_versions(prompt_id)
            
            return True
        except IOError as e:
            print(f"Error: Failed to delete prompt: {e}")
            return False
    
    def list_prompts(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """List all prompts with optional filtering"""
        prompts = []
        
        if not os.path.exists(self.config.prompts_dir):
            return prompts
        
        for filename in os.listdir(self.config.prompts_dir):
            if filename.endswith('.json'):
                try:
                    filepath = os.path.join(self.config.prompts_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        prompt = json.load(f)
                        
                        # Apply filters
                        if category and prompt.get('category') != category:
                            continue
                        
                        if tags:
                            prompt_tags = set(prompt.get('tags', []))
                            if not any(tag in prompt_tags for tag in tags):
                                continue
                        
                        prompts.append(prompt)
                except (json.JSONDecodeError, IOError):
                    continue
        
        # Sort by updated_at (newest first)
        prompts.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        return prompts
    
    def export_prompt(
        self,
        identifier: str,
        output_path: str,
        format: str = 'json',
        version: Optional[str] = None
    ) -> bool:
        """Export prompt to file"""
        prompt = self.get_prompt(identifier, version=version)
        if not prompt:
            return False
        
        try:
            if format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(prompt, f, indent=2, ensure_ascii=False)
            
            elif format == 'yaml':
                try:
                    import yaml
                    with open(output_path, 'w', encoding='utf-8') as f:
                        yaml.dump(prompt, f, allow_unicode=True, sort_keys=False)
                except ImportError:
                    # Fallback to JSON if PyYAML not available
                    print("Warning: PyYAML not installed, using JSON format")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(prompt, f, indent=2, ensure_ascii=False)
            
            elif format == 'txt':
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {prompt['name']}\n\n")
                    f.write(prompt['content'])
            
            elif format == 'md':
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {prompt['name']}\n\n")
                    if prompt.get('description'):
                        f.write(f"{prompt['description']}\n\n")
                    f.write("## Content\n\n")
                    f.write(f"```\n{prompt['content']}\n```\n\n")
                    if prompt.get('tags'):
                        f.write(f"**Tags:** {', '.join(prompt['tags'])}\n\n")
                    f.write(f"**Category:** {prompt.get('category', 'general')}\n")
                    f.write(f"**Version:** {prompt.get('version', 1)}\n")
            
            return True
        except IOError as e:
            print(f"Error: Failed to export prompt: {e}")
            return False
    
    def import_prompts(self, file_path: str, format: Optional[str] = None) -> int:
        """Import prompts from file"""
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return -1
        
        # Auto-detect format from extension
        if not format:
            ext = os.path.splitext(file_path)[1].lower()
            format = ext.lstrip('.') if ext else 'json'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if format == 'json':
                    data = json.load(f)
                elif format == 'yaml' or format == 'yml':
                    try:
                        import yaml
                        data = yaml.safe_load(f)
                    except ImportError:
                        print("Error: PyYAML not installed")
                        return -1
                elif format == 'csv':
                    return self._import_csv(f)
                else:
                    print(f"Error: Unsupported format: {format}")
                    return -1
            
            # Handle both single prompt and list of prompts
            if isinstance(data, dict):
                data = [data]
            
            count = 0
            for item in data:
                if isinstance(item, dict) and 'content' in item:
                    self.add_prompt(
                        name=item.get('name', f"Imported {count + 1}"),
                        content=item['content'],
                        category=item.get('category'),
                        tags=item.get('tags', []),
                        description=item.get('description')
                    )
                    count += 1
            
            return count
        
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error: Failed to import prompts: {e}")
            return -1
    
    def _import_csv(self, file_obj) -> int:
        """Import prompts from CSV file"""
        import csv
        count = 0
        reader = csv.DictReader(file_obj)
        
        for row in reader:
            if 'content' in row:
                tags = row.get('tags', '').split(',') if row.get('tags') else []
                self.add_prompt(
                    name=row.get('name', f"Imported {count + 1}"),
                    content=row['content'],
                    category=row.get('category'),
                    tags=[t.strip() for t in tags],
                    description=row.get('description')
                )
                count += 1
        
        return count
    
    def search_prompts(self, query: str) -> List[Dict[str, Any]]:
        """Search prompts by query string"""
        prompts = self.list_prompts()
        query_lower = query.lower()
        
        results = []
        for prompt in prompts:
            # Search in name, content, description, and tags
            searchable_text = ' '.join([
                prompt.get('name', ''),
                prompt.get('content', ''),
                prompt.get('description', ''),
                ' '.join(prompt.get('tags', []))
            ]).lower()
            
            if query_lower in searchable_text:
                results.append(prompt)
        
        return results
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        prompts = self.list_prompts()
        categories = set(p.get('category', 'general') for p in prompts)
        return sorted(list(categories))
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags"""
        prompts = self.list_prompts()
        tags = set()
        for prompt in prompts:
            tags.update(prompt.get('tags', []))
        return sorted(list(tags))
