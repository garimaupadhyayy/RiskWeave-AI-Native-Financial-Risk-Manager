<div align="center">
  
  <h1>RiskWeave: AI-Native Financial Risk Manager</h1>
  <p><strong>Razorpay AI Buildathon 2026 Submission</strong></p>

  <img width="1917" height="905" alt="Screenshot 2026-09-04 022014" src="https://github.com/user-attachments/assets/5f970473-ccfe-434d-bbca-2cbcd4296344" />

  <p>
    <a href="#live-demo">Live Demo</a> •
    <a href="#key-innovations">Innovations</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started-local-development">How to Run Locally</a> •
    <a href="#system-health--testing">Testing</a>
  </p>
</div>

---

## 🚀 Live Demo & Links
*(Note to judges: Use these links to test the deployed application)*
* **Frontend Dashboard:** [https://your-vercel-link-here.vercel.app](#) *(Replace this link)*
* **Backend API (Swagger Docs):** [https://your-render-link-here.onrender.com/docs](#) *(Replace this link)*
* **5-Minute Pitch Video:** [YouTube / Loom Link Here](#) *(Replace this link)*

---

## 📖 Overview
**RiskWeave** is an autonomous, AI-native financial risk manager. Traditional fraud systems rely on binary classification (blocking or allowing transactions), which results in massive revenue loss due to "false positive insults" (declining a legitimate customer). 

RiskWeave completely reimagines this process by combining a **MySQL Graph Engine**, **XGBoost**, and **Financial Mathematics**. It calculates the "10-D Attack DNA" of a transaction, evaluates the Expected Financial Loss ($E[Loss]), and uses **Google Gemini GenAI** to write human-readable investigation reports in real-time.

---

## 📸 Dashboard Screenshots

*(Add your screenshots here! Replace the links with your actual image paths)*

| **Live Transaction Feed & Radar** | **Gemini AI Investigation & Optimizer** |
| :---: | :---: |
| <img src="screenshot_1_placeholder.png" width="400" alt="Dashboard View 1"/> | <img src="screenshot_2_placeholder.png" width="400" alt="Dashboard View 2"/> |
| *10-D Attack Radar identifying a Rotating-Device Ring* | *Gemini GenAI generating an automated investigation report* |

---

## ⚡ Key Innovations

1. **MySQL-Native Graph Intelligence:** Instead of requiring a heavy secondary database like Neo4j, RiskWeave uses highly-optimized WITH RECURSIVE CTEs in MySQL 8.0 to traverse 2-hop entity relationships (Shared Devices, IPs, Cards) within strict 48-hour windows in milliseconds.
2. **Financial Cost Optimizer:** RiskWeave doesn't just ask "Is this fraud?". It calculates the exact dollar-value cost of an intervention (e.g., a $5.00 manual review fee vs. a $118.75 false-positive insult cost) and mathematically chooses the most profitable action.
3. **Data Leakage Immunity:** Engineered with a foolproof temporal rolling window architecture to ensure that future ground-truth data is never accidentally leaked into the training features.
4. **GenAI Advisory Investigator:** Integrates Google Gemini to translate complex XGBoost math and Graph Degree velocity into a plain-English narrative for human analysts.

---

## 🛠 Tech Stack
* **Frontend:** Next.js 14 (App Router), React, Tailwind CSS, Recharts
* **Backend:** Python, FastAPI, Pydantic, Scikit-Learn (XGBoost)
* **Databases:** MySQL 8.0 (Graph Engine), Redis (Velocity Cache)
* **AI & Machine Learning:** Google Gemini API (LLM), XGBoost (Predictor)
* **Infrastructure:** Docker, Docker Compose

---

## 💻 Getting Started (Local Development)

To run this project on your local machine, follow these steps exactly.

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
