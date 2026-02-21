"""
PersonaSight (PEK Lite) – FastAPI Application Entry Point
Dynamic Narrative Version (V3)
Stable ASGI app for Railway deployment
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from engines.inference.inference_engine import run_inference
print("RUN_INFERENCE SOURCE:", run_inference.__code__.co_filename)

app = FastAPI(
    title="PersonaSight (PEK Lite)",
    version="1.1.0"
)


class InferenceRequest(BaseModel):
    responses: List[str]
    context_flags: Optional[dict] = None
    forced_overrides: Optional[dict] = None


@app.get("/health")
def health():
    return {"status": "ok", "engine": "PersonaSight (PEK Lite)"}


def build_engine_input(payload: InferenceRequest) -> dict:
    combined_statement = " ".join(payload.responses)
    return {
        "example_statement": combined_statement,
        "context_flags": payload.context_flags or {},
        "forced_overrides": payload.forced_overrides or {}
    }


# --------------------------------------------------
# DYNAMIC NARRATIVE V3 LAYER
# --------------------------------------------------

def build_dynamic_narrative(result: dict) -> str:
    """
    Builds adaptive psychological narrative using kernel output.
    Does not assume fixed schema. Safe extraction only.
    """

    lite = result.get("lite_translation", {})
    sections = lite.get("sections", {})

    orientation = lite.get("orientation_snapshot", "")
    underlying = sections.get("underlying_patterns", "")
    dynamics = sections.get("internal_dynamics", "")
    decision = sections.get("decision_control", "")

    strengths = lite.get("strengths", [])
    risks = lite.get("common_misinterpretations", [])

    narrative_parts = []

    if orientation:
        narrative_parts.append(f"<p><strong>Core Orientation:</strong> {orientation}</p>")

    if underlying:
        narrative_parts.append(f"<p><strong>Behavioral Foundation:</strong> {underlying}</p>")

    if dynamics:
        narrative_parts.append(f"<p><strong>Internal Pressure Pattern:</strong> {dynamics}</p>")

    if decision:
        narrative_parts.append(f"<p><strong>Decision Model:</strong> {decision}</p>")

    if strengths:
        narrative_parts.append(
            "<p><strong>Primary Strengths:</strong> "
            + ", ".join(strengths[:5]) +
            "</p>"
        )

    if risks:
        narrative_parts.append(
            "<p><strong>Blind Spots Under Stress:</strong> "
            + ", ".join(risks[:5]) +
            "</p>"
        )

    if not narrative_parts:
        return "<p>Dynamic narrative unavailable. Engine output incomplete.</p>"

    return "".join(narrative_parts)


@app.post("/infer")
def infer(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)
    return JSONResponse(content=result)


@app.post("/report", response_class=HTMLResponse)
def render_report(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    engine_input = build_engine_input(payload)
    result = run_inference(engine_input)

    lite = result.get("lite_translation", {})
    sections = lite.get("sections", {})

    orientation = lite.get("orientation_snapshot", "")
    underlying = sections.get("underlying_patterns", "")
    dynamics = sections.get("internal_dynamics", "")
    decision = sections.get("decision_control", "")

    real_world = lite.get("real_world_signals", [])
    strengths = lite.get("strengths", [])
    mis = lite.get("common_misinterpretations", [])
    prompts = lite.get("reflection_prompts", [])

    dynamic_narrative_html = build_dynamic_narrative(result)

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>PersonaSight — PS Snapshot</title>
    </head>
    <body>
        <h1>PersonaSight — PS Snapshot</h1>
        {dynamic_narrative_html}
    </body>
    </html>
    """

    return HTMLResponse(content=html)


# --------------------------------------------------
# GUMROAD WEBHOOK (UPDATED WITH FULL HTML TEMPLATE)
# --------------------------------------------------

@app.post("/gumroad/webhook", response_class=HTMLResponse)
async def gumroad_webhook(request: Request):
    try:
        payload = await request.form()

        if payload.get("seller_id") is None:
            raise HTTPException(status_code=400, detail="Invalid Gumroad payload")

        buyer_email = payload.get("email")

        field_1 = payload.get("custom_fields[When important things depend on you, how do you internally feel or experience that responsibility?]", "")
        field_2 = payload.get("custom_fields[Do you usually rely on yourself or seek advice/reassurance from others before making important decisions in your life?]", "")
        field_3 = payload.get("custom_fields[After making an important decision, do you replay it in your head or second-guess yourself?]", "")
        field_4 = payload.get("custom_fields[When you’re feeling stressed or worried, how do you usually mentally or physically release it?]", "")
        field_5 = payload.get("custom_fields[How do you react when you feel you're being controlled, micromanaged, boxed in or forced to do something?]", "")
        field_6 = payload.get("custom_fields[What happens internally when a situation feels uncertain, unpredictable, or when you can't predict the outcome?]", "")
        field_7 = payload.get("custom_fields[Before taking action in a life situation, what does your mental decision process typically look and feel like?]", "")
        field_8 = payload.get("custom_fields[When evaluating yourself, whose judgment matters most — yours or other peoples?]", "")

        combined_statement = " ".join([
            field_1, field_2, field_3, field_4,
            field_5, field_6, field_7, field_8
        ])

        engine_input = {
            "example_statement": combined_statement,
            "context_flags": {},
            "forced_overrides": {}
        }

        result = run_inference(engine_input)

        dynamic_narrative_html = build_dynamic_narrative(result)

        lite = result.get("lite_translation", {})
        real_world = lite.get("real_world_signals", [])
        prompts = lite.get("reflection_prompts", [])

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>PersonaSight — PS Snapshot</title>
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
                .printbar {{
                    margin: 18px 0 34px 0;
                    padding: 14px 16px;
                    background: #111118;
                    border: 1px solid #2a2a35;
                    border-radius: 10px;
                    color: #cfd2dd;
                    line-height: 1.6;
                }}
                .printbar button {{
                    margin-top: 10px;
                    padding: 10px 14px;
                    border-radius: 10px;
                    border: 1px solid #2a2a35;
                    background: #1d1d27;
                    color: #eaeaf0;
                    cursor: pointer;
                    font-size: 0.95em;
                }}
                @media print {{
                    body {{
                        background: white;
                        color: #111;
                        padding: 0;
                    }}
                    .container {{
                        box-shadow: none;
                        background: white;
                        border-radius: 0;
                        padding: 24px;
                        max-width: 100%;
                    }}
                    .printbar {{
                        display: none;
                    }}
                }}
            </style>
            <script>
                function downloadPDF() {{
                    window.print();
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>PersonaSight — PS Snapshot</h1>

                <div class="printbar">
                    Save your Snapshot as a PDF before leaving this page.
                    <br>
                    Click below → Print → Save as PDF.
                    <br>
                    <button onclick="downloadPDF()">Download as PDF</button>
                </div>

                <h2>Dynamic Psychological Narrative</h2>
                {dynamic_narrative_html}

                <h2>Real-World Signals</h2>
                <ul>
                    {''.join(f"<li>{s}</li>" for s in real_world)}
                </ul>

                <h2>Reflection Prompts</h2>
                <ul>
                    {''.join(f"<li>{s}</li>" for s in prompts)}
                </ul>

            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=html)

    except Exception as e:
        print("GUMROAD WEBHOOK ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Webhook error")