"""
Adaptive Prompt Optimizer Package

This package contains the core optimization logic for adapting prompts
to specific AI coding tools.
"""

from .prompt_optimizer import PromptOptimizer
from .tool_optimizers import (
    BaseOptimizer,
    GitHubCopilotOptimizer,
    CursorOptimizer,
    ReplitGhostOptimizer,
    AWSCodeWhispererOptimizer,
    ClaudeSonnetOptimizer,
    GPT4Optimizer
)

__version__ = "1.0.0"
__author__ = "Adaptive Prompt Optimizer Team"

__all__ = [
    'PromptOptimizer',
    'BaseOptimizer',
    'GitHubCopilotOptimizer',
    'CursorOptimizer',
    'ReplitGhostOptimizer',
    'AWSCodeWhispererOptimizer',
    'ClaudeSonnetOptimizer',
    'GPT4Optimizer'
] 