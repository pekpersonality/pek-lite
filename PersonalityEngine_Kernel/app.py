"""
PersonaSight™ – FastAPI Application Entry Point
Production Build – Stripe Payment Link Flow
Railway Ready
"""

from fastapi import FastAPI, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference

app = FastAPI(
    title="PersonaSight™",
    version="2.0.1"
)

# -----------------------------
# Request Model
# -----------------------------

class InferenceRequest(BaseModel):
    responses: List[str]
    context_flags: Optional[dict] = None
    forced_overrides: Optional[dict] = None


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok", "engine": "PersonaSight™"}


# -----------------------------
# Engine Input Builder
# -----------------------------

def build_engine_input(payload: InferenceRequest) -> dict:
    combined_statement = " ".join(payload.responses)
    return {
        "example_statement": combined_statement,
        "context_flags": payload.context_flags or {},
        "forced_overrides": payload.forced_overrides or {}
    }


# -----------------------------
# Raw Inference Endpoint
# -----------------------------

@app.post("/infer")
def infer(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)
    return JSONResponse(content=result)


# -----------------------------
# Ritual Multi-Step Form
# -----------------------------

@app.get("/report-form", response_class=HTMLResponse)
def report_form(paid: Optional[str] = Query(None)):

    if paid != "true":
        return HTMLResponse("""
        <html>
        <head>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background: #f4f1ea;
                    color: #2c2a27;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    height:100vh;
                }
                .box {
                    background:#fbf8f3;
                    padding:40px;
                    border-radius:16px;
                    box-shadow:0 20px 50px rgba(0,0,0,0.08);
                    max-width:480px;
                    text-align:center;
                }
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Payment Required</h2>
                <p>Please complete your purchase before accessing PersonaSight.</p>
            </div>
        </body>
        </html>
        """)

    questions = [
        "When important things depend on you, how do you internally experience that responsibility?",
        "Do you rely on yourself or seek reassurance before major decisions?",
        "After making an important decision, do you replay it mentally?",
        "When stressed, how do you release pressure internally or externally?",
        "How do you react when you feel controlled or boxed in?",
        "What happens internally when things feel uncertain or unpredictable?",
        "Before taking action, what does your decision process feel like?",
        "Whose judgment matters more to you — yours or others’?"
    ]

    html_questions = "".join([
        f"""
        <div class="step">
            <h2>{q}</h2>
            <textarea name="responses" required></textarea>
            <button type="button" onclick="nextStep()">Continue</button>
        </div>
        """ for q in questions
    ])

    return HTMLResponse(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>PersonaSight™</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: radial-gradient(circle at center, #f5f2ea 0%, #ece6d8 100%);
                color: #2c2a27;
                padding: 60px 20px;
            }}
            .container {{
                max-width: 700px;
                margin: auto;
                background: #fbf8f3;
                padding: 60px;
                border-radius: 18px;
                box-shadow: 0 35px 80px rgba(0,0,0,0.12);
            }}
            h1 {{
                font-size: 2.2em;
                margin-bottom: 40px;
            }}
            h2 {{
                min-height: 90px;
                font-weight: 600;
            }}
            .step {{
                display: none;
                min-height: 320px;
            }}
            .step.active {{
                display: block;
            }}
            textarea {{
                width: 100%;
                height: 140px;
                margin-top: 20px;
                padding: 14px;
                border-radius: 10px;
                border: 1px solid #dddcc8;
                box-sizing: border-box;
                font-size: 1em;
            }}
            button {{
                margin-top: 20px;
                padding: 12px 18px;
                border-radius: 10px;
                border: none;
                background: #2c2a27;
                color: white;
                cursor: pointer;
                font-size: 1em;
            }}
        </style>
        <script>
            let current = 0;
            function nextStep() {{
                const steps = document.querySelectorAll('.step');
                steps[current].classList.remove('active');
                current++;
                if (current < steps.length) {{
                    steps[current].classList.add('active');
                }} else {{
                    document.getElementById("ritualForm").submit();
                }}
            }}
            window.onload = function() {{
                document.querySelector('.step').classList.add('active');
            }};
        </script>
    </head>
    <body>
        <div class="container">
            <h1>PersonaSight™ Personal Pattern Analysis</h1>
            <form id="ritualForm" method="post" action="/report">
                {html_questions}
            </form>
        </div>
    </body>
    </html>
    """)


# -----------------------------
# Final Report Rendering
# -----------------------------

@app.post("/report", response_class=HTMLResponse)
def render_report(responses: List[str] = Form(...)):

    payload = InferenceRequest(responses=responses)
    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)

    depth = result.get("input_depth_rating", {})
    lite = result.get("lite_translation", {})

    orientation = lite.get("orientation_snapshot", "")
    core_themes = lite.get("core_themes", "")
    sections = lite.get("sections", {})
    underlying = sections.get("underlying_patterns", "")
    dynamics = sections.get("internal_dynamics", "")
    decision = sections.get("decision_control", "")
    real_world = lite.get("real_world_signals", [])
    prompts = lite.get("reflection_prompts", [])
    next_step_note = lite.get("next_step_note", "")

    return HTMLResponse(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>PersonaSight™ Snapshot</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: radial-gradient(circle at center, #f5f2ea 0%, #ece6d8 100%);
                color: #2c2a27;
                padding: 60px 20px;
            }}
            .container {{
                max-width: 820px;
                margin: auto;
                background: #fbf8f3;
                padding: 64px;
                border-radius: 18px;
                box-shadow: 0 35px 80px rgba(0,0,0,0.12);
            }}
            h1 {{
                font-size: 2.3em;
                margin-bottom: 30px;
            }}
            h2 {{
                margin-top: 40px;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #8a8175;
            }}
            p {{
                line-height: 1.8;
                margin-top: 14px;
            }}
            ul {{
                margin-top: 16px;
                line-height: 1.8;
            }}
            li {{
                margin-bottom: 8px;
            }}
            .depth {{
                background: #f0ebe3;
                padding: 16px;
                border-radius: 10px;
                margin-bottom: 30px;
                font-size: 0.95em;
            }}
            .next {{
                margin-top: 40px;
                background: #f0ebe3;
                padding: 16px;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>PersonaSight™ Snapshot</h1>

            <div class="depth">
                <strong>Input Depth:</strong> {depth.get("label","")}<br>
                {depth.get("note","")}
            </div>

            <h2>Core Orientation</h2>
            <p>{orientation}</p>

            <p><em>{core_themes}</em></p>

            <h2>Behavioral Foundation</h2>
            <p>{underlying}</p>

            <h2>Internal Pressure Pattern</h2>
            <p>{dynamics}</p>

            <h2>Decision Model</h2>
            <p>{decision}</p>

            <h2>Real-World Signals</h2>
            <ul>
                {''.join(f"<li>{s}</li>" for s in real_world)}
            </ul>

            <h2>Reflection Prompts</h2>
            <ul>
                {''.join(f"<li>{p}</li>" for p in prompts)}
            </ul>

            <div class="next">{next_step_note}</div>

        </div>
    </body>
    </html>
    """)