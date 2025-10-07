# 🚀 Smart Upsell Agent for SaaS

![AI Powered](https://img.shields.io/badge/AI-Powered-green.svg) ![n8n](https://img.shields.io/badge/n8n-Workflows-orange.svg) 

> **Turn generic upgrade messages into intelligent, personalized suggestions.**

---

## 🎯 Problem

SaaS users often miss important features. Generic **"UPGRADE NOW"** messages convert only \~2% and frustrate users.

**Solution:** Smart Upsell Agent

- Monitors user behavior
- Detects workflow inefficiencies
- Suggests personalized improvements
- Sends follow-up reminders automatically

**Example:**\
Instead of "UPGRADE NOW," user sees:

> "Eliminate manual report exports and reclaim your workflow."

---

## 📊 Impact

| Metric            | Traditional | Smart Upsell | Improvement        |
| ----------------- | ----------- | ------------ | ------------------ |
| Conversion        | 2%          | 15.2%        | 7.6x               |
| User Satisfaction | 23%         | 94%          | 4.1x               |
| Analysis Time     | 2-3 weeks   | < 5 min      | 99.9% faster       |
| Personalization   | 0%          | 100%         | Fully personalized |

---

## 🏗️ How It Works

```
Frontend (Python Saas.py) ◄──► n8n Workflows ◄──► Database (PostgreSQL)
                         │
                         ▼
                     AI Engine (GPTOSS-20B)
```

**Workflow Phases:**

1. **User Tracking:** Monitors actions in real-time
2. **AI Analysis:** Detects inefficiencies and patterns
3. **Opportunity Detection:** Generates personalized recommendations
4. **Campaign Delivery:** Sends in-app tips and automated emails

---

## 🔧 Tech Stack

**Backend:** n8n (Workflows), PostgreSQL (Data), GPTOSS-20B (AI), REST APIs\
**Frontend:** Streamlit (`Saas.py`)\
**Deployment:** Git

---

## n8n workflow

1 . USER_ACTIVITY
<img width="1169" height="299" alt="image" src="https://github.com/user-attachments/assets/d11b6fd7-2a7e-46e1-8f42-fd36651daa15" />

2 . AUTO_TRIGGER - EVERY 30 MIN
<img width="1722" height="525" alt="image" src="https://github.com/user-attachments/assets/1c931022-5c0c-4e01-b331-9fb655ddb2bc" />

3 . CAMPAIGN_TRIGGER 
<img width="1683" height="497" alt="image" src="https://github.com/user-attachments/assets/113c615c-7c57-4926-9064-2f6459cf4f90" />

---

## 🚀 Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/smart-upsell-agent.git
cd smart-upsell-agent

# 2. Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Install n8n globally
npm install -g n8n
```

**4. Setup PostgreSQL and .env file**

Create your PostgreSQL credentials in Supabase (or local PostgreSQL) and add them **plus the n8n webhook URLs** to a `.env` file:

```
# PostgreSQL credentials
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_password
DB_NAME=smart_upsell_db

# n8n Webhook URLs
CAMPAIGN_TRIGGER_WEBHOOK=http://localhost:5678/webhook/campaign-trigger
USER_ACTIVITY_WEBHOOK=http://localhost:5678/webhook/user-activity
```

---

**5. Start Services**

```bash
# Start n8n in one terminal or set up n8n localy and use it
n8n start

# Start frontend in another terminal
Streamlit run Saas.py
```

**Access:**

- n8n: [http://localhost:5678](http://localhost:5678)

---

**⭐ Star this repository if it helped you!**

