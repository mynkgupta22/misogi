import json
import re
import os
from typing import Dict, List, Any, Optional
from .tool_optimizers import (
    GitHubCopilotOptimizer,
    CursorOptimizer,
    ReplitGhostOptimizer,
    AWSCodeWhispererOptimizer,
    ClaudeSonnetOptimizer,
    GPT4Optimizer
)

class PromptOptimizer:
    def __init__(self, tools_file: str = None):
        """Initialize the prompt optimizer with tool database"""
        if tools_file is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the Q3 directory
            parent_dir = os.path.dirname(current_dir)
            tools_file = os.path.join(parent_dir, 'tool_analysis.json')
        
        self.tools_file = tools_file
        self.tools = self._load_tools()
        
        # Initialize tool-specific optimizers
        self.tool_optimizers = {
            'github_copilot': GitHubCopilotOptimizer(),
            'cursor': CursorOptimizer(),
            'replit_ghost': ReplitGhostOptimizer(),
            'aws_codewhisperer': AWSCodeWhispererOptimizer(),
            'claude_sonnet': ClaudeSonnetOptimizer(),
            'gpt4': GPT4Optimizer()
        }
        
        # Prompt analysis keywords
        self.analysis_keywords = {
            'complexity': {
                'simple': ['simple', 'basic', 'easy', 'quick', 'small'],
                'medium': ['moderate', 'standard', 'typical', 'normal'],
                'complex': ['complex', 'difficult', 'advanced', 'challenging']
            },
            'intent': {
                'code_generation': ['create', 'build', 'write', 'generate'],
                'code_completion': ['complete', 'finish', 'add', 'extend'],
                'debugging': ['debug', 'fix', 'error', 'bug', 'issue'],
                'refactoring': ['refactor', 'improve', 'optimize'],
                'documentation': ['document', 'comment', 'explain'],
                'testing': ['test', 'unit test', 'validate']
            },
            'languages': {
                'python': r'\bpython\b',
                'javascript': r'\b(js|javascript|node|react)\b',
                'java': r'\bjava\b',
                'c++': r'\bc\+\+\b',
                'go': r'\bgo\b',
                'rust': r'\brust\b'
            },
            'domains': {
                'web_development': ['web', 'frontend', 'backend', 'api', 'rest'],
                'mobile_development': ['mobile', 'ios', 'android'],
                'data_science': ['data', 'ml', 'ai', 'machine learning'],
                'cloud_computing': ['cloud', 'aws', 'azure', 'serverless'],
                'game_development': ['game', 'unity', 'graphics'],
                'system_programming': ['system', 'low-level', 'driver']
            }
        }

    def _load_tools(self) -> List[Dict[str, Any]]:
        """Load tools from the JSON database"""
        try:
            with open(self.tools_file, 'r') as f:
                data = json.load(f)
                return data.get('tools', [])
        except FileNotFoundError:
            print(f"Warning: {self.tools_file} not found. Using empty tools list.")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {self.tools_file}. Using empty tools list.")
            return []

    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze a prompt to understand its intent, complexity, and requirements"""
        prompt_lower = prompt.lower()
        
        # Analyze complexity
        complexity = self._analyze_complexity(prompt_lower)
        
        # Analyze intent
        intent = self._analyze_intent(prompt_lower)
        
        # Detect languages
        languages = self._detect_languages(prompt_lower)
        
        # Detect domains
        domains = self._detect_domains(prompt_lower)
        
        # Analyze prompt characteristics
        characteristics = {
            'word_count': len(prompt.split()),
            'has_code_snippets': bool(re.search(r'```|`.*`', prompt)),
            'has_specific_requirements': self._has_specific_requirements(prompt_lower),
            'has_context': self._has_context(prompt_lower),
            'clarity_score': self._calculate_clarity_score(prompt)
        }
        
        return {
            'complexity': complexity,
            'intent': intent,
            'languages': languages,
            'domains': domains,
            'characteristics': characteristics,
            'suggestions': self._generate_analysis_suggestions(prompt_lower, characteristics)
        }

    def _analyze_complexity(self, prompt: str) -> str:
        """Analyze the complexity level of the prompt"""
        for level, keywords in self.analysis_keywords['complexity'].items():
            if any(keyword in prompt for keyword in keywords):
                return level
        return 'medium'

    def _analyze_intent(self, prompt: str) -> List[str]:
        """Analyze the intent of the prompt"""
        detected_intents = []
        for intent, keywords in self.analysis_keywords['intent'].items():
            if any(keyword in prompt for keyword in keywords):
                detected_intents.append(intent)
        return detected_intents if detected_intents else ['general']

    def _detect_languages(self, prompt: str) -> List[str]:
        """Detect programming languages mentioned in the prompt"""
        languages = []
        for lang, pattern in self.analysis_keywords['languages'].items():
            if re.search(pattern, prompt):
                languages.append(lang)
        return languages

    def _detect_domains(self, prompt: str) -> List[str]:
        """Detect domains mentioned in the prompt"""
        domains = []
        for domain, keywords in self.analysis_keywords['domains'].items():
            if any(keyword in prompt for keyword in keywords):
                domains.append(domain)
        return domains

    def _has_specific_requirements(self, prompt: str) -> bool:
        """Check if the prompt has specific requirements"""
        specific_indicators = ['should', 'must', 'need', 'require', 'include', 'specify']
        return any(indicator in prompt for indicator in specific_indicators)

    def _has_context(self, prompt: str) -> bool:
        """Check if the prompt provides context"""
        context_indicators = ['in', 'for', 'with', 'using', 'based on', 'given', 'context']
        return any(indicator in prompt for indicator in context_indicators)

    def _calculate_clarity_score(self, prompt: str) -> float:
        """Calculate a clarity score for the prompt (0-1)"""
        score = 0.0
        
        # Length factor
        word_count = len(prompt.split())
        if 20 <= word_count <= 100:
            score += 0.3
        elif word_count > 100:
            score += 0.2
        else:
            score += 0.1
        
        # Specificity factor
        if self._has_specific_requirements(prompt.lower()):
            score += 0.3
        
        # Context factor
        if self._has_context(prompt.lower()):
            score += 0.2
        
        # Language specificity
        if self._detect_languages(prompt.lower()):
            score += 0.2
        
        return min(score, 1.0)

    def _generate_analysis_suggestions(self, prompt: str, characteristics: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving the prompt"""
        suggestions = []
        
        if characteristics['word_count'] < 10:
            suggestions.append("Consider adding more details about your requirements")
        
        if not characteristics['has_specific_requirements']:
            suggestions.append("Try to be more specific about what you need")
        
        if not characteristics['has_context']:
            suggestions.append("Provide more context about your project or environment")
        
        if not self._detect_languages(prompt):
            suggestions.append("Specify the programming language you want to use")
        
        return suggestions

    def optimize_prompt(self, base_prompt: str, target_tool: str) -> Dict[str, Any]:
        """Optimize a prompt for a specific tool"""
        # Analyze the original prompt
        analysis = self.analyze_prompt(base_prompt)
        
        # Get tool information
        tool_info = self.get_tool_by_id(target_tool)
        if not tool_info:
            return {'error': f'Tool "{target_tool}" not found'}
        
        # Apply tool-specific optimization
        optimized_prompt = self._apply_tool_optimization(base_prompt, tool_info, analysis)
        
        # Generate explanations
        explanations = self._generate_optimization_explanations(base_prompt, optimized_prompt, tool_info, analysis)
        
        return {
            'original_prompt': base_prompt,
            'optimized_prompt': optimized_prompt,
            'target_tool': target_tool,
            'tool_info': tool_info,
            'analysis': analysis,
            'explanations': explanations,
            'improvement_score': self._calculate_improvement_score(base_prompt, optimized_prompt, analysis)
        }

    def _apply_tool_optimization(self, prompt: str, tool_info: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Apply tool-specific optimization strategies"""
        optimized = prompt
        
        # Get optimization strategies for the tool
        strategies = tool_info.get('optimization_strategies', {})
        
        # Apply context enhancement if needed
        if not analysis['characteristics']['has_context'] and 'context_enhancement' in strategies:
            optimized = self._enhance_context(optimized, tool_info)
        
        # Apply specificity improvement if needed
        if not analysis['characteristics']['has_specific_requirements'] and 'specificity_improvement' in strategies:
            optimized = self._improve_specificity(optimized, tool_info)
        
        # Apply tool-specific strategies
        if tool_info['id'] == 'github_copilot':
            optimized = self._optimize_for_copilot(optimized, analysis)
        elif tool_info['id'] == 'cursor':
            optimized = self._optimize_for_cursor(optimized, analysis)
        elif tool_info['id'] == 'aws_codewhisperer':
            optimized = self._optimize_for_codewhisperer(optimized, analysis)
        elif tool_info['id'] == 'claude_sonnet':
            optimized = self._optimize_for_claude(optimized, analysis)
        elif tool_info['id'] == 'gpt4':
            optimized = self._optimize_for_gpt4(optimized, analysis)
        elif tool_info['id'] == 'replit_ghost':
            optimized = self._optimize_for_replit(optimized, analysis)
        
        return optimized

    def _enhance_context(self, prompt: str, tool_info: Dict[str, Any]) -> str:
        """Enhance prompt with more context"""
        context_additions = []
        
        if 'context_enhancement' in tool_info.get('optimization_strategies', {}):
            context_additions.append("Please provide the code with appropriate context and comments.")
        
        if context_additions:
            prompt += " " + " ".join(context_additions)
        
        return prompt

    def _improve_specificity(self, prompt: str, tool_info: Dict[str, Any]) -> str:
        """Improve prompt specificity"""
        specificity_additions = []
        
        if 'specificity_improvement' in tool_info.get('optimization_strategies', {}):
            specificity_additions.append("Include error handling and edge cases.")
        
        if specificity_additions:
            prompt += " " + " ".join(specificity_additions)
        
        return prompt

    def _optimize_for_copilot(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for GitHub Copilot"""
        if not analysis['languages']:
            prompt += " Use Python for this implementation."
        
        if 'code_generation' in analysis['intent']:
            prompt = prompt.replace('create', 'Create a function that')
            prompt = prompt.replace('build', 'Build a function that')
        
        return prompt

    def _optimize_for_cursor(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Cursor"""
        if analysis['complexity'] == 'complex':
            prompt += " Please break this down into steps and provide a complete solution."
        
        if not analysis['characteristics']['has_context']:
            prompt += " Consider this as part of a larger project."
        
        return prompt

    def _optimize_for_codewhisperer(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for AWS CodeWhisperer"""
        if 'cloud_computing' not in analysis['domains']:
            prompt += " Consider AWS best practices and security standards."
        
        return prompt

    def _optimize_for_claude(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Claude Sonnet"""
        if analysis['complexity'] == 'complex':
            prompt += " Please provide detailed explanations and reasoning for your approach."
        
        return prompt

    def _optimize_for_gpt4(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for GPT-4"""
        prompt += " Please provide multiple approaches and explain the trade-offs."
        
        return prompt

    def _optimize_for_replit(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Optimize prompt for Replit Ghost"""
        prompt += " Include deployment considerations and educational comments."
        
        return prompt

    def _generate_optimization_explanations(self, original: str, optimized: str, tool_info: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate explanations for the optimizations made"""
        explanations = []
        
        # Compare lengths
        if len(optimized.split()) > len(original.split()) * 1.2:
            explanations.append({
                'type': 'expansion',
                'title': 'Enhanced Detail',
                'description': f'The prompt was expanded to provide more context for {tool_info["name"]}.'
            })
        
        # Check for language specification
        if not analysis['languages'] and any(lang in optimized.lower() for lang in ['python', 'javascript', 'java']):
            explanations.append({
                'type': 'language',
                'title': 'Language Specification Added',
                'description': f'Added programming language specification for {tool_info["name"]}.'
            })
        
        # Tool-specific optimizations
        if tool_info.get('optimization_strategies'):
            for strategy_name, strategy in tool_info['optimization_strategies'].items():
                explanations.append({
                    'type': 'tool_specific',
                    'title': f'{strategy_name.replace("_", " ").title()}',
                    'description': strategy['description']
                })
        
        return explanations

    def _calculate_improvement_score(self, original: str, optimized: str, analysis: Dict[str, Any]) -> float:
        """Calculate an improvement score (0-1)"""
        score = 0.0
        
        # Length improvement
        original_words = len(original.split())
        optimized_words = len(optimized.split())
        if optimized_words > original_words * 1.1:
            score += 0.3
        
        # Clarity improvement
        original_clarity = analysis['characteristics']['clarity_score']
        optimized_analysis = self.analyze_prompt(optimized)
        optimized_clarity = optimized_analysis['characteristics']['clarity_score']
        
        if optimized_clarity > original_clarity:
            score += 0.4
        
        # Specificity improvement
        if not analysis['characteristics']['has_specific_requirements'] and self._has_specific_requirements(optimized.lower()):
            score += 0.3
        
        return min(score, 1.0)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools"""
        return self.tools

    def get_tool_by_id(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific tool by ID"""
        for tool in self.tools:
            if tool['id'] == tool_id:
                return tool
        return None

    def get_optimization_strategies(self, tool_id: str) -> Dict[str, Any]:
        """Get optimization strategies for a specific tool"""
        tool = self.get_tool_by_id(tool_id)
        if tool:
            return tool.get('optimization_strategies', {})
        return {} 