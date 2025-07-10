import os
from openai import OpenAI
from typing import Dict, Any

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "test-key")
        self.is_test_mode = api_key == "test-key"
        if not self.is_test_mode:
            self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))

    def generate_content(self, idea: Dict[str, Any]) -> str:
        """
        Generate content based on the provided idea
        
        Args:
            idea (Dict[str, Any]): Dictionary containing idea details
                - title: str
                - description: str
                - keywords: List[str]
                - target_audience: str
        
        Returns:
            str: Generated content in markdown format
        """
        if self.is_test_mode:
            return self._generate_test_content(idea)
            
        prompt = self._create_prompt(idea)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional content writer who creates engaging blog posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return self._generate_test_content(idea)

    def _create_prompt(self, idea: Dict[str, Any]) -> str:
        """Create a detailed prompt for content generation"""
        return f"""
        Write a comprehensive blog post about {idea['title']}.
        
        Key points to cover:
        - {idea['description']}
        
        Target audience: {idea['target_audience']}
        Keywords to include: {', '.join(idea['keywords'])}
        
        Please write in a professional yet engaging tone, using markdown formatting.
        Include:
        1. An attention-grabbing introduction
        2. Well-structured main sections
        3. Practical examples or case studies
        4. A clear conclusion
        5. Call to action
        
        Format the content using proper markdown with headers, lists, and emphasis where appropriate.
        """

    def _generate_test_content(self, idea: Dict[str, Any]) -> str:
        """Generate test content when no API key is available"""
        return f"""# {idea['title']}

## Introduction

This is a test article generated without an OpenAI API key. To generate real content, please add your OpenAI API key to the .env file.

## About

{idea['description']}

## Target Audience

This content is written for {idea['target_audience']}.

## Keywords

Key topics covered:
{', '.join(f'- {keyword}' for keyword in idea['keywords'])}

## Note

This is a placeholder article. To generate actual content:
1. Get an OpenAI API key from https://platform.openai.com
2. Add it to your .env file as OPENAI_API_KEY=your_key_here
3. Restart the application

## Conclusion

Thank you for testing the Content Creation Tool!
"""

    def refine_content(self, content: str, feedback: str) -> str:
        """
        Refine the generated content based on feedback
        
        Args:
            content (str): Original content
            feedback (str): User feedback for improvements
            
        Returns:
            str: Refined content
        """
        if self.is_test_mode:
            return f"{content}\n\n## Feedback Applied (Test Mode)\n\n{feedback}"
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional editor who improves content while maintaining its core message."},
                    {"role": "user", "content": f"Here's the original content:\n\n{content}\n\nPlease improve it based on this feedback:\n{feedback}"}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error refining content: {str(e)}")
            return f"{content}\n\n## Feedback Applied (Error)\n\n{feedback}" 