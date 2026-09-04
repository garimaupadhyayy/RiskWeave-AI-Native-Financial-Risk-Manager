<div align="center">
  <h1>🛡️ RiskWeave: Enterprise AI-Native Financial Risk Manager</h1>
  <p><strong>Razorpay AI Buildathon 2026 Submission (Track 02: AI Risk Manager)</strong></p>

  <img width="800" alt="RiskWeave Dashboard Simulation" src="https://github.com/user-attachments/assets/011f8206-4a32-4745-96f4-efe7375e57b1" />
  <br/><br/>
  <img width="800" alt="RiskWeave Dashboard Details" src="https://github.com/user-attachments/assets/34fe4bec-502d-4146-b0a8-2bd0e601666c" />
</div>

---

## 🚀 Live Deployment

| Component | URL |
| :--- | :--- |
| **Analyst Dashboard** | [https://riskweave.vercel.app](https://riskweave.vercel.app) |
| **Pitch Video** | [YouTube / Loom Link Here](#) |

---

## 🎯 Alignment with the Razorpay Track 02 Objective

The core prompt for Track 02 was to *"Stop the merchant losing money to fraud"* while providing *"honest metrics including false-positive cost"*. We designed RiskWeave explicitly to be the ultimate answer to this prompt. 

We didn't just build a simple "fraud detector." We built an **Abuse-Ring Sentinel** (using live Graph databases) and a **Fraud-Spike Detector** (using Redis velocity windows). 

Most importantly, we directly answered the requirement for **false-positive cost metrics**: instead of a standard ML model that blindly blocks transactions over a 90% threshold, RiskWeave treats fraud as a **Financial Optimization Problem**. It actively calculates the margin lost to a "false-positive insult" (declining a legitimate user) versus the cost of a manual review, and uses calculus to pick the cheapest intervention.

---

## 🧠 The Problem & Our Solution

### The Problem: The Hidden Cost of Binary Fraud Systems
Modern financial institutions are bleeding margin not just to fraud, but to their own defense systems. Traditional fraud pipelines rely on simple binary classification (Allow vs. Block). If a transaction looks risky, it is blocked. 
However, this leads to massive revenue loss due to **"false positive insults"**—insulting and permanently losing a legitimate customer because their transaction was falsely flagged. Furthermore, traditional ML models rely on static, historical IDs (Merchant ID, User ID) to learn. In the era of AI-enabled fraud, attackers instantly rotate synthetic identities and device fingerprints, rendering historical IDs useless and resulting in devastating zero-day attacks.

### The RiskWeave Solution: Autonomous Financial Optimization
RiskWeave completely bypasses static rules and binary thresholds. 

1. **Zero-Day Generalization:** Instead of looking at *who* the user is, RiskWeave looks at *what* the user is doing. It translates raw transactions into a **10-Dimensional Behavioral DNA vector** (measuring Velocity Bursts, Entity Reuse, Graph Degree Proxies, and Refund Coupling). This allows it to instantly recognize the "shape" of an attack, even if the fraudster is using brand-new synthetic identities.
2. **The Expected Cost Matrix:** Once the XGBoost model outputs a probability of fraud, RiskWeave calculates the exact expected dollar-loss (`$E[Cost]`) for 5 possible interventions (`ALLOW`, `MONITOR`, `STEP_UP`, `REVIEW`, and `HOLD`). It factors in your business's profit margin, operational SMS/MFA costs, and cart-abandonment friction to select the action that mathematically minimizes the merchant's financial loss in real-time.

---

## ⚡ What It Does (Core Features)

* **Live Transaction Feed & Radar:** Streams incoming transactions and instantly visually maps their 10-D Attack DNA onto a live radar chart using Recharts, allowing human analysts to instantly see the visual "shape" of an attack (e.g., a massive spike in Velocity Burst and Graph Degree).
* **MySQL-Native Graph Intelligence:** To detect Abuse Rings, you normally need heavy, expensive graph databases like Neo4j. RiskWeave bypasses this entirely by utilizing highly-optimized `WITH RECURSIVE` Common Table Expressions (CTEs) natively inside MySQL 8.0. It maps the 2-hop entity radius (Customer -> Device/IP -> Peers) of an anomalous transaction in real-time, executing complex topology searches in under 50ms.
* **Financial Cost Optimizer:** Automatically calculates the mathematical Expected Loss for all possible actions. For example, it automatically chooses `STEP_UP` (MFA) over `HOLD` for medium-risk, high-value transactions to preserve conversion rates, because the $118.75 insult cost of a false positive outweighs a $5.00 manual review fee.
* **GenAI Advisory Investigator:** Integrates Google Gemini 2.5 to translate complex XGBoost math and Graph Degree velocity into a plain-English narrative. Gemini acts strictly as a "Fail-Closed" advisor, generating a human-readable markdown report for the risk analyst dashboard explaining *exactly why* the XGBoost model flagged the transaction.
* **Data Leakage Immunity:** Engineered with a foolproof temporal rolling window architecture to ensure that future ground-truth labels are never accidentally leaked into the training features.

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
├── frontend/                 Next.js 14 Analyst Dashboard
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

While the project is fully deployed to the cloud, evaluators can spin up the entire architecture on their local machine to test the raw Graph Database capabilities.

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






