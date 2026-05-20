"""
Console UI for PromptCraft CLI
"""

import sys
import json
from typing import List, Dict, Any, Optional


class ConsoleUI:
    """Console user interface"""
    
    def __init__(self, quiet: bool = False):
        """Initialize UI"""
        self.quiet = quiet
        self.colors = self._supports_colors()
    
    def _supports_colors(self) -> bool:
        """Check if terminal supports colors"""
        if sys.platform == 'win32':
            return False
        if not sys.stdout.isatty():
            return False
        return True
    
    def _color(self, text: str, color: str) -> str:
        """Apply color to text"""
        if not self.colors:
            return text
        
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        
        return f"{colors.get(color, '')}{text}{colors['reset']}"
    
    def print(self, message: str, color: Optional[str] = None):
        """Print message"""
        if not self.quiet:
            if color:
                print(self._color(message, color))
            else:
                print(message)
    
    def info(self, message: str):
        """Print info message"""
        self.print(message, 'blue')
    
    def success(self, message: str):
        """Print success message"""
        self.print(message, 'green')
    
    def warning(self, message: str):
        """Print warning message"""
        self.print(message, 'yellow')
    
    def error(self, message: str):
        """Print error message"""
        self.print(message, 'red')
    
    def confirm(self, message: str) -> bool:
        """Ask for confirmation"""
        if self.quiet:
            return True
        
        response = input(f"{message} [y/N]: ").strip().lower()
        return response in ('y', 'yes')
    
    def show_prompts(self, prompts: List[Dict[str, Any]], format: str = 'table'):
        """Display prompts list"""
        if format == 'json':
            print(json.dumps(prompts, indent=2, ensure_ascii=False))
        elif format == 'csv':
            print("ID,Name,Category,Tags,Version,Updated")
            for p in prompts:
                tags = '|'.join(p.get('tags', []))
                print(f"\"{p['id']}\",\"{p['name']}\",\"{p.get('category', 'general')}\",\"{tags}\",{p.get('version', 1)},\"{p.get('updated_at', '')}\"")
        else:
            # Table format
            if not prompts:
                self.info("No prompts found")
                return
            
            # Calculate column widths
            id_width = max(len(p['id']) for p in prompts)
            name_width = min(max(len(p['name']) for p in prompts), 30)
            cat_width = max(len(p.get('category', 'general')) for p in prompts)
            
            # Header
            header = f"{'ID':<{id_width}}  {'Name':<{name_width}}  {'Category':<{cat_width}}  {'Ver':>3}  {'Tags'}"
            print(self._color(header, 'bold'))
            print(self._color('-' * len(header), 'cyan'))
            
            # Rows
            for p in prompts:
                name = p['name'][:name_width-3] + '...' if len(p['name']) > name_width else p['name']
                tags = ', '.join(p.get('tags', []))[:30]
                row = f"{p['id']:<{id_width}}  {name:<{name_width}}  {p.get('category', 'general'):<{cat_width}}  {p.get('version', 1):>3}  {tags}"
                print(row)
            
            print(f"\nTotal: {len(prompts)} prompt(s)")
    
    def show_prompt_detail(self, prompt: Dict[str, Any]):
        """Display prompt details"""
        print()
        print(self._color(f"📋 {prompt['name']}", 'bold'))
        print(self._color('=' * 50, 'cyan'))
        
        print(f"\n{self._color('ID:', 'yellow')} {prompt['id']}")
        print(f"{self._color('Category:', 'yellow')} {prompt.get('category', 'general')}")
        print(f"{self._color('Tags:', 'yellow')} {', '.join(prompt.get('tags', [])) or 'None'}")
        print(f"{self._color('Version:', 'yellow')} {prompt.get('version', 1)}")
        print(f"{self._color('Created:', 'yellow')} {prompt.get('created_at', 'Unknown')}")
        print(f"{self._color('Updated:', 'yellow')} {prompt.get('updated_at', 'Unknown')}")
        
        if prompt.get('description'):
            print(f"\n{self._color('Description:', 'yellow')}")
            print(prompt['description'])
        
        print(f"\n{self._color('Content:', 'yellow')}")
        print(self._color('-' * 50, 'cyan'))
        print(prompt['content'])
        print(self._color('-' * 50, 'cyan'))
        
        if 'metadata' in prompt:
            print(f"\n{self._color('Statistics:', 'yellow')}")
            meta = prompt['metadata']
            print(f"  Words: {meta.get('word_count', 'N/A')}")
            print(f"  Characters: {meta.get('char_count', 'N/A')}")
            print(f"  Lines: {meta.get('line_count', 'N/A')}")
    
    def show_version_history(self, versions: List[Dict[str, Any]]):
        """Display version history"""
        print()
        print(self._color("📜 Version History", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        for v in versions:
            print(f"\n{self._color(v['id'], 'green')} - {v['timestamp']}")
            print(f"  {self._color('Author:', 'yellow')} {v.get('author', 'Unknown')}")
            print(f"  {self._color('Message:', 'yellow')} {v.get('message', 'No message')}")
            print(f"  {self._color('Size:', 'yellow')} {v.get('size', 0)} bytes")
    
    def show_diff(self, v1: Dict[str, Any], v2: Dict[str, Any], v1_label: str, v2_label: str):
        """Display diff between two versions"""
        print()
        print(self._color(f"🔍 Comparing {v1_label} vs {v2_label}", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        print(f"\n{self._color('--- ' + v1_label, 'red')}")
        print(f"{self._color('+++ ' + v2_label, 'green')}")
        
        # Simple line-by-line diff
        lines1 = v1['content'].split('\n')
        lines2 = v2['content'].split('\n')
        
        max_lines = max(len(lines1), len(lines2))
        
        print()
        for i in range(max_lines):
            line1 = lines1[i] if i < len(lines1) else None
            line2 = lines2[i] if i < len(lines2) else None
            
            if line1 != line2:
                if line1:
                    print(self._color(f"- {line1}", 'red'))
                if line2:
                    print(self._color(f"+ {line2}", 'green'))
    
    def show_optimization_result(self, result: Dict[str, Any]):
        """Display optimization result"""
        print()
        print(self._color("🔧 Optimization Result", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        print(f"\n{self._color('Optimizations Applied:', 'yellow')}")
        for opt in result.get('optimizations', []):
            print(f"  ✓ {opt}")
        
        improvements = result.get('improvements', {})
        print(f"\n{self._color('Improvements:', 'yellow')}")
        print(f"  Original length: {improvements.get('original_length', 'N/A')} chars")
        print(f"  Optimized length: {improvements.get('optimized_length', 'N/A')} chars")
        print(f"  Reduction: {improvements.get('reduction', 'N/A')} chars ({improvements.get('reduction_percent', 'N/A')}%)")
        
        print(f"\n{self._color('Optimized Content:', 'yellow')}")
        print(self._color('-' * 60, 'cyan'))
        print(result['content'])
        print(self._color('-' * 60, 'cyan'))
    
    def show_test_results(self, results: Dict[str, Any]):
        """Display test results"""
        print()
        print(self._color("🧪 A/B Test Results", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        if 'error' in results:
            self.error(f"Error: {results['error']}")
            return
        
        print(f"\n{self._color('Versions Tested:', 'yellow')} {results['versions_tested']}")
        print(f"{self._color('Iterations:', 'yellow')} {results['iterations']}")
        
        print(f"\n{self._color('Results:', 'yellow')}")
        for r in results.get('results', []):
            print(f"\n  {self._color(r['version_id'], 'green')} - Score: {r['overall_score']}")
            for metric, value in r['metrics'].items():
                print(f"    {metric}: {value}")
        
        comparison = results.get('comparison', {})
        if comparison:
            print(f"\n{self._color('Comparison:', 'yellow')}")
            print(f"  Winner: {self._color(comparison['winner'], 'green')} ({comparison['winner_score']})")
            print(f"  Difference: +{comparison['score_difference']} points")
        
        print(f"\n{self._color('Recommendation:', 'yellow')}")
        print(f"  {results.get('recommendation', 'No recommendation')}")
    
    def show_templates(self, templates: List[Dict[str, Any]]):
        """Display template list"""
        print()
        print(self._color("📋 Available Templates", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        # Group by category
        by_category = {}
        for t in templates:
            cat = t.get('category', 'general')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(t)
        
        for category, temps in sorted(by_category.items()):
            print(f"\n{self._color(category.upper(), 'yellow')}")
            for t in temps:
                print(f"  {self._color(t['id'], 'green')} - {t['name']}")
                if t.get('description'):
                    print(f"    {t['description']}")
    
    def show_template_detail(self, template: Dict[str, Any]):
        """Display template details"""
        print()
        print(self._color(f"📄 {template['name']}", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        print(f"\n{self._color('ID:', 'yellow')} {template['id']}")
        print(f"{self._color('Category:', 'yellow')} {template.get('category', 'general')}")
        
        if template.get('description'):
            print(f"\n{self._color('Description:', 'yellow')}")
            print(template['description'])
        
        print(f"\n{self._color('Content:', 'yellow')}")
        print(self._color('-' * 60, 'cyan'))
        print(template['content'])
        print(self._color('-' * 60, 'cyan'))
    
    def show_analysis(self, analysis: Dict[str, Any], detailed: bool = False):
        """Display analysis results"""
        print()
        print(self._color("🔍 Prompt Analysis", 'bold'))
        print(self._color('=' * 60, 'cyan'))
        
        # Quality Score
        quality = analysis.get('quality_score', {})
        print(f"\n{self._color('Quality Score:', 'yellow')} {quality.get('overall', 'N/A')}/100 ({quality.get('rating', 'N/A')})")
        
        breakdown = quality.get('breakdown', {})
        for metric, score in breakdown.items():
            bar = '█' * int(score / 5) + '░' * (20 - int(score / 5))
            print(f"  {metric.capitalize():12} {bar} {score}")
        
        # Basic Stats
        stats = analysis.get('basic_stats', {})
        print(f"\n{self._color('Statistics:', 'yellow')}")
        print(f"  Characters: {stats.get('char_count', 'N/A')}")
        print(f"  Words: {stats.get('word_count', 'N/A')}")
        print(f"  Sentences: {stats.get('sentence_count', 'N/A')}")
        print(f"  Paragraphs: {stats.get('paragraph_count', 'N/A')}")
        
        # Structure
        structure = analysis.get('structure_analysis', {})
        print(f"\n{self._color('Structure:', 'yellow')}")
        for key, value in structure.items():
            status = '✓' if value else '✗'
            print(f"  {status} {key.replace('_', ' ').title()}")
        
        # Suggestions
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"\n{self._color('Suggestions:', 'yellow')}")
            for s in suggestions:
                icon = '⚠️' if s['type'] == 'warning' else '💡' if s['type'] == 'suggestion' else '✅'
                print(f"  {icon} [{s['category']}] {s['message']}")
        
        # Detailed metrics
        if detailed and 'detailed_metrics' in analysis:
            print(f"\n{self._color('Detailed Metrics:', 'yellow')}")
            detailed_metrics = analysis['detailed_metrics']
            
            char_dist = detailed_metrics.get('character_distribution', {})
            if char_dist:
                print(f"\n  Character Distribution:")
                for char_type, count in char_dist.items():
                    print(f"    {char_type}: {count}")
