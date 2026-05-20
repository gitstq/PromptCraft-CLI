"""
Prompt optimization functionality
"""

import re
from typing import Dict, Any, List

from promptcraft.core.config import Config


class PromptOptimizer:
    """Prompt optimization engine"""
    
    def __init__(self, config: Config):
        """Initialize optimizer"""
        self.config = config
    
    def optimize(
        self,
        content: str,
        strategy: str = 'all'
    ) -> Dict[str, Any]:
        """Optimize prompt content"""
        original = content
        optimizations = []
        
        if strategy in ['clarity', 'all']:
            content, clarity_opts = self._optimize_clarity(content)
            optimizations.extend(clarity_opts)
        
        if strategy in ['conciseness', 'all']:
            content, concise_opts = self._optimize_conciseness(content)
            optimizations.extend(concise_opts)
        
        if strategy in ['structure', 'all']:
            content, struct_opts = self._optimize_structure(content)
            optimizations.extend(struct_opts)
        
        if strategy in ['examples', 'all']:
            content, example_opts = self._optimize_examples(content)
            optimizations.extend(example_opts)
        
        return {
            'original': original,
            'optimized': content,
            'content': content,
            'optimizations': optimizations,
            'summary': f"Applied {len(optimizations)} optimizations",
            'improvements': {
                'original_length': len(original),
                'optimized_length': len(content),
                'reduction': len(original) - len(content),
                'reduction_percent': round((len(original) - len(content)) / len(original) * 100, 1) if len(original) > 0 else 0
            }
        }
    
    def _optimize_clarity(self, content: str) -> tuple:
        """Optimize prompt for clarity"""
        optimizations = []
        original = content
        
        # Remove redundant phrases
        redundant_patterns = [
            (r'\b(please|kindly|could you|would you)\s+', ''),
            (r'\b(I want|I need|I would like)\s+', ''),
            (r'\b(make sure|ensure that|be sure to)\s+', ''),
        ]
        
        for pattern, replacement in redundant_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                optimizations.append(f"Removed redundant phrase matching: {pattern}")
        
        # Clarify ambiguous terms
        ambiguous_terms = {
            r'\bgood\b': 'high-quality',
            r'\bbest\b': 'optimal',
            r'\bbetter\b': 'improved',
            r'\bfast\b': 'efficient',
            r'\beasy\b': 'straightforward'
        }
        
        for term, replacement in ambiguous_terms.items():
            if re.search(term, content, re.IGNORECASE):
                content = re.sub(term, replacement, content, flags=re.IGNORECASE)
                optimizations.append(f"Replaced ambiguous term '{term}' with '{replacement}'")
        
        # Add specific instructions if missing
        if 'step by step' not in content.lower() and 'step-by-step' not in content.lower():
            if len(content.split('.')) > 2:
                content = content.rstrip() + "\n\nPlease provide your response step by step."
                optimizations.append("Added step-by-step instruction for clarity")
        
        return content, optimizations
    
    def _optimize_conciseness(self, content: str) -> tuple:
        """Optimize prompt for conciseness"""
        optimizations = []
        
        # Remove filler words
        filler_patterns = [
            r'\b(very|really|quite|rather|pretty)\s+',
            r'\b(in order to|so as to)\s+',
            r'\b(due to the fact that|because of the fact that)\s+',
            r'\b(at this point in time|at the present time)\s+',
            r'\b(in the event that|in case)\s+',
        ]
        
        for pattern in filler_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                optimizations.append(f"Removed filler phrase matching: {pattern}")
        
        # Remove extra whitespace
        original_len = len(content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        if len(content) < original_len:
            optimizations.append("Normalized whitespace")
        
        # Remove redundant sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        unique_sentences = []
        seen = set()
        
        for sentence in sentences:
            normalized = sentence.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_sentences.append(sentence)
            else:
                optimizations.append(f"Removed redundant sentence: {sentence[:50]}...")
        
        content = ' '.join(unique_sentences)
        
        return content, optimizations
    
    def _optimize_structure(self, content: str) -> tuple:
        """Optimize prompt structure"""
        optimizations = []
        
        # Add structure markers if missing
        has_structure = any(marker in content for marker in ['#', '##', '###', '---', '**'])
        
        if not has_structure and len(content) > 200:
            # Try to add structure
            lines = content.split('\n')
            structured_lines = []
            
            # Add title if first line doesn't look like one
            if lines and not lines[0].strip().endswith(':'):
                structured_lines.append(f"# {lines[0].strip()}")
                lines = lines[1:]
                optimizations.append("Added title header")
            
            # Group content into sections
            current_section = []
            for line in lines:
                stripped = line.strip()
                if stripped.endswith(':') and len(stripped) < 50:
                    if current_section:
                        structured_lines.extend(current_section)
                        current_section = []
                    structured_lines.append(f"\n## {stripped.rstrip(':')}")
                    optimizations.append(f"Converted to section header: {stripped}")
                else:
                    current_section.append(line)
            
            structured_lines.extend(current_section)
            content = '\n'.join(structured_lines)
        
        # Ensure proper markdown formatting
        if '```' not in content and 'code' in content.lower():
            # Try to detect code blocks
            lines = content.split('\n')
            in_code = False
            formatted_lines = []
            
            for line in lines:
                if re.match(r'^\s{4,}', line) and not in_code:
                    formatted_lines.append('```')
                    in_code = True
                elif not re.match(r'^\s{4,}', line) and in_code:
                    formatted_lines.append('```')
                    in_code = False
                formatted_lines.append(line)
            
            if in_code:
                formatted_lines.append('```')
            
            if formatted_lines != lines:
                content = '\n'.join(formatted_lines)
                optimizations.append("Added code block formatting")
        
        return content, optimizations
    
    def _optimize_examples(self, content: str) -> tuple:
        """Optimize prompt examples"""
        optimizations = []
        
        # Check if examples are present
        has_examples = any(marker in content.lower() for marker in [
            'example:', 'for example', 'e.g.,', 'here is an example',
            'input:', 'output:', '```'
        ])
        
        if not has_examples:
            # Add example structure suggestion
            content += "\n\n## Example\n\nInput: [Your input here]\n\nOutput: [Expected output format]"
            optimizations.append("Added example structure template")
        
        # Improve existing examples
        if 'input:' in content.lower() and 'output:' in content.lower():
            # Ensure consistent formatting
            content = re.sub(
                r'(?i)(input:|output:)\s*',
                lambda m: f"**{m.group(1).capitalize()}** ",
                content
            )
            optimizations.append("Standardized example formatting")
        
        return content, optimizations
    
    def suggest_improvements(self, content: str) -> List[Dict[str, Any]]:
        """Suggest improvements without applying them"""
        suggestions = []
        
        # Check for common issues
        checks = [
            (len(content) < 50, "Prompt is quite short. Consider adding more context."),
            (len(content) > 2000, "Prompt is quite long. Consider breaking it into sections."),
            ('?' not in content, "Consider phrasing your prompt as a clear question or instruction."),
            (not any(c.isupper() for c in content[:100]), "Consider starting with a clear, capitalized instruction."),
            ('example' not in content.lower(), "Consider adding an example to clarify expected output."),
            ('step' not in content.lower() and len(content) > 200, "Consider requesting step-by-step reasoning."),
            (content.count('and') > 10, "Prompt has many 'and' clauses. Consider breaking into bullet points."),
        ]
        
        for condition, message in checks:
            if condition:
                suggestions.append({
                    'type': 'warning',
                    'message': message
                })
        
        # Check for positive aspects
        positives = [
            ('specific' in content.lower() or 'detailed' in content.lower(), "Good use of specificity keywords"),
            ('```' in content, "Good use of code block formatting"),
            ('#' in content, "Good use of markdown headers"),
            (len([s for s in content.split('.') if s.strip()]) > 3, "Good sentence structure"),
        ]
        
        for condition, message in positives:
            if condition:
                suggestions.append({
                    'type': 'positive',
                    'message': message
                })
        
        return suggestions
