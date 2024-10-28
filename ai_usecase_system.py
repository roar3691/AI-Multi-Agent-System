import os
import requests
import json
from datetime import datetime
from typing import Dict, List
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download

class AIResearchSystem:
    def __init__(self):
        self.TAVILY_API_KEY = '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'
        self.HUGGINGFACE_KEY = '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'
        self.reports_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI_MULTI AGENT_SYSTEM', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        try:
            model_path = hf_hub_download(
                repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                filename="llama-2-7b-chat.Q4_K_M.gguf",
                token=self.HUGGINGFACE_KEY
            )
            return LlamaCpp(
                model_path=model_path,
                temperature=0.7,
                max_tokens=1000,  # Reduced for faster generation
                n_ctx=2048,
                top_p=1,
                callbacks=[StreamingStdOutCallbackHandler()],
                verbose=True
            )
        except Exception as e:
            print(f"Model initialization error: {str(e)}")
            return None

    def research_company(self, company_name: str) -> Dict:
        """Fast company research using parallel requests"""
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
        """Optimized API request"""
        payload = {
            'api_key': self.TAVILY_API_KEY,
            'query': query,
            'search_depth': 'advanced',
            'max_results': 3  # Reduced for faster response
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
        """Quick summary extraction"""
        summaries = []
        for result in results:
            content = result.get('content', '').strip()
            if content:
                summaries.append(content)
        return ' '.join(summaries)[:500]  # Limited length for faster processing

    def _extract_details(self, results: List) -> List[str]:
        """Quick details extraction"""
        return [r.get('content', '') for r in results if r.get('content')][:3]

    def generate_use_cases(self, research_data: Dict) -> List[Dict]:
        """Fast use case generation"""
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
        """Quick use case parsing"""
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
        """Quick report saving"""
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
        
        # Print summary
        print("\nKey Findings:")
        print("\nCompany Overview:")
        print(research_data['company_info']['summary'][:200])
        print("\nGenerated Use Cases:")
        for case in use_cases:
            print(f"\nUse Case {case['id']}:")
            print(case['description'][:300])

if __name__ == "__main__":
    main()
