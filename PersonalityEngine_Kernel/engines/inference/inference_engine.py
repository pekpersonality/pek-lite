# inference_engine.py
# PEK Lite — Inference Engine v0.5
# Layers:
# 1) Motivational Structure
# 2) Internal Tension Patterns

from typing import List, Dict


def run_inference(
    responses: List[str],
    context_flags: Dict = None,
    forced_overrides: Dict = None
) -> Dict:

    text = " ".join(responses).lower()

    # -----------------------------
    # BASE KERNEL OUTPUT
    # -----------------------------

    kernel_output = {
        "confidence_score": 0.3,
        "signal_summary": {
            "responsibility": 0,
            "autonomy": 0,
            "cognitive_load": 0,
            "internal_tension": 0
        }
    }

    lite = {
        "orientation_snapshot": "",
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": []
    }

    # -----------------------------
    # LAYER 1 — MOTIVATIONAL STRUCTURE
    # -----------------------------

    responsibility_markers = [
        "responsible", "holding everything together", "on me",
        "pressure", "expectations", "standards", "hard on myself"
    ]

    autonomy_markers = [
        "independent", "micromanaged", "freedom",
        "control", "own way", "autonomy"
    ]

    cognitive_markers = [
        "overthink", "overanalyze", "second guess",
        "doubt", "replay", "loop"
    ]

    for m in responsibility_markers:
        if m in text:
            kernel_output["signal_summary"]["responsibility"] += 1

    for m in autonomy_markers:
        if m in text:
            kernel_output["signal_summary"]["autonomy"] += 1

    for m in cognitive_markers:
        if m in text:
            kernel_output["signal_summary"]["cognitive_load"] += 1

    # -----------------------------
    # LAYER 2 — INTERNAL TENSION
    # -----------------------------

    tension_markers = [
        "oscillate", "conflicted", "torn",
        "push myself", "never enough",
        "self doubt", "pressure", "mental strain"
    ]

    for m in tension_markers:
        if m in text:
            kernel_output["signal_summary"]["internal_tension"] += 1

    # -----------------------------
    # LITE TRANSLATION (OBSERVATIONAL)
    # -----------------------------

    if kernel_output["signal_summary"]["internal_tension"] > 0:
        lite["orientation_snapshot"] = (
            "You appear to carry a meaningful amount of internal pressure. "
            "Your system tends to hold competing demands simultaneously, "
            "which can create mental strain even when external conditions are stable."
        )

        lite["real_world_signals"].extend([
            "You may feel internally busy even during periods of outward calm.",
            "Decision-making can feel heavier than it looks from the outside."
        ])

        lite["strengths"].extend([
            "High internal standards that drive depth and seriousness.",
            "Strong capacity to self-monitor and reflect."
        ])

        lite["common_misinterpretations"].extend([
            "This pattern is often mistaken for indecision or emotional volatility.",
            "In reality, it reflects internal load rather than lack of clarity."
        ])

        lite["reflection_prompts"].extend([
            "Notice when internal pressure is helping focus versus creating drag.",
            "Pay attention to moments when easing self-expectations improves momentum."
        ])

        kernel_output["confidence_score"] = 0.6

    else:
        lite["orientation_snapshot"] = (
            "Your motivational structure appears internally consistent, "
            "with relatively low internal friction at this time."
        )

        lite["real_world_signals"].append(
            "You may experience periods of clarity where decisions feel straightforward."
        )

        lite["strengths"].append(
            "Capacity to maintain internal alignment without excessive strain."
        )

        lite["common_misinterpretations"].append(
            "This can be mistaken for passivity, when it often reflects steadiness."
        )

        lite["reflection_prompts"].append(
            "Notice what conditions help you preserve this sense of internal ease."
        )

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------

    return {
        "kernel_output": kernel_output,
        "lite_translation": lite
    }
