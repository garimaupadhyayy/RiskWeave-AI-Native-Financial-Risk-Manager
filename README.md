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

Most importantly, we directly answered the requirement for **false-positive cost metrics**: instead of a standard ML model that blindly blocks transactions over a 90% threshold, RiskWeave treats fraud as a **Financial Optimization Problem**. It actively calculates the margin lost to a "false-positive insult" (declining a legitimate user) versus the cost of a manual review, and uses mathematical calculus to pick the cheapest intervention.

---

## 💥 The Problem: The Hidden Cost of Binary Fraud Systems

Modern financial institutions are bleeding margin not just to fraud, but to their own defense systems. Traditional fraud pipelines rely on simple binary classification (Allow vs. Block). If a transaction looks risky, it is blocked. 

However, this leads to massive revenue loss due to **"false positive insults"**—insulting and permanently losing a legitimate customer because their transaction was falsely flagged. 

Furthermore, traditional ML models rely on static, historical IDs (Merchant ID, User ID) to learn. In the era of AI-enabled fraud, attackers instantly rotate synthetic identities and device fingerprints, rendering historical IDs useless and resulting in devastating zero-day attacks.

---

## 💡 The RiskWeave Solution: Autonomous Financial Optimization

RiskWeave completely bypasses static rules and binary thresholds. 

### 1. Zero-Day Generalization (10-D Attack DNA)
Instead of looking at *who* the user is, RiskWeave looks at *what* the user is doing. It translates raw transactions into a **10-Dimensional Behavioral DNA vector** (measuring Velocity Bursts, Entity Reuse, Graph Degree Proxies, and Refund Coupling). This allows it to instantly recognize the "shape" of an attack, even if the fraudster is using brand-new synthetic identities.

### 2. The Expected Cost Matrix
Once the XGBoost model outputs a probability of fraud, RiskWeave calculates the exact expected dollar-loss ($E[Cost]) for 5 possible interventions (ALLOW, MONITOR, STEP_UP, REVIEW, and HOLD). It factors in your business's profit margin, operational SMS/MFA costs, and cart-abandonment friction to select the action that mathematically minimizes the merchant's financial loss in real-time.

---

## 🏗️ Core Innovations & Architecture

### Innovation 1: MySQL-Native Graph Intelligence
To detect Abuse Rings, you normally need heavy, expensive graph databases like Neo4j. RiskWeave bypasses this entirely by utilizing highly-optimized WITH RECURSIVE Common Table Expressions (CTEs) natively inside MySQL 8.0. 
It maps the 2-hop entity radius (Customer -> Device/IP -> Peers) of an anomalous transaction in real-time, executing complex topology searches in under 50ms without the overhead of maintaining a separate Graph database.

### Innovation 2: Dual-Stage ML Pipeline (Isolation Forest + XGBoost)
Running heavy graph queries on every ₹10 coffee purchase would bankrupt Razorpay's servers. 
**Our solution:** We use a lightweight **Isolation Forest** (Anomaly Detection) as a first pass. If the Isolation Forest detects weird behavior, it *triggers* the heavy MySQL Graph Query. Finally, an **XGBoost** model consumes both the baseline behavior and the newly fetched graph topology to predict the exact probability of fraud.

### Innovation 3: Fail-Closed AI Investigator (Safety Gate)
LLMs hallucinate. If an AI goes crazy, it could block every transaction in India. 
In RiskWeave, we integrated **Google Gemini 2.5** strictly as an advisory assistant. Gemini translates complex XGBoost math and Graph Degree velocity into a plain-English narrative for the human dashboard. However, a deterministic **Policy Engine** makes the final ALLOW/BLOCK decision. This completely neutralizes Prompt Injection attacks and guarantees compliance.

---

## 🔬 How Detection & Optimization Works (The Math)

Every transaction is mapped to a 10-Dimensional Vector. The XGBoost model calculates the probability of fraud ($), and the Optimizer uses this to calculate Expected Cost.

