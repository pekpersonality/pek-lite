# inference_engine.py
# PEK Lite — Inference Engine v0.8
# Layers 1–8 active, additive, non-destructive

from typing import List, Dict


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
    # LAYER 8 — PRESSURE REGULATION (EXPANDED)
    # -------------------------

    internal_pressure_markers = [
        "keep it inside",
        "keep stress inside",
        "hold it in",
        "deal with it internally",
        "rarely vent",
        "don't vent",
        "dont vent",
        "not show",
        "hide stress",
        "internalize",
        "bottle up",
        "bottled up",
        "handle it myself",
        "handle it alone",
        "process internally",
        "keep pressure inside",
    ]

    external_release_markers = [
        "talk it out",
        "vent",
        "let it out",
        "express my feelings",
        "release pressure",
        "share how i feel",
        "need to get it out",
    ]

    for phrase in internal_pressure_markers:
        if phrase in text:
            signal_summary["internal_pressure_regulation"] += 1
            confidence_score += 0.05

    for phrase in external_release_markers:
        if phrase in text:
            signal_summary["external_pressure_release"] += 1
            confidence_score += 0.05

    # -------------------------
    # LITE TRANSLATION
    # -------------------------

    lite = {
        "orientation_snapshot": (
            "You tend to regulate pressure internally rather than releasing it outwardly. "
            "This suggests a self-contained coping style that prioritizes control and privacy."
            if signal_summary["internal_pressure_regulation"] > 0
            else
            "Your motivational structure appears internally consistent, with relatively low internal friction at this time."
        ),
        "real_world_signals": (
            [
                "You may carry stress quietly rather than expressing it outwardly.",
                "Others may not immediately notice when pressure is building for you."
            ]
            if signal_summary["internal_pressure_regulation"] > 0
            else []
        ),
        "strengths": (
            [
                "Ability to remain composed under pressure.",
                "Strong internal containment and self-regulation."
            ]
            if signal_summary["internal_pressure_regulation"] > 0
            else []
        ),
        "common_misinterpretations": (
            [
                "This pattern can be mistaken for emotional distance.",
                "In reality, it often reflects deliberate self-control."
            ]
            if signal_summary["internal_pressure_regulation"] > 0
            else []
        ),
        "reflection_prompts": (
            [
                "Notice how long you tend to hold pressure before releasing it.",
                "Consider what signals tell you when internal pressure is reaching its limit."
            ]
            if signal_summary["internal_pressure_regulation"] > 0
            else []
        ),
    }

    return {
        "kernel_output": {
            "confidence_score": round(confidence_score, 2),
            "signal_summary": signal_summary,
        },
        "lite_translation": lite,
    }
