<div align="center">

# 🚀 PromptCraft-CLI

**Lightweight Prompt Engineering Optimization & Testing CLI Engine**

**轻量级Prompt工程优化与测试CLI引擎**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**PromptCraft-CLI** is a lightweight, zero-dependency command-line tool designed to help developers optimize, test, and manage AI prompts with ease. Inspired by the growing need for effective prompt engineering in the AI era, PromptCraft provides a comprehensive suite of tools to analyze prompt quality, apply optimization strategies, and test prompt performance.

**Key Differentiators:**
- 🎯 **Zero Dependencies** - Uses only Python standard library
- ⚡ **Lightning Fast** - No external API calls for core features
- 🔒 **Privacy First** - All processing happens locally
- 🎨 **Beautiful TUI** - Interactive terminal interface
- 📊 **Data-Driven** - Score-based analysis and recommendations

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| **🔍 Prompt Analysis** | Detect quality issues, vague terms, structural problems | ✅ |
| **✨ Smart Optimization** | 6 optimization strategies (Few-shot, CoT, ReAct, etc.) | ✅ |
| **🧪 Prompt Testing** | Batch testing, A/B comparison, performance metrics | ✅ |
| **📁 Project Management** | Version control for prompts with local storage | ✅ |
| **🖥️ Interactive TUI** | Beautiful terminal interface with menus and visualizations | ✅ |
| **📈 Score System** | 0-100 quality scoring with detailed breakdown | ✅ |

### 🚀 Quick Start

#### Installation

```bash
# Install from PyPI (when published)
pip install promptcraft-cli

# Or clone and install locally
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI
pip install -e .
```

#### Usage

```bash
# Launch interactive TUI
promptcraft

# Analyze a prompt
promptcraft analyze "Your prompt here"

# Optimize with specific strategy
promptcraft optimize "Your prompt" --strategy structured

# Test a prompt
promptcraft test -f prompt.txt

# List projects
promptcraft projects

# Show optimization tips
promptcraft tips
```

### 📖 Detailed Usage Guide

#### 1. Prompt Analysis

Analyze your prompts for quality issues:

```bash
promptcraft analyze "Write a good function to process data"
```

**Output Example:**
```
Score: 45/100

⚠️ Issues Found:
  • [MEDIUM] Found 1 vague/subjective term(s): good
    💡 Replace vague terms with specific, measurable criteria
  • [HIGH] No output format specified
    💡 Explicitly state the desired output format

✨ Strengths:
  • Optimal length (9 words)

📊 Metrics:
  • Word Count: 9
  • Sentence Count: 1
```

#### 2. Prompt Optimization

Apply various optimization strategies:

```bash
# Auto-select best strategy
promptcraft optimize "Your prompt"

# Use specific strategy
promptcraft optimize "Your prompt" --strategy few_shot

# Generate all variants
promptcraft optimize "Your prompt" --all
```

**Available Strategies:**
- `structured` - Add clear section headers
- `few_shot` - Include examples
- `cot` - Chain-of-Thought reasoning
- `react` - Reasoning + Acting pattern
- `role` - Role-based prompting
- `constraint` - Focus on constraints

#### 3. Prompt Testing

Test prompts with mock or real LLM providers:

```bash
# Test single prompt
promptcraft test "Your prompt"

# Compare multiple prompts
promptcraft test --compare "Prompt A" "Prompt B" "Prompt C"

# A/B testing
promptcraft test --ab prompt_a.txt prompt_b.txt --cases cases.txt
```

#### 4. Project Management

Organize prompts into projects:

```bash
# List projects
promptcraft projects

# Create new project
promptcraft projects create --name "My Project"

# Export project
promptcraft projects export --id <project_id> --format markdown
```

### 💡 Design Philosophy

**Why PromptCraft?**

1. **Developer-Centric** - Built by developers, for developers
2. **Zero-Dependency Philosophy** - No pip install hell, just pure Python
3. **Privacy-First** - Your prompts never leave your machine
4. **Extensible** - Modular design for easy extension
5. **Educational** - Learn prompt engineering while using it

### 📦 Packaging & Deployment

#### Build from Source

```bash
# Clone repository
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI

# Install in development mode
make install-dev

# Run tests
make test

# Build distribution
make build
```

#### Platform-Specific Builds

```bash
# Windows executable
make build-windows

# macOS executable  
make build-macos

# Linux executable
make build-linux
```

### 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Commit Message Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test changes

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**PromptCraft-CLI** 是一款轻量级、零依赖的命令行工具，旨在帮助开发者轻松优化、测试和管理AI Prompt。随着AI时代对高效Prompt工程的需求日益增长，PromptCraft 提供了一套全面的工具，用于分析Prompt质量、应用优化策略和测试Prompt性能。

