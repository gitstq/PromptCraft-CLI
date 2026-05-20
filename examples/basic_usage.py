#!/usr/bin/env python3
"""
PromptCraft CLI - Basic Usage Examples
"""

# Example 1: Initialize a project
"""
$ promptcraft init --name "MyPromptProject"
✅ Initialized PromptCraft project at .
"""

# Example 2: Add a prompt from file
"""
$ promptcraft add "Code Review Assistant" -f ./prompts/code_review.txt --category development --tags "code,review,ai"
✅ Added prompt 'Code Review Assistant' (ID: abc123def456)
"""

# Example 3: List all prompts
"""
$ promptcraft list
ID           Name                    Category      Ver  Tags
abc123def456 Code Review Assistant  development     1  code, review, ai
xyz789uvw012 Documentation Generator documentation   1  docs, writing
"""

# Example 4: Show prompt details
"""
$ promptcraft show abc123def456

📋 Code Review Assistant
==================================================

ID: abc123def456
Category: development
Tags: code, review, ai
Version: 1
Created: 2026-05-20T10:00:00
Updated: 2026-05-20T10:00:00

Content:
--------------------------------------------------
Please review the following code for:
1. Correctness
2. Performance
3. Security issues
4. Best practices

Provide specific recommendations.
--------------------------------------------------
"""

# Example 5: Optimize a prompt
"""
$ promptcraft optimize abc123def456 --strategy all --apply

🔧 Optimization Result
==================================================

Optimizations Applied:
  ✓ Removed redundant phrase
  ✓ Added step-by-step instruction
  ✓ Improved structure with headers

Improvements:
  Original length: 156 chars
  Optimized length: 142 chars
  Reduction: 14 chars (9.0%)

✅ Applied optimization as new version
"""

# Example 6: Version history
"""
$ promptcraft version abc123def456

📜 Version History
==================================================

v2 - 2026-05-20T10:30:00
  Author: user
  Message: Auto-optimized: Applied 3 optimizations
  Size: 142 bytes

v1 - 2026-05-20T10:00:00
  Author: user
  Message: Initial version
  Size: 156 bytes
"""

# Example 7: Compare versions
"""
$ promptcraft compare abc123def456 v1 v2

🔍 Comparing v1 vs v2
==================================================

--- v1
+++ v2

- Please review the following code for correctness, performance, security issues, and best practices. Provide specific recommendations.
+ # Code Review Request
+
+ Please review the following code:
+
+ ## Review Criteria
+
+ 1. **Correctness**: Does the code work as intended?
+ 2. **Performance**: Are there any performance issues?
+ 3. **Security**: Are there any security concerns?
+ 4. **Best Practices**: Does it follow best practices?
+
+ Please provide your response step by step.
"""

# Example 8: Analyze prompt quality
"""
$ promptcraft analyze abc123def456

🔍 Prompt Analysis
==================================================

Quality Score: 85/100 (Good)
  Clarity      ████████████████░░░░ 85
  Specificity  █████████████████░░░ 90
  Structure    ███████████████░░░░░ 75
  Completeness ████████████████░░░░ 80

Statistics:
  Characters: 142
  Words: 23
  Sentences: 5
  Paragraphs: 3

Structure:
  ✓ Has Headers
  ✗ Has Code Blocks
  ✓ Has Lists
  ✗ Has Tables
  ✓ Has Formatting

Suggestions:
  💡 [Content] Consider adding an example to clarify expected output.
  ✅ [Clarity] Good use of specificity keywords
"""

# Example 9: Use a template
"""
$ promptcraft template list

📋 Available Templates
==================================================

DEVELOPMENT
  code-review - Code Review
  unit-test - Unit Test Generator
  refactoring - Code Refactoring

DOCUMENTATION
  documentation - Documentation Generator

PRODUCTIVITY
  meeting-notes - Meeting Notes
  email - Professional Email
"""

# Example 10: Export prompt
"""
$ promptcraft export abc123def456 -o code_review.md --format md
✅ Exported prompt to code_review.md
"""

if __name__ == "__main__":
    print("PromptCraft CLI - Basic Usage Examples")
    print("=" * 50)
    print()
    print("See the comments in this file for usage examples.")
    print()
    print("Quick start:")
    print("  1. promptcraft init")
    print("  2. promptcraft add 'My Prompt' -f prompt.txt")
    print("  3. promptcraft list")
    print("  4. promptcraft optimize <id>")
