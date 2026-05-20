"""
Prompt Analysis Engine - Detects quality issues and provides insights
Prompt分析引擎 - 检测质量问题并提供洞察
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class IssueSeverity(Enum):
    """Issue severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PromptIssue:
    """Represents a detected prompt issue"""
    category: str
    severity: IssueSeverity
    message: str
    suggestion: str
    line_number: Optional[int] = None


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    score: float
    issues: List[PromptIssue]
    strengths: List[str]
    metrics: Dict[str, any]


class PromptAnalyzer:
    """
    Analyzes prompts for quality issues and optimization opportunities
    分析Prompt的质量问题和优化机会
    """
    
    # Quality detection patterns
    VAGUE_TERMS = [
        r'\bgood\b', r'\bbad\b', r'\bbetter\b', r'\bbest\b',
        r'\bnice\b', r'\bperfect\b', r'\bexcellent\b',
        r'\bappropriate\b', r'\bsuitable\b', r'\bproper\b',
        r'\bcorrect\b', r'\bright\b', r'\bwrong\b',
    ]
    
    AMBIGUOUS_WORDS = [
        r'\bit\b', r'\bthis\b', r'\bthat\b', r'\bthese\b', r'\bthose\b',
        r'\bsomething\b', r'\banything\b', r'\beverything\b',
        r'\bsomeone\b', r'\banyone\b', r'\beveryone\b',
    ]
    
    STRUCTURE_MARKERS = {
        'has_instruction': r'\b(?:please|can you|could you|would you|help me|assist me)\b',
        'has_context': r'\b(?:context|background|given|assuming|if|when)\b',
        'has_example': r'\b(?:example|for instance|such as|like|e\.g\.)\b',
        'has_constraint': r'\b(?:must|should|need to|have to|required|only|just)\b',
        'has_output_format': r'\b(?:format|output|return|provide|give me|as|in the form of)\b',
    }
    
    def __init__(self):
        self.vague_pattern = re.compile('|'.join(self.VAGUE_TERMS), re.IGNORECASE)
        self.ambiguous_pattern = re.compile('|'.join(self.AMBIGUOUS_WORDS), re.IGNORECASE)
        self.structure_patterns = {
            key: re.compile(pattern, re.IGNORECASE)
            for key, pattern in self.STRUCTURE_MARKERS.items()
        }
    
    def analyze(self, prompt: str) -> AnalysisResult:
        """
        Perform comprehensive prompt analysis
        执行全面的Prompt分析
        """
        issues = []
        strengths = []
        metrics = self._calculate_metrics(prompt)
        
        # Check for vague terms
        vague_matches = self.vague_pattern.findall(prompt)
        if vague_matches:
            issues.append(PromptIssue(
                category="Clarity",
                severity=IssueSeverity.MEDIUM,
                message=f"Found {len(vague_matches)} vague/subjective term(s): {', '.join(set(vague_matches[:3]))}",
                suggestion="Replace vague terms with specific, measurable criteria"
            ))
        
        # Check for ambiguous references
        ambiguous_matches = self.ambiguous_pattern.findall(prompt)
        if len(ambiguous_matches) > 3:
            issues.append(PromptIssue(
                category="Specificity",
                severity=IssueSeverity.MEDIUM,
                message=f"Excessive use of ambiguous pronouns ({len(ambiguous_matches)} found)",
                suggestion="Use specific nouns instead of pronouns like 'it', 'this', 'that'"
            ))
        
        # Check prompt length
        word_count = len(prompt.split())
        if word_count < 10:
            issues.append(PromptIssue(
                category="Completeness",
                severity=IssueSeverity.HIGH,
                message=f"Prompt is very short ({word_count} words)",
                suggestion="Add more context and specific instructions for better results"
            ))
        elif word_count > 500:
            issues.append(PromptIssue(
                category="Conciseness",
                severity=IssueSeverity.LOW,
                message=f"Prompt is quite long ({word_count} words)",
                suggestion="Consider breaking into smaller, focused prompts or using structured formatting"
            ))
        else:
            strengths.append(f"Optimal length ({word_count} words)")
        
        # Analyze structure
        structure_score = 0
        for key, pattern in self.structure_patterns.items():
            if pattern.search(prompt):
                structure_score += 1
                strengths.append(f"Contains {key.replace('_', ' ')}")
        
        if structure_score < 2:
            issues.append(PromptIssue(
                category="Structure",
                severity=IssueSeverity.MEDIUM,
                message="Prompt lacks structural elements",
                suggestion="Add context, specific instructions, and output format requirements"
            ))
        
        # Check for output format specification
        if not self.structure_patterns['has_output_format'].search(prompt):
            issues.append(PromptIssue(
                category="Output Specification",
                severity=IssueSeverity.HIGH,
                message="No output format specified",
                suggestion="Explicitly state the desired output format (JSON, markdown, bullet points, etc.)"
            ))
        
        # Check for examples
        if not self.structure_patterns['has_example'].search(prompt):
            issues.append(PromptIssue(
                category="Examples",
                severity=IssueSeverity.LOW,
                message="No examples provided",
                suggestion="Consider adding examples to clarify expected output (Few-shot prompting)"
            ))
        
        # Calculate overall score
        score = self._calculate_score(metrics, len(issues), len(strengths))
        
        return AnalysisResult(
            score=score,
            issues=issues,
            strengths=strengths,
            metrics=metrics
        )
    
    def _calculate_metrics(self, prompt: str) -> Dict[str, any]:
        """Calculate various prompt metrics"""
        words = prompt.split()
        sentences = re.split(r'[.!?]+', prompt)
        
        return {
            "word_count": len(words),
            "char_count": len(prompt),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "question_marks": prompt.count('?'),
            "exclamation_marks": prompt.count('!'),
            "has_code_blocks": '```' in prompt or '`' in prompt,
            "has_lists": bool(re.search(r'^\s*[-*\d]\.', prompt, re.MULTILINE)),
        }
    
    def _calculate_score(self, metrics: Dict, issue_count: int, strength_count: int) -> float:
        """Calculate overall prompt quality score (0-100)"""
        base_score = 70
        
        # Adjust for issues
        base_score -= issue_count * 5
        
        # Adjust for strengths
        base_score += strength_count * 3
        
        # Length bonus/penalty
        word_count = metrics.get("word_count", 0)
        if 20 <= word_count <= 200:
            base_score += 10
        elif word_count < 10:
            base_score -= 20
        
        # Structure bonus
        if metrics.get("has_code_blocks"):
            base_score += 5
        if metrics.get("has_lists"):
            base_score += 3
        
        return max(0, min(100, base_score))
    
    def get_quick_tips(self) -> List[str]:
        """Return list of quick optimization tips"""
        return [
            "🎯 Be specific: Replace 'good' with specific criteria",
            "📋 Use structure: Context → Instructions → Output Format",
            "💡 Add examples: Show, don't just tell",
            "🔍 Define constraints: Set clear boundaries",
            "📊 Specify format: JSON, markdown, bullet points, etc.",
            "📝 Use delimiters: Separate instructions from context",
            "🎭 Assign role: 'Act as an expert...' for better results",
            "⛓️ Chain prompts: Break complex tasks into steps",
        ]
