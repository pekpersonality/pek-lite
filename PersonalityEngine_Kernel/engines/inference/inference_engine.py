# inference_engine.py
# PEK Lite — Inference Engine v0.9
# Layers 1–8 active, cumulative, Lite-enriched (non-prescriptive)

from typing import List, Dict


ENGINE_VERSION = "PEK_LITE_V0_9_ENRICHED"


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

    # -------------------------------------------------
    # LAYER 8 — INTERNAL PRESSURE REGULATION (STABLE)
    # -------------------------------------------------

    internal_pressure_markers = [
        "keep it inside",
        "deal with it internally",
        "rarely vent",
        "hold it in",
        "bottle it up",
        "internalize",
        "handle it myself",
        "process internally",
    ]

    external_release_markers = [
        "talk it out",
        "vent",
        "express my feelings",
        "let it out",
        "share how i feel",
    ]

    for phrase in internal_pressure_markers:
        if phrase in text:
            signal_summary["internal_pressure_regulation"] += 1
            confidence_score += 0.05

    for phrase in external_release_markers:
        if phrase in text:
            signal_summary["external_pressure_release"] += 1
            confidence_score += 0.05

    # -------------------------------------------------
    # LITE TRANSLATION — ENRICHED (VALUE LAYER)
    # -------------------------------------------------

    if signal_summary["internal_pressure_regulation"] > 0:
        orientation_snapshot = (
            "Your responses suggest a pattern of carrying responsibility and pressure internally. "
            "Rather than discharging stress outwardly, you tend to process demands privately and maintain "
            "a composed external presence. This often reflects a strong internal control system — one that "
            "prioritizes stability, self-regulation, and personal accountability over immediate emotional release."
        )

        real_world_signals = [
            "You may appear steady and unaffected even during periods of elevated internal stress.",
            "Others may underestimate how much pressure you are managing at any given time.",
            "You are more likely to reflect privately than to seek immediate external validation."
        ]

        strengths = [
            "High capacity for internal self-regulation under pressure.",
            "Ability to remain composed and functional during demanding situations.",
            "Strong sense of personal responsibility and internal control."
        ]

        common_misinterpretations = [
            "This pattern can be mistaken for emotional distance or disengagement.",
            "Others may assume you are unaffected when you are actually processing deeply."
        ]

        reflection_prompts = [
            "Notice how long you tend to carry pressure before releasing it.",
            "Pay attention to early internal signals that indicate rising strain.",
            "Consider which situations benefit from private processing versus shared reflection."
        ]
    else:
        orientation_snapshot = (
            "Your responses indicate a generally consistent internal motivational structure with relatively "
            "low visible internal friction at this time. You appear to move through demands without significant "
            "strain, maintaining alignment between intention and action."
        )

        real_world_signals = [
            "You may experience periods where decisions feel clear and manageable.",
            "You are less likely to feel internally overloaded during routine demands."
        ]

        strengths = [
            "Ability to maintain internal alignment without excessive strain.",
            "Stable engagement with responsibilities and expectations."
        ]

        common_misinterpretations = [
            "This steadiness can be mistaken for passivity.",
            "Others may not recognize the deliberate nature of your pacing."
        ]

        reflection_prompts = [
            "Notice what conditions help preserve this sense of internal ease.",
            "Pay attention to changes when demands begin to stack."
        ]

    return {
        "engine_version": ENGINE_VERSION,
        "kernel_output": {
            "confidence_score": round(confidence_score, 2),
            "signal_summary": signal_summary,
        },
        "lite_translation": {
            "orientation_snapshot": orientation_snapshot,
            "real_world_signals": real_world_signals,
            "strengths": strengths,
            "common_misinterpretations": common_misinterpretations,
            "reflection_prompts": reflection_prompts,
        },
    }
