# inference_engine.py
# PersonaSight (PEK Lite) — Insightful Dynamic Narrative
# Version: PEK_LITE_INSIGHTFUL_DYNAMIC_V3
# Layers 1–8 cumulative + deterministic narrative assembly
# Stable, non-recursive, ASGI-safe, no external deps
print("INFERENCE ENGINE LOADED FROM:", __file__)
from typing import Dict, List
import hashlib


def run_inference(engine_input: dict):
    raw_text = engine_input.get("example_statement", "") or ""
    text = raw_text.lower()

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

    confidence_score = 0.30

    # -------------------------
    # MATCHING UTIL
    # -------------------------
    def match_any(phrases: List[str]) -> bool:
        return any(p in text for p in phrases)

    # -------------------------
    # CORE SIGNAL LAYERS (1–8)
    # -------------------------
    if match_any(["responsible", "holding everything", "managing outcomes", "depends on me", "on my shoulders"]):
        signal_summary["motivation"] += 1
        confidence_score += 0.06

    if match_any(["overthink", "replay", "mentally", "analyze", "loop", "second-guess"]):
        signal_summary["cognitive_load"] += 1
        confidence_score += 0.06

    if match_any(["stress", "pressure", "tension", "overwhelmed", "on edge"]):
        signal_summary["internal_tension"] += 1
        confidence_score += 0.06

    if match_any(["control", "micromanaged", "boxed in", "forced", "trapped"]):
        signal_summary["control_orientation"] += 1
        confidence_score += 0.06

    if match_any(["trust myself", "own judgment", "my call", "i decide", "i know what i know"]):
        signal_summary["internal_reference"] += 1
        confidence_score += 0.06

    if match_any(["validation", "reassurance", "approval", "what do they think", "need confirmation"]):
        signal_summary["external_validation"] += 1
        confidence_score += 0.06

    if match_any(["deliberate", "take time", "think before acting", "weigh it", "consider outcomes"]):
        signal_summary["deliberative_decision_style"] += 1
        confidence_score += 0.06

    if match_any(["decisive", "act quickly", "move fast", "no time", "immediate"]):
        signal_summary["decisive_action_style"] += 1
        confidence_score += 0.06

    if match_any([
        "keep stress inside",
        "deal with it internally",
        "rarely vent",
        "hold it in",
        "process internally",
        "i isolate",
        "i shut down"
    ]):
        signal_summary["internal_pressure_regulation"] += 1
        confidence_score += 0.10

    if match_any(["talk it out", "vent", "let it out", "release it", "get it out", "i rant"]):
        signal_summary["external_pressure_release"] += 1
        confidence_score += 0.06

    # -------------------------
    # DETERMINISTIC VARIATION PICKER
    # (No randomness; same inputs => same wording)
    # -------------------------
    def pick(options: List[str], salt: str) -> str:
        base = (raw_text + "|" + salt).encode("utf-8", errors="ignore")
        h = hashlib.sha256(base).hexdigest()
        idx = int(h[:8], 16) % len(options)
        return options[idx]

    # -------------------------
    # CLUSTER / DYNAMICS
    # -------------------------
    fired = {k: v for k, v in signal_summary.items() if v > 0}
    fired_count = len(fired)

    # simple “signal weight” feel (still not shown to user)
    if fired_count >= 6:
        confidence_score += 0.10
    elif fired_count >= 4:
        confidence_score += 0.06
    elif fired_count >= 2:
        confidence_score += 0.03

    confidence_score = min(confidence_score, 0.95)

    # narrative flags
    has_resp = signal_summary["motivation"] > 0
    has_load = signal_summary["cognitive_load"] > 0
    has_tension = signal_summary["internal_tension"] > 0
    has_control = signal_summary["control_orientation"] > 0
    has_internal_ref = signal_summary["internal_reference"] > 0
    has_ext_val = signal_summary["external_validation"] > 0
    has_delib = signal_summary["deliberative_decision_style"] > 0
    has_decisive = signal_summary["decisive_action_style"] > 0
    has_internal_reg = signal_summary["internal_pressure_regulation"] > 0
    has_external_release = signal_summary["external_pressure_release"] > 0

    # -------------------------
    # PATTERN CLUSTERS (internal)
    # -------------------------
    pattern_clusters = []
    if has_resp and has_internal_reg:
        pattern_clusters.append("High responsibility paired with self-contained pressure management.")
    if has_load and has_delib:
        pattern_clusters.append("Deep cognitive processing and deliberation before action.")
    if has_control and has_tension:
        pattern_clusters.append("Control sensitivity increases internal tension under constraint.")
    if has_internal_ref and has_ext_val:
        pattern_clusters.append("Internal judgment is primary, with occasional external confirmation seeking.")

    tension_dynamics = []
    if has_internal_ref and has_ext_val:
        tension_dynamics.append("Internal authority is strong, but reassurance-seeking appears in high-stakes moments.")
    if has_control and not has_external_release and has_internal_reg:
        tension_dynamics.append("Constraint triggers inward compression rather than outward discharge.")
    if has_load and has_tension:
        tension_dynamics.append("Mental looping amplifies internal pressure during uncertainty.")

    operational_style = []
    if has_delib and not has_decisive:
        operational_style.append("Prefers forethought, sequencing, and internal clarity before outward moves.")
    if has_decisive and not has_delib:
        operational_style.append("Prefers rapid closure and forward motion once a path is chosen.")
    if has_internal_reg:
        operational_style.append("Maintains outward stability by containing pressure internally.")
    if has_external_release:
        operational_style.append("Relieves pressure through expression and external processing.")

    silent_costs = []
    if has_internal_reg:
        silent_costs.append("Internal pressure can accumulate quietly if it isn’t periodically discharged.")
    if has_load:
        silent_costs.append("Extended mental processing can create fatigue or delay closure.")
    if has_control:
        silent_costs.append("Being boxed in can trigger disproportionate irritation or shutdown over time.")

    # -------------------------
    # DYNAMIC NARRATIVE ASSEMBLY
    # -------------------------

    # 1) Orientation Snapshot (top paragraph)
    openers = [
        "Your responses point to a self-contained style of handling pressure.",
        "Your answers describe an internal-first way of navigating responsibility and stress.",
        "Your responses suggest you carry a lot privately before you show anything outwardly.",
        "Your answers indicate a steady exterior that’s often supported by intense internal processing."
    ]

    anchors = []
    if has_resp:
        anchors.append(pick([
            "When outcomes depend on you, you tend to absorb that responsibility rather than offload it.",
            "You seem to default into ownership when something matters, even when no one asked you to.",
            "Responsibility lands internally first, as if you automatically become the stabilizer."
        ], "anchor_resp"))

    if has_load:
        anchors.append(pick([
            "You also appear to run scenarios in your head, replaying details to reduce uncertainty.",
            "There’s a clear cognitive load signature here: analysis, looping, and mental rehearsal.",
            "Your mind seems to keep processing after the moment is over, tightening the loop until it feels resolved."
        ], "anchor_load"))

    if has_internal_reg:
        anchors.append(pick([
            "Instead of venting early, you tend to contain pressure and regulate quietly.",
            "Your default release valve looks internal: you compress, stabilize, and keep going.",
            "You often hold it in long enough that other people may not realize what you’re carrying."
        ], "anchor_internal_reg"))

    if has_control:
        anchors.append(pick([
            "When you feel boxed in or controlled, the system reacts fast and sharply.",
            "Constraint and micromanagement appear to trigger a strong internal resistance response.",
            "Autonomy matters here: forced situations tend to spike irritation and tighten your internal state."
        ], "anchor_control"))

    if has_internal_ref:
        anchors.append(pick([
            "You rely heavily on your own judgment as the primary reference point.",
            "Your internal compass seems to matter more than consensus.",
            "You orient around your own calibration and tend to trust your read of reality."
        ], "anchor_internal_ref"))

    if has_ext_val:
        anchors.append(pick([
            "At the same time, there are hints that reassurance can matter in certain moments.",
            "External confirmation appears relevant at least some of the time, especially under pressure.",
            "You may occasionally seek validation, not from weakness, but to confirm you’re not missing something."
        ], "anchor_ext_val"))

    closer_pool = [
        "Overall, this points to internal strength and composure, with the main risk being that your load becomes invisible until it’s heavy.",
        "Overall, this is a stable pattern, but it can become costly if pressure builds with no outlet or acknowledgment.",
        "Overall, you look resilient and deliberate, but the hidden cost is quiet accumulation when you keep too much inside."
    ]
    opener = pick(openers, "orientation_opener")
    closer = pick(closer_pool, "orientation_closer")

    # Keep the top paragraph premium but not huge:
    # opener + up to 2–3 strongest anchors + closer
    selected_anchors = anchors[:3] if len(anchors) >= 3 else anchors
    orientation_snapshot = " ".join([opener] + selected_anchors + [closer]).strip()

    # 2) Underlying Behavioral Patterns (dynamic paragraph)
    patterns_bits = []
    if has_resp:
        patterns_bits.append(pick([
            "Responsibility is treated like an internal contract rather than a shared burden.",
            "You show a high ownership posture: you naturally take the wheel when stakes rise."
        ], "pat_resp"))
    if has_internal_ref:
        patterns_bits.append(pick([
            "Your decision compass is internally anchored, which often produces consistency and self-trust.",
            "You calibrate from the inside out, which helps you stay aligned even in noisy environments."
        ], "pat_internal_ref"))
    if has_ext_val:
        patterns_bits.append(pick([
            "External feedback still has influence, but more as a signal-check than a steering wheel.",
            "Reassurance appears as a secondary input, not the primary driver."
        ], "pat_ext_val"))

    if not patterns_bits:
        patterns_bits.append(pick([
            "Your responses suggest a generally steady self-regulation style with moderate sensitivity to stress cues.",
            "Your answers show a balanced baseline: you respond to pressure, but you don’t broadcast it dramatically."
        ], "pat_fallback"))

    underlying_patterns = " ".join(patterns_bits).strip()

    # 3) Internal Dynamics & Pressure Flow (dynamic paragraph)
    pressure_bits = []
    if has_load and has_tension:
        pressure_bits.append(pick([
            "When pressure rises, the mind tends to stay active, which can intensify internal tension over time.",
            "Stress seems to recruit thought loops, making tension feel like it’s living in the background."
        ], "press_load_tension"))
    if has_internal_reg and not has_external_release:
        pressure_bits.append(pick([
            "Release is mostly private, which preserves composure but can delay relief.",
            "You’re built for containment, but that means relief sometimes arrives late."
        ], "press_internal_only"))
    if has_external_release:
        pressure_bits.append(pick([
            "You do have an external outlet at times, which can prevent long-term buildup when you actually use it.",
            "Expression and discharge appear available to you, and when used, they likely reduce the hidden load."
        ], "press_external_release"))

    if not pressure_bits:
        pressure_bits.append(pick([
            "Pressure appears manageable, with mild internalization and a generally stable regulation style.",
            "Your pressure flow looks steady: you process it, stabilize, then move forward without much drama."
        ], "press_fallback"))

    internal_dynamics = " ".join(pressure_bits).strip()

    # 4) Decision & Control Style (dynamic paragraph)
    decision_bits = []
    if has_delib and not has_decisive:
        decision_bits.append(pick([
            "You tend to build internal clarity first, then act once the path feels clean.",
            "Your process favors forethought: you run the sequence before you move."
        ], "dec_delib"))
    if has_decisive and not has_delib:
        decision_bits.append(pick([
            "Once you choose a direction, you prefer momentum and quick execution.",
            "You favor closure and action once a decision crystallizes."
        ], "dec_decisive"))
    if has_control:
        decision_bits.append(pick([
            "Autonomy is a key stabilizer for you; forced constraints disrupt your internal rhythm.",
            "Control sensitivity shows up strongest when the environment tries to dictate your moves."
        ], "dec_control"))
    if not decision_bits:
        decision_bits.append(pick([
            "Your decision style looks balanced: enough thought to stay aligned, enough action to keep moving.",
            "You appear to alternate between internal evaluation and execution depending on the stakes."
        ], "dec_fallback"))

    decision_control = " ".join(decision_bits).strip()

    # -------------------------
    # DYNAMIC BULLETS (still curated)
    # -------------------------
    real_world_signals = []
    if has_internal_reg:
        real_world_signals.append(pick([
            "You may look calm while carrying more internally than people realize.",
            "You often appear steady even when the internal load is high."
        ], "rws_internal_reg"))
    if has_load:
        real_world_signals.append(pick([
            "You may replay decisions after the fact, looking for the cleanest interpretation.",
            "You may mentally revisit events to reduce uncertainty or regret."
        ], "rws_load"))
    if has_control:
        real_world_signals.append(pick([
            "When you feel boxed in, your patience can drop quickly.",
            "Constraint tends to trigger irritation, urgency, or withdrawal."
        ], "rws_control"))
    if not real_world_signals:
        real_world_signals = [
            "You tend to maintain a stable outward presence across changing demands.",
            "You prefer to process internally before sharing externally."
        ]

    strengths = []
    if has_internal_ref:
        strengths.append(pick([
            "Strong internal compass and self-trust under pressure.",
            "Consistent self-calibration that resists external noise."
        ], "str_internal_ref"))
    if has_internal_reg:
        strengths.append(pick([
            "High self-regulation capacity when demands spike.",
            "Ability to stay composed and functional even when stressed."
        ], "str_internal_reg"))
    if has_delib:
        strengths.append(pick([
            "Thoughtful decision sequencing that reduces impulsive mistakes.",
            "Ability to think through outcomes before acting."
        ], "str_delib"))
    if not strengths:
        strengths = [
            "Stable self-regulation and practical composure.",
            "Ability to hold a steady line during moderate stress."
        ]

    common_misinterpretations = []
    if has_internal_reg:
        common_misinterpretations.append(pick([
            "People may underestimate what you’re carrying because you don’t broadcast it.",
            "Your steadiness can be misread as not being affected."
        ], "mis_internal_reg"))
    if has_internal_ref and not has_ext_val:
        common_misinterpretations.append(pick([
            "Your independence can be misread as not wanting support.",
            "Self-reliance can be mistaken for emotional distance."
        ], "mis_internal_ref"))
    if has_control:
        common_misinterpretations.append(pick([
            "Resistance to being controlled can be misread as being difficult, when it’s actually autonomy-protection.",
            "Boundary sensitivity can be interpreted as stubbornness rather than self-preservation."
        ], "mis_control"))
    if not common_misinterpretations:
        common_misinterpretations = [
            "Your calm demeanor can be mistaken for passivity.",
            "Your internal processing can be misread as emotional distance."
        ]

    reflection_prompts = []
    if has_internal_reg:
        reflection_prompts.append(pick([
            "Where do you quietly accumulate pressure, and what is a clean outlet that doesn’t feel like dumping?",
            "What’s your earliest signal that you’re compressing too much inside?"
        ], "ref_internal_reg"))
    if has_load:
        reflection_prompts.append(pick([
            "When you replay a decision, what are you trying to protect against: regret, uncertainty, or criticism?",
            "What would ‘good enough closure’ look like when your mind wants 100% certainty?"
        ], "ref_load"))
    if has_control:
        reflection_prompts.append(pick([
            "When you feel boxed in, what boundary could you state early to prevent escalation?",
            "What autonomy need is being threatened when you feel controlled?"
        ], "ref_control"))
    if not reflection_prompts:
        reflection_prompts = [
            "Notice what helps you stay grounded when demands rise.",
            "Pay attention to early signs that stress is accumulating."
        ]

    # -------------------------
    # OUTPUT
    # -------------------------
    return {
        "engine_version": "PEK_LITE_INSIGHTFUL_DYNAMIC_V3",
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
            "sections": {
                "underlying_patterns": underlying_patterns,
                "internal_dynamics": internal_dynamics,
                "decision_control": decision_control,
            },
            "real_world_signals": real_world_signals,
            "strengths": strengths,
            "common_misinterpretations": common_misinterpretations,
            "reflection_prompts": reflection_prompts,
        }
    }