# 🚀 PromptCraft CLI

<p align="center">
  <strong>轻量级Prompt工程优化与版本管理CLI工具</strong><br>
  <strong>Lightweight Prompt Engineering & Version Management CLI Tool</strong>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="Zero Dependencies">
</p>

---

## 简体中文

### 🎉 项目介绍

PromptCraft CLI 是一款专为Prompt工程师和AI应用开发者打造的轻量级命令行工具。它解决了Prompt版本管理混乱、优化困难、团队协作低效等核心痛点，让Prompt工程变得像代码工程一样专业。

**灵感来源**：在使用Claude Code、Cursor等AI编码工具时，我们发现高质量的Prompt往往经过多次迭代，但缺乏有效的版本管理和优化工具。PromptCraft应运而生，填补了这一空白。

### ✨ 核心特性

- 📝 **Prompt版本控制** - 完整的版本历史追踪，随时回滚到任意版本
- 🔧 **智能优化引擎** - 自动优化Prompt的清晰度、简洁性、结构和示例
- 📊 **质量分析** - 多维度Prompt质量评分，可读性分析
- 🧪 **A/B测试** - 对比不同Prompt版本的效果
- 📋 **模板系统** - 10+内置专业模板（代码审查、文档生成、单元测试等）
- 🔄 **导入导出** - 支持JSON、YAML、CSV、Markdown多种格式
- 🎯 **零依赖** - 核心功能无需任何第三方依赖
- 🌈 **彩色终端** - 美观的TUI界面，支持多种输出格式

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- Linux / macOS / Windows

#### 安装

```bash
# 从PyPI安装（推荐）
pip install promptcraft-cli

# 或从源码安装
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI
pip install -e .
```

#### 基础用法

```bash
# 初始化项目
promptcraft init

# 添加新Prompt
promptcraft add "代码审查助手" -f prompt.txt --category development --tags "code,review,ai"

# 列出所有Prompt
promptcraft list

# 查看Prompt详情
promptcraft show <prompt-id>

# 优化Prompt
promptcraft optimize <prompt-id> --strategy all

# 查看版本历史
promptcraft version <prompt-id>

# 对比两个版本
promptcraft compare <prompt-id> v1 v2

# 导出Prompt
promptcraft export <prompt-id> -o output.md --format md
```

### 📖 详细使用指南

#### 1. 项目管理

```bash
# 初始化新项目
promptcraft init --name "MyPromptProject"

# 项目结构
MyPromptProject/
├── .promptcraft.json    # 项目配置
├── prompts/             # Prompt存储
├── templates/           # 自定义模板
└── exports/            # 导出文件
```

#### 2. Prompt管理

```bash
# 添加Prompt（交互式）
promptcraft add "产品需求分析"
# 然后输入Prompt内容，按Ctrl+D结束

# 从文件添加
promptcraft add "技术文档生成" -f ./docs/prompt.txt --category documentation

# 编辑Prompt
promptcraft edit <prompt-id> -f new_content.txt -m "优化了示例部分"

# 删除Prompt
promptcraft delete <prompt-id> --force
```

#### 3. 智能优化

```bash
# 全面优化
promptcraft optimize <prompt-id>

# 针对特定方面优化
promptcraft optimize <prompt-id> --strategy clarity      # 清晰度
promptcraft optimize <prompt-id> --strategy conciseness  # 简洁性
promptcraft optimize <prompt-id> --strategy structure    # 结构
promptcraft optimize <prompt-id> --strategy examples     # 示例

# 优化并应用为新版本
promptcraft optimize <prompt-id> --apply
```

#### 4. 质量分析

```bash
# 基础分析
promptcraft analyze <prompt-id>

# 详细分析
promptcraft analyze <prompt-id> --detailed
```

#### 5. 模板使用

```bash
# 列出所有模板
promptcraft template list

# 查看模板详情
promptcraft template show code-review

# 使用模板
promptcraft template use code-review -o my_review.txt
```

### 💡 设计思路与迭代规划

#### 技术选型
- **Python 3.8+**：兼顾兼容性和现代特性
- **零依赖设计**：核心功能不依赖第三方库，确保稳定性和可移植性
- **模块化架构**：core/ui/utils三层架构，易于扩展

#### 后续迭代计划
- [ ] Web UI界面
- [ ] 团队协作功能（Git同步）
- [ ] LLM API集成（自动测试）
- [ ] Prompt marketplace
- [ ] VS Code插件

### 📦 打包与部署

```bash
# 构建分发包
make build

# 发布到PyPI
make publish

# 本地安装测试
pip install dist/promptcraft_cli-1.0.0-py3-none-any.whl
```

### 🤝 贡献指南

