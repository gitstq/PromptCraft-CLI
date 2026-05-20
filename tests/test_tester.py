"""
Tests for PromptTester
"""

import unittest
from promptcraft.tester import PromptTester, TestStatus


class TestPromptTester(unittest.TestCase):
    """Test cases for PromptTester"""
    
    def setUp(self):
        self.tester = PromptTester()
    
    def test_test_single(self):
        """Test single prompt testing"""
        prompt = "Write a hello world program"
        result = self.tester.test_single(prompt)
        
        self.assertEqual(result.status, TestStatus.SUCCESS)
        self.assertIsNotNone(result.response)
        self.assertIsNotNone(result.latency_ms)
    
    def test_test_batch(self):
        """Test batch testing"""
        prompts = [
            "Prompt 1",
            "Prompt 2",
            "Prompt 3"
        ]
        results = self.tester.test_batch(prompts)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r.status == TestStatus.SUCCESS for r in results))
    
    def test_compare_prompts(self):
        """Test prompt comparison"""
        prompts = ["Prompt A", "Prompt B"]
        comparison = self.tester.compare_prompts(prompts, "Test case")
        
        self.assertEqual(len(comparison.results), 2)
        self.assertIsNotNone(comparison.analysis)
    
    def test_ab_test(self):
        """Test A/B testing"""
        prompt_a = "Version A"
        prompt_b = "Version B"
        test_cases = ["Test 1", "Test 2"]
        
        results = self.tester.ab_test(prompt_a, prompt_b, test_cases)
        
        self.assertIn("prompt_a_wins", results)
        self.assertIn("prompt_b_wins", results)
        self.assertIn("overall_winner", results)
    
    def test_generate_report(self):
        """Test report generation"""
        prompt = "Test"
        result = self.tester.test_single(prompt)
        
        text_report = self.tester.generate_report([result], "text")
        self.assertIn("Test Report", text_report)
        
        json_report = self.tester.generate_report([result], "json")
        self.assertIn("prompt_id", json_report)
        
        md_report = self.tester.generate_report([result], "markdown")
        self.assertIn("# Prompt Test Report", md_report)


if __name__ == '__main__':
    unittest.main()
