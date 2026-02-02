# inference_engine.py
# PEK Lite — Inference Engine (Layers 1–7)

from typing import List, Dict


class InferenceEngine:
    def __init__(self):
        self.version = "0.7.0"

    def interpret(self, responses: List[str]) -> Dict:
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
            "external_validation": 0,
            "internal_reference": 0,
            # Layer 7
            "deliberative_decision_style": 0,
            "decisive_action_style": 0,
        }

        lite = {
            "orientation_snapshot": "",
            "real_world_signals": [],
            "strengths": [],
            "common_misinterpretations": [],
            "reflection_prompts": []
        }

        confidence_score = 0.3

        # -----------------------------
        # LAYER 7 — DECISIONAL STYLE
        # -----------------------------
        deliberative_markers = [
            "overanalyze", "think it through", "need clarity",
            "weigh options", "sit with", "process before acting",
            "hesitate", "double check"
        ]

        decisive_markers = [
            "act quickly", "decide fast", "jump in",
            "figure it out later", "move forward",
            "take action immediately"
        ]

        for phrase in deliberative_markers:
            if phrase in text:
                signal_summary["deliberative_decision_style"] += 1

        for phrase in decisive_markers:
            if phrase in text:
                signal_summary["decisive_action_style"] += 1

        # -----------------------------
        # Lite Translation — Layer 7
        # -----------------------------
        if signal_summary["deliberative_decision_style"] > signal_summary["decisive_action_style"]:
            lite["real_world_signals"].append(
                "You tend to move toward decisions after internal processing rather than immediate action."
            )
            lite["strengths"].append(
                "Decisions are often well-considered rather than impulsive."
            )
            lite["common_misinterpretations"].append(
                "This can be mistaken for hesitation, when it often reflects care and depth."
            )
            lite["reflection_prompts"].append(
                "Notice when deliberation improves outcomes — and when it slows momentum."
            )

        elif signal_summary["decisive_action_style"] > signal_summary["deliberative_decision_style"]:
            lite["real_world_signals"].append(
                "You often act quickly and refine direction as you go."
            )
            lite["strengths"].append(
                "Ability to create momentum and adapt in real time."
            )
            lite["common_misinterpretations"].append(
                "This can be mistaken for recklessness, when it often reflects confidence."
            )
            lite["reflection_prompts"].append(
                "Notice when quick action serves you — and when pause might add clarity."
            )

        # -----------------------------
        # Orientation Snapshot (fallback-safe)
        # -----------------------------
        lite["orientation_snapshot"] = (
            "Your motivational structure appears internally consistent, "
            "with relatively low internal friction at this time."
        )

        return {
            "kernel_output": {
                "confidence_score": confidence_score,
                "signal_summary": signal_summary
            },
            "lite_translation": lite
        }


def run_inference(responses: List[str], **kwargs) -> Dict:
    engine = InferenceEngine()
    return engine.interpret(responses)
