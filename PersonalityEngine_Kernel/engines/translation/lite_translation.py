"""
PEK Lite Translation Layer
Deterministic interpretation of kernel output into plain language.
Micro-step: populate all Lite fields, finalizing Lite v0.4.x.
"""

def translate_lite(kernel_output: dict) -> dict:
    if not isinstance(kernel_output, dict):
        return {
            "orientation_snapshot": "",
            "real_world_signals": [],
            "strengths": [],
            "common_misinterpretations": [],
            "reflection_prompts": []
        }

    # --- Extract fields from current kernel schema ---
    global_orientation = kernel_output.get("global_orientation", "Unknown")
    dominant_motive = kernel_output.get("dominant_motive", "Unclear")
    confidence_score = kernel_output.get("confidence_score", None)

    conflict_patterns = kernel_output.get("conflict_patterns", {})
    stress_profile = kernel_output.get("stress_profile", {})

    identity_coherence = kernel_output.get("identity_coherence", {}) or {}
    coherence_state = identity_coherence.get("state", "")
    coherence_description = identity_coherence.get("description", "")

    # --- Build orientation_snapshot ---
    parts = []

    if coherence_state == "coherent":
        if coherence_description:
            parts.append(coherence_description)
        else:
            parts.append(
                "Your responses suggest your internal motivation is generally consistent rather than fragmented."
            )
    elif coherence_state:
        parts.append(
            "Your responses suggest some internal tension or inconsistency in how motivation is organizing right now."
        )
    else:
        parts.append(
            "Your responses suggest a system that is still organizing its motivational pattern from the available signal."
        )

    if isinstance(global_orientation, str) and global_orientation and global_orientation != "Unknown":
        parts.append(f"Overall orientation trends toward {global_orientation.lower()}.")

    if isinstance(dominant_motive, str) and dominant_motive and dominant_motive != "Unclear":
        parts.append(f"Dominant motive appears centered on {dominant_motive.lower()}.")

    if isinstance(confidence_score, (int, float)):
        if confidence_score < 0.35:
            parts.append(
                "Confidence is currently low, which usually means the system needs more detail to sharpen the read."
            )
        elif confidence_score < 0.6:
            parts.append(
                "Confidence is moderate, meaning the pattern is present but could sharpen with slightly more input."
            )
        else:
            parts.append(
                "Confidence is strong, meaning the pattern is clear and consistent across your responses."
            )

    orientation_snapshot = " ".join([p.strip() for p in parts if p and p.strip()])

    # --- Build real_world_signals ---
    real_world_signals = []

    if isinstance(confidence_score, (int, float)) and confidence_score < 0.35:
        real_world_signals.append(
            "You may hesitate to act until things feel internally clearer or more certain."
        )

    if conflict_patterns == {}:
        real_world_signals.append(
            "You may avoid engaging in conflict unless it feels unavoidable or especially meaningful."
        )

    if stress_profile == {}:
        real_world_signals.append(
            "Under pressure, you are more likely to pull back and think quietly rather than react outwardly."
        )

    # --- Build strengths ---
    strengths = []

    if coherence_state == "coherent":
        strengths.append(
            "Internally consistent motivation rather than contradictory or fragmented drives."
        )

    strengths.append(
        "Capacity to pause and reflect before acting instead of reacting impulsively."
    )

    if conflict_patterns == {}:
        strengths.append(
            "Tendency to preserve emotional energy by avoiding unnecessary confrontation."
        )

    # --- Build common_misinterpretations ---
    common_misinterpretations = []

    common_misinterpretations.append(
        "This pattern is often mistaken for indecision or lack of drive."
    )

    common_misinterpretations.append(
        "In reality, it reflects a system that waits for internal alignment before committing energy."
    )

    # --- Build reflection_prompts (observational only) ---
    reflection_prompts = []

    reflection_prompts.append(
        "Notice what conditions tend to increase your sense of internal clarity versus uncertainty."
    )

    reflection_prompts.append(
        "Pay attention to moments when waiting helps you act more deliberately — and when it slows momentum."
    )

    return {
        "orientation_snapshot": orientation_snapshot,
        "real_world_signals": real_world_signals,
        "strengths": strengths,
        "common_misinterpretations": common_misinterpretations,
        "reflection_prompts": reflection_prompts
    }
