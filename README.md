# RiskWeave 🛡️
**Enterprise AI-Native Financial Risk Manager**

A paradigm-shifting autonomous risk platform that reimagines fraud detection as a **financial optimization problem**. RiskWeave ingests transactions, calculates a 10-Dimensional Behavioral DNA vector, traverses live graph topologies in MySQL to detect entity-rings, and uses Google Gemini to mathematically minimize Expected Loss while generating real-time Analyst investigation reports.

<div align="center">
  <img width="800" alt="RiskWeave Dashboard" src="https://github.com/user-attachments/assets/5f970473-ccfe-434d-bbca-2cbcd4296344" />
</div>

---

## 🚀 Live Deployment

| Component | URL |
| :--- | :--- |
| **Analyst Dashboard** | [https://your-vercel-link-here.vercel.app](#) |
| **API Docs (Swagger UI)** | [https://your-render-link-here.onrender.com/docs](#) |
| **Pitch Video** | [YouTube / Loom Link Here](#) |

---

## 🧠 The Problem & Our Solution

**The Problem:** Traditional fraud systems rely on simple binary classification (blocking or allowing transactions). This leads to massive revenue loss due to **"false positive insults"**—declining a legitimate customer. Furthermore, traditional ML relies on historical static IDs (Merchant ID, User ID) which fail instantly when fraudsters rotate devices or use synthetic identities in zero-day attacks.

**The RiskWeave Solution:** 
RiskWeave completely bypasses static rules. It translates raw transactions into a **10-Dimensional Behavioral DNA vector** (Velocity Burst, Entity Reuse, Graph Degree Proxy, Refund Coupling, etc.). It then calculates the exact `$E[Cost]` for 5 possible interventions (`ALLOW`, `MONITOR`, `STEP_UP`, `REVIEW`, and `HOLD`). It factors in margin loss, operational SMS costs, and cart-abandonment friction to select the action that mathematically minimizes Razorpay's financial loss, all in under 50ms.

---

## ⚡ What It Does

* **Live Transaction Feed & Radar:** Streams incoming transactions and instantly visually maps their 10-D Attack DNA onto a live radar chart using Recharts, allowing analysts to instantly see the "shape" of an attack (e.g., a massive spike in Velocity Burst and Graph Degree).
* **MySQL-Native Graph Intelligence:** Bypasses the heavy infrastructure requirement of Neo4j. By utilizing highly-optimized `WITH RECURSIVE` Common Table Expressions (CTEs) in MySQL 8.0, RiskWeave maps the 2-hop entity radius (Customer -> Device/IP -> Peers) of an anomalous transaction in real-time.
* **Financial Cost Optimizer:** Automatically calculates the mathematical Expected Loss for all possible actions. For example, it automatically chooses `STEP_UP` (MFA) over `HOLD` for medium-risk, high-value transactions to preserve conversion rates, because the $118.75 insult cost of a false positive outweighs a $5.00 manual review fee.
* **GenAI Advisory Investigator:** Integrates Google Gemini 2.5 to translate complex XGBoost math and Graph Degree velocity into a plain-English narrative. Gemini acts strictly as a "Fail-Closed" advisor, generating a human-readable markdown report for the risk analyst dashboard explaining *why* the transaction is dangerous.
* **Data Leakage Immunity:** Engineered with a foolproof temporal rolling window architecture to ensure that future ground-truth data is never accidentally leaked into the training features.

---

## 🛠 Tech Stack

* **Backend:** Python, FastAPI, Pydantic, SQLAlchemy
* **AI & Machine Learning:** XGBoost (Predictor), Google Gemini API (LLM Agent)
* **Frontend:** Next.js 14 (App Router), React, TypeScript, Tailwind CSS, Recharts
* **Database & Graph Engine:** MySQL 8.0 (Relational + Graph CTEs)
* **Cache & Velocity:** Redis
* **Deployment:** Vercel (Frontend), Render (Backend)

---

## 📂 Project Structure

```text
RiskWeave-AI-Native-Financial-Risk-Manager/
├── frontend/                 FastAPI application
│   ├── src/app/
│   │   ├── page.tsx          Main Dashboard UI, Live Feed, and Radar Logic
│   │   ├── globals.css       Global styles and Tailwind imports
│   │   └── icon.svg          RiskWeave Logo
│   ├── tailwind.config.ts    Dark Mode Theme Configuration
│   └── package.json          React Dependencies
│
├── backend/                  FastAPI AI & Graph Engine
│   ├── app/
│   │   ├── main.py           API Routes & Cost Optimizer Logic
│   │   ├── agent.py          Gemini AI Integration & Prompt Engineering
│   │   ├── db/database.py    MySQL Graph Connection & CTE Queries
│   │   └── models/           XGBoost Predictor Models
│   └── requirements.txt      Python Dependencies
│
├── docker-compose.yml        Orchestrates MySQL and Redis for local dev
└── README.md                 Project Documentation
```

---

## 💻 Running Locally (For Evaluators)

While the project is fully deployed to the cloud, you can easily spin up the entire architecture on your local machine to test the raw Graph Database capabilities.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.

**1. Clone and start the databases:**
```bash
git clone https://github.com/garimaupadhyayy/RiskWeave-AI-Native-Financial-Risk-Manager.git
cd RiskWeave-AI-Native-Financial-Risk-Manager
docker-compose up -d mysql redis
```

**2. Start the FastAPI AI Engine:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**3. Start the Next.js Dashboard:**
```bash
cd ../frontend
npm install
npm run dev
```
Open `http://localhost:3000`. Click the **"Simulate Zero-Day Attack"** button at the top right to witness the entire RiskWeave pipeline execute, calculate the graph topography, optimize the financial decision, and stream the Gemini report in real-time!

---

## 🧬 How Detection & Optimization Works

Every transaction is mapped to a 10-Dimensional Vector. The XGBoost model calculates the probability of fraud ($P$), and the Optimizer uses this to calculate Expected Cost.

| Attack Vector | Metric | What it Detects |
| :--- | :--- | :--- |
| **Velocity Burst** | `tx_count_1h` | Rapid succession of transactions from a single entity indicating a script/bot. |
| **Graph Degree** | `device_account_count` | A single device or IP logging into dozens of different accounts (Rotating Device Ring). |
| **Amount Escalation** | `amt_vs_avg_30d` | A compromised account suddenly making a purchase 10x larger than its historical average. |
| **Refund Coupling** | `refund_ratio_7d` | Money laundering attempts where transactions are rapidly followed by chargebacks/refunds. |
| **Entity Reuse** | `card_fingerprint_velocity` | Stolen credit card details being tested across multiple Razorpay merchant gateways. |

<div align="center">
  <i>Built with precision for the Razorpay AI Buildathon 2026.</i>
</div>
