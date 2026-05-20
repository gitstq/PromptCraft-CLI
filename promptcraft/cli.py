#!/usr/bin/env python3
"""
PromptCraft CLI - Command Line Interface
"""

import argparse
import sys
import os
from pathlib import Path

from promptcraft.core.config import Config
from promptcraft.core.prompt_manager import PromptManager
from promptcraft.core.version_control import VersionControl
from promptcraft.core.optimizer import PromptOptimizer
from promptcraft.core.templates import TemplateManager
from promptcraft.core.analyzer import PromptAnalyzer
from promptcraft.ui.console import ConsoleUI
from promptcraft.utils.helpers import setup_logging


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='promptcraft',
        description='🚀 PromptCraft CLI - Lightweight Prompt Engineering & Version Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  promptcraft init                          Initialize a new prompt project
  promptcraft add "My Prompt" -f prompt.txt Add a new prompt from file
  promptcraft list                          List all prompts
  promptcraft optimize <id>                 Optimize a prompt
  promptcraft version <id>                  Show version history
  promptcraft compare <id1> <id2>           Compare two prompt versions
  promptcraft test <id>                     Run A/B test on prompt
  promptcraft export <id> -o output.json    Export prompt to file
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '--config', 
        '-c',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--verbose', 
        '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--quiet', 
        '-q',
        action='store_true',
        help='Suppress non-error output'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # init command
    init_parser = subparsers.add_parser(
        'init', 
        help='Initialize a new PromptCraft project'
    )
    init_parser.add_argument(
        '--path', 
        '-p',
        default='.',
        help='Project path (default: current directory)'
    )
    init_parser.add_argument(
        '--name', 
        '-n',
        help='Project name'
    )
    
    # add command
    add_parser = subparsers.add_parser(
        'add', 
        help='Add a new prompt'
    )
    add_parser.add_argument(
        'name',
        help='Prompt name'
    )
    add_parser.add_argument(
        '--file', 
        '-f',
        help='Read prompt content from file'
    )
    add_parser.add_argument(
        '--content', 
        '-c',
        help='Prompt content (inline)'
    )
    add_parser.add_argument(
        '--category', 
        '-cat',
        help='Prompt category'
    )
    add_parser.add_argument(
        '--tags', 
        '-t',
        help='Comma-separated tags'
    )
    add_parser.add_argument(
        '--description', 
        '-d',
        help='Prompt description'
    )
    
    # list command
    list_parser = subparsers.add_parser(
        'list', 
        help='List all prompts'
    )
    list_parser.add_argument(
        '--category', 
        '-c',
        help='Filter by category'
    )
    list_parser.add_argument(
        '--tags', 
        '-t',
        help='Filter by tags'
    )
    list_parser.add_argument(
        '--format', 
        '-f',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format'
    )
    
    # show command
    show_parser = subparsers.add_parser(
        'show', 
        help='Show prompt details'
    )
    show_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    show_parser.add_argument(
        '--version', 
        '-v',
        help='Show specific version'
    )
    
    # edit command
    edit_parser = subparsers.add_parser(
        'edit', 
        help='Edit a prompt'
    )
    edit_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    edit_parser.add_argument(
        '--file', 
        '-f',
        help='Read new content from file'
    )
    edit_parser.add_argument(
        '--content', 
        '-c',
        help='New content (inline)'
    )
    edit_parser.add_argument(
        '--message', 
        '-m',
        help='Version commit message'
    )
    
    # optimize command
    optimize_parser = subparsers.add_parser(
        'optimize', 
        help='Optimize a prompt'
    )
    optimize_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    optimize_parser.add_argument(
        '--strategy', 
        '-s',
        choices=['clarity', 'conciseness', 'structure', 'examples', 'all'],
        default='all',
        help='Optimization strategy'
    )
    optimize_parser.add_argument(
        '--output', 
        '-o',
        help='Save optimized prompt to file'
    )
    optimize_parser.add_argument(
        '--apply', 
        '-a',
        action='store_true',
        help='Apply optimization as new version'
    )
    
    # version command
    version_parser = subparsers.add_parser(
        'version', 
        help='Show version history'
    )
    version_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    version_parser.add_argument(
        '--limit', 
        '-l',
        type=int,
        default=10,
        help='Number of versions to show'
    )
    
    # compare command
    compare_parser = subparsers.add_parser(
        'compare', 
        help='Compare two prompt versions'
    )
    compare_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    compare_parser.add_argument(
        'version1',
        help='First version'
    )
    compare_parser.add_argument(
        'version2',
        nargs='?',
        help='Second version (default: current)'
    )
    
    # test command
    test_parser = subparsers.add_parser(
        'test', 
        help='Run A/B test on prompt'
    )
    test_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    test_parser.add_argument(
        '--versions', 
        '-v',
        help='Versions to compare (comma-separated)'
    )
    test_parser.add_argument(
        '--iterations', 
        '-i',
        type=int,
        default=5,
        help='Number of test iterations'
    )
    test_parser.add_argument(
        '--input', 
        '-in',
        help='Test input file'
    )
    
    # export command
    export_parser = subparsers.add_parser(
        'export', 
        help='Export prompt'
    )
    export_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    export_parser.add_argument(
        '--output', 
        '-o',
        required=True,
        help='Output file path'
    )
    export_parser.add_argument(
        '--format', 
        '-f',
        choices=['json', 'yaml', 'txt', 'md'],
        default='json',
        help='Export format'
    )
    export_parser.add_argument(
        '--version', 
        '-v',
        help='Specific version to export'
    )
    
    # import command
    import_parser = subparsers.add_parser(
        'import', 
        help='Import prompts from file'
    )
    import_parser.add_argument(
        'file',
        help='Import file path'
    )
    import_parser.add_argument(
        '--format', 
        '-f',
        choices=['json', 'yaml', 'csv'],
        help='Import format (auto-detected if not specified)'
    )
    
    # template command
    template_parser = subparsers.add_parser(
        'template', 
        help='Manage prompt templates'
    )
    template_subparsers = template_parser.add_subparsers(
        dest='template_command',
        help='Template commands'
    )
    
    template_list = template_subparsers.add_parser(
        'list',
        help='List available templates'
    )
    template_show = template_subparsers.add_parser(
        'show',
        help='Show template details'
    )
    template_show.add_argument('name', help='Template name')
    template_use = template_subparsers.add_parser(
        'use',
        help='Use a template'
    )
    template_use.add_argument('name', help='Template name')
    template_use.add_argument('--output', '-o', help='Output file')
    
    # analyze command
    analyze_parser = subparsers.add_parser(
        'analyze', 
        help='Analyze prompt quality'
    )
    analyze_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    analyze_parser.add_argument(
        '--detailed', 
        '-d',
        action='store_true',
        help='Show detailed analysis'
    )
    
    # delete command
    delete_parser = subparsers.add_parser(
        'delete', 
        help='Delete a prompt'
    )
    delete_parser.add_argument(
        'id',
        help='Prompt ID or name'
    )
    delete_parser.add_argument(
        '--force', 
        '-f',
        action='store_true',
        help='Force deletion without confirmation'
    )
    
    return parser


