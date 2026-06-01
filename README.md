# AI-Powered Product Strategy Assistant

Multi-agent AI system that analyzes business documents and generates strategic product insights.

## 1. Source Code Repository

[https://github.com/Anuvarshini-dot/FDE_asses3_product_strategy_assistant](https://github.com/Anuvarshini-dot/FDE_asses3_product_strategy_assistant)

## 2. Live Application URL

[https://fde-asses3-product-strategy-assistant.onrender.com](https://fde-asses3-product-strategy-assistant.onrender.com)

## 3. Architecture Diagram

![Architecture Diagram](architecture.png)

> Add your architecture image file as `architecture.png` in the repo root, then commit it.

## 4. Sample Generated Report (PDF)

A sample AI-generated strategy report is available in the repository:

[Download Sample Report](samples/sample_report.pdf)

> To generate your own: upload a document, run the analysis, and click **Download PDF Report** in the app.

## 5. Project Documentation

Full project documentation is available here: [DOCUMENTATION.md](DOCUMENTATION.md)

---

## Architecture Overview

```
Documents → FastAPI Backend → LangGraph Pipeline → React Frontend
                                      |
              ┌───────────────────────┴────────────────────────┐
              ↓                       ↓                         ↓
  Customer Feedback Agent    Market & Competitor Agent   Feature Prioritization Agent
              ↓                                                  ↓
       SWOT Analysis Agent ←──────────────────────────────────┘
              ↓
    Executive Report Agent
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Backend | FastAPI + Uvicorn |
| AI Pipeline | LangGraph + LangChain |
| Vector Store | ChromaDB (in-memory) |
| PDF Export | ReportLab |
| Deployment | Render |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Anuvarshini-dot/FDE_asses3_product_strategy_assistant.git
cd FDE_asses3_product_strategy_assistant
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
npm install
npm run dev
```

Open http://localhost:5173

## Deployment (Render)

The project includes a `render.yaml` for Blueprint deployment, or deploy manually as a **Web Service**:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `cd frontend && npm install && npm run build && cd ../backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` |
| Start Command | `cd backend && .venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |

The React frontend is served as static files by FastAPI from `frontend/dist`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check |
| GET | /documents | List uploaded documents |
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

## Usage

1. Upload one or more documents (TXT, PDF, CSV, or JSON)
2. Select the documents to include using the checkboxes
3. Click **Run Analysis** to trigger the 5-agent pipeline
4. View results across the **Results**, **Chat**, and **Report** tabs
5. Download a formatted PDF report from the **Report** tab

## Notes

- Document storage is in-memory — re-upload files after a server restart
- Analysis runs 5 sequential AI agents and may take 30–60 seconds
