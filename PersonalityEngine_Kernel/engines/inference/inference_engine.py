# inference_engine.py
# PEK Lite — Incremental Inference Engine (Layers 1–5)

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
    # Layer 5 — Control vs Trust Orientation
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
    # Lite Translation
    # -----------------------------
    lite = {
        "orientation_snapshot": "",
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": [],
    }

    if signal_summary["control_orientation"] > signal_summary["trust_orientation"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest a tendency to maintain control over outcomes, "
            "especially when responsibility feels high."
        )
        lite["real_world_signals"].append(
            "You may feel most at ease when you are actively managing variables."
        )
        lite["common_misinterpretations"].append(
            "This can be mistaken for rigidity, when it often reflects conscientiousness."
        )
        lite["reflection_prompts"].append(
            "Notice when control feels stabilizing versus draining."
        )

    elif signal_summary["trust_orientation"] > signal_summary["control_orientation"]:
        lite["orientation_snapshot"] = (
            "Your responses suggest comfort with allowing situations to develop without heavy intervention."
        )
        lite["strengths"].append(
            "Capacity to conserve energy by trusting processes and timing."
        )
        lite["reflection_prompts"].append(
            "Notice which situations invite trust versus active involvement."
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
