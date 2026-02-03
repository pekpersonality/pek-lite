# inference_engine.py
# PEK Lite — Inference Engine v0.9
# Layers 1–8 cumulative, additive, non-destructive

from typing import List, Dict


ENGINE_VERSION = "PEK_LITE_LAYERS_1_TO_8"


def run_inference(responses: List[str], context_flags=None, forced_overrides=None):
    text = " ".join(responses).lower()

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
        "deliberative_decision_style": 0,
        "decisive_action_style": 0,
        "internal_pressure_regulation": 0,
        "external_pressure_release": 0,
    }

    confidence_score = 0.3

    # -------------------------
    # LAYER 1 — MOTIVATION / RESPONSIBILITY
    # -------------------------
    motivation_markers = [
        "responsible", "holding everything together", "carry the load",
        "depend on me", "my responsibility"
    ]

    # -------------------------
    # LAYER 2 — COGNITIVE LOAD / OVERTHINKING
    # -------------------------
    cognitive_markers = [
        "overthink", "replay decisions", "analyze too much",
        "can't stop thinking", "mentally exhausting"
    ]

    # -------------------------
    # LAYER 3 — INTERNAL TENSION
    # -------------------------
    tension_markers = [
        "pressure", "tense", "on edge", "stress building",
        "tight", "anxious"
    ]

    # -------------------------
    # LAYER 4 — IDENTITY STRUCTURE
    # -------------------------
    rigidity_markers = [
        "i am this way", "always been like this",
        "that's just who i am"
    ]

    flexibility_markers = [
        "depends", "changes", "sometimes",
        "can adapt", "varies"
    ]

    # -------------------------
    # LAYER 5 — CONTROL VS TRUST
    # -------------------------
    control_markers = [
        "control", "manage everything", "handle it myself",
        "keep things in order"
    ]

    trust_markers = [
        "trust others", "let go", "delegate",
        "rely on others"
    ]

    # -------------------------
    # LAYER 6 — VALIDATION SOURCE
    # -------------------------
    external_validation_markers = [
        "need reassurance", "approval", "validation",
        "what others think"
    ]

    internal_reference_markers = [
        "i know internally", "my own judgment",
        "i trust myself"
    ]

    # -------------------------
    # LAYER 7 — DECISION STYLE
    # -------------------------
    deliberative_markers = [
        "think it through", "take my time deciding",
        "deliberate", "weigh options"
    ]

    decisive_markers = [
        "act quickly", "decide fast",
        "go with my gut immediately"
    ]

    # -------------------------
    # LAYER 8 — PRESSURE REGULATION
    # -------------------------
    internal_pressure_markers = [
        "keep stress inside", "deal with it internally",
        "rarely vent", "hold it in",
        "bottle it up", "process internally"
    ]

    external_release_markers = [
        "vent", "talk it out", "let it out",
        "express my feelings"
    ]

    # -------------------------
    # SCORING
    # -------------------------
    def score(markers, key):
        nonlocal confidence_score
        for phrase in markers:
            if phrase in text:
                signal_summary[key] += 1
                confidence_score += 0.05

    score(motivation_markers, "motivation")
    score(cognitive_markers, "cognitive_load")
    score(tension_markers, "internal_tension")
    score(rigidity_markers, "identity_rigidity")
    score(flexibility_markers, "identity_flexibility")
    score(control_markers, "control_orientation")
    score(trust_markers, "trust_orientation")
    score(external_validation_markers, "external_validation")
    score(internal_reference_markers, "internal_reference")
    score(deliberative_markers, "deliberative_decision_style")
    score(decisive_markers, "decisive_action_style")
    score(internal_pressure_markers, "internal_pressure_regulation")
    score(external_release_markers, "external_pressure_release")

    # -------------------------
    # LITE TRANSLATION (MINIMAL, OBSERVATIONAL)
    # -------------------------
    if signal_summary["internal_pressure_regulation"] > 0:
        orientation_snapshot = (
            "You tend to manage pressure internally rather than releasing it outwardly. "
            "This reflects a contained, self-directed coping style."
        )
    else:
        orientation_snapshot = (
            "Your motivational structure appears internally consistent, "
            "with relatively low internal friction at this time."
        )

    lite = {
        "orientation_snapshot": orientation_snapshot,
        "real_world_signals": [
            "You may carry stress quietly without signaling it to others."
            if signal_summary["internal_pressure_regulation"] > 0 else
            "You may appear steady and composed to people around you."
        ],
        "strengths": [
            "Strong internal regulation and self-control."
            if signal_summary["internal_pressure_regulation"] > 0 else
            "Ability to maintain internal alignment."
        ],
        "common_misinterpretations": [
            "This pattern can be mistaken for emotional distance."
            if signal_summary["internal_pressure_regulation"] > 0 else
            "This can be mistaken for passivity."
        ],
        "reflection_prompts": [
            "Notice when holding pressure internally helps you — and when it becomes costly."
        ]
    }

    return {
        "engine_version": ENGINE_VERSION,
        "kernel_output": {
            "confidence_score": round(confidence_score, 2),
            "signal_summary": signal_summary,
        },
        "lite_translation": lite,
    }
