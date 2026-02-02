# inference_engine.py
# Core inference logic for the Personality Engine Kernel (PEK)

class InferenceEngine:
    def __init__(self):
        self.version = "0.3.2"
        self.loaded = True

    def interpret(self, responses: list[str]) -> dict:
        # ----------------------------------------------------------
        # Merge all user responses into a single analyzable statement
        # ----------------------------------------------------------
        statement = " ".join(responses).lower()

        # ----------------------------------------------------------
        # Base result skeleton
        # ----------------------------------------------------------
        result = {
            "global_orientation": "Unknown",
            "dominant_motive": "Unclear",
            "confidence_score": 0.2,
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

        # ----------------------------------------------------------
        # RULESET — Autonomy / Control / Responsibility
        # ----------------------------------------------------------
        autonomy_signals = [
            "independent", "freedom", "control", "micromanaged",
            "responsible", "holding everything together",
            "clarity", "standards"
        ]

        autonomy_hits = [w for w in autonomy_signals if w in statement]

        if autonomy_hits:
            result["global_orientation"] = "Self-directed"
            result["dominant_motive"] = "Autonomy with responsibility"
            result["confidence_score"] = min(0.85, 0.4 + (0.1 * len(autonomy_hits)))

            result["core_motives"]["active_clusters"].append({
                "cluster": "autonomy_responsibility",
                "label": "Autonomy / Responsibility Pattern",
                "score": len(autonomy_hits),
                "evidence": autonomy_hits
            })

        return result


def run_inference(responses: list[str]) -> dict:
    engine = InferenceEngine()
    return engine.interpret(responses)
