import json
import re
from typing import List, Dict, Any
import numpy as np

class RecommendationEngine:
    def __init__(self, agents_file: str = 'agents_db.json'):
        """Initialize the recommendation engine with agent database"""
        self.agents_file = agents_file
        self.agents = self._load_agents()
        
        # Task type keywords for classification
        self.task_keywords = {
            'code_completion': [
                'complete', 'finish', 'suggest', 'autocomplete', 'boilerplate',
                'template', 'skeleton', 'fill in', 'missing code'
            ],
            'ide_integration': [
                'ide', 'editor', 'vscode', 'intellij', 'pycharm', 'sublime',
                'atom', 'integrated', 'plugin', 'extension'
            ],
            'multi_language': [
                'python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust',
                'php', 'ruby', 'swift', 'kotlin', 'typescript', 'multiple languages'
            ],
            'real_time': [
                'real-time', 'live', 'instant', 'immediate', 'as you type',
                'continuous', 'streaming', 'interactive'
            ],
            'complex_problem_solving': [
                'algorithm', 'complex', 'difficult', 'challenging', 'optimization',
                'design pattern', 'architecture', 'system design', 'advanced',
                'sophisticated', 'intricate', 'multi-step', 'problem solving'
            ],
            'file_management': [
                'file', 'create', 'delete', 'modify', 'organize', 'structure',
                'project setup', 'file system', 'directory', 'folder'
            ],
            'debugging': [
                'debug', 'fix', 'error', 'bug', 'issue', 'troubleshoot',
                'problem', 'crash', 'exception', 'log', 'trace'
            ],
            'testing': [
                'test', 'unit test', 'integration test', 'test case',
                'assertion', 'coverage', 'qa', 'quality assurance'
            ]
        }
        
        # Task complexity indicators
        self.complexity_indicators = {
            'simple': ['simple', 'basic', 'easy', 'quick', 'small', 'minor'],
            'medium': ['moderate', 'standard', 'typical', 'normal', 'average'],
            'complex': ['complex', 'difficult', 'advanced', 'sophisticated', 'challenging']
        }
        
        # Domain-specific keywords
        self.domain_keywords = {
            'web_development': ['web', 'frontend', 'backend', 'html', 'css', 'react', 'angular', 'vue', 'node'],
            'mobile_development': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin'],
            'data_science': ['data', 'ml', 'ai', 'machine learning', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
            'cloud_computing': ['cloud', 'aws', 'azure', 'gcp', 'serverless', 'microservices', 'docker', 'kubernetes'],
            'game_development': ['game', 'unity', 'unreal', 'graphics', '3d', '2d', 'gaming'],
            'system_programming': ['system', 'low-level', 'c', 'c++', 'assembly', 'driver', 'kernel']
        }

    def _load_agents(self) -> List[Dict[str, Any]]:
        """Load agents from the JSON database"""
        try:
            with open(self.agents_file, 'r') as f:
                data = json.load(f)
                return data.get('agents', [])
        except FileNotFoundError:
            print(f"Warning: {self.agents_file} not found. Using empty agent list.")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {self.agents_file}. Using empty agent list.")
            return []

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze the task description to extract requirements and characteristics"""
        task_lower = task_description.lower()
        
        # Analyze task type requirements
        task_requirements = {}
        for requirement, keywords in self.task_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            task_requirements[requirement] = min(score / len(keywords), 1.0)
        
        # Determine complexity
        complexity = 'medium'  # default
        for comp_level, indicators in self.complexity_indicators.items():
            if any(indicator in task_lower for indicator in indicators):
                complexity = comp_level
                break
        
        # Identify domains
        identified_domains = []
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                identified_domains.append(domain)
        
        # Language detection
        languages = []
        language_patterns = {
            'python': r'\bpython\b',
            'javascript': r'\b(js|javascript|node|react|vue|angular)\b',
            'java': r'\bjava\b',
            'c++': r'\bc\+\+\b',
            'c#': r'\bc#\b',
            'go': r'\bgo\b',
            'rust': r'\brust\b',
            'php': r'\bphp\b',
            'ruby': r'\bruby\b',
            'swift': r'\bswift\b',
            'kotlin': r'\bkotlin\b'
        }
        
        for lang, pattern in language_patterns.items():
            if re.search(pattern, task_lower):
                languages.append(lang)
        
        return {
            'requirements': task_requirements,
            'complexity': complexity,
            'domains': identified_domains,
            'languages': languages,
            'word_count': len(task_description.split()),
            'has_code_snippets': bool(re.search(r'```|`.*`', task_description))
        }

    def calculate_agent_score(self, agent: Dict[str, Any], task_analysis: Dict[str, Any]) -> float:
        """Calculate a score for how well an agent matches the task requirements"""
        score = 0.0
        weights = agent.get('score_weights', {})
        requirements = task_analysis.get('requirements', {})
        
        # Base matching score
        for requirement, task_score in requirements.items():
            if requirement in weights:
                agent_capability = weights[requirement]
                # Weighted score based on how well agent capability matches task requirement
                score += task_score * agent_capability * 0.3
        
        # Complexity adjustment
        complexity = task_analysis.get('complexity', 'medium')
        if complexity == 'complex' and weights.get('complex_problem_solving', 0) > 0.7:
            score += 0.2
        elif complexity == 'simple' and weights.get('code_completion', 0) > 0.7:
            score += 0.1
        
        # Domain-specific bonuses
        domains = task_analysis.get('domains', [])
        if 'cloud_computing' in domains and agent['id'] == 'aws_codewhisperer':
            score += 0.3
        elif 'web_development' in domains and agent['id'] in ['replit_ghost', 'cursor']:
            score += 0.2
        elif 'data_science' in domains and agent['id'] in ['claude_sonnet', 'gpt4']:
            score += 0.2
        
        # Language-specific bonuses
        languages = task_analysis.get('languages', [])
        if languages:
            if 'python' in languages and agent['id'] == 'kite':
                score += 0.2
            elif 'javascript' in languages and agent['id'] == 'kite':
                score += 0.2
        
        # Code snippet detection
        if task_analysis.get('has_code_snippets', False):
            if weights.get('code_completion', 0) > 0.7:
                score += 0.1
        
        # Length-based adjustments
        word_count = task_analysis.get('word_count', 0)
        if word_count > 100 and weights.get('complex_problem_solving', 0) > 0.6:
            score += 0.1
        elif word_count < 50 and weights.get('real_time', 0) > 0.7:
            score += 0.1
        
        return min(score, 1.0)

    def get_recommendations(self, task_description: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Get top-k agent recommendations for a given task"""
        if not self.agents:
            return []
        
        # Analyze the task
        task_analysis = self.analyze_task(task_description)
        
        # Calculate scores for all agents
        agent_scores = []
        for agent in self.agents:
            score = self.calculate_agent_score(agent, task_analysis)
            agent_scores.append({
                'agent': agent,
                'score': score,
                'justification': self._generate_justification(agent, task_analysis, score)
            })
        
        # Sort by score and return top-k
        agent_scores.sort(key=lambda x: x['score'], reverse=True)
        
        recommendations = []
        for i, item in enumerate(agent_scores[:top_k]):
            recommendation = {
                'rank': i + 1,
                'agent': item['agent'],
                'score': round(item['score'], 3),
                'justification': item['justification'],
                'match_percentage': round(item['score'] * 100, 1)
            }
            recommendations.append(recommendation)
        
        return recommendations

    def _generate_justification(self, agent: Dict[str, Any], task_analysis: Dict[str, Any], score: float) -> str:
        """Generate a human-readable justification for the recommendation"""
        justifications = []
        
        # High-scoring capabilities
        weights = agent.get('score_weights', {})
        requirements = task_analysis.get('requirements', {})
        
        strong_matches = []
        for req, req_score in requirements.items():
            if req_score > 0.5 and req in weights and weights[req] > 0.6:
                strong_matches.append(req.replace('_', ' ').title())
        
        if strong_matches:
            justifications.append(f"Strong in: {', '.join(strong_matches)}")
        
        # Domain-specific reasoning
        domains = task_analysis.get('domains', [])
        if 'cloud_computing' in domains and agent['id'] == 'aws_codewhisperer':
            justifications.append("Specialized for AWS and cloud development")
        elif 'web_development' in domains and agent['id'] == 'replit_ghost':
            justifications.append("Excellent for web development with built-in deployment")
        
        # Complexity reasoning
        complexity = task_analysis.get('complexity', 'medium')
        if complexity == 'complex' and weights.get('complex_problem_solving', 0) > 0.7:
            justifications.append("Well-suited for complex problem solving")
        elif complexity == 'simple' and weights.get('code_completion', 0) > 0.7:
            justifications.append("Perfect for quick code completion tasks")
        
        # Language-specific reasoning
        languages = task_analysis.get('languages', [])
        if languages and agent['id'] == 'kite':
            if any(lang in languages for lang in ['python', 'javascript']):
                justifications.append(f"Specialized in {', '.join(languages)} development")
        
        # Default justification if no specific matches
        if not justifications:
            if score > 0.7:
                justifications.append("Good overall match for your requirements")
            elif score > 0.5:
                justifications.append("Moderate match with some relevant capabilities")
            else:
                justifications.append("Basic match - consider other options for better fit")
        
        return '; '.join(justifications)

    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all available agents"""
        return self.agents

    def get_agent_by_id(self, agent_id: str) -> Dict[str, Any]:
        """Get a specific agent by ID"""
        for agent in self.agents:
            if agent['id'] == agent_id:
                return agent
        return None

    def search_agents(self, query: str) -> List[Dict[str, Any]]:
        """Search agents by name, description, or capabilities"""
        query_lower = query.lower()
        results = []
        
        for agent in self.agents:
            # Search in name
            if query_lower in agent['name'].lower():
                results.append(agent)
                continue
            
            # Search in description
            if query_lower in agent['description'].lower():
                results.append(agent)
                continue
            
            # Search in capabilities
            if any(query_lower in cap.lower() for cap in agent.get('capabilities', [])):
                results.append(agent)
                continue
            
            # Search in strengths
            if any(query_lower in strength.lower() for strength in agent.get('strengths', [])):
                results.append(agent)
                continue
        
        return results 