"""
Command Line Interface - Main entry point for PromptCraft-CLI
命令行接口 - PromptCraft-CLI的主入口
"""

import sys
import argparse
from typing import Optional

from .analyzer import PromptAnalyzer
from .optimizer import PromptOptimizer, OptimizationStrategy
from .storage import PromptStorage
from .tester import PromptTester
from .tui import TUI


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='promptcraft',
        description='🚀 PromptCraft-CLI: Lightweight Prompt Engineering Optimization & Testing Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Launch interactive TUI
  %(prog)s analyze "Your prompt"    Analyze a prompt
  %(prog)s optimize -f prompt.txt   Optimize prompt from file
  %(prog)s test -f prompt.txt       Test a prompt
  %(prog)s projects                 List all projects
  %(prog)s tips                     Show optimization tips

For more information: https://github.com/gitstq/PromptCraft-CLI
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze', 
        help='Analyze a prompt for quality issues',
        aliases=['a']
    )
    analyze_parser.add_argument(
        'prompt',
        nargs='?',
        help='Prompt text to analyze'
    )
    analyze_parser.add_argument(
        '-f', '--file',
        help='Read prompt from file'
    )
    analyze_parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    
    # Optimize command
    optimize_parser = subparsers.add_parser(
        'optimize',
        help='Optimize a prompt using various strategies',
        aliases=['o', 'opt']
    )
    optimize_parser.add_argument(
        'prompt',
        nargs='?',
        help='Prompt text to optimize'
    )
    optimize_parser.add_argument(
        '-f', '--file',
        help='Read prompt from file'
    )
    optimize_parser.add_argument(
        '-s', '--strategy',
        choices=['structured', 'few_shot', 'cot', 'react', 'role', 'constraint'],
        help='Optimization strategy'
    )
    optimize_parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all optimization variants'
    )
    optimize_parser.add_argument(
        '--save',
        metavar='PROJECT',
        help='Save to project'
    )
    
    # Test command
    test_parser = subparsers.add_parser(
        'test',
        help='Test a prompt',
        aliases=['t']
    )
    test_parser.add_argument(
        'prompt',
        nargs='?',
        help='Prompt text to test'
    )
    test_parser.add_argument(
        '-f', '--file',
        help='Read prompt from file'
    )
    test_parser.add_argument(
        '--compare',
        nargs='+',
        metavar='PROMPT',
        help='Compare multiple prompts'
    )
    test_parser.add_argument(
        '--provider',
        default='mock',
        help='LLM provider (default: mock)'
    )
    
    # Project commands
    project_parser = subparsers.add_parser(
        'projects',
        help='Manage prompt projects',
        aliases=['p', 'proj']
    )
    project_parser.add_argument(
        'action',
        nargs='?',
        choices=['list', 'create', 'delete', 'export'],
        default='list',
        help='Project action'
    )
    project_parser.add_argument(
        '--name', '-n',
        help='Project name'
    )
    project_parser.add_argument(
        '--id',
        help='Project ID'
    )
    project_parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='json',
        help='Export format'
    )
    
    # Tips command
    subparsers.add_parser(
        'tips',
        help='Show optimization tips',
        aliases=['tip']
    )
    
    # Interactive command (default)
    subparsers.add_parser(
        'interactive',
        help='Launch interactive TUI (default)',
        aliases=['i', 'tui']
    )
    
    return parser


def read_prompt_from_source(args) -> Optional[str]:
    """Read prompt from args or file"""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    elif args.prompt:
        return args.prompt
    return None


def handle_analyze(args, analyzer: PromptAnalyzer) -> int:
    """Handle analyze command"""
    prompt = read_prompt_from_source(args)
    if not prompt:
        print("Error: No prompt provided. Use -f or provide prompt as argument.")
        return 1
    
    result = analyzer.analyze(prompt)
    
    if args.json:
        import json
        from dataclasses import asdict
        print(json.dumps(asdict(result), indent=2, default=str))
    else:
        tui = TUI()
        tui.show_analysis_result(result)
    
    return 0


