"""
Prompt analysis functionality
"""

import re
from typing import Dict, Any, List
from collections import Counter

from promptcraft.core.config import Config


class PromptAnalyzer:
    """Prompt quality analyzer"""
    
    def __init__(self, config: Config):
        """Initialize analyzer"""
        self.config = config
    
    def analyze(self, content: str, detailed: bool = False) -> Dict[str, Any]:
        """Analyze prompt quality"""
        analysis = {
            'basic_stats': self._basic_stats(content),
            'quality_score': self._calculate_quality_score(content),
            'structure_analysis': self._analyze_structure(content),
            'content_analysis': self._analyze_content(content),
            'readability': self._analyze_readability(content),
            'suggestions': self._generate_suggestions(content)
        }
        
        if detailed:
            analysis['detailed_metrics'] = self._detailed_metrics(content)
        
        return analysis
    
    def _basic_stats(self, content: str) -> Dict[str, Any]:
        """Calculate basic statistics"""
        words = content.split()
        lines = content.split('\n')
        sentences = re.split(r'[.!?]+', content)
        
        return {
            'char_count': len(content),
            'word_count': len(words),
            'line_count': len(lines),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'paragraph_count': len([p for p in content.split('\n\n') if p.strip()])
        }
    
    def _calculate_quality_score(self, content: str) -> Dict[str, Any]:
        """Calculate overall quality score"""
        scores = {
            'clarity': self._score_clarity(content),
            'specificity': self._score_specificity(content),
            'structure': self._score_structure(content),
            'completeness': self._score_completeness(content)
        }
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'overall': round(overall, 1),
            'breakdown': scores,
            'rating': self._get_rating(overall)
        }
    
    def _score_clarity(self, content: str) -> float:
        """Score prompt clarity (0-100)"""
        score = 100
        
        # Penalize ambiguity
        ambiguous_terms = ['good', 'bad', 'best', 'better', 'fast', 'slow', 'easy', 'hard']
        for term in ambiguous_terms:
            if re.search(rf'\b{term}\b', content, re.IGNORECASE):
                score -= 5
        
        # Penalize excessive length
        word_count = len(content.split())
        if word_count > 500:
            score -= 10
        if word_count > 1000:
            score -= 20
        
        # Reward clear instructions
        if re.search(r'\b(please|kindly)\b', content, re.IGNORECASE):
            score -= 5  # Too polite can be unclear
        
        # Reward direct language
        if re.search(r'^\s*[A-Z]', content):
            score += 5
        
        return max(0, min(100, score))
    
    def _score_specificity(self, content: str) -> float:
        """Score prompt specificity (0-100)"""
        score = 50  # Base score
        
        # Reward specific details
        indicators = [
            (r'\d+', 'numbers'),
            (r'\b(example|sample|instance)\b', 'examples'),
            (r'\b(step|phase|stage)\b', 'steps'),
            (r'```', 'code blocks'),
            (r'\|', 'tables'),
            (r'#{1,3}\s+', 'headers')
        ]
        
        for pattern, name in indicators:
            if re.search(pattern, content, re.IGNORECASE):
                score += 10
        
        # Penalize vague requests
        vague_patterns = [
            r'\b(something|anything|whatever)\b',
            r'\b(etc|and so on|and more)\b',
        ]
        
        for pattern in vague_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score -= 10
        
        return max(0, min(100, score))
    
    def _score_structure(self, content: str) -> float:
        """Score prompt structure (0-100)"""
        score = 50
        
        # Reward good structure
        if '#' in content:
            score += 15
        if '```' in content:
            score += 10
        if '-' in content or '*' in content:
            score += 5
        if re.search(r'\d+\.', content):
            score += 5
        
        # Reward proper formatting
        lines = content.split('\n')
        if len(lines) > 1:
            avg_line_length = sum(len(l) for l in lines) / len(lines)
            if 20 < avg_line_length < 100:
                score += 10
        
        # Penalize wall of text
        if len(content) > 500 and '\n\n' not in content:
            score -= 20
        
        return max(0, min(100, score))
    
    def _score_completeness(self, content: str) -> float:
        """Score prompt completeness (0-100)"""
        score = 50
        
        # Check for key elements
        elements = [
            (r'\b(context|background)\b', 'context'),
            (r'\b(task|goal|objective)\b', 'objective'),
            (r'\b(requirement|constraint)\b', 'constraints'),
            (r'\b(output|result|deliverable)\b', 'expected output'),
            (r'\b(example|sample)\b', 'examples'),
        ]
        
        for pattern, name in elements:
            if re.search(pattern, content, re.IGNORECASE):
                score += 10
        
        return max(0, min(100, score))
    
    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        elif score >= 40:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze prompt structure"""
        return {
            'has_headers': '#' in content,
            'has_code_blocks': '```' in content,
            'has_lists': bool(re.search(r'^[\s]*[-*\d]', content, re.MULTILINE)),
            'has_tables': '|' in content,
            'has_formatting': '**' in content or '*' in content.replace('```', ''),
            'sections': len(re.findall(r'^#+\s', content, re.MULTILINE)),
            'code_blocks': content.count('```') // 2
        }
    
    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze prompt content"""
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = Counter(words)
        
        # Find repeated words
        repeated = {word: count for word, count in word_freq.items() if count > 3}
        
        # Check for instruction words
        instruction_words = [
            'explain', 'describe', 'analyze', 'compare', 'contrast',
            'list', 'summarize', 'generate', 'create', 'write',
            'provide', 'give', 'show', 'tell', 'make'
        ]
        
        found_instructions = [
            word for word in instruction_words
            if word in word_freq
        ]
        
        return {
            'unique_words': len(word_freq),
            'total_words': len(words),
            'vocabulary_diversity': round(len(word_freq) / len(words), 3) if words else 0,
            'repeated_words': repeated,
            'instruction_words': found_instructions,
            'questions': content.count('?'),
            'imperatives': len(re.findall(r'\b\w+(?:\s+\w+){0,5}\s*[.!]', content))
        }
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """Analyze readability metrics"""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        if not words or not sentences:
            return {'error': 'Cannot calculate readability'}
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Average syllables per word (simplified)
        def count_syllables(word):
            word = word.lower()
            vowels = 'aeiouy'
            syllables = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = is_vowel
            
            if word.endswith('e'):
                syllables -= 1
            
            return max(1, syllables)
        
        avg_syllables = sum(count_syllables(w) for w in words) / len(words)
        
        # Flesch Reading Ease (simplified)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        
        return {
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_syllables_per_word': round(avg_syllables, 2),
            'flesch_reading_ease': round(flesch_score, 1),
            'difficulty': self._get_difficulty(flesch_score)
        }
    
    def _get_difficulty(self, flesch_score: float) -> str:
        """Get difficulty level from Flesch score"""
        if flesch_score >= 90:
            return 'Very Easy'
        elif flesch_score >= 80:
            return 'Easy'
        elif flesch_score >= 70:
            return 'Fairly Easy'
        elif flesch_score >= 60:
            return 'Standard'
        elif flesch_score >= 50:
            return 'Fairly Difficult'
        elif flesch_score >= 30:
            return 'Difficult'
        else:
            return 'Very Difficult'
    
    def _generate_suggestions(self, content: str) -> List[Dict[str, Any]]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Length suggestions
        word_count = len(content.split())
        if word_count < 20:
            suggestions.append({
                'type': 'warning',
                'category': 'Length',
                'message': 'Prompt is very short. Consider adding more context.'
            })
        elif word_count > 1000:
            suggestions.append({
                'type': 'warning',
                'category': 'Length',
                'message': 'Prompt is very long. Consider breaking it into sections.'
            })
        
        # Structure suggestions
        if '\n\n' not in content and word_count > 100:
            suggestions.append({
                'type': 'suggestion',
                'category': 'Structure',
                'message': 'Consider adding paragraph breaks for better readability.'
            })
        
        if '#' not in content and word_count > 200:
            suggestions.append({
                'type': 'suggestion',
                'category': 'Structure',
                'message': 'Consider using headers to organize content.'
            })
        
        # Content suggestions
        if 'example' not in content.lower():
            suggestions.append({
                'type': 'suggestion',
                'category': 'Content',
                'message': 'Consider adding an example to clarify expected output.'
            })
        
        if not re.search(r'\b(step|first|then|finally)\b', content, re.IGNORECASE):
            suggestions.append({
                'type': 'tip',
                'category': 'Clarity',
                'message': 'Consider requesting step-by-step output for complex tasks.'
            })
        
        # Check for common issues
        if re.search(r'\b(etc|and so on)\b', content, re.IGNORECASE):
            suggestions.append({
                'type': 'warning',
                'category': 'Specificity',
                'message': 'Avoid using "etc." or "and so on." Be specific about requirements.'
            })
        
        return suggestions
    
    def _detailed_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate detailed metrics"""
        return {
            'character_distribution': self._char_distribution(content),
            'word_length_distribution': self._word_length_distribution(content),
            'sentence_type_distribution': self._sentence_types(content)
        }
    
    def _char_distribution(self, content: str) -> Dict[str, int]:
        """Analyze character distribution"""
        return {
            'letters': sum(1 for c in content if c.isalpha()),
            'digits': sum(1 for c in content if c.isdigit()),
            'spaces': sum(1 for c in content if c.isspace()),
            'punctuation': sum(1 for c in content if c in '.,;:!?'),
            'special': sum(1 for c in content if not c.isalnum() and not c.isspace())
        }
    
    def _word_length_distribution(self, content: str) -> Dict[str, int]:
        """Analyze word length distribution"""
        words = re.findall(r'\b\w+\b', content)
        distribution = Counter(len(w) for w in words)
        
        return {
            'short (1-3)': sum(distribution[i] for i in range(1, 4)),
            'medium (4-6)': sum(distribution[i] for i in range(4, 7)),
            'long (7-10)': sum(distribution[i] for i in range(7, 11)),
            'very long (11+)': sum(distribution[i] for i in range(11, max(distribution.keys()) + 1))
        }
    
    def _sentence_types(self, content: str) -> Dict[str, int]:
        """Analyze sentence types"""
        return {
            'questions': content.count('?'),
            'exclamations': content.count('!'),
            'statements': len(re.split(r'[.!?]+', content)) - content.count('?') - content.count('!')
        }