def handle_init(args, ui):
    """Handle init command"""
    from promptcraft.core.project import Project
    
    project = Project(args.path)
    if project.initialize(args.name):
        ui.success(f"✅ Initialized PromptCraft project at {args.path}")
        return 0
    else:
        ui.error("❌ Failed to initialize project")
        return 1


def handle_add(args, ui, config):
    """Handle add command"""
    manager = PromptManager(config)
    
    # Get content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            ui.error(f"❌ Failed to read file: {e}")
            return 1
    elif args.content:
        content = args.content
    else:
        # Interactive mode
        ui.info("📝 Enter prompt content (Ctrl+D to finish):")
        content = sys.stdin.read()
    
    if not content.strip():
        ui.error("❌ Prompt content cannot be empty")
        return 1
    
    # Parse tags
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    
    # Add prompt
    prompt_id = manager.add_prompt(
        name=args.name,
        content=content,
        category=args.category,
        tags=tags,
        description=args.description
    )
    
    if prompt_id:
        ui.success(f"✅ Added prompt '{args.name}' (ID: {prompt_id})")
        return 0
    else:
        ui.error("❌ Failed to add prompt")
        return 1


def handle_list(args, ui, config):
    """Handle list command"""
    manager = PromptManager(config)
    
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    
    prompts = manager.list_prompts(
        category=args.category,
        tags=tags
    )
    
    if not prompts:
        ui.info("📭 No prompts found")
        return 0
    
    ui.show_prompts(prompts, format=args.format)
    return 0


