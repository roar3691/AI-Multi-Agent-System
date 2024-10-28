"""
AI/GenAI Use Case Generator
Author: Y RAGHUVAMSHI REDDY
Description: A multi-agent system that researches companies and generates AI/GenAI use cases 
using LLaMA model and Tavily API.

This system:
1. Researches companies using Tavily API
2. Generates AI use cases using LLaMA model
3. Saves comprehensive reports in JSON format
"""

import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from typing import Dict, List
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download

# Load environment variables
load_dotenv()

class AIResearchSystem:
    """Multi-agent system for company research and AI use case generation"""
    
    def __init__(self):
        # Load API keys from environment variables
        self.TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
        self.HUGGINGFACE_KEY = os.getenv('HUGGINGFACE_KEY')
        
        if not self.TAVILY_API_KEY or not self.HUGGINGFACE_KEY:
            raise ValueError("API keys not found. Please set TAVILY_API_KEY and HUGGINGFACE_KEY in .env file")
        
        # Setup reports directory
        self.reports_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI_MULTI AGENT_SYSTEM', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Initialize LLaMA model
        self.llm = self._initialize_llm()

    [Rest of your code remains exactly the same, just add proper docstrings]
