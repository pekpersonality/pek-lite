# inference_engine.py
# Core inference logic for the Personality Engine Kernel (PEK)

class InferenceEngine:
    def __init__(self):
        self.version = "0.3.1"
        self.loaded = True

    def interpret(self, user_input: dict) -> dict:
        statement = user_input.get("example_statement", "").lower()

        # ----------------------------------------------------------
        # Base result skeleton
        # ----------------------------------------------------------
        result = {
            "global_orientation": None,
            "dominant_motive": None,
            "confidence_score": 0.0,
            "core_motives": {
                "active_clusters": [],
                "evidence_summary": {},
                "motive_expressions": ""
            },
            "conflict_patterns": {},
            "stress_profile": {},
            "identity_structure": {},
            "identity_coherence": {}
        }

        # ----------------------------------------------------------
        # RULESET 0.1 — Stability / Structure (Active)
        # ----------------------------------------------------------
        stability_words = [
            "structure", "stability", "routine", "order",
            "predictable", "consistency", "daily routine"
        ]

        stability_score = 0.0
        stability_evidence = []

        for word in stability_words:
            if word in statement:
                stability_score += 1.5
                stability_evidence.append(word)

        if stability_score >= 3.0:
            result["global_orientation"] = "High Threat Sensitivity"
            result["dominant_motive"] = "Stability Seeking"
            result["confidence_score"] = 0.90

            result["core_motives"]["active_clusters"].append({
                "cluster": "stability_order",
                "label": "Stability / Structure Orientation",
                "score": stability_score,
                "evidence": stability_evidence
            })

            result["identity_structure"] = {
                "state": "single-drive",
                "orientation_axis": "Stability / Structure"
            }

        # ----------------------------------------------------------
        # RULESET 0.2.1 — Autonomy / Exploration (Active)
        # ----------------------------------------------------------
        autonomy_words = [
            "freedom", "free", "explore", "exploration", "independent",
            "autonomy", "choice", "options", "open", "adventure",
            "novelty", "growth"
        ]

        constraint_words = [
            "trapped", "confined", "restricted", "boxed in",
            "stuck", "limited", "suffocated"
        ]

        autonomy_score = 0.0
        autonomy_evidence = []

        for word in autonomy_words:
            if word in statement:
                autonomy_score += 1.0
                autonomy_evidence.append(word)

        for word in constraint_words:
            if word in statement:
                autonomy_score += 1.5
                autonomy_evidence.append(word)

        if autonomy_score >= 2.0:
            result["core_motives"]["active_clusters"].append({
                "cluster": "autonomy_exploration",
                "label": "Autonomy / Exploration Orientation",
                "score": autonomy_score,
                "evidence": autonomy_evidence
            })

            if result.get("identity_structure", {}).get("state") == "single-drive":
                result["identity_structure"] = {
                    "state": "dual-axis",
                    "orientation_axes": [
                        "Stability / Structure",
                        "Autonomy / Exploration"
                    ],
                    "description": (
                        "A stable base coexists with a strong desire for autonomy, "
                        "freedom, and exploration."
                    )
                }

            result["confidence_score"] = min(
                result.get("confidence_score", 0.85) + 0.03,
                0.97
            )

        # ----------------------------------------------------------
        # RULESET 0.3.1 — Latent / Aspirational Stability Anchor
        # ----------------------------------------------------------
        aspirational_stability_phrases = [
            "crave stability", "want stability", "need stability",
            "looking for stability", "seeking stability",
            "need a base", "need grounding", "want structure"
        ]

        latent_stability_detected = any(
            phrase in statement for phrase in aspirational_stability_phrases
        )

        if latent_stability_detected:
            result["core_motives"]["active_clusters"].append({
                "cluster": "latent_stability_anchor",
                "label": "Aspirational Stability Anchor",
                "score": 1.5,
                "evidence": ["expressed desire for grounding or stability"]
            })

            result["core_motives"]["motive_expressions"] += (
                " Stability appears as a desired anchor rather than a current constraint."
            )

        # ----------------------------------------------------------
        # INTERPRETIVE POLISH — Human-Safe Narrative
        # ----------------------------------------------------------
        notes = []

        clusters = [c["cluster"] for c in result["core_motives"]["active_clusters"]]

        if "autonomy_exploration" in clusters:
            notes.append(
                "A desire for autonomy does not imply avoidance or instability. "
                "It often reflects a healthy need for growth, space, or self-directed experience."
            )

        if "latent_stability_anchor" in clusters:
            notes.append(
                "Wanting stability can reflect a healthy search for grounding — "
                "a safe base that supports exploration rather than limits it."
            )

        if "stability_order" in clusters:
            notes.append(
                "A preference for structure and predictability often serves as an emotional anchor, "
                "supporting resilience and long-term engagement."
            )

        if notes:
            result["interpretive_summary"] = " ".join(notes)

        # ----------------------------------------------------------
        # COHERENCE ASSESSMENT
        # ----------------------------------------------------------
        if len(clusters) <= 2:
            result["identity_coherence"] = {
                "state": "coherent",
                "description": "Motivational structure appears internally consistent."
            }
        else:
            result["identity_coherence"] = {
                "state": "complex-but-stable",
                "description": "Multiple motivational layers are present but remain integrated."
            }

        # ----------------------------------------------------------
        # DEFAULT CASE
        # ----------------------------------------------------------
        if result["global_orientation"] is None:
            result["global_orientation"] = "Unknown"
            result["dominant_motive"] = "Unclear"
            result["confidence_score"] = 0.2

        return result


def run_inference(user_input: dict):
    engine = InferenceEngine()
    return engine.interpret(user_input)
