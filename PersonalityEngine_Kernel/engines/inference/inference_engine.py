# inference_engine.py
# Personality Engine Kernel — Lite
# Version: PEK_LITE_INSIGHTFUL_A_V2
# Layers 1–8 cumulative + Insight Enrichment
# Stable, non-recursive, ASGI-safe

from typing import Dict


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
    # MATCHING UTIL
    # -------------------------

    def match_any(phrases):
        return any(p in text for p in phrases)

    # -------------------------
    # CORE SIGNAL LAYERS (1–8)
    # -------------------------

    if match_any(["responsible", "holding everything", "managing outcomes"]):
        signal_summary["motivation"] += 1
        confidence_score += 0.05

    if match_any(["overthink", "replay", "mentally", "analyze"]):
        signal_summary["cognitive_load"] += 1
        confidence_score += 0.05

    if match_any(["stress", "pressure", "tension"]):
        signal_summary["internal_tension"] += 1
        confidence_score += 0.05

    if match_any(["control", "micromanaged", "boxed in"]):
        signal_summary["control_orientation"] += 1
        confidence_score += 0.05

    if match_any(["trust myself", "own judgment", "my call"]):
        signal_summary["internal_reference"] += 1
        confidence_score += 0.05

    if match_any(["validation", "reassurance", "approval"]):
        signal_summary["external_validation"] += 1
        confidence_score += 0.05

    if match_any(["deliberate", "take time", "think before acting"]):
        signal_summary["deliberative_decision_style"] += 1
        confidence_score += 0.05

    if match_any(["decisive", "act quickly", "move fast"]):
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
    # INSIGHT ENRICHMENT LAYERS
    # -------------------------

    pattern_clusters = []
    if signal_summary["motivation"] and signal_summary["internal_pressure_regulation"]:
        pattern_clusters.append(
            "High internal responsibility combined with self-contained pressure management."
        )
    if signal_summary["cognitive_load"] and signal_summary["deliberative_decision_style"]:
        pattern_clusters.append(
            "Tendency to process decisions deeply before committing to action."
        )

    tension_dynamics = []
    if signal_summary["internal_reference"] and signal_summary["external_validation"]:
        tension_dynamics.append(
            "Reliance on internal judgment coexists with moments of external validation seeking."
        )
    if signal_summary["control_orientation"] and signal_summary["trust_orientation"] == 0:
        tension_dynamics.append(
            "Strong need for control without an equivalent reliance on external trust."
        )

    operational_style = [
        "Processes complexity internally before engaging outwardly.",
        "Maintains composure under load by prioritizing internal regulation."
    ]

    silent_costs = []
    if signal_summary["internal_pressure_regulation"]:
        silent_costs.append(
            "Sustained internal pressure may accumulate without visible release."
        )
    if signal_summary["cognitive_load"]:
        silent_costs.append(
            "Extended mental processing can increase fatigue over time."
        )

    # -------------------------
    # LITE TRANSLATION (INSIGHTFUL)
    # -------------------------

    orientation_snapshot = (
        "Your responses suggest a person who carries responsibility internally and "
        "processes pressure quietly rather than outwardly. You rely strongly on your "
        "own judgment and internal calibration, which allows you to stay composed even "
        "as demands increase. This creates stability and clarity, though much of the "
        "effort you exert may go unseen by others."
    )

    real_world_signals = [
        "You often appear steady even while managing significant internal load.",
        "Stress is more likely to be processed privately than expressed outwardly.",
        "Others may underestimate the level of responsibility you carry."
    ]

    strengths = [
        "Strong internal self-regulation under pressure.",
        "Ability to remain deliberate rather than reactive.",
        "High tolerance for responsibility and sustained focus."
    ]

    common_misinterpretations = [
        "This pattern may be mistaken for emotional distance.",
        "Your independence can be misread as not needing support."
    ]

    reflection_prompts = [
        "Notice when internal processing supports clarity versus when it increases strain.",
        "Consider which situations might benefit from selective sharing.",
        "Pay attention to early signals of accumulating pressure."
    ]

    return {
        "engine_version": "PEK_LITE_INSIGHTFUL_A_V2",
        "kernel_output": {
            "confidence_score": round(confidence_score, 2),
            "signal_summary": signal_summary,
            "pattern_clusters": pattern_clusters,
            "tension_dynamics": tension_dynamics,
            "operational_style": operational_style,
            "silent_costs": silent_costs,
        },
        "lite_translation": {
            "orientation_snapshot": orientation_snapshot,
            "real_world_signals": real_world_signals,
            "strengths": strengths,
            "common_misinterpretations": common_misinterpretations,
            "reflection_prompts": reflection_prompts,
        }
    }
