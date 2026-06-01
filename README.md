# AI-Powered Product Strategy Assistant

Multi-agent AI system that analyzes business documents and generates strategic product insights.

## Architecture

```
Documents → FastAPI Backend → LangGraph Pipeline → Streamlit Frontend
                                      |
              ┌───────────────────────┴────────────────────────┐
              ↓                       ↓                         ↓
  Customer Feedback Agent    Market & Competitor Agent   Feature Prioritization Agent
              ↓                                                  ↓
       SWOT Analysis Agent ←──────────────────────────────────┘
              ↓
    Executive Report Agent
```

## Setup

### 1. Environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend (new terminal)

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload | Upload documents (TXT, PDF, CSV, JSON) |
| POST | /analyze | Run 5-agent analysis pipeline |
| GET | /results | Get analysis results |
| POST | /chat | Chat with your data |
| GET | /report/pdf | Download PDF report |
| DELETE | /reset | Clear all data |

## Agents

| Agent | Responsibility |
|-------|---------------|
| Customer Feedback Agent | Pain points, satisfaction drivers, feature requests |
| Market & Competitor Agent | Market trends, competitive landscape, positioning |
| Feature Prioritization Agent | RICE scoring, roadmap, Must/Should/Nice-to-Have |
| SWOT Analysis Agent | Strengths, Weaknesses, Opportunities, Threats |
| Executive Report Agent | C-suite summary, strategic priorities, 30/60/90 day plan |

## Sample Data

A sample `Sample Sales Data.csv` is included. Upload it to test the system.
