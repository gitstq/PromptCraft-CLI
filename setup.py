#!/usr/bin/env python3
"""
Setup script for PromptCraft CLI
"""

from setuptools import setup, find_packages
import os

# Read README
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.md')
long_description = ''
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='promptcraft-cli',
    version='1.0.0',
    author='PromptCraft Team',
    author_email='promptcraft@example.com',
    description='🚀 Lightweight Prompt Engineering & Version Management CLI Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitstq/promptcraft-cli',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    install_requires=[
        # No external dependencies for core functionality
        # Keeping it lightweight and zero-dependency
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'yaml': [
            'PyYAML>=6.0',
        ],
        'clipboard': [
            'pyperclip>=1.8.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'promptcraft=promptcraft.cli:main',
            'pc=promptcraft.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords='prompt engineering, llm, ai, cli, version control, optimization',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/promptcraft-cli/issues',
        'Source': 'https://github.com/gitstq/promptcraft-cli',
        'Documentation': 'https://github.com/gitstq/promptcraft-cli#readme',
    },
)
