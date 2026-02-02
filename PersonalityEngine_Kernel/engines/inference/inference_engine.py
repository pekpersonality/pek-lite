# inference_engine.py
# PEK Lite — Layered inference engine (Layers 1–3)

from typing import List, Dict


def run_inference(
    responses: List[str],
    context_flags: Dict | None = None,
    forced_overrides: Dict | None = None
) -> Dict:

    text = " ".join(responses).lower()

    # -----------------------------
    # SIGNAL INITIALIZATION
    # -----------------------------
    signals = {
        "motivation": 0,
        "cognitive_load": 0,
        "internal_tension": 0
    }

    # -----------------------------
    # LAYER 1 — MOTIVATIONAL STRUCTURE
    # -----------------------------
    motivation_keywords = [
        "drive", "goal", "purpose", "standard", "expectation",
        "independent", "autonomy", "control", "clarity"
    ]

    for word in motivation_keywords:
        if word in text:
            signals["motivation"] += 1

    # -----------------------------
    # LAYER 2 — COGNITIVE LOAD / OVERANALYSIS
    # -----------------------------
    cognitive_keywords = [
        "overthink", "analyze", "replay", "second guess",
        "mental", "loop", "exhausted", "can't stop thinking"
    ]

    for word in cognitive_keywords:
        if word in text:
            signals["cognitive_load"] += 1

    # -----------------------------
    # LAYER 3 — INTERNAL TENSION / RESPONSIBILITY LOAD
    # -----------------------------
    tension_keywords = [
        "holding everything together",
        "responsible for",
        "carry the weight",
        "pressure",
        "expectations",
        "hard on myself",
        "self doubt",
        "let people down",
        "burden",
        "on me"
    ]

    for phrase in tension_keywords:
        if phrase in text:
            signals["internal_tension"] += 1

    # -----------------------------
    # CONFIDENCE SCORE (Lite-scale)
    # -----------------------------
    total_signal = sum(signals.values())

    if total_signal == 0:
        confidence = 0.3
    elif total_signal <= 2:
        confidence = 0.45
    elif total_signal <= 4:
        confidence = 0.6
    else:
        confidence = 0.75

    # -----------------------------
    # LITE TRANSLATION (OBSERVATIONAL)
    # -----------------------------
    orientation_snapshot = (
        "Your motivational structure appears internally consistent, "
        "with moderate internal pressure shaping how you engage with decisions."
        if signals["internal_tension"] > 0 else
        "Your motivational structure appears internally consistent, "
        "with relatively low internal friction at this time."
    )

    real_world_signals = []

    if signals["cognitive_load"] > 0:
        real_world_signals.append(
            "You may find yourself revisiting decisions internally, even after they’re made."
        )

    if signals["internal_tension"] > 0:
        real_world_signals.append(
            "You may take on more responsibility internally than others realize."
        )

    strengths = []

    if signals["motivation"] > 0:
        strengths.append(
            "Strong internal standards and self-direction."
        )

    if signals["internal_tension"] > 0:
        strengths.append(
            "High reliability and capacity to carry responsibility under pressure."
        )

    common_misinterpretations = []

    if signals["internal_tension"] > 0:
        common_misinterpretations.append(
            "This pattern can be mistaken for emotional distance, when it often reflects containment."
        )

    reflection_prompts = [
        "Notice what situations tend to increase internal pressure versus internal clarity."
    ]

    # -----------------------------
    # OUTPUT
    # -----------------------------
    return {
        "kernel_output": {
            "confidence_score": confidence,
            "signal_summary": signals
        },
        "lite_translation": {
            "orientation_snapshot": orientation_snapshot,
            "real_world_signals": real_world_signals,
            "strengths": strengths,
            "common_misinterpretations": common_misinterpretations,
            "reflection_prompts": reflection_prompts
        }
    }
