"""
Prompt template management
"""

import os
import json
from typing import List, Dict, Any, Optional

from promptcraft.core.config import Config


class TemplateManager:
    """Manager for prompt templates"""
    
    # Built-in templates
    BUILTIN_TEMPLATES = {
        'code-review': {
            'name': 'Code Review',
            'description': 'Template for reviewing code',
            'category': 'development',
            'content': """# Code Review

Please review the following code:

```
{code}
```

## Review Criteria

1. **Correctness**: Does the code work as intended?
2. **Performance**: Are there any performance issues?
3. **Security**: Are there any security concerns?
4. **Maintainability**: Is the code readable and maintainable?
5. **Best Practices**: Does it follow language/framework best practices?

## Output Format

Please provide:
- Summary of findings
- Specific issues with line references
- Suggestions for improvement
- Overall rating (1-5)"""
        },
        'bug-report': {
            'name': 'Bug Report Analysis',
            'description': 'Template for analyzing bug reports',
            'category': 'development',
            'content': """# Bug Report Analysis

## Bug Description
{description}

## Environment
- OS: {os}
- Version: {version}
- Browser: {browser}

## Steps to Reproduce
{steps}

## Expected Behavior
{expected}

## Actual Behavior
{actual}

## Analysis Request

Please analyze this bug report and provide:
1. Severity assessment (Critical/High/Medium/Low)
2. Possible root causes
3. Suggested debugging steps
4. Potential fixes"""
        },
        'documentation': {
            'name': 'Documentation Generator',
            'description': 'Template for generating documentation',
            'category': 'documentation',
            'content': """# Documentation Generator

Please generate documentation for:

```
{code_or_description}
```

## Documentation Type
{type}

## Requirements
- Clear and concise language
- Include examples where applicable
- Cover all public APIs/interfaces
- Add usage instructions
- Include any prerequisites

## Output Format
Generate the documentation in {format} format."""
        },
        'unit-test': {
            'name': 'Unit Test Generator',
            'description': 'Template for generating unit tests',
            'category': 'testing',
            'content': """# Unit Test Generator

Please generate unit tests for the following code:

```
{code}
```

## Requirements

1. Test all public methods/functions
2. Include edge cases
3. Test error conditions
4. Aim for high code coverage
5. Use {framework} testing framework

## Test Structure

For each test case, include:
- Test name describing the scenario
- Setup/Arrange phase
- Action/Act phase
- Assertion/Assert phase

## Output

Provide the complete test code with comments explaining each test case."""
        },
        'refactoring': {
            'name': 'Code Refactoring',
            'description': 'Template for refactoring code',
            'category': 'development',
            'content': """# Code Refactoring Request

Please refactor the following code:

```
{code}
```

## Refactoring Goals

{goals}

## Constraints
- Maintain existing functionality
- Preserve public APIs
- Improve code quality
- Add appropriate comments

## Output

Provide:
1. Refactored code
2. Explanation of changes made
3. Benefits of the refactoring
4. Any potential risks or considerations"""
        },
        'learning': {
            'name': 'Learning Assistant',
            'description': 'Template for explaining concepts',
            'category': 'education',
            'content': """# Learning Assistant

Please explain the following concept:

**Topic**: {topic}

## Explanation Style
{style}

## Requirements

1. Start with a simple, high-level overview
2. Break down into key components
3. Provide concrete examples
4. Include analogies where helpful
5. Address common misconceptions
6. Suggest resources for further learning

## Output Format

Structure your response as:
- Overview
- Key Concepts
- Examples
- Summary
- Further Reading"""
        },
        'meeting-notes': {
            'name': 'Meeting Notes',
            'description': 'Template for meeting notes',
            'category': 'productivity',
            'content': """# Meeting Notes

**Meeting**: {title}
**Date**: {date}
**Attendees**: {attendees}

## Agenda
{agenda}

## Discussion Points
{discussion}

## Action Items
| Task | Owner | Due Date |
|------|-------|----------|
{action_items}

## Decisions Made
{decisions}

## Next Steps
{next_steps}

---

Please format the above meeting notes professionally and ensure all action items are clear and actionable."""
        },
        'email': {
            'name': 'Professional Email',
            'description': 'Template for professional emails',
            'category': 'communication',
            'content': """# Professional Email

**To**: {recipient}
**Subject**: {subject}
**Tone**: {tone}

## Key Points
{points}

## Context
{context}

## Requirements
- Professional and courteous tone
- Clear and concise message
- Proper greeting and closing
- Include necessary details
- Call to action if applicable

Please draft a professional email based on the above information."""
        },
        'api-design': {
            'name': 'API Design Review',
            'description': 'Template for reviewing API designs',
            'category': 'development',
            'content': """# API Design Review

Please review the following API design:

```
{api_spec}
```

## Review Criteria

1. **RESTfulness**: Does it follow REST principles?
2. **Consistency**: Are naming conventions consistent?
3. **Versioning**: Is versioning strategy appropriate?
4. **Security**: Are authentication/authorization considered?
5. **Documentation**: Is the API well-documented?
6. **Error Handling**: Are error responses clear?

## Output

Provide:
- Overall assessment
- Specific recommendations
- Best practices alignment
- Potential improvements"""
        },
        'sql-optimization': {
            'name': 'SQL Query Optimization',
            'description': 'Template for optimizing SQL queries',
            'category': 'database',
            'content': """# SQL Query Optimization

Please optimize the following SQL query:

```sql
{query}
```

## Database Context
- Database: {database}
- Table sizes: {table_sizes}
- Indexes: {indexes}

## Optimization Goals
{goals}

## Output

Provide:
1. Optimized query
2. Explanation of optimizations
3. Performance comparison (if estimable)
4. Index recommendations
5. Alternative approaches if applicable"""
        }
    }
    
    def __init__(self, config: Config):
        """Initialize template manager"""
        self.config = config
        self.config.ensure_directories()
        self._ensure_builtin_templates()
    
    def _ensure_builtin_templates(self):
        """Ensure built-in templates are saved"""
        for template_id, template in self.BUILTIN_TEMPLATES.items():
            template_path = os.path.join(
                self.config.templates_dir,
                f"{template_id}.json"
            )
            
            if not os.path.exists(template_path):
                try:
                    with open(template_path, 'w', encoding='utf-8') as f:
                        json.dump(template, f, indent=2, ensure_ascii=False)
                except IOError:
                    pass
    
    def list_templates(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available templates"""
        templates = []
        
        # Load from templates directory
        if os.path.exists(self.config.templates_dir):
            for filename in os.listdir(self.config.templates_dir):
                if filename.endswith('.json'):
                    try:
                        filepath = os.path.join(self.config.templates_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            template = json.load(f)
                            template['id'] = filename[:-5]
                            
                            if category and template.get('category') != category:
                                continue
                            
                            templates.append(template)
                    except (json.JSONDecodeError, IOError):
                        continue
        
        return templates
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific template"""
        # Check built-in first
        if template_id in self.BUILTIN_TEMPLATES:
            template = self.BUILTIN_TEMPLATES[template_id].copy()
            template['id'] = template_id
            return template
        
        # Check saved templates
        template_path = os.path.join(
            self.config.templates_dir,
            f"{template_id}.json"
        )
        
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                    template['id'] = template_id
                    return template
            except (json.JSONDecodeError, IOError):
                pass
        
        return None
    
    def use_template(self, template_id: str, **variables) -> Optional[str]:
        """Use a template with variables"""
        template = self.get_template(template_id)
        if not template:
            return None
        
        content = template['content']
        
        # Replace variables
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    def save_template(
        self,
        template_id: str,
        name: str,
        content: str,
        category: str = 'custom',
        description: str = ''
    ) -> bool:
        """Save a custom template"""
        template = {
            'name': name,
            'description': description,
            'category': category,
            'content': content
        }
        
        template_path = os.path.join(
            self.config.templates_dir,
            f"{template_id}.json"
        )
        
        try:
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Failed to save template: {e}")
            return False
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a custom template"""
        # Don't allow deleting built-in templates
        if template_id in self.BUILTIN_TEMPLATES:
            print("Error: Cannot delete built-in template")
            return False
        
        template_path = os.path.join(
            self.config.templates_dir,
            f"{template_id}.json"
        )
        
        try:
            if os.path.exists(template_path):
                os.remove(template_path)
            return True
        except IOError as e:
            print(f"Error: Failed to delete template: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get all template categories"""
        templates = self.list_templates()
        categories = set(t.get('category', 'general') for t in templates)
        categories.update(t.get('category', 'general') for t in self.BUILTIN_TEMPLATES.values())
        return sorted(list(categories))