### The Attack DNA
| Attack Vector | Metric | What it Detects |
| :--- | :--- | :--- |
| **Velocity Burst** | 	x_count_1h | Rapid succession of transactions from a single entity indicating a script/bot. |
| **Graph Degree** | device_account_count | A single device or IP logging into dozens of different accounts (Rotating Device Ring). |
| **Amount Escalation** | mt_vs_avg_30d | A compromised account suddenly making a purchase 10x larger than its historical average. |
| **Refund Coupling** | efund_ratio_7d | Money laundering attempts where transactions are rapidly followed by chargebacks/refunds. |
| **Entity Reuse** | card_fingerprint_velocity | Stolen credit card details being tested across multiple Razorpay merchant gateways. |

### The Financial Calculus (rgmin)
For every transaction, we calculate:
* CFN (Cost of False Negative): Transaction Amount + ₹1500 Chargeback Fee.
* CFP (Cost of False Positive): Lost lifetime revenue (customer churn).
* CInt (Intervention Cost): The cost of sending an SMS OTP, or paying a human analyst to review it.

The system uses rgmin(E[Cost]) to choose the absolute cheapest action for the merchant!

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Pydantic, Pandas
* **AI & Machine Learning:** XGBoost (Predictor), Scikit-Learn (Isolation Forest), Google Gemini API (LLM)
* **Frontend:** Next.js 14 (App Router), React, TypeScript, Tailwind CSS, Recharts
* **Database & Graph Engine:** TiDB Serverless Cloud (MySQL 8.0 with Recursive CTEs)
* **Cache & Velocity:** Render Redis (Key-Value Cache)
* **Deployment:** Vercel (Frontend), Render (Backend)

---

## 📂 Project Structure

`	ext
RiskWeave-AI-Native-Financial-Risk-Manager/
├── frontend/                 # Next.js 14 Analyst Dashboard
│   ├── src/app/
│   │   ├── page.tsx          # Main Dashboard UI, Live Feed, and Radar Logic
│   │   ├── globals.css       # Global styles and Tailwind imports
│   │   ├── icon.svg          # RiskWeave Logo
│   ├── tailwind.config.ts    # Dark Mode Theme Configuration
│   ├── package.json          # React Dependencies
│
├── backend/                  # FastAPI AI & Graph Engine
│   ├── app/
│   │   ├── main.py           # API Routes, Redis Cache, & Health Checks
│   │   ├── api/              # evaluate.py & graph.py routers
│   │   ├── services/         # Policy Engine, Gemini Investigator, Cost Optimizer
│   │   ├── db/session.py     # Secure TiDB Cloud Connection
│   ├── features/             # FeatureEngine (Pandas 10-D Attack DNA rolling windows)
│   ├── models/               # XGBoost Predictor & Isolation Forest Artifacts
│   ├── requirements.txt      # Python Dependencies
│
├── README.md                 # Project Documentation
`

---

## 💻 Running Locally (For Evaluators)

While the project is fully deployed to the cloud, evaluators can spin up the entire architecture on their local machine.

**1. Clone the repository:**
`ash
git clone https://github.com/garimaupadhyayy/RiskWeave-AI-Native-Financial-Risk-Manager.git
cd RiskWeave-AI-Native-Financial-Risk-Manager
`

**2. Start the FastAPI AI Engine:**
`ash
cd backend
python -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)
pip install -r requirements.txt
# Requires .env file with TiDB, Redis, and Gemini Keys
uvicorn app.main:app --reload --port 8000
`

**3. Start the Next.js Dashboard:**
`ash
cd ../frontend
npm install
npm run dev
`
Open http://localhost:3000. Click the **"Simulate Zero-Day Attack"** button at the top right to witness the entire RiskWeave pipeline execute, calculate the graph topography, optimize the financial decision, and stream the Gemini report in real-time!

---

<div align="center">
  <i>Engineered with precision for the Razorpay AI Buildathon 2026.</i><br/>
  <b>Garima & Indresh</b>
</div>
