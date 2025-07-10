import asyncio
from typing import Optional, Dict, Any
import httpx
from app.core.config import settings

class LLMManager:
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=settings.MAX_QUEUE_SIZE)
        
    async def generate_response(self, prompt: str, context: str, intent: str) -> str:
        """
        Generate a response using either Ollama or OpenAI (fallback).
        
        Args:
            prompt: User's query
            context: Retrieved context from vector store
            intent: Classified intent
            
        Returns:
            Generated response
        """
        # Add request to queue
        await self.queue.put((prompt, context))
        
        try:
            # Try Ollama first
            response = await self._generate_ollama(prompt, context, intent)
            if response:
                return response
                
            # Fallback to OpenAI if Ollama fails and API key is available
            if settings.OPENAI_API_KEY:
                return await self._generate_openai(prompt, context, intent)
                
            return "Error: Unable to generate response. Both Ollama and OpenAI are unavailable."
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"
        finally:
            # Remove request from queue
            await self.queue.get()
            
    async def _generate_ollama(self, prompt: str, context: str, intent: str) -> Optional[str]:
        """Generate response using Ollama"""
        try:
            # Construct prompt based on intent
            system_prompt = self._get_system_prompt(intent)
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}\n\nAnswer:"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.MODEL_NAME,
                        "prompt": full_prompt,
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()["response"]
                return None
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return None
            
    async def _generate_openai(self, prompt: str, context: str, intent: str) -> str:
        """Generate response using OpenAI (fallback)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": self._get_system_prompt(intent)},
                            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
                        ],
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                return f"OpenAI API error: {response.status_code}"
                
        except Exception as e:
            return f"OpenAI API error: {str(e)}"
            
    def _get_system_prompt(self, intent: str) -> str:
        """Get appropriate system prompt based on intent"""
        prompts = {
            "technical": "You are a technical support specialist. Provide clear, step-by-step solutions to technical problems.",
            "billing": "You are a billing support specialist. Help users with pricing, payments, and account-related queries.",
            "feature": "You are a product specialist. Help users understand current features and provide information about upcoming features."
        }
        return prompts.get(intent, "You are a helpful support assistant.") 