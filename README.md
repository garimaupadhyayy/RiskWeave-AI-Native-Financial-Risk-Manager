<div align="center">
  <img src="frontend/public/icon.svg" alt="RiskWeave Logo" width="100"/>
  <h1>RiskWeave: AI-Native Financial Risk Manager</h1>
  <p><strong>Razorpay AI Buildathon 2026 Submission</strong></p>

  <img width="800" alt="RiskWeave Dashboard" src="https://github.com/user-attachments/assets/5f970473-ccfe-434d-bbca-2cbcd4296344" />

  <p>
    <a href="#key-innovations">Innovations</a> •
    <a href="#project-structure">Project Structure</a> •
    <a href="#how-to-run-locally">How to Run Locally</a> •
    <a href="#system-health--testing">Testing</a>
  </p>
</div>

---

## 📖 Overview
**RiskWeave** is an autonomous, AI-native financial risk manager. Traditional fraud systems rely on binary classification (blocking or allowing transactions), which results in massive revenue loss due to "false positive insults" (declining a legitimate customer). 

RiskWeave completely reimagines this process by combining a **MySQL Graph Engine**, **XGBoost**, and **Financial Mathematics**. It calculates the "10-D Attack DNA" of a transaction, evaluates the Expected Financial Loss ($E[Loss]), and uses **Google Gemini GenAI** to write human-readable investigation reports in real-time.

---

## ⚡ Key Innovations

1. **MySQL-Native Graph Intelligence:** Instead of requiring a heavy secondary database like Neo4j, RiskWeave uses highly-optimized WITH RECURSIVE CTEs in MySQL 8.0 to traverse 2-hop entity relationships (Shared Devices, IPs, Cards) within strict 48-hour windows in milliseconds.
2. **Financial Cost Optimizer:** RiskWeave doesn't just ask "Is this fraud?". It calculates the exact dollar-value cost of an intervention (e.g., a $5.00 manual review fee vs. a $118.75 false-positive insult cost) and mathematically chooses the most profitable action.
3. **Data Leakage Immunity:** Engineered with a foolproof temporal rolling window architecture to ensure that future ground-truth data is never accidentally leaked into the training features.
4. **GenAI Advisory Investigator:** Integrates Google Gemini to translate complex XGBoost math and Graph Degree velocity into a plain-English narrative for human analysts.

---

## 📂 Project Structure

\\\	ext
RiskWeave-AI-Native-Financial-Risk-Manager/
├── frontend/                 # Next.js 14 Analyst Dashboard
│   ├── src/app/
│   │   ├── page.tsx          # Main Dashboard UI & Logic
│   │   └── icon.svg          # RiskWeave Logo
│   ├── tailwind.config.ts    # Dark Mode Theme Configuration
│   └── package.json          # React Dependencies
│
├── backend/                  # FastAPI AI & Graph Engine
│   ├── app/
│   │   ├── main.py           # API Routes
│   │   ├── agent.py          # Gemini AI Integration
│   │   ├── db/database.py    # MySQL Graph Connection
│   │   └── models/           # XGBoost Predictor Models
│   ├── scripts/              # Training & DB Initialization
│   └── requirements.txt      # Python Dependencies
│
├── docker-compose.yml        # Orchestrates MySQL and Redis
└── README.md                 # Project Documentation
\\\

---

## 💻 How to Run Locally

Because this project is designed for enterprise-grade security and speed, it is orchestrated to run completely on your local machine using Docker for the databases.

### Step 1: Environment Variables
Create a .env file in the root directory (where docker-compose.yml is) and add the following:
\\\env
# Project Settings
PROJECT_NAME="RiskWeave"

# MySQL Settings
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=riskweave
MYSQL_USER=riskuser
MYSQL_PASSWORD=riskpassword
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Redis Settings
REDIS_HOST=localhost
REDIS_PORT=6379

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
\\\

### Step 2: Start the Databases (Docker)
Open a terminal in the project root and start the MySQL and Redis containers in the background:
\\\ash
docker-compose up -d mysql redis
\\\

### Step 3: Start the FastAPI Backend
Open a **new terminal**, navigate to the backend folder, and start the Python server:
\\\ash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
\\\
*(The backend is now running at http://localhost:8000)*

### Step 4: Start the Next.js Frontend
Open another **new terminal**, navigate to the frontend folder, and start the UI:
\\\ash
cd frontend
npm install
npm run dev
\\\
*(The dashboard is now running at http://localhost:3000)*

---

## 🩺 System Health & Testing

To verify the system is running correctly, you can check the following health endpoints:

1. **Backend Health Check:**
   Open your browser and go to: http://localhost:8000/health
   *Expected Output: {"status": "ok", "mysql": "connected", "redis": "connected"}*

2. **Interactive API Documentation:**
   Go to: http://localhost:8000/docs
   *This opens the Swagger UI where you can manually test the AI risk evaluation endpoints.*

---
<div align="center">
  <i>Built with precision for the Razorpay AI Buildathon 2026.</i>
</div>
