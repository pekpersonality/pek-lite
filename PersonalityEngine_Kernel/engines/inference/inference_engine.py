# PersonalityEngine_Kernel/engines/inference/inference_engine.py
# PEK Lite inference engine (response-driven, non-echo, returns kernel_output + lite_translation)

from __future__ import annotations

from typing import List, Dict, Any, Optional


# -----------------------------
# Helpers
# -----------------------------

def _normalize_text(responses: List[str]) -> str:
    # Merge user responses into one internal paragraph for smoother analysis
    cleaned = []
    for r in responses:
        if not isinstance(r, str):
            continue
        s = " ".join(r.strip().split())
        if s:
            cleaned.append(s)
    return " ".join(cleaned).lower()


def _keyword_score(text: str, keywords: List[str], weight: float) -> tuple[float, list[str]]:
    score = 0.0
    evidence = []
    for k in keywords:
        if k in text:
            score += weight
            evidence.append(k)
    return score, evidence


def translate_lite(kernel_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lite translation rules:
    - observational, not prescriptive
    - avoids 'you should/need'
    - short, readable
    """

    conf = float(kernel_output.get("confidence_score", 0.0) or 0.0)
    coh = (kernel_output.get("identity_coherence") or {}).get("description", "") or ""
    dom = kernel_output.get("dominant_motive", "Unclear") or "Unclear"
    orient = kernel_output.get("global_orientation", "Unknown") or "Unknown"

    # Orientation snapshot
    if conf < 0.45:
        orientation_snapshot = (
            f"{coh} Confidence is currently low, which usually means the system needs more detail "
            "to sharpen the read."
        )
    else:
        orientation_snapshot = (
            f"Primary pattern reads as {dom.lower()} with a {orient.lower()} tilt. {coh}"
        )

    # Real-world signals (observational)
    signals: list[str] = []
    strengths: list[str] = []
    misreads: list[str] = []
    prompts: list[str] = []

    # Map based on motive/orientation
    if dom == "Autonomy / Exploration":
        signals += [
            "You may resist being boxed in, especially when rules feel arbitrary.",
            "You may move fast once you see the pattern, and feel friction when others don’t.",
            "Under pressure, you may pull away from control and look for space to think."
        ]
        strengths += [
            "High self-direction and internal drive when you choose the target.",
            "Pattern recognition that can compress complexity quickly.",
            "Strong intolerance for wasted motion or needless constraint."
        ]
        misreads += [
            "This pattern is often mistaken for being difficult or uncooperative.",
            "In reality, it reflects a need for autonomy and clean logic before committing energy."
        ]
        prompts += [
            "Notice what kinds of constraints feel energizing versus suffocating.",
            "Pay attention to when speed helps you lead — and when it creates avoidable friction."
        ]

    elif dom == "Stability Seeking":
        signals += [
            "You may feel calmer when structure is clear and expectations are stable.",
            "You may notice threats early and prefer to reduce uncertainty fast.",
            "Under pressure, you may seek order and predictability before taking action."
        ]
        strengths += [
            "Strong ability to create consistency and keep things running.",
            "Early detection of risk, drift, or hidden instability.",
            "Reliable follow-through when the plan is clear."
        ]
        misreads += [
            "This pattern is often mistaken for rigidity or control.",
            "In reality, it reflects a protective drive to reduce uncertainty and maintain stability."
        ]
        prompts += [
            "Notice what kinds of uncertainty reliably spike your stress.",
            "Track which structures actually help you feel freer, not tighter."
        ]

    else:
        # Low-confidence / unclear default (still useful, not diagnostic)
        signals += [
            "You may hesitate to act until things feel internally clearer or more certain.",
            "You may avoid engaging in conflict unless it feels unavoidable or especially meaningful.",
            "Under pressure, you may pull back and think quietly rather than react outwardly."
        ]
        strengths += [
            "Internally consistent motivation rather than contradictory or fragmented drives.",
            "Capacity to pause and reflect before acting instead of reacting impulsively.",
            "Tendency to preserve emotional energy by avoiding unnecessary confrontation."
        ]
        misreads += [
            "This pattern is often mistaken for indecision or lack of drive.",
            "In reality, it reflects a system that waits for internal alignment before committing energy."
        ]
        prompts += [
            "Notice what conditions tend to increase your sense of internal clarity versus uncertainty.",
            "Pay attention to moments when waiting helps you act more deliberately — and when it slows momentum."
        ]

    return {
        "orientation_snapshot": orientation_snapshot,
        "real_world_signals": signals[:5],
        "strengths": strengths[:5],
        "common_misinterpretations": misreads[:4],
        "reflection_prompts": prompts[:4],
    }


# -----------------------------
# Core Engine
# -----------------------------

class InferenceEngine:
    def __init__(self):
        self.version = "0.4.0"
        self.loaded = True

    def interpret(self, responses: List[str], context_flags: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        text = _normalize_text(responses)
        context_flags = context_flags or {}

        # Base result skeleton
        kernel_output: Dict[str, Any] = {
            "global_orientation": "Unknown",
            "dominant_motive": "Unclear",
            "confidence_score": 0.20,
            "core_motives": {
                "active_clusters": [],
                "evidence_summary": {},
                "motive_expressions": ""
            },
            "conflict_patterns": {},
            "stress_profile": {},
            "identity_structure": {},
            "identity_coherence": {
                "state": "coherent",
                "description": "Motivational structure appears internally consistent."
            }
        }

        # Simple keyword scoring across merged text
        stability_keywords = [
            "structure", "stability", "routine", "order", "predictable", "consistency", "plan", "clear expectations"
        ]
        autonomy_keywords = [
            "independent", "independence", "autonomy", "freedom", "space", "options", "choice", "explore",
            "micromanaged", "control", "boxed in", "restricted"
        ]
        drive_keywords = [
            "ambition", "driven", "standards", "high standards", "hold everything together", "responsible"
        ]
        uncertainty_keywords = [
            "overanalyze", "self-doubt", "uncertain", "oscillate", "second guess"
        ]

        stability_score, stability_ev = _keyword_score(text, stability_keywords, 1.2)
        autonomy_score, autonomy_ev = _keyword_score(text, autonomy_keywords, 1.2)
        drive_score, drive_ev = _keyword_score(text, drive_keywords, 1.0)
        uncertain_score, uncertain_ev = _keyword_score(text, uncertainty_keywords, 1.0)

        clusters = []

        if stability_score >= 2.4:
            clusters.append({
                "cluster": "stability_order",
                "label": "Stability / Structure Orientation",
                "score": stability_score,
                "evidence": stability_ev
            })

        if autonomy_score >= 2.4:
            clusters.append({
                "cluster": "autonomy_exploration",
                "label": "Autonomy / Exploration Orientation",
                "score": autonomy_score,
                "evidence": autonomy_ev
            })

        if drive_score >= 2.0:
            clusters.append({
                "cluster": "responsibility_drive",
                "label": "Responsibility / Standards Drive",
                "score": drive_score,
                "evidence": drive_ev
            })

        if uncertain_score >= 2.0:
            clusters.append({
                "cluster": "uncertainty_loop",
                "label": "Uncertainty / Analysis Loop",
                "score": uncertain_score,
                "evidence": uncertain_ev
            })

        kernel_output["core_motives"]["active_clusters"] = clusters

        # Decide dominant motive
        # (Lite rule: keep it simple, no overreach)
        if autonomy_score > stability_score and autonomy_score >= 2.4:
            kernel_output["dominant_motive"] = "Autonomy / Exploration"
            kernel_output["global_orientation"] = "Constraint Sensitivity"
            kernel_output["confidence_score"] = 0.70 if len(text.split()) >= 60 else 0.55
            kernel_output["identity_structure"] = {"state": "single-drive", "orientation_axis": "Autonomy / Exploration"}

        elif stability_score >= 2.4:
            kernel_output["dominant_motive"] = "Stability Seeking"
            kernel_output["global_orientation"] = "Threat Sensitivity"
            kernel_output["confidence_score"] = 0.70 if len(text.split()) >= 60 else 0.55
            kernel_output["identity_structure"] = {"state": "single-drive", "orientation_axis": "Stability / Structure"}

        # Coherence
        if len(clusters) <= 2:
            kernel_output["identity_coherence"] = {
                "state": "coherent",
                "description": "Motivational structure appears internally consistent."
            }
        else:
            kernel_output["identity_coherence"] = {
                "state": "complex-but-stable",
                "description": "Multiple motivational layers are present but remain integrated."
            }

        return {
            "kernel_output": kernel_output,
            "lite_translation": translate_lite(kernel_output)
        }


# -----------------------------
# Public API
# -----------------------------

def run_inference(
    responses: List[str],
    context_flags: Optional[Dict[str, Any]] = None,
    forced_overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    # forced_overrides reserved for later; ignored safely for Lite
    engine = InferenceEngine()
    return engine.interpret(responses=responses, context_flags=context_flags or {})
