# 🚀 DodgeAI

AI‑Powered SAP Order‑to‑Cash Graph Intelligence Platform

DodgeAI is an AI‑driven graph intelligence system built on SAP Order‑to‑Cash datasets that allows users to query complex business flows using natural language.

Instead of manually tracing orders, deliveries, invoices, and payments — DodgeAI builds a graph‑based data engine and lets users ask:

- "Which products have the most billings?"
- "Trace billing flow for customer X"
- "Find broken O2C flows"
- "Show customer order lifecycle"

---

# ✨ Features

## 🧠 AI Query Engine
Natural language → Graph queries using LLM

## 📊 Graph Intelligence
Builds relationships between:
- Customers
- Orders
- Deliveries
- Invoices
- Payments

## 🔍 Flow Tracing
Customer → Order → Delivery → Invoice → Payment

## ⚡ FastAPI Backend
High‑performance API server

## 🌐 React Frontend
Interactive UI for graph queries

---

# 🏗️ Architecture

Frontend (React / Vercel)
        ↓
FastAPI Backend (Railway)
        ↓
Graph Engine (NetworkX)
        ↓
SAP O2C Dataset
        ↓
LLM (GROQ API)

---

# 📁 Project Structure

DodgeAI/
│
├── backend/
│   ├── api/
│   ├── graph_builder/
│   ├── graph_query/
│   ├── llm/
│   ├── data_loader/
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── package.json
│
└── data/
    └── sap-o2c-data/

---

# ⚙️ Backend Setup

## Install Dependencies

cd backend
pip install -r requirements.txt

---

## Run Backend

uvicorn api.main:app --reload

Backend runs at:

http://localhost:8000

Swagger Docs:

http://localhost:8000/docs

---

# 💻 Frontend Setup

cd frontend
npm install
npm run dev

Runs at:

http://localhost:5173

---

# 🔑 Environment Variables

Backend .env

GROQ_API_KEY=your_api_key

---

# 📊 Supported Queries

Products with most billings

Trace billing flow

Find broken flows

Customer info

---

# 🚀 Deployment

## Backend (Railway)

Root Directory: backend

Start Command:

uvicorn api.main:app --host 0.0.0.0 --port $PORT

---

## Frontend (Vercel)

Deploy frontend folder

Update API URL

---

# 🧠 Tech Stack

Backend:
- FastAPI
- NetworkX
- Python
- GROQ

Frontend:
- React
- Axios
- Vite

Deployment:
- Railway
- Vercel

---

# 👨‍💻 Author

PaRougv

https://github.com/PaRougv

---

# ⭐ Star the Repo

If you like this project, star the repository.
