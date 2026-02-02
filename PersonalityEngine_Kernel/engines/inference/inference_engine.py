# inference_engine.py
# PEK Lite — Incremental Inference Engine (Layers 1–4)

from typing import List, Dict


def run_inference(responses: List[str], context_flags=None, forced_overrides=None) -> dict:
    text = " ".join(responses).lower()

    # -----------------------------
    # Base containers
    # -----------------------------
    signal_summary = {
        "motivation": 0,
        "cognitive_load": 0,
        "internal_tension": 0,
        "identity_rigidity": 0,
        "identity_flexibility": 0,
    }

    confidence_score = 0.3

    # -----------------------------
    # Layer 1 — Motivation
    # -----------------------------
    motivation_terms = ["drive", "push", "ambition", "goal", "prove", "achieve"]
    for term in motivation_terms:
        if term in text:
            signal_summary["motivation"] += 1

    # -----------------------------
    # Layer 2 — Cognitive Load / Overanalysis
    # -----------------------------
    cognitive_terms = ["overthink", "analyze", "ruminate", "second guess", "mentally exhausted"]
    for term in cognitive_terms:
        if term in text:
            signal_summary["cognitive_load"] += 1

    # -----------------------------
    # Layer 3 — Internal Tension / Pressure
    # -----------------------------
    tension_terms = ["pressure", "holding everything", "responsible for", "weight on me", "stress"]
    for term in tension_terms:
        if term in text:
            signal_summary["internal_tension"] += 1

    # -----------------------------
    # Layer 4 — Identity Rigidity vs Flexibility
    # -----------------------------
    rigidity_terms = [
        "this is just who i am",
        "i've always been this way",
        "people never change",
        "that's just me",
        "fixed"
    ]

    flexibility_terms = [
        "depends on the situation",
        "i adapt",
        "changes over time",
        "different sides of me",
        "context matters"
    ]

    for term in rigidity_terms:
        if term in text:
            signal_summary["identity_rigidity"] += 1

    for term in flexibility_terms:
        if term in text:
            signal_summary["identity_flexibility"] += 1

    # -----------------------------
    # Lite Translation Logic
    # -----------------------------
    lite = {
        "orientation_snapshot": "",
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": [],
    }

    if signal_summary["identity_rigidity"] > signal_summary["identity_flexibility"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest a relatively stable and consistent sense of self, "
            "with a tendency to define identity in fixed terms."
        )
        lite["real_world_signals"].append(
            "You may rely on a clear internal identity when navigating decisions or roles."
        )
        lite["common_misinterpretations"].append(
            "This can be mistaken for inflexibility, when it often reflects self-consistency."
        )
        lite["reflection_prompts"].append(
            "Notice when stability feels grounding versus when flexibility feels useful."
        )

    elif signal_summary["identity_flexibility"] > signal_summary["identity_rigidity"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest an adaptive sense of identity that shifts across situations."
        )
        lite["real_world_signals"].append(
            "You may adjust how you show up depending on context or environment."
        )
        lite["strengths"].append(
            "Capacity to navigate different roles without feeling confined to a single self-definition."
        )
        lite["reflection_prompts"].append(
            "Notice which environments invite flexibility versus consistency."
        )

    else:
        lite["orientation_snapshot"] = (
            "Your motivational structure appears internally consistent, "
            "with relatively low internal friction at this time."
        )
        lite["reflection_prompts"].append(
            "Notice what situations tend to increase internal pressure versus internal clarity."
        )

    return {
        "kernel_output": {
            "confidence_score": confidence_score,
            "signal_summary": signal_summary
        },
        "lite_translation": lite
    }
