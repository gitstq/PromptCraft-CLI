"""
Terminal User Interface - Interactive TUI for PromptCraft
终端用户界面 - PromptCraft的交互式TUI
"""

import os
import sys
from typing import Optional, List, Callable


class TUI:
    """
    Simple Terminal User Interface using only standard library
    仅使用标准库的简单终端用户界面
    """
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    
    def __init__(self):
        self.width = self._get_terminal_width()
        self.use_colors = self._supports_colors()
    
    def _get_terminal_width(self) -> int:
        """Get terminal width"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    def _supports_colors(self) -> bool:
        """Check if terminal supports colors"""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def color(self, text: str, color_code: str) -> str:
        """Apply color to text"""
        if self.use_colors:
            return f"{color_code}{text}{self.RESET}"
        return text
    
    def print_header(self, title: str):
        """Print a header"""
        print()
        print(self.color("=" * self.width, self.CYAN))
        print(self.color(f"  {title}", self.BOLD + self.CYAN))
        print(self.color("=" * self.width, self.CYAN))
        print()
    
    def print_section(self, title: str):
        """Print a section title"""
        print()
        print(self.color(f"▶ {title}", self.BOLD + self.YELLOW))
        print(self.color("─" * min(len(title) + 3, self.width), self.DIM))
    
    def print_success(self, message: str):
        """Print success message"""
        print(self.color(f"✓ {message}", self.GREEN))
    
    def print_error(self, message: str):
        """Print error message"""
        print(self.color(f"✗ {message}", self.RED))
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(self.color(f"⚠ {message}", self.YELLOW))
    
    def print_info(self, message: str):
        """Print info message"""
        print(self.color(f"ℹ {message}", self.BLUE))
    
    def print_prompt_box(self, prompt: str, title: str = "Prompt"):
        """Print prompt in a box"""
        lines = prompt.split('\n')
        max_len = max(len(line) for line in lines) if lines else 0
        box_width = min(max_len + 4, self.width - 2)
        
        print()
        print(self.color(f"┌─ {title} ", self.CYAN) + self.color("─" * (box_width - len(title) - 3), self.CYAN) + self.color("┐", self.CYAN))
        
        for line in lines:
            truncated = line[:box_width - 4]
            padding = " " * (box_width - len(truncated) - 4)
            print(self.color("│ ", self.CYAN) + truncated + padding + self.color(" │", self.CYAN))
        
        print(self.color("└" + "─" * (box_width - 2) + "┘", self.CYAN))
        print()
    
    def print_score_bar(self, score: float, max_width: int = 50):
        """Print a visual score bar"""
        filled = int((score / 100) * max_width)
        bar = "█" * filled + "░" * (max_width - filled)
        
        # Color based on score
        if score >= 80:
            color = self.GREEN
        elif score >= 60:
            color = self.YELLOW
        else:
            color = self.RED
        
        print(f"Score: {self.color(f'{score:.1f}/100', color)}")
        print(self.color(f"[{bar}]", color))
    
    def print_list(self, items: List[str], bullet: str = "•"):
        """Print a bulleted list"""
        for item in items:
            print(f"  {self.color(bullet, self.CYAN)} {item}")
    
    def print_table(self, headers: List[str], rows: List[List[str]]):
        """Print a simple table"""
        if not rows:
            return
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(
            self.color(h.ljust(col_widths[i]), self.BOLD + self.CYAN)
            for i, h in enumerate(headers)
        )
        print(header_row)
        print(self.color("-" * len(header_row), self.DIM))
        
        # Print rows
        for row in rows:
            print(" | ".join(
                str(cell).ljust(col_widths[i])
                for i, cell in enumerate(row)
            ))
    
    def print_menu(self, options: List[str], title: str = "Menu"):
        """Print a numbered menu"""
        self.print_section(title)
        for i, option in enumerate(options, 1):
            print(f"  {self.color(str(i), self.YELLOW)}. {option}")
        print()
    
    def get_input(self, prompt: str = "") -> str:
        """Get user input"""
        try:
            return input(self.color(f"{prompt}> ", self.GREEN))
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def get_multiline_input(self, prompt: str = "Enter text (Ctrl+D or empty line to finish):") -> str:
        """Get multi-line input from user"""
        print(self.color(prompt, self.DIM))
        lines = []
        try:
            while True:
                line = input()
                if not line and lines:
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass
        return '\n'.join(lines)
    
    def confirm(self, message: str) -> bool:
        """Ask for confirmation"""
        response = self.get_input(f"{message} (y/n)").lower()
        return response in ('y', 'yes')
    
    def select_option(self, options: List[str], prompt: str = "Select") -> Optional[int]:
        """Let user select an option"""
        self.print_menu(options, prompt)
        
        try:
            choice = self.get_input("Enter number")
            index = int(choice) - 1
            if 0 <= index < len(options):
                return index
        except ValueError:
            pass
        
        self.print_error("Invalid selection")
        return None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗       ║
║   ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝       ║
║   ██████╔╝██████╔╝██║   ██║██╔████╔██║██║  ██║█████╗         ║
║   ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██║  ██║██╔══╝         ║
║   ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗       ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝       ║
║                                                              ║
║         🚀 Prompt Engineering Optimization CLI 🚀            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(self.color(banner, self.CYAN))
    
    def show_analysis_result(self, result):
        """Display analysis result"""
        self.print_section("Analysis Results")
        
        # Score
        self.print_score_bar(result.score)
        print()
        
        # Strengths
        if result.strengths:
            print(self.color("✨ Strengths:", self.GREEN))
            self.print_list(result.strengths)
            print()
        
        # Issues
        if result.issues:
            print(self.color("⚠️  Issues Found:", self.YELLOW))
            for issue in result.issues:
                severity_color = self.RED if issue.severity.value == "critical" else self.YELLOW if issue.severity.value == "high" else self.BLUE
                print(f"  {self.color('•', severity_color)} [{issue.severity.value.upper()}] {issue.message}")
                print(f"    {self.color('💡', self.DIM)} {issue.suggestion}")
            print()
        
        # Metrics
        if result.metrics:
            print(self.color("📊 Metrics:", self.BLUE))
            for key, value in result.metrics.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    def show_optimization_result(self, result):
        """Display optimization result"""
        self.print_section(f"Optimization: {result.strategy.value}")
        
        print(self.color("📈 Estimated Impact:", self.GREEN))
        print(f"  {result.estimated_impact}")
        print()
        
        print(self.color("✨ Improvements:", self.GREEN))
        self.print_list(result.improvements)
        print()
        
        self.print_prompt_box(result.optimized, "Optimized Prompt")
    
    def interactive_menu(self, storage, analyzer, optimizer, tester):
        """Run interactive TUI menu"""
        self.clear_screen()
        self.print_banner()
        
        while True:
            options = [
                "Analyze a prompt",
                "Optimize a prompt",
                "Test a prompt",
                "Manage projects",
                "View quick tips",
                "Exit"
            ]
            
            self.print_menu(options, "Main Menu")
            choice = self.get_input("Select option")
            
            if choice == "1":
                self._handle_analyze(analyzer)
            elif choice == "2":
                self._handle_optimize(optimizer)
            elif choice == "3":
                self._handle_test(tester)
            elif choice == "4":
                self._handle_projects(storage)
            elif choice == "5":
                self._handle_tips(analyzer)
            elif choice == "6" or choice.lower() in ("q", "quit", "exit"):
                self.print_info("Goodbye! 👋")
                break
            else:
                self.print_error("Invalid option")
            
            print()
            self.get_input("Press Enter to continue")
            self.clear_screen()
    
    def _handle_analyze(self, analyzer):
        """Handle prompt analysis"""
        self.print_section("Prompt Analysis")
        prompt = self.get_multiline_input("Enter your prompt:")
        
        if prompt.strip():
            result = analyzer.analyze(prompt)
            self.show_analysis_result(result)
        else:
            self.print_error("Empty prompt")
    
    def _handle_optimize(self, optimizer):
        """Handle prompt optimization"""
        self.print_section("Prompt Optimization")
        prompt = self.get_multiline_input("Enter your prompt:")
        
        if not prompt.strip():
            self.print_error("Empty prompt")
            return
        
        # Strategy selection
        strategies = [
            "Auto-select best strategy",
            "Structured formatting",
            "Few-shot prompting",
            "Chain-of-Thought",
            "ReAct pattern",
            "Role-based",
            "Constraint-focused"
        ]
        
        choice = self.select_option(strategies, "Select optimization strategy")
        if choice is None:
            return
        
        from .optimizer import OptimizationStrategy
        
        strategy_map = {
            0: None,
            1: OptimizationStrategy.STRUCTURED,
            2: OptimizationStrategy.FEW_SHOT,
            3: OptimizationStrategy.CHAIN_OF_THOUGHT,
            4: OptimizationStrategy.REACT,
            5: OptimizationStrategy.ROLE_BASED,
            6: OptimizationStrategy.CONSTRAINT_FOCUS
        }
        
        result = optimizer.optimize(prompt, strategy_map.get(choice))
        self.show_optimization_result(result)
    
    def _handle_test(self, tester):
        """Handle prompt testing"""
        self.print_section("Prompt Testing")
        prompt = self.get_multiline_input("Enter your prompt:")
        
        if prompt.strip():
            self.print_info("Running test...")
            result = tester.test_single(prompt)
            
            if result.status.value == "success":
                self.print_success(f"Test completed in {result.latency_ms}ms")
                print()
                print(self.color("Response:", self.CYAN))
                print(result.response)
            else:
                self.print_error(f"Test failed: {result.error_message}")
        else:
            self.print_error("Empty prompt")
    
    def _handle_projects(self, storage):
        """Handle project management"""
        self.print_section("Project Management")
        
        projects = storage.list_projects()
        if projects:
            print(self.color(f"📁 {len(projects)} project(s) found:", self.CYAN))
            for p in projects:
                print(f"  • {p['name']} ({p['version_count']} versions)")
        else:
            self.print_info("No projects yet")
        
        print()
        if self.confirm("Create new project?"):
            name = self.get_input("Project name")
            if name:
                project = storage.create_project(name)
                self.print_success(f"Created project: {project.name}")
    
    def _handle_tips(self, analyzer):
        """Handle quick tips"""
        self.print_section("Quick Optimization Tips")
        tips = analyzer.get_quick_tips()
        self.print_list(tips)
