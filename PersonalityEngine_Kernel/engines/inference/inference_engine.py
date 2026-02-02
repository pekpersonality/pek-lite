# inference_engine.py
# PEK Lite — Inference Engine v0.8
# Layers 1–8 (Motivation → Emotional Pressure Regulation)

from typing import List, Dict


def run_inference(
    responses: List[str],
    context_flags: Dict = None,
    forced_overrides: Dict = None
):
    text = " ".join(responses).lower()

    signal_summary = {
        # Layer 1–2
        "motivation": 0,

        # Layer 3
        "cognitive_load": 0,

        # Layer 4
        "internal_tension": 0,

        # Layer 5
        "identity_rigidity": 0,
        "identity_flexibility": 0,

        # Layer 6
        "control_orientation": 0,
        "trust_orientation": 0,

        # Layer 7
        "deliberative_decision_style": 0,
        "decisive_action_style": 0,

        # Layer 8
        "internal_pressure_regulation": 0,
        "external_pressure_release": 0,
    }

    confidence_score = 0.3

    # -----------------------------
    # Layer 3 — Cognitive Load / Overanalysis
    # -----------------------------
    if any(p in text for p in [
        "overanalyze", "overthinking", "mental load", "too much in my head"
    ]):
        signal_summary["cognitive_load"] += 1
        confidence_score += 0.05

    # -----------------------------
    # Layer 4 — Internal Tension
    # -----------------------------
    if any(p in text for p in [
        "pressure", "tight", "on edge", "holding it together"
    ]):
        signal_summary["internal_tension"] += 1
        confidence_score += 0.05

    # -----------------------------
    # Layer 5 — Identity Rigidity vs Flexibility
    # -----------------------------
    if any(p in text for p in [
        "this is just how i am", "i don't change", "fixed"
    ]):
        signal_summary["identity_rigidity"] += 1

    if any(p in text for p in [
        "i'm adapting", "i'm learning", "i've changed"
    ]):
        signal_summary["identity_flexibility"] += 1

    # -----------------------------
    # Layer 6 — Control vs Trust Orientation
    # -----------------------------
    if any(p in text for p in [
        "i need control", "i handle it myself", "i don't rely on others"
    ]):
        signal_summary["control_orientation"] += 1

    if any(p in text for p in [
        "i trust the process", "i let things unfold", "i rely on others"
    ]):
        signal_summary["trust_orientation"] += 1

    # -----------------------------
    # Layer 7 — Decision Style
    # -----------------------------
    if any(p in text for p in [
        "overanalyze before acting", "need clarity before deciding",
        "sit with decisions", "weigh options"
    ]):
        signal_summary["deliberative_decision_style"] += 1

    if any(p in text for p in [
        "act fast", "jump in", "decide quickly", "figure it out later"
    ]):
        signal_summary["decisive_action_style"] += 1

    # -----------------------------
    # Layer 8 — Emotional Pressure Regulation
    # -----------------------------
    if any(p in text for p in [
        "keep it inside", "hold it in", "deal with it internally",
        "i don't show stress"
    ]):
        signal_summary["internal_pressure_regulation"] += 1

    if any(p in text for p in [
        "vent", "talk it out", "need to release",
        "i let it out", "express my stress"
    ]):
        signal_summary["external_pressure_release"] += 1

    # -----------------------------
    # Lite Translation (fallback-safe)
    # -----------------------------
    lite_translation = {
        "orientation_snapshot": (
            "Your motivational structure appears internally consistent, "
            "with relatively low internal friction at this time."
        ),
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": []
    }

    return {
        "kernel_output": {
            "confidence_score": round(min(confidence_score, 0.95), 2),
            "signal_summary": signal_summary
        },
        "lite_translation": lite_translation
    }
