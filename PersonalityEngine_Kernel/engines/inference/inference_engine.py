# inference_engine.py
# PEK Lite — Inference Engine v0.9
# Layers 1–8 cumulative, relaxed keyword-family matching

from typing import List, Dict


ENGINE_VERSION = "PEK_LITE_LAYERS_1_TO_8_RELAXED"


def keyword_hit(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


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
    # LAYER 1 — RESPONSIBILITY / MOTIVATION
    # -------------------------
    if keyword_hit(text, [
        "responsible", "holding", "carry", "depend", "outcomes", "manage"
    ]):
        signal_summary["motivation"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 2 — COGNITIVE LOAD / OVERANALYSIS
    # -------------------------
    if keyword_hit(text, [
        "overthink", "over analyze", "replay", "ruminate", "analyze", "mentally"
    ]):
        signal_summary["cognitive_load"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 3 — INTERNAL TENSION
    # -------------------------
    if keyword_hit(text, [
        "pressure", "stress", "tension", "strain", "frustrated"
    ]):
        signal_summary["internal_tension"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 4 — IDENTITY RIGIDITY / FLEXIBILITY
    # -------------------------
    if keyword_hit(text, [
        "standards", "hard on myself", "expect", "should be", "my role"
    ]):
        signal_summary["identity_rigidity"] += 1
        confidence_score += 0.05

    if keyword_hit(text, [
        "adapt", "flexible", "open", "adjust"
    ]):
        signal_summary["identity_flexibility"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 5 — CONTROL vs TRUST
    # -------------------------
    if keyword_hit(text, [
        "control", "handle", "manage", "my responsibility"
    ]):
        signal_summary["control_orientation"] += 1
        confidence_score += 0.05

    if keyword_hit(text, [
        "trust", "rely", "let go"
    ]):
        signal_summary["trust_orientation"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 6 — VALIDATION SOURCE
    # -------------------------
    if keyword_hit(text, [
        "approval", "validation", "recognition", "noticed"
    ]):
        signal_summary["external_validation"] += 1
        confidence_score += 0.05

    if keyword_hit(text, [
        "my own standards", "internal", "for myself"
    ]):
        signal_summary["internal_reference"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 7 — DECISION STYLE
    # -------------------------
    if keyword_hit(text, [
        "deliberate", "think through", "consider"
    ]):
        signal_summary["deliberative_decision_style"] += 1
        confidence_score += 0.05

    if keyword_hit(text, [
        "decide quickly", "act fast", "jump in"
    ]):
        signal_summary["decisive_action_style"] += 1
        confidence_score += 0.05

    # -------------------------
    # LAYER 8 — PRESSURE REGULATION
    # -------------------------
    if keyword_hit(text, [
        "keep it inside", "internally", "rarely vent", "hold it in",
        "don't show", "not show"
    ]):
        signal_summary["internal_pressure_regulation"] += 1
        confidence_score += 0.05

    if keyword_hit(text, [
        "vent", "talk it out", "let it out", "express"
    ]):
        signal_summary["external_pressure_release"] += 1
        confidence_score += 0.05

    # -------------------------
    # LITE TRANSLATION (OBSERVATIONAL)
    # -------------------------
    lite = {
        "orientation_snapshot": (
            "Your responses suggest a pattern of internal responsibility, cognitive load, "
            "and self-contained pressure regulation. You appear to process demands internally "
            "before acting outwardly."
            if confidence_score > 0.4
            else
            "Your motivational structure appears internally consistent, with relatively low internal friction at this time."
        ),
        "real_world_signals": [
            "You may carry responsibility and stress internally without outward display."
        ] if signal_summary["internal_pressure_regulation"] else [],
        "strengths": [
            "Capacity for self-regulation and sustained internal focus."
        ] if confidence_score > 0.4 else [],
        "common_misinterpretations": [
            "This can be mistaken for passivity or emotional distance."
        ] if signal_summary["internal_pressure_regulation"] else [],
        "reflection_prompts": [
            "Notice when internal processing helps you — and when sharing might reduce load."
        ] if confidence_score > 0.4 else [],
    }

    return {
        "engine_version": ENGINE_VERSION,
        "kernel_output": {
            "confidence_score": round(confidence_score, 2),
            "signal_summary": signal_summary,
        },
        "lite_translation": lite,
    }
