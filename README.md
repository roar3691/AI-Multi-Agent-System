```markdown
# AI/GenAI Use Case Generator

A sophisticated multi-agent system that automatically researches companies and generates AI/GenAI use cases using LLaMA model and Tavily API.

## Architecture
```mermaid
graph TD
    A[User Input] --> B[Research Agent]
    B --> C[Tavily API Research]
    C --> D[Data Processing]
    D --> E[LLaMA Model]
    E --> F[Use Case Generation]
    F --> G[JSON Report]
```

## Features

- **Automated Research**: Uses Tavily API to gather company information, market position, and AI initiatives
- **AI Use Case Generation**: Leverages LLaMA model for context-aware use case generation
- **Structured Output**: Generates detailed JSON reports with research findings and use cases
- **Error Handling**: Comprehensive error management and recovery
- **Optimized Performance**: Fast processing with parallel requests and efficient data handling

## Prerequisites

- Python 3.9+
- API Keys:
  - Tavily API key: `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`
  - HuggingFace API key: `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`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Multi-Agent-System.git
cd AI-Multi-Agent-System
```

2. Install dependencies:
```bash
pip install langchain-community huggingface_hub requests
```

## Usage

Run the system:
```bash
python ai_usecase_system1.py
```

Example interaction:
```
Enter company name (or 'quit' to exit): Tesla

Researching Tesla...
Generating AI use cases...

Report saved: reports/tesla_20241027_181232_ai_recommendations.json
```

## Output Format

The system generates structured JSON reports:
```json
{
    "company_name": "tesla",
    "analysis_date": "2024-10-27",
    "research_data": {
        "company_info": {
            "summary": "Tesla, Inc. designs, develops, manufactures...",
            "details": [...]
        },
        "market_info": {...},
        "ai_info": {...}
    },
    "ai_use_cases": [...]
}
```

## System Components

### Research Agent
- Company information gathering
- Market analysis
- AI initiatives research
- Parallel data processing

### LLaMA Integration
- Model initialization
- Context-aware prompting
- Use case generation
- Response parsing

### Report Generator
- JSON formatting
- File management
- Error handling
- Data validation

## Performance Optimizations

- Reduced token generation (max_tokens=1000)
- Optimized context window (n_ctx=2048)
- Parallel API requests
- Efficient data extraction
- Quick summary generation

## Error Handling

The system includes error handling for:
- API connection failures
- Model initialization issues
- Data processing errors
- File operations
- Invalid inputs

## Limitations

- Requires active internet connection
- API rate limits apply
- Processing time varies with input size
- Model loading requires sufficient memory

## Future Improvements

- Add more data sources
- Implement caching
- Add visualization tools
- Enhance error recovery
- Improve use case parsing

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Author

Y.Raghuvamshi Reddy

## Acknowledgments

- LangChain Community
- Tavily API
- HuggingFace
- LLaMA Model

```
