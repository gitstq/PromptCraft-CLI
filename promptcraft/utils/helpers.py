"""
Helper utilities for PromptCraft CLI
"""

import os
import sys
import logging
from typing import Optional


def setup_logging(verbose: bool = False, quiet: bool = False):
    """Setup logging configuration"""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )


def get_editor() -> Optional[str]:
    """Get system editor"""
    editor = os.environ.get('EDITOR')
    if not editor:
        # Try common editors
        for ed in ['vim', 'nano', 'emacs', 'code']:
            if os.system(f"which {ed} > /dev/null 2>&1") == 0:
                return ed
    return editor


def open_in_editor(content: str, editor: Optional[str] = None) -> str:
    """Open content in system editor"""
    import tempfile
    
    if not editor:
        editor = get_editor() or 'vi'
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        # Open in editor
        os.system(f'{editor} "{temp_path}"')
        
        # Read back
        with open(temp_path, 'r') as f:
            return f.read()
    finally:
        # Cleanup
        os.unlink(temp_path)


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_bytes(size: int) -> str:
    """Format byte size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe use"""
    import re
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename or 'unnamed'


def parse_tags(tag_string: str) -> list:
    """Parse comma-separated tags"""
    if not tag_string:
        return []
    return [t.strip() for t in tag_string.split(',') if t.strip()]


def merge_dicts(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def validate_prompt_content(content: str) -> tuple:
    """Validate prompt content"""
    errors = []
    warnings = []
    
    if not content or not content.strip():
        errors.append("Prompt content cannot be empty")
    
    if len(content) > 10000:
        warnings.append("Prompt is very long (>10000 chars)")
    
    if len(content.split()) < 3:
        warnings.append("Prompt is very short (<3 words)")
    
    # Check for common issues
    if '???' in content or '!!!' in content:
        warnings.append("Avoid excessive punctuation")
    
    if content.isupper():
        warnings.append("All caps text may be interpreted as shouting")
    
    return len(errors) == 0, errors, warnings


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    import re
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Limit length
    return text[:50]


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimate reading time in seconds"""
    word_count = len(text.split())
    seconds = (word_count / wpm) * 60
    return max(1, int(seconds))


def chunk_text(text: str, chunk_size: int = 1000) -> list:
    """Split text into chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        word_size = len(word) + 1  # +1 for space
        if current_size + word_size > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_size = word_size
        else:
            current_chunk.append(word)
            current_size += word_size
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def highlight_diff(old: str, new: str) -> tuple:
    """Generate highlighted diff"""
    try:
        import difflib
        
        diff = list(difflib.ndiff(old.splitlines(), new.splitlines()))
        
        added = []
        removed = []
        
        for line in diff:
            if line.startswith('+ '):
                added.append(line[2:])
            elif line.startswith('- '):
                removed.append(line[2:])
        
        return added, removed
    except ImportError:
        return [], []


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard"""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        # Try platform-specific methods
        if sys.platform == 'darwin':
            import subprocess
            subprocess.run(['pbcopy'], input=text.encode())
            return True
        elif sys.platform == 'win32':
            import subprocess
            subprocess.run(['clip'], input=text.encode())
            return True
        elif sys.platform == 'linux':
            import subprocess
            try:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode())
                return True
            except FileNotFoundError:
                pass
        return False


def read_from_clipboard() -> str:
    """Read text from clipboard"""
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError:
        return ""


def is_interactive() -> bool:
    """Check if running in interactive mode"""
    return sys.stdin.isatty() and sys.stdout.isatty()


def get_terminal_width() -> int:
    """Get terminal width"""
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def wrap_text(text: str, width: Optional[int] = None) -> str:
    """Wrap text to terminal width"""
    if width is None:
        width = get_terminal_width()
    
    try:
        import textwrap
        return textwrap.fill(text, width=width)
    except ImportError:
        return text
