from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

API_KEY = "ak_3x490kl55gbv57dj6fj8r8hi"
EMAIL = "24f1002662@ds.study.iitm.ac.in"   # <-- replace with your logged-in email

app = FastAPI()

# CORS: allow the grader page to call us from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    # 1. Check the API key
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2. Read the events
    body = await request.json()
    events = body.get("events", [])

    # 3. Do the math
    total_events = len(events)
    unique_users = len({e["user"] for e in events})

    totals = defaultdict(float)   # positive-amount total per user
    revenue = 0.0
    for e in events:
        amount = e["amount"]
        if amount > 0:
            revenue += amount
            totals[e["user"]] += amount

    top_user = max(totals, key=totals.get) if totals else None

    # 4. Send the answer
    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }