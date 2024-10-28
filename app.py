"""
Fast AI/GenAI Use Case Generator
Author: Y RAGHUVAMSHI REDDY

A Streamlit application that generates AI/GenAI use cases for companies using:
- LLaMA model for use case generation
- Tavily API for research
- Parallel processing for faster results
- Caching for improved performance

The system performs:
1. Company research
2. Market analysis
3. AI initiatives investigation
4. Use case generation
"""

import os
from dotenv import load_dotenv
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, List
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
import concurrent.futures

# Load environment variables
load_dotenv()

class FastAIGenerator:
    """Main class for AI use case generation system"""
    
    def __init__(self):
        """Initialize the system with API keys and LLaMA model"""
        # Load API keys from environment variables
        self.TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
        self.HUGGINGFACE_KEY = os.getenv('HUGGINGFACE_KEY')
        
        if not self.TAVILY_API_KEY or not self.HUGGINGFACE_KEY:
            raise ValueError("API keys not found. Please set TAVILY_API_KEY and HUGGINGFACE_KEY in .env file")
            
        # Initialize LLaMA model
        self.llm = self._init_llm()

    def _init_llm(self):
        """Initialize and configure optimized LLaMA model"""
        try:
            # Download quantized model
            model_path = hf_hub_download(
                repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                filename="llama-2-7b-chat.Q4_K_M.gguf",
                token=self.HUGGINGFACE_KEY
            )
            
            # Configure model with optimized parameters
            return LlamaCpp(
                model_path=model_path,
                temperature=0.7,      # Creativity vs consistency
                max_tokens=256,       # Reduced for speed
                n_ctx=512,           # Reduced context window
                n_batch=2048,        # Increased batch size
                n_threads=12,        # More threads
                f16_kv=True,         # Half precision
                use_mlock=True,      # Memory optimization
                use_mmap=True,       # Memory mapping
                verbose=False
            )
        except Exception as e:
            st.error(f"Model Error: {e}")
            return None

    def _make_search_request(self, query: str) -> Dict:
        """Make optimized API request to Tavily"""
        payload = {
            'api_key': self.TAVILY_API_KEY,
            'query': query,
            'search_depth': 'basic',  # Using basic for speed
            'max_results': 2          # Reduced results
        }
        
        try:
            response = requests.post(
                'https://api.tavily.com/search',
                json=payload,
                timeout=5             # Reduced timeout
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'summary': self._extract_summary(data.get('results', [])),
                    'details': self._extract_details(data.get('results', []))
                }
        except Exception as e:
            st.error(f"Search Error: {e}")
        return {'summary': '', 'details': []}

    def _extract_summary(self, results: List) -> str:
        """Extract and combine relevant information into summary"""
        return ' '.join(
            r.get('content', '').strip()[:200]
            for r in results[:2]
            if r.get('content')
        )

    def _extract_details(self, results: List) -> List[str]:
        """Extract detailed information points"""
        return [r.get('content', '') for r in results[:1] if r.get('content')]

@st.cache_data(ttl=3600)
def cached_research(_company_name: str, _api_key: str) -> Dict:
    """Perform cached research with parallel processing"""
    queries = {
        'company_info': f"{_company_name} company overview",
        'market_info': f"{_company_name} market position",
        'ai_info': f"{_company_name} AI initiatives"
    }
    
    results = {}
    for category, query in queries.items():
        payload = {
            'api_key': _api_key,
            'query': query,
            'search_depth': 'basic',
            'max_results': 2
        }
        
        try:
            response = requests.post(
                'https://api.tavily.com/search',
                json=payload,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                results[category] = {
                    'summary': ' '.join(r.get('content', '').strip()[:200] 
                                      for r in data.get('results', [])[:2]),
                    'details': [r.get('content', '') 
                              for r in data.get('results', [])[:1]]
                }
            else:
                results[category] = {'summary': '', 'details': []}
        except Exception as e:
            st.error(f"API Error for {category}: {e}")
            results[category] = {'summary': '', 'details': []}
    
    return results

@st.cache_data(ttl=3600)
def cached_use_cases(_research_data: Dict, _model_output: str) -> List[Dict]:
    """Generate and cache use cases"""
    try:
        cases = _model_output.split('Use Case #')[1:]
        return [
            {
                'id': i,
                'description': case.strip(),
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            for i, case in enumerate(cases, 1)
            if case.strip()
        ]
    except Exception as e:
        st.error(f"Parsing Error: {e}")
        return []

def main():
    """Main application function"""
    # Configure Streamlit page
    st.set_page_config(
        page_title="Fast AI Use Case Generator",
        page_icon="⚡",
        layout="wide"
    )
    
    # Initialize or get generator from session state
    if 'generator' not in st.session_state:
        st.session_state.generator = FastAIGenerator()
    
    st.title("⚡ Fast AI Use Case Generator")
    
    # User input
    company_name = st.text_input("Enter company name:")
    
    if st.button("Generate"):
        if company_name:
            with st.spinner("Processing..."):
                # Research phase
                research_data = cached_research(
                    company_name,
                    st.session_state.generator.TAVILY_API_KEY
                )
                
                # Display results in columns
                cols = st.columns(3)
                for col, (category, data) in zip(cols, research_data.items()):
                    with col:
                        st.subheader(category.replace('_', ' ').title())
                        st.write(data['summary'])
                
                # Generate use cases if model is available
                if st.session_state.generator.llm:
                    prompt = f"""Quick analysis for:
Company: {research_data['company_info']['summary'][:100]}
Generate 3 AI use cases. Format:
Use Case #[n]:
1. Problem: [brief]
2. Solution: [AI approach]
3. Impact: [brief]"""

                    model_output = st.session_state.generator.llm.invoke(prompt)
                    use_cases = cached_use_cases(research_data, model_output)
                    
                    # Display generated use cases
                    for case in use_cases:
                        with st.expander(f"Use Case {case['id']}"):
                            st.write(case['description'])
                    
                    # Prepare and offer report download
                    report = {
                        'company': company_name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'research': research_data,
                        'use_cases': use_cases
                    }
                    
                    st.download_button(
                        "📥 Download Report",
                        json.dumps(report, indent=2),
                        f"{company_name.lower()}_ai_report.json",
                        "application/json"
                    )
        else:
            st.warning("Please enter a company name")

if __name__ == "__main__":
    main()
