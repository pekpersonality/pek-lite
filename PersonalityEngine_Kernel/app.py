"""
PEK Lite – FastAPI Application Entry Point
Stable ASGI app for Railway deployment
"""
from fastapi import Request
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference


# -----------------------------
# FASTAPI APP (ASGI ROOT)
# -----------------------------
app = FastAPI(
    title="PEK Lite",
    version="1.0.0"
)


# -----------------------------
# REQUEST MODEL
# -----------------------------
class InferenceRequest(BaseModel):
    responses: List[str]
    context_flags: Optional[dict] = None
    forced_overrides: Optional[dict] = None


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok", "engine": "PEK Lite"}


# -----------------------------
# INPUT NORMALIZATION
# -----------------------------
def build_engine_input(payload: InferenceRequest) -> dict:
    combined_statement = " ".join(payload.responses)
    return {
        "example_statement": combined_statement,
        "context_flags": payload.context_flags or {},
        "forced_overrides": payload.forced_overrides or {}
    }


# -----------------------------
# JSON INFERENCE ENDPOINT
# -----------------------------
@app.post("/infer")
def infer(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)
    return JSONResponse(content=result)


# -----------------------------
# HTML REPORT ENDPOINT (PREMIUM COPY)
# -----------------------------
@app.post("/report", response_class=HTMLResponse)
def render_report(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)

    lt = result["lite_translation"]

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PersonaSight™ Snapshot Report</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: #0e0e11;
                color: #eaeaf0;
                padding: 60px 20px;
            }}
            .container {{
                max-width: 900px;
                margin: auto;
                background: #16161c;
                padding: 52px;
                border-radius: 14px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.6);
            }}
            h1 {{
                font-size: 2.3em;
                margin-bottom: 6px;
            }}
            .sub {{
                color: #9aa0b0;
                margin-bottom: 36px;
            }}
            h2 {{
                margin-top: 42px;
                border-bottom: 1px solid #2a2a35;
                padding-bottom: 6px;
            }}
            p {{
                line-height: 1.7;
                margin-top: 14px;
            }}
            ul {{
                line-height: 1.7;
                margin-top: 14px;
            }}
            .footer {{
                margin-top: 48px;
                color: #777;
                font-size: 0.85em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Personality Engine Kernel - Lite</h1>
            <div class="sub">Behavioral and cognitive pattern snapshot</div>

            <h2>Orientation Snapshot</h2>
            <p>{lt["orientation_snapshot"]}</p>

            <h2>Underlying Behavioral Patterns</h2>
            <p>
                Your responses indicate a tendency toward internally driven regulation. Motivation,
                responsibility, and cognitive processing appear to be handled quietly and deliberately
                rather than through outward expression. This reflects a pattern of self-reliance and
                internal calibration, where stability is maintained by internal control rather than
                reactive adjustment.
            </p>

            <h2>Internal Dynamics and Pressure Flow</h2>
            <p>
                Signals related to cognitive load, internal tension, and pressure regulation suggest
                that demands are absorbed internally before being released. This creates outward
                composure, but can allow pressure to accumulate beneath the surface over time if not
                periodically discharged or acknowledged.
            </p>

            <h2>Decision and Control Style</h2>
            <p>
                Your profile reflects a deliberate decision-making approach. You tend to think through
                outcomes before acting, with control anchored internally rather than imposed externally.
                This supports consistency and clarity, though it may slow visible responsiveness in
                fast-moving or emotionally charged environments.
            </p>

            <h2>Real-World Signals</h2>
            <ul>
                {''.join(f"<li>{s}</li>" for s in lt["real_world_signals"])}
            </ul>

            <h2>Strengths</h2>
            <ul>
                {''.join(f"<li>{s}</li>" for s in lt["strengths"])}
            </ul>

            <h2>Common Misinterpretations</h2>
            <ul>
                {''.join(f"<li>{s}</li>" for s in lt["common_misinterpretations"])}
            </ul>

            <h2>Reflection Prompts</h2>
            <ul>
                {''.join(f"<li>{s}</li>" for s in lt["reflection_prompts"])}
            </ul>

            <div class="footer">
                Generated by PersonaSight Intelligence System
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
# -----------------------------
# GUMROAD WEBHOOK (PHASE 2)
# -----------------------------
@app.post("/gumroad/webhook")
async def gumroad_webhook(request: Request):
    try:
        payload = await request.form()

        if payload.get("seller_id") is None:
            raise HTTPException(status_code=400, detail="Invalid Gumroad payload")

        # Extract buyer email
        buyer_email = payload.get("email")

        # Extract custom fields (LOCKED TEXT KEYS)
        field_1 = payload.get("custom_fields[When important things depend on you, how do you internally feel or experience that responsibility?]", "")
        field_2 = payload.get("custom_fields[Do you usually rely on yourself or seek advice/reassurance from others before making important decisions in your life?]", "")
        field_3 = payload.get("custom_fields[After making an important decision, do you replay it in your head or second-guess yourself?]", "")
        field_4 = payload.get("custom_fields[When you’re feeling stressed or worried, how do you usually mentally or physically release it?]", "")
        field_5 = payload.get("custom_fields[How do you react when you feel you're being controlled, micromanaged, boxed in or forced to do something?]", "")
        field_6 = payload.get("custom_fields[What happens internally when a situation feels uncertain, unpredictable, or when you can't predict the outcome?]", "")
        field_7 = payload.get("custom_fields[Before taking action in a life situation, what does your mental decision process typically look and feel like?]", "")
        field_8 = payload.get("custom_fields[When evaluating yourself, whose judgment matters most — yours or other peoples?]", "")

        # Combine into single narrative blob
        combined_statement = " ".join([
            field_1, field_2, field_3, field_4,
            field_5, field_6, field_7, field_8
        ])

        # Run inference engine
        engine_input = {
            "example_statement": combined_statement,
            "context_flags": {},
            "forced_overrides": {}
        }

        result = run_inference(engine_input)

        # Log result for verification
        print("WEBHOOK BUYER:", buyer_email)
        print("WEBHOOK RESULT:", result)

        return {"status": "processed"}

    except Exception as e:
        print("GUMROAD WEBHOOK ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Webhook error")
