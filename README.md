# 🧠 Project Cortex

> **An anti-shame, AI-driven External Prefrontal Cortex for high-neuroticism productivity.**

## 🛑 The Problem: Perfectionist Freeze
Traditional task managers (like Notion, Todoist, or Google Calendar) are built for neurotypical "Executive Functioning." For users prone to overwhelm, ADHD paralysis, or perfectionism, these apps fail. They show the user the "Mountain" of tasks, triggering anxiety, procrastination, and a shame-spiral. Unfinished tasks turn red, overdue dates induce guilt, and the user eventually abandons the system entirely.

## 🌟 The Solution: The "Flashlight" Method
Project Cortex is not a to-do list; it is a **Behavioral Intervention Tool**. It acts as an external prefrontal cortex. It deliberately *hides* the overarching goals from the user. Instead of showing you the mountain, it asks for your current biological state (Energy/Stamina) and shines a "flashlight" on the next 1 to 3 immediate, frictionless steps you need to take right now. 

No overdue dates. No red text. No shame. Just the next step.

---

## ⚙️ Core Mechanics & Features

### 1. 🗣️ The AI Empathy Router
Users interact with the system via a natural language AI Partner (Powered by Gemini). The AI does not just blindly create tasks; it operates on a strict **3-Phase State Machine (Clarify → Confirm → Execute)** to prevent cognitive overload and AI hallucinations. It assesses the user's current Stamina and refuses to assign heavy coding tasks if the user is tired or it is past 11:00 PM.

### 2. 🏰 The Vault (Boss Monsters)
Massive, anxiety-inducing goals (e.g., "Build a full-stack Django app") are stored in the Vault. The user rarely looks at the Vault. These are the Boss Monsters.

### 3. 🗡️ Micro-Execution (The Goblins)
Vault Goals are broken down into incredibly small, frictionless tasks taking 20-45 minutes. Each task is assigned a `Threat Level` (10 to 50). The system will ONLY dispense a task if the Threat Level is less than or equal to the User's current Stamina. 

### 4. 🛡️ Biological Management
Cortex prioritizes human hardware. If the user mentions they are stuck in a "Sloth Loop" (rotting in bed), Cortex will assign a Threat Level 10 "Maintenance Task" (e.g., Drink water, stand up) to break the inertia before assigning real work.

---

## 🛠️ Tech Stack
*   **Backend:** Python, Django
*   **Database:** SQLite (Relational structure mapping Users -> Vaults -> Micro-tasks)
*   **AI Integration:** Google Gemini (Generative AI API)
*   **Frontend:** HTML, Tailwind CSS, Django Templates

---

## 🚀 Local Installation & Setup

Want to run your own External Prefrontal Cortex? Follow these steps:

**1. Clone the repository:**
```bash
git clone https://github.com/Omnisslayer01/Baadme-Sochenge.git
cd Baadme-Sochenge
```

**2. Create and activate a virtual environment:**
*   **Windows:** `python -m venv venv` and `venv\Scripts\activate`
*   **Mac/Linux:** `python3 -m venv venv` and `source venv/bin/activate`

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up your Environment Variables:**
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_api_key_here
```

**5. Build the Database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create a Superuser (Admin):**
```bash
python manage.py createsuperuser
```

**7. Run the Server:**
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000` in your browser to access the app!

---
*Built with ❤️ by two developers learning Django and behavioral psychology.*
