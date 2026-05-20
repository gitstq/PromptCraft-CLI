"""
Prompt Testing Engine - Batch testing and comparison functionality
Prompt测试引擎 - 批量测试与对比功能
"""

import time
import json
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class TestResult:
    """Result of a single test"""
    prompt_id: str
    prompt_content: str
    status: TestStatus
    response: Optional[str] = None
    latency_ms: Optional[int] = None
    token_count: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class TestSuite:
    """A collection of tests"""
    id: str
    name: str
    description: str
    created_at: str
    results: List[TestResult]


@dataclass
class ComparisonResult:
    """Result of comparing multiple prompts"""
    prompts: List[str]
    test_case: str
    results: List[TestResult]
    winner_id: Optional[str] = None
    analysis: Optional[str] = None


class PromptTester:
    """
    Manages prompt testing, batch execution, and comparison
    管理Prompt测试、批量执行和对比
    """
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.test_history: List[TestSuite] = []
    
    def test_single(self, prompt: str, provider: str = "mock",
                    timeout: int = 30) -> TestResult:
        """
        Test a single prompt
        测试单个Prompt
        """
        import hashlib
        prompt_id = hashlib.md5(prompt.encode()).hexdigest()[:8]
        
        result = TestResult(
            prompt_id=prompt_id,
            prompt_content=prompt[:100] + "..." if len(prompt) > 100 else prompt,
            status=TestStatus.RUNNING,
            timestamp=self._get_timestamp()
        )
        
        try:
            start_time = time.time()
            
            # Mock provider for demonstration
            if provider == "mock":
                response = self._mock_llm_call(prompt)
            else:
                response = f"[Provider {provider} not implemented in demo]"
            
            end_time = time.time()
            
            result.status = TestStatus.SUCCESS
            result.response = response
            result.latency_ms = int((end_time - start_time) * 1000)
            result.token_count = len(prompt.split()) + len(response.split())
            
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        
        return result
    
    def test_batch(self, prompts: List[str], provider: str = "mock",
                   timeout: int = 30) -> List[TestResult]:
        """
        Test multiple prompts in batch
        批量测试多个Prompt
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_prompt = {
                executor.submit(self.test_single, prompt, provider, timeout): prompt
                for prompt in prompts
            }
            
            for future in as_completed(future_to_prompt):
                try:
                    result = future.result(timeout=timeout)
                    results.append(result)
                except Exception as e:
                    prompt = future_to_prompt[future]
                    import hashlib
                    results.append(TestResult(
                        prompt_id=hashlib.md5(prompt.encode()).hexdigest()[:8],
                        prompt_content=prompt[:100] + "...",
                        status=TestStatus.FAILED,
                        error_message=str(e),
                        timestamp=self._get_timestamp()
                    ))
        
        return results
    
    def compare_prompts(self, prompts: List[str], test_case: str,
                        provider: str = "mock") -> ComparisonResult:
        """
        Compare multiple prompts on the same test case
        在同一测试用例上对比多个Prompt
        """
        results = self.test_batch(prompts, provider)
        
        # Simple winner selection based on response length and success
        winner = None
        best_score = -1
        
        for result in results:
            if result.status == TestStatus.SUCCESS:
                score = len(result.response) if result.response else 0
                # Bonus for faster responses
                if result.latency_ms and result.latency_ms < 1000:
                    score += 100
                
                if score > best_score:
                    best_score = score
                    winner = result.prompt_id
        
        # Generate analysis
        analysis = self._generate_comparison_analysis(results, test_case)
        
        return ComparisonResult(
            prompts=prompts,
            test_case=test_case,
            results=results,
            winner_id=winner,
            analysis=analysis
        )
    
    def ab_test(self, prompt_a: str, prompt_b: str, test_cases: List[str],
                provider: str = "mock") -> Dict[str, Any]:
        """
        Perform A/B testing between two prompts
        对两个Prompt进行A/B测试
        """
        results = {
            "prompt_a_wins": 0,
            "prompt_b_wins": 0,
            "ties": 0,
            "details": []
        }
        
        for test_case in test_cases:
            comparison = self.compare_prompts([prompt_a, prompt_b], test_case, provider)
            
            detail = {
                "test_case": test_case,
                "winner": comparison.winner_id,
                "results": [
                    {
                        "prompt_id": r.prompt_id,
                        "status": r.status.value,
                        "latency_ms": r.latency_ms,
                        "token_count": r.token_count
                    }
                    for r in comparison.results
                ]
            }
            results["details"].append(detail)
            
            # Determine winner (simplified)
            if comparison.winner_id:
                import hashlib
                a_id = hashlib.md5(prompt_a.encode()).hexdigest()[:8]
                if comparison.winner_id == a_id:
                    results["prompt_a_wins"] += 1
                else:
                    results["prompt_b_wins"] += 1
            else:
                results["ties"] += 1
        
        # Overall winner
        total_tests = len(test_cases)
        if results["prompt_a_wins"] > results["prompt_b_wins"]:
            results["overall_winner"] = "A"
        elif results["prompt_b_wins"] > results["prompt_a_wins"]:
            results["overall_winner"] = "B"
        else:
            results["overall_winner"] = "Tie"
        
        results["win_rate_a"] = results["prompt_a_wins"] / total_tests * 100
        results["win_rate_b"] = results["prompt_b_wins"] / total_tests * 100
        
        return results
    
    def _mock_llm_call(self, prompt: str) -> str:
        """Mock LLM call for demonstration"""
        # Simulate processing time
        time.sleep(0.1)
        
        prompt_lower = prompt.lower()
        
        if "code" in prompt_lower or "program" in prompt_lower:
            return """Here's a sample code solution:\n\n```python\ndef example():\n    return \"Hello, World!\"\n```\n\nThis code defines a simple function that returns a greeting."""
        
        elif "explain" in prompt_lower or "what is" in prompt_lower:
            return """This is an explanation of the requested topic:\n\nKey points:\n1. First important concept\n2. Second important concept\n3. Third important concept\n\nIn summary, understanding these points will help you grasp the topic better."""
        
        elif "list" in prompt_lower or "enumerate" in prompt_lower:
            return """Here's the requested list:\n\n1. Item One - Description of first item\n2. Item Two - Description of second item\n3. Item Three - Description of third item\n4. Item Four - Description of fourth item\n\nThese items cover the main aspects of your request."""
        
        else:
            return """I've processed your request. Here's my response:\n\nBased on the information provided, I can offer the following insights:\n\n- The prompt is well-structured\n- Key elements have been identified\n- A comprehensive response has been generated\n\nIs there anything specific you'd like me to elaborate on?"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_comparison_analysis(self, results: List[TestResult], 
                                      test_case: str) -> str:
        """Generate analysis text for comparison"""
        successful = [r for r in results if r.status == TestStatus.SUCCESS]
        failed = [r for r in results if r.status != TestStatus.SUCCESS]
        
        lines = [
            f"Comparison Analysis for: {test_case[:50]}...",
            f"",
            f"Successful responses: {len(successful)}/{len(results)}",
            f"Failed responses: {len(failed)}/{len(results)}",
        ]
        
        if successful:
            avg_latency = sum(r.latency_ms for r in successful if r.latency_ms) / len(successful)
            lines.extend([
                f"",
                f"Average latency: {avg_latency:.0f}ms",
            ])
        
        return "\n".join(lines)
    
    def generate_report(self, results: List[TestResult], 
                        format_type: str = "text") -> str:
        """Generate test report in various formats"""
        if format_type == "json":
            def serialize(obj):
                if isinstance(obj, TestStatus):
                    return obj.value
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            return json.dumps([asdict(r) for r in results], indent=2, default=serialize)
        
        elif format_type == "markdown":
            lines = ["# Prompt Test Report", ""]
            
            for i, result in enumerate(results, 1):
                lines.extend([
                    f"## Test {i}",
                    f"- **Status**: {result.status.value}",
                    f"- **Prompt ID**: {result.prompt_id}",
                    f"- **Latency**: {result.latency_ms}ms" if result.latency_ms else "- **Latency**: N/A",
                    f"- **Tokens**: {result.token_count}" if result.token_count else "- **Tokens**: N/A",
                    f"",
                    f"### Response",
                    f"```",
                    f"{result.response or 'No response'}",
                    f"```",
                    f""
                ])
                
                if result.error_message:
                    lines.extend([
                        f"### Error",
                        f"```",
                        f"{result.error_message}",
                        f"```",
                        f""
                    ])
            
            return "\n".join(lines)
        
        else:  # text format
            lines = ["Prompt Test Report", "=" * 50, ""]
            
            for i, result in enumerate(results, 1):
                lines.extend([
                    f"Test {i}: {result.status.value.upper()}",
                    f"Prompt: {result.prompt_content[:80]}...",
                    f"Latency: {result.latency_ms}ms" if result.latency_ms else "Latency: N/A",
                ])
                
                if result.response:
                    lines.append(f"Response preview: {result.response[:100]}...")
                
                if result.error_message:
                    lines.append(f"Error: {result.error_message}")
                
                lines.append("")
            
            return "\n".join(lines)