**核心差异化亮点：**
- 🎯 **零依赖** - 仅使用Python标准库
- ⚡ **极速运行** - 核心功能无需外部API调用
- 🔒 **隐私优先** - 所有处理均在本地完成
- 🎨 **精美TUI** - 交互式终端界面
- 📊 **数据驱动** - 基于评分的分析和建议

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| **🔍 Prompt分析** | 检测质量问题、模糊术语、结构问题 | ✅ |
| **✨ 智能优化** | 6种优化策略（Few-shot、CoT、ReAct等） | ✅ |
| **🧪 Prompt测试** | 批量测试、A/B对比、性能指标 | ✅ |
| **📁 项目管理** | 本地存储的Prompt版本控制 | ✅ |
| **🖥️ 交互式TUI** | 带有菜单和可视化的精美终端界面 | ✅ |
| **📈 评分系统** | 0-100质量评分，详细分解 | ✅ |

### 🚀 快速开始

#### 安装

```bash
# 从PyPI安装（发布后）
pip install promptcraft-cli

# 或本地克隆安装
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI
pip install -e .
```

#### 使用

```bash
# 启动交互式TUI
promptcraft

# 分析Prompt
promptcraft analyze "Your prompt here"

# 使用特定策略优化
promptcraft optimize "Your prompt" --strategy structured

# 测试Prompt
promptcraft test -f prompt.txt

# 列出项目
promptcraft projects

# 显示优化技巧
promptcraft tips
```

### 📖 详细使用指南

#### 1. Prompt分析

分析您的Prompt质量问题：

```bash
promptcraft analyze "写一个处理数据的好函数"
```

**输出示例：**
```
评分：45/100

⚠️ 发现的问题：
  • [中等] 发现1个模糊/主观术语：好
    💡 用具体、可衡量的标准替换模糊术语
  • [高] 未指定输出格式
    💡 明确说明期望的输出格式

✨ 优势：
  • 长度适中（9个词）

📊 指标：
  • 词数：9
  • 句子数：1
```

#### 2. Prompt优化

应用各种优化策略：

```bash
# 自动选择最佳策略
promptcraft optimize "Your prompt"

# 使用特定策略
promptcraft optimize "Your prompt" --strategy few_shot

# 生成所有变体
promptcraft optimize "Your prompt" --all
```

**可用策略：**
- `structured` - 添加清晰的章节标题
- `few_shot` - 包含示例
- `cot` - 思维链推理
- `react` - 推理+行动模式
- `role` - 基于角色的Prompt
- `constraint` - 聚焦约束条件

#### 3. Prompt测试

使用模拟或真实LLM提供商测试Prompt：

```bash
# 测试单个Prompt
promptcraft test "Your prompt"

# 对比多个Prompt
promptcraft test --compare "Prompt A" "Prompt B" "Prompt C"

# A/B测试
promptcraft test --ab prompt_a.txt prompt_b.txt --cases cases.txt
```

#### 4. 项目管理

将Prompt组织到项目中：

```bash
# 列出项目
promptcraft projects

# 创建新项目
promptcraft projects create --name "My Project"

# 导出项目
promptcraft projects export --id <project_id> --format markdown
```

### 💡 设计理念

**为什么选择PromptCraft？**

1. **开发者中心** - 由开发者打造，为开发者服务
2. **零依赖理念** - 没有pip安装地狱，只有纯Python
3. **隐私优先** - 您的Prompt永远不会离开您的机器
4. **可扩展** - 模块化设计，易于扩展
5. **教育性** - 在使用中学习Prompt工程

### 📦 打包与部署

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI

# 开发模式安装
make install-dev

# 运行测试
make test

# 构建分发包
make build
```

#### 平台特定构建

```bash
# Windows可执行文件
make build-windows

# macOS可执行文件  
make build-macos