def handle_show(args, ui, config):
    """Handle show command"""
    manager = PromptManager(config)
    
    prompt = manager.get_prompt(args.id, version=args.version)
    if not prompt:
        ui.error(f"❌ Prompt '{args.id}' not found")
        return 1
    
    ui.show_prompt_detail(prompt)
    return 0


def handle_edit(args, ui, config):
    """Handle edit command"""
    manager = PromptManager(config)
    
    # Get new content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            ui.error(f"❌ Failed to read file: {e}")
            return 1
    elif args.content:
        content = args.content
    else:
        # Get current content and open editor
        current = manager.get_prompt(args.id)
        if not current:
            ui.error(f"❌ Prompt '{args.id}' not found")
            return 1
        
        ui.info("📝 Enter new content (Ctrl+D to finish):")
        content = sys.stdin.read()
    
    if not content.strip():
        ui.error("❌ Prompt content cannot be empty")
        return 1
    
    if manager.update_prompt(args.id, content, message=args.message):
        ui.success(f"✅ Updated prompt '{args.id}'")
        return 0
    else:
        ui.error("❌ Failed to update prompt")
        return 1


def handle_optimize(args, ui, config):
    """Handle optimize command"""
    manager = PromptManager(config)
    optimizer = PromptOptimizer(config)
    
    prompt = manager.get_prompt(args.id)
    if not prompt:
        ui.error(f"❌ Prompt '{args.id}' not found")
        return 1
    
    ui.info(f"🔧 Optimizing prompt '{args.id}' with strategy: {args.strategy}")
    
    optimized = optimizer.optimize(prompt['content'], strategy=args.strategy)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(optimized['content'])
            ui.success(f"✅ Saved optimized prompt to {args.output}")
        except Exception as e:
            ui.error(f"❌ Failed to save: {e}")
            return 1
    else:
        ui.show_optimization_result(optimized)
    
    if args.apply:
        manager.update_prompt(
            args.id,
            optimized['content'],
            message=f"Auto-optimized: {optimized['summary']}"
        )
        ui.success("✅ Applied optimization as new version")
    
    return 0


def handle_version(args, ui, config):
    """Handle version command"""
    manager = PromptManager(config)
    vc = VersionControl(config)
    
    versions = vc.get_version_history(args.id, limit=args.limit)
    if not versions:
        ui.error(f"❌ No version history found for '{args.id}'")
        return 1
    
    ui.show_version_history(versions)
    return 0


def handle_compare(args, ui, config):
    """Handle compare command"""
    manager = PromptManager(config)
    
    v1 = manager.get_prompt(args.id, version=args.version1)
    if not v1:
        ui.error(f"❌ Version '{args.version1}' not found")
        return 1
    
    if args.version2:
        v2 = manager.get_prompt(args.id, version=args.version2)
        if not v2:
            ui.error(f"❌ Version '{args.version2}' not found")
            return 1
    else:
        v2 = manager.get_prompt(args.id)
    
    ui.show_diff(v1, v2, args.version1, args.version2 or 'current')
    return 0


def handle_test(args, ui, config):
    """Handle test command"""
    from promptcraft.core.tester import PromptTester
    
    manager = PromptManager(config)
    tester = PromptTester(config)
    
    # Get test input
    test_input = ""
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                test_input = f.read()
        except Exception as e:
            ui.error(f"❌ Failed to read test input: {e}")
            return 1
    
    # Get versions to compare
    versions = None
    if args.versions:
        versions = [v.strip() for v in args.versions.split(',')]
    
    ui.info(f"🧪 Running A/B test on '{args.id}'...")
    results = tester.run_ab_test(
        args.id,
        versions=versions,
        test_input=test_input,
        iterations=args.iterations
    )
    
    ui.show_test_results(results)
    return 0


