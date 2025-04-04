
# 🧠 Policy Insight Explorer

A full-stack AI reasoning tool for analyzing public policy processes using structured data, GPT reasoning, Supabase logging, and a professional no-code frontend.

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI (Python) |
| LLM Reasoning | OpenAI GPT-4 |
| Frontend UI | Lovable.dev |
| Logs / DB | Supabase |
| Deployment | Render (FastAPI) + Lovable (cloud editor) |

---

## 🚀 Features

- ✅ GPT-powered reasoning with 5 structured policy query types
- ✅ Uploadable CSV (real + synthetic hybrid) dataset
- ✅ Freeform question interface with GPT answers
- ✅ Supabase logging of all GPT reasoning responses
- ✅ Swagger docs with `/reasoning-query`, `/free-question`, and `/test-batch-reasoning` endpoints
- ✅ Secure `.env` with OpenAI & Supabase keys
- ✅ Designed for policy teams, lawyers, and data analysts

---

## 📁 Project Structure

```
policy-insight-explorer/
├── main.py                   # FastAPI app with all endpoints
├── reasoning.py              # GPT prompt logic
├── supabase_logger.py        # Logs to Supabase
├── load_data.py              # CSV loading for test-batch
├── requirements.txt          # Python dependencies
├── .env.template             # Env vars to copy for deployment
├── Policy_Analysis_Cases.csv
├── Policy_Analysis_Events.csv
```

---

## 📦 Installation (Local)

1. Clone this repo or unzip folder
2. Copy `.env.template` to `.env` and add your OpenAI/Supabase keys
3. Run:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

4. Visit `http://127.0.0.1:8000/docs`

---

## 🌐 Live Deployment

- API (Render): [`https://policy-reasoning-api.onrender.com`](https://policy-reasoning-api.onrender.com)
- Lovable Frontend: _Insert your Lovable.dev project URL here_

---

## 📝 API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/reasoning-query` | POST structured reasoning request |
| `/free-question`   | POST natural language question |
| `/test-batch-reasoning` | GET test run over CSV |

---

## 🗃️ Supabase Logging

All responses from GPT are logged with:
- `case_name`
- `process`, `kg`, `causal`
- `created_at`

Can be used for:
- Auditing / Review
- Trend detection
- Export to dashboards

---

## 🧪 Dataset

- Hybrid of synthetic + real-style event logs
- 2 CSVs: one for cases, one for events
- Columns: `case_id`, `event_id`, `timestamp`, `actor`, `review_outcome`, `comments`

---

## 🧠 Prompt Templates

Located in `reasoning.py`, for:
- Policy Analysis
- Clause Rejections
- Department Delays
- Multi-Department Impact
- AI Regulation Bottlenecks
- Freeform Question

---

## 🧪 Testing

Run Swagger UI locally:
```bash
uvicorn main:app --reload
# then visit http://localhost:8000/docs
```

Test via `/test-batch-reasoning` to simulate a full CSV run.

---

## 📄 License

MIT. Built for educational and policy research use.

---

*Generated on 2025-04-04*