# Linux可执行文件
make build-linux
```

### 🤝 贡献指南

欢迎贡献！请遵循以下指南：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加 amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

**提交信息规范：**
- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更改
- `refactor:` 代码重构
- `test:` 测试更改

### 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

**PromptCraft-CLI** 是一款輕量級、零依賴的命令列工具，旨在幫助開發者輕鬆優化、測試和管理AI Prompt。隨著AI時代對高效Prompt工程的需求日益增長，PromptCraft 提供了一套全面的工具，用於分析Prompt品質、應用優化策略和測試Prompt效能。

**核心差異化亮點：**
- 🎯 **零依賴** - 僅使用Python標準庫
- ⚡ **極速執行** - 核心功能無需外部API呼叫
- 🔒 **隱私優先** - 所有處理均在本地完成
- 🎨 **精美TUI** - 互動式終端介面
- 📊 **資料驅動** - 基於評分的分析和建議

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| **🔍 Prompt分析** | 檢測品質問題、模糊術語、結構問題 | ✅ |
| **✨ 智慧優化** | 6種優化策略（Few-shot、CoT、ReAct等） | ✅ |
| **🧪 Prompt測試** | 批次測試、A/B對比、效能指標 | ✅ |
| **📁 專案管理** | 本地儲存的Prompt版本控制 | ✅ |
| **🖥️ 互動式TUI** | 帶有選單和視覺化的精美終端介面 | ✅ |
| **📈 評分系統** | 0-100品質評分，詳細分解 | ✅ |

### 🚀 快速開始

#### 安裝

```bash
# 從PyPI安裝（釋出後）
pip install promptcraft-cli

# 或本地克隆安裝
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI
pip install -e .
```

#### 使用

```bash
# 啟動互動式TUI
promptcraft

# 分析Prompt
promptcraft analyze "Your prompt here"

# 使用特定策略優化
promptcraft optimize "Your prompt" --strategy structured

# 測試Prompt
promptcraft test -f prompt.txt

# 列出專案
promptcraft projects

# 顯示優化技巧
promptcraft tips
```

### 📖 詳細使用指南

#### 1. Prompt分析

分析您的Prompt品質問題：

```bash
promptcraft analyze "寫一個處理資料的好函式"
```

**輸出示例：**
```
評分：45/100

⚠️ 發現的問題：
  • [中等] 發現1個模糊/主觀術語：好
    💡用具體、可衡量的標準替換模糊術語
  • [高] 未指定輸出格式
    💡明確說明期望的輸出格式

✨ 優勢：
  • 長度適中（9個詞）

📊 指標：
  • 詞數：9
  • 句子數：1
```

#### 2. Prompt優化

應用各種優化策略：

```bash
# 自動選擇最佳策略
promptcraft optimize "Your prompt"

# 使用特定策略
promptcraft optimize "Your prompt" --strategy few_shot

# 生成所有變體
promptcraft optimize "Your prompt" --all
```

**可用策略：**
- `structured` - 新增清晰的章節標題
- `few_shot` - 包含示例
- `cot` - 思維鏈推理
- `react` - 推理+行動模式
- `role` - 基於角色的Prompt
- `constraint` - 聚焦約束條件

#### 3. Prompt測試

使用模擬或真實LLM提供商測試Prompt：

```bash
# 測試單個Prompt
promptcraft test "Your prompt"

# 對比多個Prompt
promptcraft test --compare "Prompt A" "Prompt B" "Prompt C"

# A/B測試
promptcraft test --ab prompt_a.txt prompt_b.txt --cases cases.txt
```

#### 4. 專案管理

將Prompt組織到專案中：

```bash
# 列出專案
promptcraft projects

# 建立新專案
promptcraft projects create --name "My Project"

# 匯出專案
promptcraft projects export --id <project_id> --format markdown
```

### 💡 設計理念

**為什麼選擇PromptCraft？**

1. **開發者中心** - 由開發者打造，為開發者服務
2. **零依賴理念** - 沒有pip安裝地獄，只有純Python
3. **隱私優先** - 您的Prompt永遠不會離開您的機器
4. **可擴充套件** - 模組化設計，易於擴充套件
5. **教育性** - 在使用中學習Prompt工程

### 📦 打包與部署

#### 從原始碼構建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/PromptCraft-CLI.git
cd PromptCraft-CLI

# 開發模式安裝
make install-dev

# 執行測試
make test

# 構建分發包
make build
```

#### 平臺特定構建

```bash
# Windows可執行檔案
make build-windows

# macOS可執行檔案  
make build-macos

# Linux可執行檔案
make build-linux
```

### 🤝 貢獻指南

歡迎貢獻！請遵循以下指南：

1. Fork 倉庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 新增 amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

**提交資訊規範：**
- `feat:` 新功能
- `fix:` Bug修復
- `docs:` 文件更改
- `refactor:` 程式碼重構
- `test:` 測試更改

### 📄 開源協議

本專案採用 MIT 協議 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by gitstq**

[⭐ Star this repo](https://github.com/gitstq/PromptCraft-CLI) | [🐛 Report Bug](https://github.com/gitstq/PromptCraft-CLI/issues) | [💡 Request Feature](https://github.com/gitstq/PromptCraft-CLI/issues)

</div>
