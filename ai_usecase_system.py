"""
AI/GenAI Use Case Generator
Author: Y RAGHUVAMSHI REDDY
Description: A multi-agent system that researches companies and generates AI/GenAI use cases 
using LLaMA model and Tavily API.

Features:
- Company research using Tavily API
- AI use case generation using LLaMA
- Structured JSON reports
- Error handling and recovery
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

    def _initialize_llm(self):
        """Initialize and configure LLaMA model"""
        try:
            model_path = hf_hub_download(
                repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                filename="llama-2-7b-chat.Q4_K_M.gguf",
                token=self.HUGGINGFACE_KEY
            )
            return LlamaCpp(
                model_path=model_path,
                temperature=0.7,
                max_tokens=1000,
                n_ctx=2048,
                top_p=1,
                callbacks=[StreamingStdOutCallbackHandler()],
                verbose=True
            )
        except Exception as e:
            print(f"Model initialization error: {str(e)}")
            return None

    def research_company(self, company_name: str) -> Dict:
        """Research company using parallel requests"""
        queries = {
            'company_info': f"{company_name} company overview business model products",
            'market_info': f"{company_name} market position industry trends competitors",
            'ai_info': f"{company_name} artificial intelligence machine learning initiatives"
        }
        
        results = {}
        for category, query in queries.items():
            results[category] = self._make_search_request(query)
        
        return results

    def _make_search_request(self, query: str) -> Dict:
        """Make API request to Tavily"""
        payload = {
            'api_key': self.TAVILY_API_KEY,
            'query': query,
            'search_depth': 'advanced',
            'max_results': 3
        }
        
        try:
            response = requests.post('https://api.tavily.com/search', json=payload)
            if response.status_code == 200:
                data = response.json()
                return {
                    'summary': self._extract_summary(data.get('results', [])),
                    'details': self._extract_details(data.get('results', []))
                }
        except Exception as e:
            print(f"Search error: {str(e)}")
        return {'summary': '', 'details': []}

    def _extract_summary(self, results: List) -> str:
        """Extract and combine relevant information into summary"""
        summaries = []
        for result in results:
            content = result.get('content', '').strip()
            if content:
                summaries.append(content)
        return ' '.join(summaries)[:500]

    def _extract_details(self, results: List) -> List[str]:
        """Extract detailed information points"""
        return [r.get('content', '') for r in results if r.get('content')][:3]

    def generate_use_cases(self, research_data: Dict) -> List[Dict]:
        """Generate AI use cases based on research data"""
        if not self.llm:
            return []

        prompt = f"""Based on this research, generate 5 practical AI/GenAI use cases for {research_data['company_info']['summary'][:200]}

Focus areas:
- Operational Efficiency
- Customer Experience
- Product Innovation
- Process Automation
- Data Analytics

Format each as:
Use Case #[number]:
1. Problem: [challenge]
2. Solution: [AI/ML approach]
3. Complexity: [Low/Medium/High]
4. Impact: [benefits]
5. Resources: [requirements]"""

        try:
            response = self.llm.invoke(prompt)
            return self._parse_use_cases(response)
        except Exception as e:
            print(f"Generation error: {str(e)}")
            return []

    def _parse_use_cases(self, response: str) -> List[Dict]:
        """Parse and structure generated use cases"""
        use_cases = []
        try:
            cases = response.split('Use Case #')[1:]
            for i, case in enumerate(cases, 1):
                if case.strip():
                    lines = case.strip().split('\n')
                    use_cases.append({
                        'id': i,
                        'description': case.strip(),
                        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
        except Exception as e:
            print(f"Parsing error: {str(e)}")
        return use_cases

    def save_report(self, company_name: str, research_data: Dict, use_cases: List[Dict]) -> str:
        """Save generated report to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report = {
            'company_name': company_name,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'research_data': research_data,
            'ai_use_cases': use_cases
        }
        
        filename = f"{company_name.lower().replace(' ', '_')}_{timestamp}_ai_recommendations.json"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        
        return filepath

def main():
    """Main execution function"""
    try:
        system = AIResearchSystem()
        
        while True:
            company = input("\nEnter company name (or 'quit' to exit): ").strip()
            if company.lower() == 'quit':
                break
            
            print(f"\nResearching {company}...")
            research_data = system.research_company(company)
            
            print("\nGenerating AI use cases...")
            use_cases = system.generate_use_cases(research_data)
            
            report_path = system.save_report(company, research_data, use_cases)
            print(f"\nReport saved: {report_path}")
            
            print("\nKey Findings:")
            print("\nCompany Overview:")
            print(research_data['company_info']['summary'][:200])
            print("\nGenerated Use Cases:")
            for case in use_cases:
                print(f"\nUse Case {case['id']}:")
                print(case['description'][:300])
                
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please ensure API keys are set in .env file")

if __name__ == "__main__":
    main()
