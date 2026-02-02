# inference_engine.py
# PEK Lite — Incremental Inference Engine (Layers 1–6)

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
        "control_orientation": 0,
        "trust_orientation": 0,
        "external_validation": 0,
        "internal_reference": 0,
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
    # Layer 2 — Cognitive Load
    # -----------------------------
    cognitive_terms = ["overthink", "analyze", "ruminate", "second guess", "mentally exhausted"]
    for term in cognitive_terms:
        if term in text:
            signal_summary["cognitive_load"] += 1

    # -----------------------------
    # Layer 3 — Internal Tension
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
    # Layer 5 — Control vs Trust
    # -----------------------------
    control_terms = [
        "i have to make sure",
        "i can't rely on others",
        "i need to manage",
        "if i don't handle it",
        "i keep things from falling apart"
    ]

    trust_terms = [
        "i let things unfold",
        "i trust the process",
        "things work out",
        "i allow",
        "i step back"
    ]

    for term in control_terms:
        if term in text:
            signal_summary["control_orientation"] += 1

    for term in trust_terms:
        if term in text:
            signal_summary["trust_orientation"] += 1

    # -----------------------------
    # Layer 6 — External Validation vs Internal Reference
    # -----------------------------
    validation_terms = [
        "what do people think",
        "i need approval",
        "how i'm perceived",
        "validation",
        "recognized",
        "seen as"
    ]

    internal_reference_terms = [
        "i know for myself",
        "internally",
        "my own standards",
        "i trust my judgment",
        "inner sense"
    ]

    for term in validation_terms:
        if term in text:
            signal_summary["external_validation"] += 1

    for term in internal_reference_terms:
        if term in text:
            signal_summary["internal_reference"] += 1

    # -----------------------------
    # Lite Translation
    # -----------------------------
    lite = {
        "orientation_snapshot": "",
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": [],
    }

    if signal_summary["external_validation"] > signal_summary["internal_reference"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest attentiveness to how your actions are perceived by others."
        )
        lite["real_world_signals"].append(
            "You may calibrate decisions based on external feedback or recognition."
        )
        lite["common_misinterpretations"].append(
            "This can be mistaken for insecurity, when it often reflects social awareness."
        )
        lite["reflection_prompts"].append(
            "Notice when external input feels informative versus distracting."
        )

    elif signal_summary["internal_reference"] > signal_summary["external_validation"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest reliance on internal standards when evaluating decisions."
        )
        lite["strengths"].append(
            "Capacity to self-evaluate without heavy dependence on external feedback."
        )
        lite["reflection_prompts"].append(
            "Notice which situations reinforce trust in your internal judgment."
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
