"""
Prompt testing and A/B testing functionality
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

from promptcraft.core.config import Config
from promptcraft.core.prompt_manager import PromptManager


class PromptTester:
    """Prompt testing engine"""
    
    def __init__(self, config: Config):
        """Initialize tester"""
        self.config = config
        self.manager = PromptManager(config)
    
    def run_ab_test(
        self,
        prompt_id: str,
        versions: Optional[List[str]] = None,
        test_input: str = "",
        iterations: int = 5
    ) -> Dict[str, Any]:
        """Run A/B test on prompt versions"""
        from promptcraft.core.version_control import VersionControl
        
        vc = VersionControl(self.config)
        
        # Get versions to test
        if versions:
            test_versions = []
            for v in versions:
                version_data = vc.get_version(prompt_id, v)
                if version_data:
                    test_versions.append(version_data)
        else:
            # Get last 2 versions
            test_versions = vc.get_version_history(prompt_id, limit=2)
        
        if len(test_versions) < 2:
            return {
                'error': 'Need at least 2 versions to compare',
                'versions_found': len(test_versions)
            }
        
        # Run simulated tests
        results = []
        for version in test_versions:
            version_result = self._test_version(
                version,
                test_input,
                iterations
            )
            results.append(version_result)
        
        # Compare results
        comparison = self._compare_results(results)
        
        return {
            'prompt_id': prompt_id,
            'test_date': datetime.now().isoformat(),
            'iterations': iterations,
            'versions_tested': len(test_versions),
            'results': results,
            'comparison': comparison,
            'recommendation': self._generate_recommendation(results, comparison)
        }
    
    def _test_version(
        self,
        version: Dict[str, Any],
        test_input: str,
        iterations: int
    ) -> Dict[str, Any]:
        """Test a single version (simulated)"""
        # In a real implementation, this would call an LLM API
        # For now, we'll simulate metrics based on prompt characteristics
        
        content = version['content']
        
        # Simulate metrics
        metrics = {
            'clarity_score': self._simulate_clarity(content),
            'response_time': self._simulate_response_time(content),
            'token_usage': self._estimate_tokens(content, test_input),
            'consistency_score': self._simulate_consistency(content, iterations),
            'completeness_score': self._simulate_completeness(content)
        }
        
        # Calculate overall score
        overall = sum(metrics.values()) / len(metrics)
        
        return {
            'version_id': version['id'],
            'metrics': metrics,
            'overall_score': round(overall, 2),
            'test_runs': iterations
        }
    
    def _simulate_clarity(self, content: str) -> float:
        """Simulate clarity score based on prompt characteristics"""
        score = 70.0
        
        # Factors that improve clarity
        if '#' in content:
            score += 10
        if '```' in content:
            score += 5
        if len(content.split('.')) > 3:
            score += 5
        
        # Factors that reduce clarity
        if len(content) > 1000:
            score -= 10
        if content.count('and') > 10:
            score -= 5
        
        return round(min(100, max(0, score)), 1)
    
    def _simulate_response_time(self, content: str) -> float:
        """Simulate response time in seconds"""
        base_time = 1.0
        word_count = len(content.split())
        
        # Longer prompts take longer to process
        time_estimate = base_time + (word_count / 100)
        
        return round(time_estimate, 2)
    
    def _estimate_tokens(self, prompt: str, input_text: str) -> int:
        """Estimate token usage"""
        # Rough estimation: ~1.3 tokens per word
        total_words = len(prompt.split()) + len(input_text.split())
        return int(total_words * 1.3)
    
    def _simulate_consistency(self, content: str, iterations: int) -> float:
        """Simulate consistency score"""
        # More structured prompts are more consistent
        score = 75.0
        
        if '#' in content:
            score += 10
        if re.search(r'\d+\.', content):
            score += 5
        if 'example' in content.lower():
            score += 5
        
        return round(min(100, score), 1)
    
    def _simulate_completeness(self, content: str) -> float:
        """Simulate completeness score"""
        score = 70.0
        
        # Check for completeness indicators
        indicators = [
            'context', 'example', 'output', 'format',
            'step', 'requirement', 'constraint'
        ]
        
        for indicator in indicators:
            if indicator in content.lower():
                score += 3
        
        return round(min(100, score), 1)
    
    def _compare_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare test results"""
        if len(results) < 2:
            return {}
        
        winner = max(results, key=lambda x: x['overall_score'])
        loser = min(results, key=lambda x: x['overall_score'])
        
        # Calculate improvements
        improvements = {}
        for metric in winner['metrics']:
            if metric in loser['metrics']:
                diff = winner['metrics'][metric] - loser['metrics'][metric]
                improvements[metric] = round(diff, 2)
        
        return {
            'winner': winner['version_id'],
            'winner_score': winner['overall_score'],
            'loser': loser['version_id'],
            'loser_score': loser['overall_score'],
            'score_difference': round(winner['overall_score'] - loser['overall_score'], 2),
            'improvements': improvements
        }
    
    def _generate_recommendation(
        self,
        results: List[Dict[str, Any]],
        comparison: Dict[str, Any]
    ) -> str:
        """Generate test recommendation"""
        if not comparison:
            return "Insufficient data for recommendation"
        
        winner = comparison['winner']
        score_diff = comparison['score_difference']
        
        if score_diff > 10:
            return f"Version {winner} is significantly better. Consider adopting this version."
        elif score_diff > 5:
            return f"Version {winner} shows moderate improvement. Worth considering."
        elif score_diff > 2:
            return f"Version {winner} is slightly better. Marginal improvement."
        else:
            return "Versions perform similarly. Choose based on other criteria."
    
    def save_test_report(
        self,
        prompt_id: str,
        results: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> bool:
        """Save test report to file"""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"test_report_{prompt_id}_{timestamp}.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            return True
        except IOError as e:
            print(f"Error: Failed to save test report: {e}")
            return False
