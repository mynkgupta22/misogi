"""
Tool-specific optimizer classes for different AI coding tools
"""

from typing import Dict, Any, List

class BaseOptimizer:
    """Base class for tool-specific optimizers"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize a prompt for the specific tool"""
        raise NotImplementedError

class GitHubCopilotOptimizer(BaseOptimizer):
    """Optimizer for GitHub Copilot"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for GitHub Copilot"""
        optimized = prompt
        
        # Add language specification if missing
        if not analysis['languages']:
            optimized += " Use Python for this implementation."
        
        # Improve function/class naming
        if 'code_generation' in analysis['intent']:
            optimized = optimized.replace('create', 'Create a function that')
            optimized = optimized.replace('build', 'Build a function that')
            optimized = optimized.replace('write', 'Write a function that')
        
        # Add type hints for better completion
        if 'python' in analysis['languages']:
            optimized += " Include type hints and docstrings."
        
        # Add context for better suggestions
        if not analysis['characteristics']['has_context']:
            optimized += " Consider this as part of a larger codebase."
        
        return optimized

class CursorOptimizer(BaseOptimizer):
    """Optimizer for Cursor"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Cursor"""
        optimized = prompt
        
        # Add project structure for complex tasks
        if analysis['complexity'] == 'complex':
            optimized += " Please break this down into steps and provide a complete solution with file structure."
        
        # Add comprehensive requirements
        if not analysis['characteristics']['has_specific_requirements']:
            optimized += " Include error handling, testing, and documentation."
        
        # Add architecture context
        if not analysis['characteristics']['has_context']:
            optimized += " Consider this as part of a larger project with proper architecture."
        
        # Add deployment considerations
        if 'web_development' in analysis['domains']:
            optimized += " Include deployment and hosting considerations."
        
        return optimized

class ReplitGhostOptimizer(BaseOptimizer):
    """Optimizer for Replit Ghost"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Replit Ghost"""
        optimized = prompt
        
        # Add educational context
        optimized += " Include detailed comments explaining the code for educational purposes."
        
        # Add deployment considerations
        optimized += " Consider deployment and hosting on Replit."
        
        # Add collaboration features
        if analysis['complexity'] == 'medium' or analysis['complexity'] == 'complex':
            optimized += " Make the code suitable for team collaboration and learning."
        
        # Add responsive design for web projects
        if 'web_development' in analysis['domains']:
            optimized += " Include responsive design and mobile-friendly features."
        
        return optimized

class AWSCodeWhispererOptimizer(BaseOptimizer):
    """Optimizer for AWS CodeWhisperer"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for AWS CodeWhisperer"""
        optimized = prompt
        
        # Add AWS-specific context
        if 'cloud_computing' not in analysis['domains']:
            optimized += " Consider AWS best practices and security standards."
        
        # Add security requirements
        optimized += " Include security best practices, IAM roles, and encryption."
        
        # Add AWS service specifications
        if 'web_development' in analysis['domains']:
            optimized += " Use AWS Lambda, API Gateway, and DynamoDB where appropriate."
        
        # Add monitoring and logging
        optimized += " Include CloudWatch monitoring and proper logging."
        
        return optimized

class ClaudeSonnetOptimizer(BaseOptimizer):
    """Optimizer for Claude Sonnet"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Claude Sonnet"""
        optimized = prompt
        
        # Add reasoning requirements for complex tasks
        if analysis['complexity'] == 'complex':
            optimized += " Please provide detailed explanations and reasoning for your approach."
        
        # Add step-by-step breakdown
        if len(optimized.split()) > 50:
            optimized += " Break down the solution into logical steps with explanations."
        
        # Add algorithm analysis if applicable
        if 'data_science' in analysis['domains'] or 'system_programming' in analysis['domains']:
            optimized += " Analyze the time and space complexity of your solution."
        
        # Add documentation requirements
        optimized += " Include comprehensive documentation and comments explaining the logic."
        
        return optimized

class GPT4Optimizer(BaseOptimizer):
    """Optimizer for GPT-4"""
    
    def optimize(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for GPT-4"""
        optimized = prompt
        
        # Leverage GPT-4's broad knowledge
        optimized += " Please provide multiple approaches and explain the trade-offs."
        
        # Add best practices
        optimized += " Include industry best practices and design patterns."
        
        # Add comprehensive analysis
        if analysis['complexity'] == 'medium' or analysis['complexity'] == 'complex':
            optimized += " Provide a comprehensive analysis with pros and cons of different approaches."
        
        # Add learning resources
        optimized += " Include references to relevant documentation and learning resources."
        
        return optimized 