# inference_engine.py
# PersonaSight™ — Insightful Dynamic Narrative
# Version: PEK_LITE_INSIGHTFUL_DYNAMIC_V3_INTENSITY_CONTRASTIVE
# Contrastive narrative selection (archetype-based) + deterministic wording
# Stable, non-recursive, ASGI-safe, no external deps

print("INFERENCE ENGINE LOADED FROM:", __file__)
import sys
print("ACTIVE ENGINE FILE:", __file__)
print("ACTIVE PYTHON:", sys.executable)
print("ENGINE MARKER: INTENSITY BUILD ACTIVE (CONTRASTIVE)")

from typing import List, Dict, Tuple
import hashlib


def run_inference(engine_input: dict):
    raw_text = engine_input.get("example_statement", "") or ""
    text = raw_text.lower().strip()

    # ---------------------------------------
    # INPUT DEPTH (NO % / NO NUMERIC LEAK)
    # ---------------------------------------
    def estimate_input_depth_label(t: str) -> dict:
        cleaned = t.replace("\n", " ").strip()
        words = [w for w in cleaned.split(" ") if w.strip()]
        word_count = len(words)
        sentence_count = max(1, sum(1 for ch in cleaned if ch in ".!?"))

        if word_count < 80 or sentence_count < 4:
            return {
                "label": "Limited",
                "note": "Your Snapshot is based on a lower amount of input. More detail usually improves precision and personalization."
            }
        if word_count < 170 or sentence_count < 7:
            return {
                "label": "Moderate",
                "note": "Your Snapshot is based on a solid amount of input. More specificity can sharpen nuance and accuracy."
            }
        return {
            "label": "High",
            "note": "Your Snapshot is based on rich input. This typically produces stronger nuance and higher personal alignment."
        }

    input_depth_rating = estimate_input_depth_label(raw_text)

    # ---------------------------------------
    # DETERMINISTIC VARIATION PICKER
    # ---------------------------------------
    def pick(options: List[str], salt: str) -> str:
        base = (raw_text + "|" + salt).encode("utf-8", errors="ignore")
        h = hashlib.sha256(base).hexdigest()
        idx = int(h[:8], 16) % len(options)
        return options[idx]

    # ---------------------------------------
    # MATCHING UTIL (PHRASE HITS)
    # - simple substring matching (fast)
    # - optional dampening if negation phrases are present
    # ---------------------------------------
    NEGATORS = [
        "not really", "not that", "not much", "doesn't", "dont", "don't",
        "rarely", "hardly", "never", "no issue", "does not", "do not"
    ]

    def has_any(phrases: List[str]) -> bool:
        for p in phrases:
            if p and p in text:
                return True
        return False

    def count_hits(phrases: List[str]) -> int:
        hits = 0
        for p in phrases:
            if p and p in text:
                hits += 1
        return hits

    def negation_dampen(hits: int, negation_phrases: List[str]) -> int:
        # If user explicitly negates that domain, reduce its impact.
        # This is intentionally conservative (only dampens if we see a negator phrase).
        if hits <= 0:
            return 0
        if has_any(negation_phrases):
            return max(0, hits - 1)
        if has_any(NEGATORS):
            return max(0, hits - 1)
        return hits

    def clamp(n: int, lo: int = 0, hi: int = 8) -> int:
        return max(lo, min(hi, n))

    # ---------------------------------------
    # INTERNAL SIGNALS (0–8)
    # (NOT EXPOSED TO USER OUTPUT)
    # ---------------------------------------
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

    # ---------------------------------------
    # PHRASE BANKS (BROADENED + MORE CONTRAST)
    # ---------------------------------------
    BANK = {
        "motivation": {
            "hits": [
                "responsible", "responsibility", "depends on me", "on my shoulders", "carry it",
                "carry it all", "holding everything", "holding it together", "provide", "protector",
                "leader", "i have to", "i must", "i should"
            ],
            "neg": ["not my job", "not responsible", "i don’t care", "i dont care", "whatever"]
        },
        "cognitive_load": {
            "hits": [
                "overthink", "overthinking", "replay", "loop", "loops", "ruminate", "ruminating",
                "second-guess", "analyze", "analysis", "run scenarios", "what if", "can’t stop thinking",
                "can't stop thinking", "spin", "spiral", "mentally"
            ],
            "neg": ["i don't overthink", "i dont overthink", "i move on", "i let it go"]
        },
        "internal_tension": {
            "hits": [
                "stress", "stressed", "pressure", "tension", "overwhelmed", "on edge",
                "tight", "uneasy", "wired", "restless", "anxious", "anxiety", "panic",
                "irritated", "irritation", "angry", "rage", "frustrated", "shut down", "shutdown"
            ],
            "neg": ["not stressed", "not anxious", "i’m fine", "im fine", "no big deal"]
        },
        "control_orientation": {
            "hits": [
                "controlled", "control", "micromanaged", "boxed in", "forced", "trapped",
                "dictated to", "no choice", "cornered", "manipulated", "held hostage",
                "pressure me", "coerced"
            ],
            "neg": ["i don't care if", "i dont care if", "fine with", "i’m flexible", "im flexible"]
        },
        "internal_reference": {
            "hits": [
                "trust myself", "own judgment", "my call", "i decide", "i know what i know",
                "i trust my read", "my intuition", "i stand by", "i’m sure", "im sure"
            ],
            "neg": ["i don't trust myself", "i dont trust myself", "i’m not sure", "im not sure"]
        },
        "external_validation": {
            "hits": [
                "validation", "reassurance", "approval", "need confirmation", "am i right",
                "what do they think", "i need someone to tell me", "i need them to tell me",
                "i ask people", "i check with", "i seek advice", "i need feedback"
            ],
            "neg": ["i don't need approval", "i dont need approval", "i don’t care what they think", "i dont care what they think"]
        },
        "deliberative_decision_style": {
            "hits": [
                "deliberate", "take time", "think before acting", "weigh it", "consider outcomes",
                "map it out", "sequence it", "plan", "planning", "research", "i evaluate", "i compare"
            ],
            "neg": ["i don't think", "i dont think", "i just go", "i act fast"]
        },
        "decisive_action_style": {
            "hits": [
                "decisive", "act quickly", "move fast", "no time", "immediate", "just do it",
                "rip the band-aid", "rip the bandaid", "i commit", "i execute", "i take action"
            ],
            "neg": ["i hesitate", "i freeze", "i get stuck", "i avoid", "i procrastinate"]
        },
        "internal_pressure_regulation": {
            "hits": [
                "keep stress inside", "deal with it internally", "rarely vent", "hold it in",
                "process internally", "i isolate", "i go quiet", "i shut down", "i withdraw",
                "i keep it to myself", "i bottle it", "i bottle up"
            ],
            "neg": ["i talk it out", "i vent", "i get it out", "i open up quickly"]
        },
        "external_pressure_release": {
            "hits": [
                "talk it out", "vent", "let it out", "release it", "get it out", "i rant",
                "i need to say it", "i need to talk", "i call someone", "i process out loud",
                "i tell people", "i verbalize"
            ],
            "neg": ["i never talk", "i don't vent", "i dont vent", "i keep it inside"]
        },

        # optional extra internal signals (not exposed)
        "_avoidance_freeze": {
            "hits": [
                "i avoid", "avoid it", "procrastinate", "freeze", "i freeze", "i get stuck",
                "i shut down", "i can’t move", "can't move", "paralyzed", "numb", "dissociate"
            ],
            "neg": ["i push through", "i take action", "i handle it"]
        },
        "_social_harmony": {
            "hits": [
                "keep the peace", "avoid conflict", "don’t want to upset", "dont want to upset",
                "people-please", "people please", "i try to be liked", "i keep everyone happy"
            ],
            "neg": ["i don't care if they’re upset", "i dont care if they’re upset", "i set boundaries easily"]
        }
    }

    def apply_signal(key: str, cap: int = 8) -> int:
        conf = BANK.get(key, {})
        phrases = conf.get("hits", [])
        negs = conf.get("neg", [])
        hits = count_hits(phrases)
        hits = negation_dampen(hits, negs)
        signal_summary[key] = clamp(hits, 0, cap)
        return signal_summary[key]

    # compute core signals
    apply_signal("motivation")
    apply_signal("cognitive_load")
    apply_signal("internal_tension")
    apply_signal("control_orientation")
    apply_signal("internal_reference")
    apply_signal("external_validation")
    apply_signal("deliberative_decision_style")
    apply_signal("decisive_action_style")
    apply_signal("internal_pressure_regulation")
    apply_signal("external_pressure_release")

    # internal-only extras (not exposed)
    avoid_freeze = clamp(negation_dampen(count_hits(BANK["_avoidance_freeze"]["hits"]), BANK["_avoidance_freeze"]["neg"]))
    social_harmony = clamp(negation_dampen(count_hits(BANK["_social_harmony"]["hits"]), BANK["_social_harmony"]["neg"]))

    # ---------------------------------------
    # MODE SELECTOR (CONTRASTIVE)
    # Forces the narrative to "commit" so outputs diverge more.
    # ---------------------------------------
    def lvl(k: str) -> int:
        return int(signal_summary.get(k, 0) or 0)

    def top_modes() -> List[Tuple[str, int]]:
        # Weighted emphasis to prevent "control" from dominating everything
        # unless it’s truly strong in the text.

        scores = {
            "AUTONOMY_SENTINEL": int(lvl("control_orientation") * 1.6 + lvl("internal_tension") * 0.8),
            "RUMINATIVE_ANALYST": int(lvl("cognitive_load") * 2.6 + lvl("deliberative_decision_style") * 1.3),
            "CONTAINED_LOAD_BEARER": int(lvl("internal_pressure_regulation") * 2.5 + lvl("motivation") * 1.2),
            "EXTERNAL_PROCESSOR": int(lvl("external_pressure_release") * 2.7 + lvl("external_validation") * 0.9),
            "DECISIVE_EXECUTOR": int(lvl("decisive_action_style") * 2.6 + max(0, 2 - lvl("cognitive_load")) * 1.4),
            "COLLAB_CALIBRATOR": int(lvl("external_validation") * 2.2 + social_harmony * 1.2),
            "FREEZE_AVOIDANCE": int(avoid_freeze * 2.6 + lvl("internal_tension") * 1.1),
        }

        # Hard gate: autonomy cannot win unless control signal is meaningful
        if lvl("control_orientation") < 3:
            scores["AUTONOMY_SENTINEL"] = int(scores["AUTONOMY_SENTINEL"] * 0.25)
    
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked

    ranked_modes = top_modes()
    best_mode, best_score = ranked_modes[0]

    # If everything is basically "off", don’t force a weird archetype.
    total_activity = sum(lvl(k) for k in signal_summary.keys())
    if total_activity <= 1 and input_depth_rating["label"] == "Limited":
        best_mode = "LOW_SIGNAL_BASELINE"

    # Secondary mode can add nuance without making everything blend.
    second_mode = ranked_modes[1][0] if len(ranked_modes) > 1 else None

    # ---------------------------------------
    # CORE THEMES (SYNTHESIS PARAGRAPH)
    # ---------------------------------------
    def build_core_themes() -> str:
        # Themes should reflect the chosen mode first (contrast).
        mode_themes = {
            "AUTONOMY_SENTINEL": [
                "rapid internal shift when autonomy feels threatened",
                "boundary pressure sensitivity",
                "a need to regain choice fast"
            ],
            "RUMINATIVE_ANALYST": [
                "looping analysis under uncertainty",
                "mental replay to reach clean closure",
                "a high-detail internal model of outcomes"
            ],
            "CONTAINED_LOAD_BEARER": [
                "quiet load-bearing and responsibility absorption",
                "containment first, relief later",
                "staying functional even when carrying weight"
            ],
            "EXTERNAL_PROCESSOR": [
                "pressure release through expression and discharge",
                "clarity arriving through talking",
                "resetting faster when emotion has a clean outlet"
            ],
            "DECISIVE_EXECUTOR": [
                "commitment and forward motion once a path is chosen",
                "low tolerance for open loops",
                "execution as regulation"
            ],
            "COLLAB_CALIBRATOR": [
                "checking perspective to reduce blind spots",
                "relational calibration under pressure",
                "seeking alignment before committing"
            ],
            "FREEZE_AVOIDANCE": [
                "stalling or shutting down when stakes spike",
                "avoidance as an overload signal",
                "needing safety before movement returns"
            ],
            "LOW_SIGNAL_BASELINE": [
                "steady baseline with limited signal visibility",
                "more depth increases precision",
                "broad stability with unknown nuance"
            ]
        }

        base = mode_themes.get(best_mode, [])
        extras = []

        # Add a single secondary texture if it’s truly present (prevents sameness).
        if second_mode and second_mode != best_mode:
            if second_mode == "AUTONOMY_SENTINEL" and lvl("control_orientation") >= 2:
                extras.append("sensitivity to constraint and control")
            if second_mode == "RUMINATIVE_ANALYST" and lvl("cognitive_load") >= 2:
                extras.append("scenario replay until it feels resolved")
            if second_mode == "EXTERNAL_PROCESSOR" and lvl("external_pressure_release") >= 2:
                extras.append("relief through talking or venting")
            if second_mode == "CONTAINED_LOAD_BEARER" and lvl("internal_pressure_regulation") >= 2:
                extras.append("holding it in until it gets heavy")

        themes = (base[:3] + extras[:2])[:5]
        if not themes:
            return pick([
                "Overall, your inputs show a steady baseline with balanced self-regulation. With more detail, PersonaSight can sharpen nuance and specificity.",
                "Overall, your inputs suggest a stable core with moderate sensitivity to stress signals. More depth tends to increase precision and personalization."
            ], "themes_fallback")

        return "Core Themes: " + ", ".join(themes) + "."

    core_themes = build_core_themes()

    # ---------------------------------------
    # ORIENTATION SNAPSHOT (MODE-BASED)
    # ---------------------------------------
    def build_orientation_snapshot() -> str:
        # Each mode has a distinct voice and emphasis so outputs diverge.
        if best_mode == "AUTONOMY_SENTINEL":
            opener = pick([
                "Your answers read like someone whose nervous system tracks autonomy as a primary stabilizer.",
                "You come across as someone who does fine until choice is removed — and then your internal state shifts quickly."
            ], "o_auto_open")
            body = pick([
                "When you feel boxed in, pressured, or directed without consent, the reaction isn’t subtle: it tightens the system and pushes for exit, control, or clarity.",
                "Constraint doesn’t just irritate you. It changes your internal state fast, and you start looking for a way to restore choice."
            ], "o_auto_body")
            nuance = pick([
                "This can look like intensity to other people, but it often functions as self-protection and boundary enforcement.",
                "The upside is fast boundary intelligence. The downside is that prolonged constraint can create disproportionate irritation or shutdown."
            ], "o_auto_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "RUMINATIVE_ANALYST":
            opener = pick([
                "Your responses read like someone who processes pressure by thinking it through — again and again — until it feels resolved.",
                "You come across as a high-processing mind: detail-oriented, outcome-aware, and allergic to sloppy closure."
            ], "o_rum_open")
            body = pick([
                "You don’t just decide; you simulate. You replay. You tighten the loop until you can stand behind the outcome.",
                "Uncertainty pulls you into scenario-mapping, and the mind stays active long after the moment ends."
            ], "o_rum_body")
            nuance = pick([
                "The upside is precision and reduced impulsivity. The risk is mental fatigue and delayed relief when closure takes too long.",
                "This pattern is powerful for problem-solving, but it can quietly raise load if the loop never lands."
            ], "o_rum_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "CONTAINED_LOAD_BEARER":
            opener = pick([
                "Your answers read like someone who carries responsibility internally and keeps functioning even when the load is real.",
                "You come across as a stabilizer: you hold the line, keep things moving, and often carry more than people realize."
            ], "o_cont_open")
            body = pick([
                "Instead of discharging early, you contain pressure and manage it privately — which preserves composure but can delay relief.",
                "You tend to absorb responsibility like it’s personal, then regulate quietly while still showing up."
            ], "o_cont_body")
            nuance = pick([
                "The upside is resilience. The risk is accumulation: the load can become invisible until it’s heavy.",
                "You may look steady on the outside while running hot internally, especially if there’s no clean outlet."
            ], "o_cont_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "EXTERNAL_PROCESSOR":
            opener = pick([
                "Your responses read like someone whose clarity improves when pressure is expressed rather than contained.",
                "You come across as a person who resets through honest discharge: getting it out helps you stabilize."
            ], "o_ext_open")
            body = pick([
                "Talking, venting, or processing out loud seems to reduce load quickly — not because you need permission, but because expression clears internal noise.",
                "When you can verbalize what’s happening, your system settles faster and decisions get cleaner."
            ], "o_ext_body")
            nuance = pick([
                "The upside is faster recovery and emotional throughput. The risk is bottling it too long and then releasing abruptly.",
                "When you don’t allow expression, pressure may stack; when you do, you tend to recalibrate quickly."
            ], "o_ext_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "DECISIVE_EXECUTOR":
            opener = pick([
                "Your answers read like someone who stabilizes through action and forward motion.",
                "You come across as a person who prefers clean commitment over endless evaluation."
            ], "o_dec_open")
            body = pick([
                "Once you choose a direction, you want momentum. Lingering open loops feel expensive, so you close them and move.",
                "Execution looks like regulation for you: action reduces noise and restores internal order."
            ], "o_dec_body")
            nuance = pick([
                "The upside is speed and traction. The risk is moving too quickly when nuance is still forming — especially under pressure.",
                "This is a strong pattern for progress. It works best when paired with a brief clarity check before commitment."
            ], "o_dec_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "COLLAB_CALIBRATOR":
            opener = pick([
                "Your answers read like someone who improves accuracy by checking perspective, not by outsourcing decisions.",
                "You come across as a calibrator: you value alignment and feedback to reduce blind spots."
            ], "o_col_open")
            body = pick([
                "External input functions like a mirror: it helps you see angles you might miss, especially when stakes are high.",
                "You don’t necessarily need approval, but you do benefit from a signal-check before locking in."
            ], "o_col_body")
            nuance = pick([
                "The upside is balanced judgment and fewer avoidable errors. The risk is friction if feedback becomes inconsistent or emotionally loaded.",
                "This pattern is strongest when you choose high-quality voices to calibrate with, instead of too many opinions."
            ], "o_col_nuance")
            return " ".join([opener, body, nuance]).strip()

        if best_mode == "FREEZE_AVOIDANCE":
            opener = pick([
                "Your answers suggest that when pressure spikes, movement can stall — not from weakness, but from overload.",
                "You come across as someone who can go quiet or freeze when stakes feel too uncertain or too heavy."
            ], "o_frz_open")
            body = pick([
                "Avoidance or shutdown can be the system’s way of trying to reduce internal threat and regain safety before acting.",
                "When the environment feels unpredictable, your system may pull inward until the risk feels containable."
            ], "o_frz_body")
            nuance = pick([
                "The upside is self-protection. The risk is delayed action and regret loops if the stall lasts too long.",
                "This pattern improves when you add a small first step that restores agency without forcing full exposure."
            ], "o_frz_nuance")
            return " ".join([opener, body, nuance]).strip()

        # LOW_SIGNAL_BASELINE fallback
        opener = pick([
            "Your inputs show a relatively steady baseline, with limited signal density to fully personalize the pattern.",
            "Your responses read stable overall, but there isn’t enough detail to lock onto sharper nuance yet."
        ], "o_low_open")
        nuance = pick([
            "With more specificity, PersonaSight can sharpen alignment, distinguish stress signatures, and produce a more individualized Snapshot.",
            "More detail usually increases precision. Even a few concrete examples can shift the Snapshot noticeably."
        ], "o_low_nuance")
        return " ".join([opener, nuance]).strip()

    orientation_snapshot = build_orientation_snapshot()

    # ---------------------------------------
    # SECTIONS (MODE-BASED SHORT PARAGRAPHS)
    # ---------------------------------------
    def build_underlying_patterns() -> str:
        if best_mode == "AUTONOMY_SENTINEL":
            return pick([
                "Your baseline stabilizes when choice is intact. You tend to operate best with clear agency, and you react strongly when that agency is threatened.",
                "You appear boundary-aware and autonomy-driven. You’re cooperative until cooperation becomes control."
            ], "u_auto")
        if best_mode == "RUMINATIVE_ANALYST":
            return pick([
                "Your baseline is analytical and outcome-aware. You build internal certainty before you commit, and you prefer decisions you can defend logically.",
                "You rely on internal modeling: thinking it through is part of how you stay safe and precise."
            ], "u_rum")
        if best_mode == "CONTAINED_LOAD_BEARER":
            return pick([
                "Responsibility tends to land internally first. You stabilize the environment by stabilizing yourself, often without asking for much.",
                "You default into the stabilizer role under stress and keep functioning even when the load increases."
            ], "u_cont")
        if best_mode == "EXTERNAL_PROCESSOR":
            return pick([
                "You regulate through expression. Clarity tends to improve when you can name what’s happening and get it into the open.",
                "You process best with a clean outlet. Communication isn’t drama here; it’s stabilization."
            ], "u_ext")
        if best_mode == "DECISIVE_EXECUTOR":
            return pick([
                "Your baseline favors closure and action. You build enough clarity to commit, then you move.",
                "You’re oriented toward execution. Traction reduces internal noise more than extended deliberation."
            ], "u_dec")
        if best_mode == "COLLAB_CALIBRATOR":
            return pick([
                "You balance internal judgment with external signal-checking. You’re not dependent on feedback, but you use it to increase accuracy.",
                "Your baseline leans toward alignment: you prefer to confirm reality before committing fully."
            ], "u_col")
        if best_mode == "FREEZE_AVOIDANCE":
            return pick([
                "Your baseline can look steady until stakes spike. Under heavier load, withdrawal or stalling can become a protective response.",
                "You may stabilize by reducing exposure first, then re-engaging once things feel safer."
            ], "u_frz")

        return pick([
            "Your baseline reads balanced and steady. More detail tends to sharpen specificity and personalization.",
            "Your inputs show stable self-regulation with moderate sensitivity to stress cues."
        ], "u_fallback")

    def build_internal_dynamics() -> str:
        if best_mode == "AUTONOMY_SENTINEL":
            return pick([
                "Pressure rises fastest when you feel trapped or dictated to. Restoring choice tends to restore calm.",
                "Constraint is a high-intensity trigger. Relief usually arrives when agency is re-established."
            ], "d_auto")
        if best_mode == "RUMINATIVE_ANALYST":
            return pick([
                "When uncertainty rises, thought loops activate. This can increase precision, but it can also keep tension alive in the background.",
                "Your mind stays active under pressure, and relief often arrives only after the loop lands on clean closure."
            ], "d_rum")
        if best_mode == "CONTAINED_LOAD_BEARER":
            return pick([
                "Containment is your default. You hold pressure inside, keep functioning, and often discharge later than you should.",
                "You can carry load quietly for a long time. The risk is that relief arrives late, after accumulation."
            ], "d_cont")
        if best_mode == "EXTERNAL_PROCESSOR":
            return pick([
                "Expression functions as your reset switch. Talking it out tends to reduce load quickly when you allow it.",
                "When you verbalize what’s happening, your system stabilizes faster and tension drops sooner."
            ], "d_ext")
        if best_mode == "DECISIVE_EXECUTOR":
            return pick([
                "Action reduces internal noise for you. Decision → movement is a primary regulation pathway.",
                "Tension tends to drop after commitment. Indecision is more stressful than execution."
            ], "d_dec")
        if best_mode == "COLLAB_CALIBRATOR":
            return pick([
                "Pressure drops when you can confirm reality with a trusted signal-check. Uncertainty becomes easier when you’re not alone in the read.",
                "You stabilize through alignment: verifying assumptions reduces noise and helps you commit cleanly."
            ], "d_col")
        if best_mode == "FREEZE_AVOIDANCE":
            return pick([
                "When pressure spikes, the system may stall. Relief often begins with a small safe step that restores agency without forcing full exposure.",
                "Overload can pull you inward. Movement returns faster when you reduce threat and re-enter gradually."
            ], "d_frz")

        return pick([
            "Pressure appears manageable overall, with mild internalization and a steady regulation style.",
            "Your pressure flow looks stable. With more detail, PersonaSight can better identify where tension accumulates and how it resolves."
        ], "d_fallback")

    def build_decision_control() -> str:
        if best_mode == "AUTONOMY_SENTINEL":
            return pick([
                "You make cleaner decisions when choice is intact. Forced constraints disrupt your rhythm and can trigger sharp resistance.",
                "Control sensitivity is high: you’ll cooperate, but you don’t tolerate being cornered for long."
            ], "c_auto")
        if best_mode == "RUMINATIVE_ANALYST":
            return pick([
                "You prefer decisions you can justify internally. You weigh outcomes, tighten logic, and commit once the path feels clean.",
                "Your decision style favors forethought and sequencing. You move when your internal model settles."
            ], "c_rum")
        if best_mode == "CONTAINED_LOAD_BEARER":
            return pick([
                "You tend to decide quietly and carry the consequences internally. You keep moving even if the decision costs you.",
                "You don’t always announce your process. You absorb the weight and choose the most stabilizing path."
            ], "c_cont")
        if best_mode == "EXTERNAL_PROCESSOR":
            return pick([
                "Your decisions get clearer when you can talk them through. Expression helps you separate signal from noise.",
                "You often decide best after discharge: once the pressure is out, the choice becomes simpler."
            ], "c_ext")
        if best_mode == "DECISIVE_EXECUTOR":
            return pick([
                "Once a decision crystallizes, you prefer momentum and closure. Open loops feel expensive.",
                "You commit quickly when a path is chosen, and you stabilize through execution."
            ], "c_dec")
        if best_mode == "COLLAB_CALIBRATOR":
            return pick([
                "You decide best with a trusted signal-check. Feedback reduces blind spots and helps you commit cleanly.",
                "You balance internal judgment with external calibration, especially under higher stakes."
            ], "c_col")
        if best_mode == "FREEZE_AVOIDANCE":
            return pick([
                "Under higher stakes, the decision channel can stall. Smaller first steps tend to restore movement without triggering overwhelm.",
                "You may delay commitment when threat is high. Safety and clarity reopen the decision pathway."
            ], "c_frz")

        return pick([
            "You appear to alternate between internal evaluation and execution depending on stakes.",
            "Your decision style reads balanced — enough evaluation to stay aligned, enough action to keep moving."
        ], "c_fallback")

    underlying_patterns = build_underlying_patterns()
    internal_dynamics = build_internal_dynamics()
    decision_control = build_decision_control()

    # ---------------------------------------
    # REAL-WORLD SIGNALS / REFLECTION PROMPTS
    # (Minimal, but mode-tuned for contrast)
    # ---------------------------------------
    def build_real_world_signals() -> List[str]:
        if best_mode == "AUTONOMY_SENTINEL":
            return [
                pick([
                    "When choice is removed, your internal state can tighten fast.",
                    "You may tolerate a lot until you feel cornered — then you shift quickly."
                ], "r_auto_1"),
                pick([
                    "You’ll often look for the fastest way to restore agency: clarity, exit, or renegotiation.",
                    "You may become more blunt or urgent when autonomy feels threatened."
                ], "r_auto_2")
            ]
        if best_mode == "RUMINATIVE_ANALYST":
            return [
                pick([
                    "You may replay decisions afterward until they feel logically clean.",
                    "You may mentally revisit events to reduce uncertainty or regret."
                ], "r_rum_1"),
                pick([
                    "You can carry invisible cognitive load even while appearing calm.",
                    "You may keep thinking long after the moment ends."
                ], "r_rum_2")
            ]
        if best_mode == "CONTAINED_LOAD_BEARER":
            return [
                pick([
                    "People may underestimate what you’re carrying because you don’t broadcast it.",
                    "You may look calm while carrying more internally than people realize."
                ], "r_cont_1"),
                pick([
                    "Relief may arrive late because you contain first and discharge later.",
                    "You may keep functioning even when your internal load is high."
                ], "r_cont_2")
            ]
        if best_mode == "EXTERNAL_PROCESSOR":
            return [
                pick([
                    "When you can talk it out, you tend to reset faster.",
                    "Clarity often arrives after expression, not before it."
                ], "r_ext_1"),
                pick([
                    "If you bottle too long, release may come out sharper than intended.",
                    "When you don’t get a clean outlet, pressure can stack."
                ], "r_ext_2")
            ]
        if best_mode == "DECISIVE_EXECUTOR":
            return [
                pick([
                    "Once you commit, momentum stabilizes you quickly.",
                    "You may feel restless when things stay unresolved too long."
                ], "r_dec_1"),
                pick([
                    "You may prefer action over discussion when stress rises.",
                    "You may cut through ambiguity by moving first, refining second."
                ], "r_dec_2")
            ]
        if best_mode == "COLLAB_CALIBRATOR":
            return [
                pick([
                    "You may seek a trusted signal-check before committing under high stakes.",
                    "You may ask for perspective to reduce blind spots, not to outsource decisions."
                ], "r_col_1"),
                pick([
                    "When feedback is noisy or contradictory, your stress can rise.",
                    "You do best when calibration comes from high-quality voices, not too many opinions."
                ], "r_col_2")
            ]
        if best_mode == "FREEZE_AVOIDANCE":
            return [
                pick([
                    "When stakes spike, you may go quiet, stall, or avoid until safety returns.",
                    "Overload can look like procrastination or shutdown from the outside."
                ], "r_frz_1"),
                pick([
                    "Smaller first steps tend to restore movement faster than forcing a big leap.",
                    "You may re-engage once uncertainty drops and the path feels safer."
                ], "r_frz_2")
            ]

        return [
            "You tend to maintain a stable outward presence across changing demands.",
            "You prefer to process internally before sharing externally."
        ]

    def build_reflection_prompts() -> List[str]:
        if best_mode == "AUTONOMY_SENTINEL":
            return [
                pick([
                    "What boundary could you state earlier so constraint doesn’t build into a spike?",
                    "What would a clean renegotiation look like before you hit the wall?"
                ], "p_auto_1"),
                pick([
                    "When you feel controlled, what autonomy need is being threatened?",
                    "What restores agency fastest for you: clarity, space, or a new agreement?"
                ], "p_auto_2")
            ]
        if best_mode == "RUMINATIVE_ANALYST":
            return [
                pick([
                    "What would ‘good enough closure’ look like when your mind wants 100% certainty?",
                    "When do you know a loop is helpful vs draining?"
                ], "p_rum_1"),
                pick([
                    "When you replay a decision, what are you trying to protect against: regret, uncertainty, or criticism?",
                    "What single fact would let your mind release the loop sooner?"
                ], "p_rum_2")
            ]
        if best_mode == "CONTAINED_LOAD_BEARER":
            return [
                pick([
                    "Where do you quietly accumulate pressure — and what outlet feels clean instead of like dumping?",
                    "What’s your earliest signal that you’re containing too much?"
                ], "p_cont_1"),
                pick([
                    "If you asked for support earlier, what would it look like that still preserves your dignity?",
                    "What small discharge would prevent the load from stacking?"
                ], "p_cont_2")
            ]
        if best_mode == "EXTERNAL_PROCESSOR":
            return [
                pick([
                    "What’s your cleanest outlet when pressure rises: one trusted person, a voice note, or writing it out?",
                    "What kind of expression helps you reset without escalating?"
                ], "p_ext_1"),
                pick([
                    "When you vent, what do you actually need: clarity, comfort, or a plan?",
                    "What does ‘healthy discharge’ look like for you this week?"
                ], "p_ext_2")
            ]
        if best_mode == "DECISIVE_EXECUTOR":
            return [
                pick([
                    "Before you commit, what’s the one clarity check that prevents avoidable mistakes?",
                    "What’s the smallest decision that restores momentum without locking you into the wrong path?"
                ], "p_dec_1"),
                pick([
                    "When stress rises, do you move fast to regulate — or because you feel pressured to close?",
                    "Where would a 10-minute pause improve accuracy without killing momentum?"
                ], "p_dec_2")
            ]
        if best_mode == "COLLAB_CALIBRATOR":
            return [
                pick([
                    "Who are your highest-quality calibration voices — and who adds noise?",
                    "When you seek perspective, what question gets you the best signal?"
                ], "p_col_1"),
                pick([
                    "What would it look like to trust your internal read first, then verify once?",
                    "How do you know when feedback is helping vs distracting?"
                ], "p_col_2")
            ]
        if best_mode == "FREEZE_AVOIDANCE":
            return [
                pick([
                    "What is the smallest safe step you can take when you feel stuck?",
                    "What would make the next move feel 10% safer — not perfect, just safer?"
                ], "p_frz_1"),
                pick([
                    "When you shut down, what is your system protecting you from?",
                    "What helps you re-enter: structure, reassurance, or a clear first step?"
                ], "p_frz_2")
            ]

        return [
            "Notice what helps you stay grounded when demands rise.",
            "Pay attention to early signs that stress is accumulating."
        ]

    real_world_signals = build_real_world_signals()
    reflection_prompts = build_reflection_prompts()

    # ---------------------------------------
    # LIMITED INPUT CTA (POST-SNAPSHOT)
    # ---------------------------------------
    if input_depth_rating["label"] == "Limited":
        next_step_note = (
            "If you want a sharper and more personalized Snapshot, consider re-running with more detail per answer. "
            "Even adding a few specific examples can change the nuance significantly."
        )
    else:
        next_step_note = ""

    # ---------------------------------------
    # OUTPUT (IP-PROTECTIVE)
    # ---------------------------------------
    return {
        "engine_version": "PEK_LITE_INSIGHTFUL_DYNAMIC_V3_INTENSITY",
        "input_depth_rating": input_depth_rating,
        "lite_translation": {
            "orientation_snapshot": orientation_snapshot,
            "core_themes": core_themes,
            "sections": {
                "underlying_patterns": underlying_patterns,
                "internal_dynamics": internal_dynamics,
                "decision_control": decision_control,
            },
            "real_world_signals": real_world_signals,
            "reflection_prompts": reflection_prompts,
            "next_step_note": next_step_note
        }
    }