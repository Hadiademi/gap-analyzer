import os
import openai
import requests
import json
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenSourceEmbeddings:
    """
    Open source embeddings using Sentence Transformers
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embeddings model
        
        Args:
            model_name: Name of the sentence transformer model to use
                      Options: 'all-MiniLM-L6-v2', 'all-mpnet-base-v2', 'paraphrase-multilingual-MiniLM-L12-v2'
        """
        self.model = SentenceTransformer(model_name)
        
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query
        
        Args:
            text: Input text to embed
            
        Returns:
            List of embedding values
        """
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

class OpenAILLM:
    """
    OpenAI API client for LLM operations
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (if not provided, will use environment variable)
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
        openai.api_key = self.api_key
    
    def ask_llm(self, question: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Send a question to OpenAI API
        
        Args:
            question: The prompt/question to send
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Response from the model
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": question}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Error: Could not get response from OpenAI"

class AnthropicLLM:
    """
    Anthropic API client for LLM operations
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize Anthropic client
        
        Args:
            api_key: Anthropic API key (if not provided, will use environment variable)
            model: Model to use (claude-3-sonnet-20240229, claude-3-haiku-20240307, etc.)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
    
    def ask_llm(self, question: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Send a question to Anthropic API
        
        Args:
            question: The prompt/question to send
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Response from the model
        """
        try:
            headers = {
                "x-api-key": self.api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                error_msg = f"Anthropic API error: Status {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text[:500]}"
                print(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error calling Anthropic API: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error calling Anthropic API: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)

# Factory functions for easy usage
def create_embeddings(model_name: str = "all-MiniLM-L6-v2") -> OpenSourceEmbeddings:
    """
    Create embeddings instance
    
    Args:
        model_name: Sentence transformer model name
        
    Returns:
        OpenSourceEmbeddings instance
    """
    return OpenSourceEmbeddings(model_name)

def create_openai_llm(model: str = "gpt-4") -> OpenAILLM:
    """
    Create OpenAI LLM instance
    
    Args:
        model: OpenAI model name
        
    Returns:
        OpenAILLM instance
    """
    return OpenAILLM(model=model)

def create_anthropic_llm(model: str = "claude-3-sonnet-20240229") -> AnthropicLLM:
    """
    Create Anthropic LLM instance
    
    Args:
        model: Anthropic model name
        
    Returns:
        AnthropicLLM instance
    """
    return AnthropicLLM(model=model)

def get_llm():
    """
    Get LLM instance based on environment variable LLM_PROVIDER
    Defaults to Anthropic if available, otherwise OpenAI
    
    Returns:
        LLM instance (OpenAILLM or AnthropicLLM)
    """
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022") if provider == "anthropic" else os.getenv("OPENAI_MODEL", "gpt-4")
    
    if provider == "anthropic":
        return create_anthropic_llm(model=model)
    else:
        return create_openai_llm(model=model)

# Default instances for backward compatibility
def get_default_embeddings():
    """Get default embeddings instance"""
    return create_embeddings()

def get_default_llm():
    """Get default LLM instance (OpenAI by default)"""
    return create_openai_llm()
