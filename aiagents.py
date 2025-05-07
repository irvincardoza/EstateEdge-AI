from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------- AI Agent Logic ----------------------
def ProfileAgent(budget, investment_style, goal, risk, duration):
    return f"The user has ${budget} to invest, prefers '{investment_style}' investing, has a '{risk}' risk tolerance, and seeks '{goal}' over a '{duration}' period."

def StrategyAgent(profile_summary):
    prompt = f"""
    Based on the following investor profile, suggest the top 2 real estate investment strategies.

    Return the response using only valid HTML tags — include:
    - <h3> for strategy titles
    - <ul><li> for pros and cons
    - <p> for paragraphs
    - No Markdown formatting
    - Be concise and readable

    Profile:
    {profile_summary}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI StrategyAgent error:", e)
        return "⚠️ Failed to fetch strategy from AI."


def ROIAgent(strategy_summary):
    prompt = f"""
    Given the following investment strategy summary, simulate ROI over 1, 3, and 5 years for two property types.

    Return the result using only valid HTML:
    - Format as bullet points using <ul><li> for each data point
    - Each bullet should follow this format:
      📌 [Investment Type] ([Duration]): ROI ~X–Y%, Risk: Low/Medium/High
    - Add one <p> explanation before or after the bullet list
    - DO NOT use tables or Markdown formatting

    Strategy:
    {strategy_summary}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI ROIAgent error:", e)
        return "⚠️ Failed to fetch ROI from AI."


# ---------------------- ROUTES ----------------------
# ---------------------- ROUTES ----------------------
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/investment_form", response_class=HTMLResponse)
async def get_investment_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/smart_matcher", response_class=HTMLResponse)
async def get_smart_matcher(request: Request):
    return templates.TemplateResponse("smart.html", {"request": request})

@app.post("/generate_report", response_class=HTMLResponse)
async def generate_report(
    request: Request,
    budget: float = Form(...),
    investment_style: str = Form(...),
    goal: str = Form(...),
    risk: str = Form(...),
    duration: str = Form(...),
    online_only: str = Form(...)
):
    profile = ProfileAgent(budget, investment_style, goal, risk, duration)
    strategy = StrategyAgent(profile)
    roi = ROIAgent(strategy)

    return templates.TemplateResponse("report_template.html", {
        "request": request,
        "profile": profile,
        "strategy": strategy,
        "roi": roi
    })

@app.get("/preview_report", response_class=HTMLResponse)
async def preview_report(request: Request):
    profile = "The user has $100000.0 to invest, prefers 'All at once' investing, has a 'Medium' risk tolerance, and seeks 'Passive income' over a '3+ years' period."

    strategy = """
    <h3>Rental Properties</h3>
    <p>Investing in rental properties can provide a stable source of passive income through monthly tenant payments.</p>
    <ul>
        <li><strong>Pros:</strong> Steady monthly income, property appreciation, tax deductions.</li>
        <li><strong>Cons:</strong> Requires active management, maintenance, vacancies.</li>
    </ul>
    <h3>REITs</h3>
    <p>REITs allow you to invest in real estate without direct property ownership.</p>
    <ul>
        <li><strong>Pros:</strong> High liquidity, diversification, dividends.</li>
        <li><strong>Cons:</strong> Volatility, limited control, tax inefficiencies.</li>
    </ul>
    """

    roi = """
    <p>Here’s the simulated ROI based on investment type and duration:</p>
    <ul>
        <li>📌 Rental Properties (1 Year): ROI ~5–10%, Risk: Medium</li>
        <li>📌 Rental Properties (3 Years): ROI ~15–30%, Risk: Medium</li>
        <li>📌 REITs (1 Year): ROI ~4–8%, Risk: High</li>
        <li>📌 REITs (3 Years): ROI ~12–25%, Risk: High</li>
    </ul>
    <p>Note: ROI estimates are illustrative and not guaranteed. Always consult a financial advisor.</p>
    """
    roi_data = {
        "labels": ["1 Year", "3 Years", "5 Years"],
        "rental": [7, 15, 25],
        "reit": [5, 12, 18]
    }

    return templates.TemplateResponse("report_template.html", {
        "request": request,
        "profile": profile,
        "strategy": strategy,
        "roi": roi,
        "roi_labels": roi_data["labels"],
        "roi_rental": roi_data["rental"],
        "roi_reit": roi_data["reit"]
    })
from fastapi import Form

@app.post("/predict_price", response_class=HTMLResponse)
async def predict_price(
    request: Request,
    city: str = Form(...),
    zipcode: str = Form(...),
    bedrooms: int = Form(...),
    bathrooms: float = Form(...),
    sqft: int = Form(...)
):
    user_summary = (
        f"The user wants to estimate the price of a house in {city}, {zipcode} "
        f"with {bedrooms} bedrooms, {bathrooms} bathrooms, and {sqft} sqft of living space."
    )

    prompt = f"""
    Based on historical real estate data in the United States, estimate a reasonable price range for a house with the following characteristics:

    - Location: {city}, {zipcode}
    - Bedrooms: {bedrooms}
    - Bathrooms: {bathrooms}
    - Living Area: {sqft} sqft

    Provide a price estimate range and a 2–3 sentence explanation. Format everything in HTML using <p> and <strong> for clarity. No markdown.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result_html = response.choices[0].message.content
    except Exception as e:
        result_html = f"<p><strong>Error:</strong> {e}</p>"

    return templates.TemplateResponse("prediction_result.html", {
        "request": request,
        "summary": user_summary,
        "result": result_html
    })
