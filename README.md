## 🏗️ Project Story

### 🚀 About the Project

We built **SmartProp AI** — a web-based real estate advisor that simplifies property investment and price estimation using the power of AI. 

The inspiration came from a simple question:  
*“What if anyone could get personalized real estate advice and price insights instantly, without needing an agent?”*

We wanted to empower users to make smarter investment decisions and estimate home prices with confidence — using just a few inputs.

The project has **two main features**:

---

### 🧠 Feature 1: AI Investment Planner

The first feature helps users understand how and where to invest based on their risk level, goals, and budget.

We designed a form with dropdowns and fields for:
- Investment style (e.g., all at once, monthly)
- Goal (growth, income, etc.)
- Budget, duration, and risk level

Once submitted, the backend uses **custom-built AI agents** to:
1. **Summarize the user’s profile**
2. **Generate two real estate investment strategies**
3. **Predict the ROI over 1, 3, and 5 years**

All of this is wrapped into a beautifully styled HTML report. We used GPT-4 to reason through the investment options, simulate returns, and format the output in a clean, readable way. The result? A report that feels like it came from a personal financial advisor — instantly.

This feature taught us how to:
- Orchestrate multiple AI agents in a logical flow
- Prompt GPT to produce clean HTML with no markdown
- Style dynamic AI content in a readable and engaging way

---

### 🏷️ Feature 2: AI Property Price Estimator

This part started out ambitious. We wanted to fetch live housing prices from Zillow or MLS. But here’s the catch — **no free, reliable API** was accessible for us within the hackathon time frame.

After hitting that wall hard, we decided to pivot.

Instead of live APIs, we:
- **Downloaded a real real-estate dataset** for a U.S. city
- It contained 20+ property features like price, location, square footage, bedrooms, etc.
- We **cleaned the data using pandas** and created a simplified, useful dataset

Now, when a user enters property details (like bedrooms, bathrooms, region, etc.), our **AI Price Estimator Agent** compares it against the cleaned dataset and estimates a fair market price. GPT acts as the analyst — reasoning over the data and giving back an **explanation + estimated value** in plain English.

💡 **This was our biggest challenge:**  
Going from "fetch real-time API data" to “simulate a live pricing experience” using pre-downloaded data — while keeping it useful and realistic.

---

### 🛠️ Tech Stack

- **FastAPI** (Backend)
- **Jinja2 Templates** (Dynamic HTML)
- **OpenAI GPT-4 Turbo** (AI Reasoning)
- **Bootstrap 5 + Custom CSS** (Frontend UI)
- **Pandas + CSV** (Local data processing)