欢迎提交PR！请遵循以下规范：
- 使用 [Conventional Commits](https://www.conventionalcommits.org/)
- 代码通过 `make lint` 检查
- 添加相应的测试用例

### 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 繁體中文

### 🎉 專案介紹

PromptCraft CLI 是一款專為 Prompt 工程師和 AI 應用開發者打造的輕量級命令列工具。它解決了 Prompt 版本管理混亂、優化困難、團隊協作低效等核心痛點，讓 Prompt 工程變得像程式工程一樣專業。

### ✨ 核心特性

- 📝 **Prompt 版本控制** - 完整的版本歷史追蹤，隨時回滾到任意版本
- 🔧 **智慧優化引擎** - 自動優化 Prompt 的清晰度、簡潔性、結構和範例
- 📊 **品質分析** - 多維度 Prompt 品質評分，可讀性分析
- 🧪 **A/B 測試** - 對比不同 Prompt 版本的效果
- 📋 **模板系統** - 10+ 內建專業模板
- 🔄 **匯入匯出** - 支援 JSON、YAML、CSV、Markdown 多種格式
- 🎯 **零依賴** - 核心功能無需任何第三方依賴
- 🌈 **彩色終端** - 美觀的 TUI 介面

### 🚀 快速開始

#### 安裝

```bash
pip install promptcraft-cli
```

#### 基礎用法

```bash
# 初始化專案
promptcraft init

# 新增 Prompt
promptcraft add "程式碼審查助手" -f prompt.txt

# 列出所有 Prompt
promptcraft list

# 優化 Prompt
promptcraft optimize <prompt-id>
```

### 📖 詳細使用指南

詳細文檔請參考上方簡體中文版本或 English 版本。

### 📄 開源協議

MIT License

---

## English

### 🎉 Introduction

PromptCraft CLI is a lightweight command-line tool designed for Prompt Engineers and AI application developers. It solves core pain points like chaotic Prompt version management, difficult optimization, and inefficient team collaboration, making Prompt Engineering as professional as code engineering.

**Inspiration**: When using AI coding tools like Claude Code and Cursor, we found that high-quality Prompts often go through multiple iterations, but lacked effective version management and optimization tools. PromptCraft was born to fill this gap.

### ✨ Core Features

- 📝 **Prompt Version Control** - Complete version history tracking, rollback to any version anytime
- 🔧 **Intelligent Optimization Engine** - Auto-optimize Prompt clarity, conciseness, structure, and examples
- 📊 **Quality Analysis** - Multi-dimensional Prompt quality scoring, readability analysis
- 🧪 **A/B Testing** - Compare effectiveness of different Prompt versions
- 📋 **Template System** - 10+ built-in professional templates (code review, documentation, unit testing, etc.)
- 🔄 **Import/Export** - Support JSON, YAML, CSV, Markdown formats
- 🎯 **Zero Dependencies** - Core functionality requires no third-party dependencies
- 🌈 **Colorful Terminal** - Beautiful TUI interface with multiple output formats

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- Linux / macOS / Windows

#### Installation

```bash
# Install from PyPI (recommended)
pip install promptcraft-cli

# Or install from source
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI
pip install -e .
```

#### Basic Usage

```bash
# Initialize project
promptcraft init

# Add new Prompt
promptcraft add "Code Review Assistant" -f prompt.txt --category development --tags "code,review,ai"

# List all Prompts
promptcraft list

# Show Prompt details
promptcraft show <prompt-id>

# Optimize Prompt
promptcraft optimize <prompt-id> --strategy all

# View version history
promptcraft version <prompt-id>

# Compare two versions
promptcraft compare <prompt-id> v1 v2

# Export Prompt
promptcraft export <prompt-id> -o output.md --format md
```

### 📖 Detailed Usage Guide

#### 1. Project Management

```bash
# Initialize new project
promptcraft init --name "MyPromptProject"
```

#### 2. Prompt Management

```bash
# Add Prompt (interactive)
promptcraft add "Product Requirements Analysis"
# Then enter Prompt content, press Ctrl+D to finish

# Add from file
promptcraft add "Technical Documentation" -f ./docs/prompt.txt --category documentation

# Edit Prompt
promptcraft edit <prompt-id> -f new_content.txt -m "Optimized examples section"
```

#### 3. Smart Optimization

```bash
# Full optimization
promptcraft optimize <prompt-id>

# Optimize specific aspects
promptcraft optimize <prompt-id> --strategy clarity      # Clarity
promptcraft optimize <prompt-id> --strategy conciseness  # Conciseness
promptcraft optimize <prompt-id> --strategy structure    # Structure
promptcraft optimize <prompt-id> --strategy examples     # Examples
```

#### 4. Quality Analysis

```bash
# Basic analysis
promptcraft analyze <prompt-id>

# Detailed analysis
promptcraft analyze <prompt-id> --detailed
```

#### 5. Template Usage

```bash
# List all templates
promptcraft template list

# Show template details
promptcraft template show code-review

# Use template
promptcraft template use code-review -o my_review.txt
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices
- **Python 3.8+**: Balance compatibility and modern features
- **Zero Dependency Design**: Core functionality without third-party libraries for stability
- **Modular Architecture**: core/ui/utils three-layer architecture for easy extension

#### Roadmap
- [ ] Web UI interface
- [ ] Team collaboration features (Git sync)
- [ ] LLM API integration (auto-testing)
- [ ] Prompt marketplace
- [ ] VS Code extension

### 📦 Packaging & Deployment

```bash
# Build distribution
make build

# Publish to PyPI
make publish

# Local installation test
pip install dist/promptcraft_cli-1.0.0-py3-none-any.whl
```

### 🤝 Contributing

PRs welcome! Please follow:
- Use [Conventional Commits](https://www.conventionalcommits.org/)
- Pass `make lint` checks
- Add corresponding test cases

### 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Inspired by the Prompt Engineering community
- Built with ❤️ for AI developers worldwide

## 📞 Contact

- GitHub Issues: [https://github.com/gitstq/PromptCraft-CLI/issues](https://github.com/gitstq/PromptCraft-CLI/issues)
- Email: promptcraft@example.com

---

<p align="center">
  Made with ❤️ by PromptCraft Team
</p>
