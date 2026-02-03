# inference_engine.py
# Personality Engine Kernel — Lite
# Version: PEK_LITE_INSIGHTFUL_A_V1
# Layers 1–8 cumulative, non-destructive

from typing import List, Dict


def run_inference(engine_input: dict):
    text = engine_input.get("example_statement", "").lower()

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
    # SIGNAL MATCHING (RELAXED)
    # -------------------------

    def match_any(phrases):
        return any(p in text for p in phrases)

    if match_any(["responsible", "holding everything", "managing outcomes"]):
        signal_summary["motivation"] += 1
        confidence_score += 0.05

    if match_any(["overthink", "replay", "mentally"]):
        signal_summary["cognitive_load"] += 1
        confidence_score += 0.05

    if match_any(["stress", "pressure"]):
        signal_summary["internal_tension"] += 1
        confidence_score += 0.05

    if match_any(["control", "micromanaged", "boxed in"]):
        signal_summary["control_orientation"] += 1
        confidence_score += 0.05

    if match_any(["trust myself", "own judgment"]):
        signal_summary["internal_reference"] += 1
        confidence_score += 0.05

    if match_any(["external validation", "reassurance"]):
        signal_summary["external_validation"] += 1
        confidence_score += 0.05

    if match_any(["deliberate", "take time", "think before acting"]):
        signal_summary["deliberative_decision_style"] += 1
        confidence_score += 0.05

    if match_any(["decisive", "act quickly"]):
        signal_summary["decisive_action_style"] += 1
        confidence_score += 0.05

    if match_any([
        "keep stress inside",
        "deal with it internally",
        "rarely vent",
        "hold it in",
        "process internally"
    ]):
        signal_summary["internal_pressure_regulation"] += 1
        confidence_score += 0.1

    if match_any(["talk it out", "vent", "let it out"]):
        signal_summary["external_pressure_release"] += 1
        confidence_score += 0.05

    # -------------------------
    # INSIGHTFUL LITE TRANSLATION (OPTION A)
    # -------------------------

    orientation_snapshot = (
        "Your responses suggest a person who carries responsibility internally and processes pressure quietly rather than outwardly. "
        "You tend to rely on your own judgment and internal calibration more than reassurance from others, which often allows you to stay "
        "composed even when demands increase. This self-contained style can create stability and clarity, but it may also mean that the effort "
        "you are exerting goes largely unseen. Overall, your pattern reflects internal strength, deliberate control, and a preference for "
        "handling complexity privately rather than reactively."
    )

    real_world_signals = [
        "You may appear calm or steady even when you are carrying significant internal responsibility.",
        "You often process stress internally before deciding whether it needs to be shared.",
        "Others may underestimate how much cognitive and emotional load you are managing."
    ]

    strengths = [
        "Strong internal self-regulation under pressure.",
        "Ability to remain aligned with your intentions without becoming reactive.",
        "High tolerance for responsibility and sustained focus."
    ]

    common_misinterpretations = [
        "This pattern can be mistaken for emotional distance or passivity.",
        "Your independence may be misread as not needing support."
    ]

    reflection_prompts = [
        "Notice when internal processing helps you stay grounded — and when it quietly increases strain.",
        "Consider which situations might benefit from selective sharing rather than full self-containment.",
        "Pay attention to early signals that pressure is accumulating beneath the surface."
    ]

    return {
        "engine_version": "PEK_LITE_INSIGHTFUL_A_V1",
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
        }
    }
