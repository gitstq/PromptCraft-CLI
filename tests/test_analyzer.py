"""
Tests for PromptAnalyzer
"""

import unittest
from promptcraft.analyzer import PromptAnalyzer, IssueSeverity


class TestPromptAnalyzer(unittest.TestCase):
    """Test cases for PromptAnalyzer"""
    
    def setUp(self):
        self.analyzer = PromptAnalyzer()
    
    def test_analyze_short_prompt(self):
        """Test analyzing a short prompt"""
        result = self.analyzer.analyze("Hello")
        self.assertLess(result.score, 60)  # Short prompts should score low
        self.assertTrue(any("short" in issue.message.lower() for issue in result.issues))
    
    def test_analyze_good_prompt(self):
        """Test analyzing a well-structured prompt"""
        prompt = """Context: You are a Python expert.

Task: Write a function to calculate factorial.

Output format: Python code with docstring."""
        
        result = self.analyzer.analyze(prompt)
        self.assertGreater(result.score, 60)  # Good prompts should score higher
        self.assertTrue(len(result.strengths) > 0)
    
    def test_detect_vague_terms(self):
        """Test detection of vague terms"""
        prompt = "Give me a good solution to this problem."
        result = self.analyzer.analyze(prompt)
        
        vague_issues = [i for i in result.issues if i.category == "Clarity"]
        self.assertTrue(len(vague_issues) > 0)
    
    def test_detect_ambiguous_pronouns(self):
        """Test detection of ambiguous pronouns"""
        prompt = "It is important. This should be done. That is correct. Those are wrong. These work well."
        result = self.analyzer.analyze(prompt)
        
        ambiguous_issues = [i for i in result.issues if i.category == "Specificity"]
        self.assertTrue(len(ambiguous_issues) > 0)
    
    def test_metrics_calculation(self):
        """Test metrics are calculated correctly"""
        prompt = "Hello world. This is a test!"
        result = self.analyzer.analyze(prompt)
        
        self.assertIn("word_count", result.metrics)
        self.assertIn("sentence_count", result.metrics)
        self.assertEqual(result.metrics["word_count"], 6)
    
    def test_quick_tips(self):
        """Test quick tips are returned"""
        tips = self.analyzer.get_quick_tips()
        self.assertTrue(len(tips) > 0)
        self.assertTrue(all(isinstance(tip, str) for tip in tips))


if __name__ == '__main__':
    unittest.main()
