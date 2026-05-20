"""
Tests for PromptOptimizer
"""

import unittest
from promptcraft.optimizer import PromptOptimizer, OptimizationStrategy


class TestPromptOptimizer(unittest.TestCase):
    """Test cases for PromptOptimizer"""
    
    def setUp(self):
        self.optimizer = PromptOptimizer()
    
    def test_optimize_structured(self):
        """Test structured optimization"""
        prompt = "Context: Python project. Write a Python function. Output: code."
        result = self.optimizer.optimize(prompt, OptimizationStrategy.STRUCTURED)
        
        self.assertIn("##", result.optimized)  # Has section headers
        self.assertEqual(result.strategy, OptimizationStrategy.STRUCTURED)
    
    def test_optimize_few_shot(self):
        """Test few-shot optimization"""
        prompt = "Classify sentiment"
        result = self.optimizer.optimize(prompt, OptimizationStrategy.FEW_SHOT)
        
        self.assertIn("Example 1", result.optimized)
        self.assertIn("Example 2", result.optimized)
        self.assertEqual(result.strategy, OptimizationStrategy.FEW_SHOT)
    
    def test_optimize_cot(self):
        """Test chain-of-thought optimization"""
        prompt = "Solve this math problem"
        result = self.optimizer.optimize(prompt, OptimizationStrategy.CHAIN_OF_THOUGHT)
        
        self.assertIn("step-by-step", result.optimized.lower())
        self.assertEqual(result.strategy, OptimizationStrategy.CHAIN_OF_THOUGHT)
    
    def test_optimize_react(self):
        """Test ReAct optimization"""
        prompt = "Search for information"
        result = self.optimizer.optimize(prompt, OptimizationStrategy.REACT)
        
        self.assertIn("Thought:", result.optimized)
        self.assertIn("Action:", result.optimized)
        self.assertEqual(result.strategy, OptimizationStrategy.REACT)
    
    def test_auto_select_strategy(self):
        """Test auto-selection of strategy"""
        # Should select few_shot for prompts with examples
        prompt_with_example = "Do this. For example: ..."
        result = self.optimizer.optimize(prompt_with_example)
        self.assertEqual(result.strategy, OptimizationStrategy.FEW_SHOT)
    
    def test_optimize_all(self):
        """Test generating all optimizations"""
        prompt = "Test prompt"
        results = self.optimizer.optimize_all(prompt)
        
        self.assertEqual(len(results), len(OptimizationStrategy))
        strategies = [r.strategy for r in results]
        self.assertEqual(len(set(strategies)), len(strategies))  # All unique
    
    def test_compare_strategies(self):
        """Test strategy comparison"""
        prompt = "Test prompt"
        comparison = self.optimizer.compare_strategies(prompt)
        
        self.assertIn("strategies", comparison)
        self.assertIn("recommendation", comparison)
        self.assertTrue(len(comparison["strategies"]) > 0)


if __name__ == '__main__':
    unittest.main()
