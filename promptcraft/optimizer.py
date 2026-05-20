"""
Prompt Optimization Engine - Applies various optimization strategies
Prompt优化引擎 - 应用各种优化策略
"""

import re
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class OptimizationStrategy(Enum):
    """Available optimization strategies"""
    STRUCTURED = "structured"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    REACT = "react"
    ROLE_BASED = "role_based"
    CONSTRAINT_FOCUS = "constraint_focus"


@dataclass
class OptimizationResult:
    """Result of prompt optimization"""
    original: str
    optimized: str
    strategy: OptimizationStrategy
    improvements: List[str]
    estimated_impact: str


class PromptOptimizer:
    """
    Applies various prompt engineering techniques to improve prompt quality
    应用各种Prompt工程技术来提高Prompt质量
    """
    
    def __init__(self):
        self.strategies: Dict[OptimizationStrategy, Callable] = {
            OptimizationStrategy.STRUCTURED: self._apply_structured,
            OptimizationStrategy.FEW_SHOT: self._apply_few_shot,
            OptimizationStrategy.CHAIN_OF_THOUGHT: self._apply_cot,
            OptimizationStrategy.REACT: self._apply_react,
            OptimizationStrategy.ROLE_BASED: self._apply_role_based,
            OptimizationStrategy.CONSTRAINT_FOCUS: self._apply_constraint_focus,
        }
    
    def optimize(self, prompt: str, strategy: OptimizationStrategy = None) -> OptimizationResult:
        """
        Optimize a prompt using specified or auto-selected strategy
        使用指定或自动选择的策略优化Prompt
        """
        if strategy is None:
            strategy = self._select_best_strategy(prompt)
        
        optimizer_func = self.strategies.get(strategy, self._apply_structured)
        return optimizer_func(prompt)
    
    def optimize_all(self, prompt: str) -> List[OptimizationResult]:
        """
        Generate optimized versions using all strategies
        使用所有策略生成优化版本
        """
        results = []
        for strategy in OptimizationStrategy:
            try:
                result = self.optimize(prompt, strategy)
                results.append(result)
            except Exception:
                continue
        return results
    
    def _select_best_strategy(self, prompt: str) -> OptimizationStrategy:
        """Auto-select best strategy based on prompt content"""
        prompt_lower = prompt.lower()
        
        # Check for existing patterns
        if 'example' in prompt_lower or 'e.g.' in prompt_lower:
            return OptimizationStrategy.FEW_SHOT
        elif 'step' in prompt_lower or 'think' in prompt_lower:
            return OptimizationStrategy.CHAIN_OF_THOUGHT
        elif 'act as' in prompt_lower or 'role' in prompt_lower:
            return OptimizationStrategy.ROLE_BASED
        elif 'search' in prompt_lower or 'calculate' in prompt_lower:
            return OptimizationStrategy.REACT
        else:
            return OptimizationStrategy.STRUCTURED
    
    def _apply_structured(self, prompt: str) -> OptimizationResult:
        """Apply structured formatting optimization"""
        lines = prompt.strip().split('\n')
        
        # Extract components
        context = []
        instruction = []
        output_format = []
        
        current_section = instruction
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in ['context', 'background', 'given']):
                current_section = context
            elif any(word in line_lower for word in ['format', 'output', 'return']):
                current_section = output_format
            current_section.append(line)
        
        # Build structured prompt
        structured_parts = []
        if context:
            structured_parts.append("## Context\n" + '\n'.join(context))
        if instruction:
            structured_parts.append("## Task\n" + '\n'.join(instruction))
        if output_format:
            structured_parts.append("## Output Format\n" + '\n'.join(output_format))
        
        if not structured_parts:
            structured_parts = [
                "## Context\n[Add relevant background information here]",
                "## Task\n" + prompt,
                "## Output Format\n[Specify desired output format]"
            ]
        
        optimized = '\n\n'.join(structured_parts)
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            strategy=OptimizationStrategy.STRUCTURED,
            improvements=[
                "Added clear section headers for better organization",
                "Separated context from instructions",
                "Explicit output format section"
            ],
            estimated_impact="High - Improves clarity and structure significantly"
        )
    
    def _apply_few_shot(self, prompt: str) -> OptimizationResult:
        """Apply few-shot prompting optimization"""
        template = """## Task
{task}

## Examples

### Example 1:
Input: [Example input 1]
Output: [Expected output 1]

### Example 2:
Input: [Example input 2]
Output: [Expected output 2]

### Example 3:
Input: [Example input 3]
Output: [Expected output 3]

## Your Turn
Input: {original_input}
Output:"""
        
        optimized = template.format(
            task=prompt,
            original_input="[Your actual input here]"
        )
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            strategy=OptimizationStrategy.FEW_SHOT,
            improvements=[
                "Added example-based learning pattern",
                "Demonstrates expected input/output format",
                "Enables pattern recognition for better results"
            ],
            estimated_impact="Very High - Examples significantly improve output quality"
        )
    
    def _apply_cot(self, prompt: str) -> OptimizationResult:
        """Apply Chain-of-Thought optimization"""
        cot_instruction = """Let's approach this step-by-step:

1. First, understand the problem and identify key requirements
2. Break down the task into smaller components
3. Analyze each component systematically
4. Synthesize findings into a coherent response
5. Review and verify the solution

Now, let's begin:"""
        
        optimized = f"{prompt}\n\n{cot_instruction}"
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            strategy=OptimizationStrategy.CHAIN_OF_THOUGHT,
            improvements=[
                "Added step-by-step reasoning instruction",
                "Encourages systematic problem-solving",
                "Improves accuracy for complex tasks"
            ],
            estimated_impact="High - CoT improves reasoning on complex problems"
        )
    
    def _apply_react(self, prompt: str) -> OptimizationResult:
        """Apply ReAct (Reasoning + Acting) optimization"""
        react_template = """You will solve this problem using the ReAct pattern:

Thought: Consider what you need to know or do
Action: Take an action (search, calculate, etc.)
Observation: Note what you learned from the action
... (repeat Thought/Action/Observation as needed)
Final Answer: Provide your final response

## Problem
{problem}

Begin:
Thought:"""
        
        optimized = react_template.format(problem=prompt)
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            strategy=OptimizationStrategy.REACT,
            improvements=[
                "Integrated reasoning and action steps",
                "Enables tool use and external knowledge",
                "Structured problem-solving workflow"
            ],
            estimated_impact="Very High - ReAct excels at complex multi-step tasks"
        )
    
    def _apply_role_based(self, prompt: str) -> OptimizationResult:
        """Apply role-based optimization"""
        roles = [
            "expert software engineer",
            "senior data scientist",
            "technical writer",
            "product manager",
            "security analyst"
        ]
        
        role_prompt = f"""You are an {roles[0]} with 10+ years of experience. 
Your expertise includes deep technical knowledge, best practices, and industry standards.
Approach this task with professional rigor and attention to detail.

## Request
{prompt}

Please provide your expert analysis and recommendations."""
        
        return OptimizationResult(
            original=prompt,
            optimized=role_prompt,
            strategy=OptimizationStrategy.ROLE_BASED,
            improvements=[
                "Assigned expert role for higher quality responses",
                "Sets professional tone and expectations",
                "Leverages persona for domain-specific knowledge"
            ],
            estimated_impact="Medium-High - Role assignment improves response quality"
        )
    
    def _apply_constraint_focus(self, prompt: str) -> OptimizationResult:
        """Apply constraint-focused optimization"""
        constraint_template = """{original}

## Constraints & Requirements
- Be concise and direct in your response
- Focus on actionable insights
- Avoid unnecessary explanations
- If uncertain, acknowledge limitations clearly
- Prioritize accuracy over completeness
- Use specific examples where applicable"""
        
        optimized = constraint_template.format(original=prompt)
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            strategy=OptimizationStrategy.CONSTRAINT_FOCUS,
            improvements=[
                "Added explicit constraints and boundaries",
                "Clarifies expectations and limitations",
                "Reduces unwanted verbosity"
            ],
            estimated_impact="Medium - Helps focus responses but depends on task"
        )
    
    def compare_strategies(self, prompt: str) -> Dict[str, any]:
        """Compare all optimization strategies"""
        results = self.optimize_all(prompt)
        
        comparison = {
            "original": prompt,
            "strategies": [],
            "recommendation": None
        }
        
        best_strategy = None
        best_score = -1
        
        for result in results:
            # Simple scoring based on estimated impact
            score = 0
            if "Very High" in result.estimated_impact:
                score = 4
            elif "High" in result.estimated_impact:
                score = 3
            elif "Medium-High" in result.estimated_impact:
                score = 2
            elif "Medium" in result.estimated_impact:
                score = 1
            
            comparison["strategies"].append({
                "name": result.strategy.value,
                "optimized_preview": result.optimized[:200] + "..." if len(result.optimized) > 200 else result.optimized,
                "improvements": result.improvements,
                "estimated_impact": result.estimated_impact,
                "score": score
            })
            
            if score > best_score:
                best_score = score
                best_strategy = result.strategy.value
        
        comparison["recommendation"] = best_strategy
        return comparison
