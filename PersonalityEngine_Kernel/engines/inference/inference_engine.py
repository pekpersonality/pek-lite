"""
PEK Lite — Inference Engine v0.4
More expressive, observational-only inference.
No advice language. Pattern description only.
"""

from typing import List, Dict


def run_inference(
    responses: List[str],
    context_flags: Dict | None = None,
    forced_overrides: Dict | None = None
) -> Dict:
    text = " ".join(responses).lower()

    # -----------------------------
    # SIGNAL BUCKETS (expressive)
    # -----------------------------

    responsibility_signals = [
        "responsible", "holding everything together", "hard on myself",
        "pressure", "expectations", "burden", "carry", "weight",
        "overanalyze", "overthinking", "self-doubt", "standards"
    ]

    autonomy_signals = [
        "independent", "micromanaged", "freedom", "control",
        "clarity", "own decisions"
    ]

    cognitive_load_signals = [
        "patterns", "analyze", "thinking", "clarity",
        "notice", "understand", "explain"
    ]

    # -----------------------------
    # SCORE ACCUMULATION
    # -----------------------------

    scores = {
        "responsibility": 0,
        "autonomy": 0,
        "cognitive_load": 0
    }

    for word in responsibility_signals:
        if word in text:
            scores["responsibility"] += 1

    for word in autonomy_signals:
        if word in text:
            scores["autonomy"] += 1

    for word in cognitive_load_signals:
        if word in text:
            scores["cognitive_load"] += 1

    # -----------------------------
    # LITE TRANSLATION (OUTPUT)
    # -----------------------------

    lite_translation = {
        "orientation_snapshot": "",
        "real_world_signals": [],
        "strengths": [],
        "common_misinterpretations": [],
        "reflection_prompts": []
    }

    # RESPONSIBILITY / SELF-PRESSURE CLUSTER
    if scores["responsibility"] >= 2:
        lite_translation["orientation_snapshot"] = (
            "Your responses suggest a strong internal sense of responsibility. "
            "You tend to carry ownership for outcomes, often holding yourself "
            "to high internal standards."
        )

        lite_translation["real_world_signals"].extend([
            "You may feel like the stabilizing force in uncertain situations.",
            "You often internalize pressure rather than expressing it outwardly.",
            "You tend to evaluate yourself more critically than others do."
        ])

        lite_translation["strengths"].extend([
            "Reliability under pressure.",
            "Strong internal accountability.",
            "Ability to sustain effort without external validation."
        ])

        lite_translation["common_misinterpretations"].extend([
            "This pattern can be mistaken for rigidity or self-doubt.",
            "In reality, it reflects internal discipline and responsibility."
        ])

        lite_translation["reflection_prompts"].extend([
            "Notice when responsibility energizes you versus when it becomes heavy.",
            "Pay attention to how often you assume ownership by default."
        ])

    # AUTONOMY OVERLAY
    if scores["autonomy"] >= 1:
        lite_translation["real_world_signals"].append(
            "You appear sensitive to unnecessary constraint or micromanagement."
        )

        lite_translation["strengths"].append(
            "Clear internal boundaries around autonomy and self-direction."
        )

    # COGNITIVE LOAD OVERLAY
    if scores["cognitive_load"] >= 2:
        lite_translation["orientation_snapshot"] += (
            " You process experiences through analysis and pattern recognition, "
            "often thinking several steps ahead."
        )

        lite_translation["common_misinterpretations"].append(
            "This analytical style is sometimes mistaken for indecision."
        )

    # FALLBACK (still valid, not an error)
    if lite_translation["orientation_snapshot"] == "":
        lite_translation["orientation_snapshot"] = (
            "Motivational structure appears internally consistent. "
            "Confidence is currently low, which usually means the system "
            "needs more detail to sharpen the read."
        )

        lite_translation["real_world_signals"] = [
            "You may hesitate to act until things feel internally clearer.",
            "You may avoid conflict unless it feels especially meaningful."
        ]

        lite_translation["strengths"] = [
            "Internal consistency rather than impulsive action."
        ]

        lite_translation["common_misinterpretations"] = [
            "This can be mistaken for indecision."
        ]

        lite_translation["reflection_prompts"] = [
            "Notice what increases internal clarity for you."
        ]

    # -----------------------------
    # FINAL STRUCTURE
    # -----------------------------

    return {
        "kernel_output": {
            "confidence_score": round(
                min(0.9, 0.3 + (sum(scores.values()) * 0.1)), 2
            ),
            "signal_summary": scores
        },
        "lite_translation": lite_translation
    }