def handle_export(args, ui, config):
    """Handle export command"""
    manager = PromptManager(config)
    
    if manager.export_prompt(args.id, args.output, args.format, args.version):
        ui.success(f"✅ Exported prompt to {args.output}")
        return 0
    else:
        ui.error("❌ Export failed")
        return 1


def handle_import(args, ui, config):
    """Handle import command"""
    manager = PromptManager(config)
    
    count = manager.import_prompts(args.file, args.format)
    if count >= 0:
        ui.success(f"✅ Imported {count} prompts from {args.file}")
        return 0
    else:
        ui.error("❌ Import failed")
        return 1


def handle_template(args, ui, config):
    """Handle template command"""
    templates = TemplateManager(config)
    
    if args.template_command == 'list':
        template_list = templates.list_templates()
        ui.show_templates(template_list)
    
    elif args.template_command == 'show':
        template = templates.get_template(args.name)
        if template:
            ui.show_template_detail(template)
        else:
            ui.error(f"❌ Template '{args.name}' not found")
            return 1
    
    elif args.template_command == 'use':
        content = templates.use_template(args.name)
        if content:
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(content)
                ui.success(f"✅ Saved template to {args.output}")
            else:
                print(content)
        else:
            ui.error(f"❌ Template '{args.name}' not found")
            return 1
    
    return 0


def handle_analyze(args, ui, config):
    """Handle analyze command"""
    manager = PromptManager(config)
    analyzer = PromptAnalyzer(config)
    
    prompt = manager.get_prompt(args.id)
    if not prompt:
        ui.error(f"❌ Prompt '{args.id}' not found")
        return 1
    
    ui.info(f"🔍 Analyzing prompt '{args.id}'...")
    analysis = analyzer.analyze(prompt['content'], detailed=args.detailed)
    
    ui.show_analysis(analysis, detailed=args.detailed)
    return 0


def handle_delete(args, ui, config):
    """Handle delete command"""
    manager = PromptManager(config)
    
    if not args.force:
        confirm = ui.confirm(f"⚠️ Are you sure you want to delete '{args.id}'?")
        if not confirm:
            ui.info("❌ Cancelled")
            return 0
    
    if manager.delete_prompt(args.id):
        ui.success(f"✅ Deleted prompt '{args.id}'")
        return 0
    else:
        ui.error("❌ Failed to delete prompt")
        return 1


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose, quiet=args.quiet)
    
    # Initialize UI
    ui = ConsoleUI(quiet=args.quiet)
    
    # Show help if no command
    if not args.command:
        parser.print_help()
        return 0
    
    # Load configuration
    config = Config(args.config)
    
    # Route commands
    try:
        if args.command == 'init':
            return handle_init(args, ui)
        elif args.command == 'add':
            return handle_add(args, ui, config)
        elif args.command == 'list':
            return handle_list(args, ui, config)
        elif args.command == 'show':
            return handle_show(args, ui, config)
        elif args.command == 'edit':
            return handle_edit(args, ui, config)
        elif args.command == 'optimize':
            return handle_optimize(args, ui, config)
        elif args.command == 'version':
            return handle_version(args, ui, config)
        elif args.command == 'compare':
            return handle_compare(args, ui, config)
        elif args.command == 'test':
            return handle_test(args, ui, config)
        elif args.command == 'export':
            return handle_export(args, ui, config)
        elif args.command == 'import':
            return handle_import(args, ui, config)
        elif args.command == 'template':
            return handle_template(args, ui, config)
        elif args.command == 'analyze':
            return handle_analyze(args, ui, config)
        elif args.command == 'delete':
            return handle_delete(args, ui, config)
        else:
            parser.print_help()
            return 0
    
    except KeyboardInterrupt:
        ui.error("\n❌ Interrupted by user")
        return 130
    except Exception as e:
        ui.error(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
