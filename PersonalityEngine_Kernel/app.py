"""
PEK Lite – FastAPI Application Entry Point
Thin HTTP wrapper around the Personality Engine Kernel.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import json

from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference
from PersonalityEngine_Kernel.engines.translation.lite_translation import translate_lite


app = FastAPI(
    title="PEK Lite",
    version="0.4"
)

# ---------------- INPUT RULES ----------------
MIN_PROMPTS = 3
MAX_PROMPTS = 7
MIN_TOTAL_WORDS = 60
# ---------------------------------------------


class InferenceRequest(BaseModel):
    email: str
    responses: list[str]
    context_flags: dict | None = None
    forced_overrides: dict | None = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": "PEK Lite",
        "version": "0.4"
    }


def validate_input(responses: list[str]):
    if not responses or len(responses) < MIN_PROMPTS:
        raise HTTPException(
            status_code=422,
            detail="Please provide a bit more detail so the system has enough signal to work with."
        )

    if len(responses) > MAX_PROMPTS:
        raise HTTPException(
            status_code=422,
            detail="Too many responses provided for PEK Lite."
        )

    total_words = sum(len(r.split()) for r in responses)

    if total_words < MIN_TOTAL_WORDS:
        raise HTTPException(
            status_code=422,
            detail="Please expand your responses slightly so we can generate a meaningful report."
        )


@app.post("/infer")
def infer(payload: InferenceRequest, background_tasks: BackgroundTasks):
    validate_input(payload.responses)

    engine_input = {
        "responses": payload.responses,
        "context_flags": payload.context_flags or {},
        "forced_overrides": payload.forced_overrides or {}
    }

    kernel_output = run_inference(engine_input)

    lite_translation = translate_lite(kernel_output)

    return {
        "kernel_output": kernel_output,
        "lite_translation": lite_translation
    }