def handle_optimize(args, optimizer: PromptOptimizer, storage: PromptStorage) -> int:
    """Handle optimize command"""
    prompt = read_prompt_from_source(args)
    if not prompt:
        print("Error: No prompt provided. Use -f or provide prompt as argument.")
        return 1
    
    strategy_map = {
        'structured': OptimizationStrategy.STRUCTURED,
        'few_shot': OptimizationStrategy.FEW_SHOT,
        'cot': OptimizationStrategy.CHAIN_OF_THOUGHT,
        'react': OptimizationStrategy.REACT,
        'role': OptimizationStrategy.ROLE_BASED,
        'constraint': OptimizationStrategy.CONSTRAINT_FOCUS,
    }
    
    if args.all:
        results = optimizer.optimize_all(prompt)
        tui = TUI()
        for result in results:
            tui.show_optimization_result(result)
            print("\n" + "="*60 + "\n")
    else:
        strategy = strategy_map.get(args.strategy) if args.strategy else None
        result = optimizer.optimize(prompt, strategy)
        
        tui = TUI()
        tui.show_optimization_result(result)
        
        # Save to project if requested
        if args.save:
            project = storage.create_project(args.save)
            storage.add_version(
                project.id,
                result.optimized,
                description=f"Optimized using {result.strategy.value} strategy",
                tags=[result.strategy.value, "optimized"]
            )
            tui.print_success(f"Saved to project: {args.save}")
    
    return 0


def handle_test(args, tester: PromptTester) -> int:
    """Handle test command"""
    if args.compare:
        results = tester.compare_prompts(args.compare, "Comparison test", args.provider)
        tui = TUI()
        tui.print_section("Comparison Results")
        
        for result in results.results:
            status_icon = "✓" if result.status.value == "success" else "✗"
            print(f"  {status_icon} {result.prompt_id}: {result.status.value}")
            if result.latency_ms:
                print(f"    Latency: {result.latency_ms}ms")
        
        if results.winner_id:
            print(f"\n  🏆 Winner: {results.winner_id}")
    else:
        prompt = read_prompt_from_source(args)
        if not prompt:
            print("Error: No prompt provided. Use -f or provide prompt as argument.")
            return 1
        
        result = tester.test_single(prompt, args.provider)
        tui = TUI()
        
        if result.status.value == "success":
            tui.print_success(f"Test passed in {result.latency_ms}ms")
            print(f"\nResponse:\n{result.response}")
        else:
            tui.print_error(f"Test failed: {result.error_message}")
    
    return 0


def handle_projects(args, storage: PromptStorage) -> int:
    """Handle project commands"""
    tui = TUI()
    
    if args.action == 'list' or not args.action:
        projects = storage.list_projects()
        if projects:
            tui.print_section(f"Projects ({len(projects)})")
            for p in projects:
                print(f"  • {p['name']} - {p['version_count']} versions")
                print(f"    ID: {p['id']}")
        else:
            tui.print_info("No projects found")
    
    elif args.action == 'create':
        if not args.name:
            print("Error: Project name required (--name)")
            return 1
        project = storage.create_project(args.name)
        tui.print_success(f"Created project: {project.name} (ID: {project.id})")
    
    elif args.action == 'delete':
        if not args.id:
            print("Error: Project ID required (--id)")
            return 1
        if storage.delete_project(args.id):
            tui.print_success(f"Deleted project: {args.id}")
        else:
            tui.print_error(f"Project not found: {args.id}")
    
    elif args.action == 'export':
        if not args.id:
            print("Error: Project ID required (--id)")
            return 1
        content = storage.export_project(args.id, args.format)
        if content:
            print(content)
        else:
            tui.print_error(f"Project not found: {args.id}")
    
    return 0


def handle_tips(analyzer: PromptAnalyzer) -> int:
    """Handle tips command"""
    tui = TUI()
    tui.print_section("Quick Optimization Tips")
    tips = analyzer.get_quick_tips()
    tui.print_list(tips)
    return 0


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize components
    analyzer = PromptAnalyzer()
    optimizer = PromptOptimizer()
    storage = PromptStorage()
    tester = PromptTester()
    
    # Route to appropriate handler
    if args.command in ('analyze', 'a'):
        return handle_analyze(args, analyzer)
    
    elif args.command in ('optimize', 'o', 'opt'):
        return handle_optimize(args, optimizer, storage)
    
    elif args.command in ('test', 't'):
        return handle_test(args, tester)
    
    elif args.command in ('projects', 'p', 'proj'):
        return handle_projects(args, storage)
    
    elif args.command == 'tips':
        return handle_tips(analyzer)
    
    else:
        # Launch interactive TUI
        tui = TUI()
        try:
            tui.interactive_menu(storage, analyzer, optimizer, tester)
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
