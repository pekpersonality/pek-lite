"""
PEK Lite – FastAPI Application Entry Point
Stable ASGI app for Railway deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference


# -----------------------------
# FASTAPI APP (THIS IS WHAT RAILWAY NEEDS)
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
    return {
        "status": "ok",
        "engine": "PEK Lite"
    }


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
# HTML REPORT ENDPOINT
# -----------------------------
@app.post("/report", response_class=HTMLResponse)
def render_report(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)

    lt = result["lite_translation"]
    ks = result["kernel_output"]["signal_summary"]

    html = f"""
    <html>
    <head>
        <title>Personality Engine Kernel — Lite Snapshot</title>
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
                margin-top: 12px;
            }}
            ul {{
                line-height: 1.7;
                margin-top: 12px;
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
            <h1>Personality Engine Kernel — Lite</h1>
            <div class="sub">Behavioral & cognitive pattern snapshot</div>

            <h2>Orientation Snapshot</h2>
            <p>{lt["orientation_snapshot"]}</p>

            <h2>Underlying Behavioral Patterns</h2>
            <p>
                Your responses indicate a tendency toward internally driven regulation. Motivation, responsibility,
                and cognitive processing appear to be handled quietly and deliberately, often without outward signaling.
                This suggests a pattern of self-reliance and internal calibration rather than reactive adjustment.
            </p>

            <h2>Internal Dynamics & Pressure Flow</h2>
            <p>
                Signals related to cognitive load, internal tension, and pressure regulation suggest that demands are
                absorbed internally before being expressed. This creates outward composure, but also means pressure
                may accumulate below the surface over time.
            </p>

            <h2>Decision & Control Style</h2>
            <p>
                Your profile reflects a more deliberate decision-making style, with a preference for thinking through
                outcomes before acting. Control orientation appears internally anchored rather than externally enforced,
                allowing for stability but sometimes slowing outward responsiveness.
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
                Generated by PEK Lite · Insightful Snapshot
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
