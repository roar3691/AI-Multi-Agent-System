# AI Multi-Agent System for Use Case Generation

A sophisticated multi-agent system that leverages AI to research companies and generate relevant AI/GenAI use cases using LLaMA and Tavily API.

## Architecture

```mermaid
graph TD
    A[User Input] --> B[Research Agent]
    B --> C[Tavily API]
    C --> D[Data Processing]
    D --> E[LLaMA Model]
    E --> F[Use Case Generation]
    F --> G[Report Generation]
