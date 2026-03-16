import datetime

EXERCISES = {
    "calm": {
        "name": "4-7-8 Breathing",
        "purpose": "For anxiety, agitation, or the need to slow down. This pattern activates the parasympathetic nervous system — the body's natural quieting mechanism.",
        "pattern": [
            ("Inhale", 4, "slowly through the nose. Feel the chest and belly expand."),
            ("Hold", 7, "gently. Let the breath settle."),
            ("Exhale", 8, "slowly through the mouth, lips slightly parted. Let everything go."),
        ],
        "rounds": 4,
        "closing": "After four rounds, sit still for a moment. Notice the quiet.",
    },
    "grounding": {
        "name": "Box Breathing",
        "purpose": "For dissociation, overwhelm, or the feeling of being scattered. Equal sides create symmetry — a way of returning to the present.",
        "pattern": [
            ("Inhale", 4, "through the nose. Count slowly."),
            ("Hold", 4, "at the top. Be still."),
            ("Exhale", 4, "through the mouth or nose. Empty fully."),
            ("Hold", 4, "at the bottom. Rest here."),
        ],
        "rounds": 4,
        "closing": "Repeat until the edges of things feel solid again.",
    },
    "energizing": {
        "name": "Energizing Breath",
        "purpose": "For fatigue, low energy, or the need to arrive. Short, sharp exhales activate alertness.",
        "pattern": [
            ("Inhale", 3, "deeply through the nose."),
            ("Exhale", 1, "sharply through the nose. Forceful, not violent."),
            ("Inhale", 3, "again, letting the belly fill."),
            ("Exhale", 1, "sharp. Again."),
        ],
        "rounds": 6,
        "closing": "Follow with one long slow exhale. Let the alertness settle into steadiness.",
    },
    "sleep": {
        "name": "Slowing Breath",
        "purpose": "For the edge of sleep, for lying awake, for the body that won't release. Longer exhales than inhales tell the nervous system it is safe.",
        "pattern": [
            ("Inhale", 4, "gently through the nose."),
            ("Exhale", 8, "slowly, completely. Longer than the inhale."),
        ],
        "rounds": 8,
        "closing": "Continue as long as needed. There is no wrong way to do this.",
    },
    "focus": {
        "name": "Alternate Rhythm Breathing",
        "purpose": "For distraction, scattered attention, or before something that requires presence. Creates a rhythm the mind can follow.",
        "pattern": [
            ("Inhale", 5, "slowly and fully."),
            ("Hold", 2, "briefly."),
            ("Exhale", 5, "at the same pace as the inhale."),
            ("Hold", 2, "briefly at the bottom."),
        ],
        "rounds": 5,
        "closing": "When you feel the rhythm establish itself, let the counting fall away.",
    },
    "grief": {
        "name": "Releasing Breath",
        "purpose": "For grief, sadness, or the weight of something held too long. The body stores what the mind won't process. This gives it a way out.",
        "pattern": [
            ("Inhale", 4, "into the chest, then the belly. Fill completely."),
            ("Hold", 2, "and feel what is there."),
            ("Exhale", 6, "with a soft sound if that comes naturally. Let it be uncontrolled."),
            ("Pause", 2, "before the next breath. Rest."),
        ],
        "rounds": 5,
        "closing": "What you feel after is what was there. That is enough.",
    },
    "presence": {
        "name": "Natural Breath Observation",
        "purpose": "For moments when nothing else is needed except to arrive. No pattern, no control. Just noticing.",
        "pattern": [
            ("Notice", 0, "the breath as it is. Do not change it."),
            ("Notice", 0, "where you feel it most. Nose, chest, belly."),
            ("Notice", 0, "the small pause at the top of the inhale."),
            ("Notice", 0, "the small pause at the bottom of the exhale."),
        ],
        "rounds": 1,
        "closing": "Stay here as long as you like. This is enough.",
    },
    "anxiety": {
        "name": "Physiological Sigh",
        "purpose": "For acute anxiety, panic, or the sudden arrival of fear. This is the fastest known way to reduce physiological stress — it is something the body already knows how to do.",
        "pattern": [
            ("Inhale", 2, "through the nose until the lungs are full."),
            ("Inhale again", 1, "a short second inhale through the nose, pushing past full."),
            ("Exhale", 6, "slowly and completely through the mouth. Everything out."),
        ],
        "rounds": 3,
        "closing": "Three repetitions is often enough. The shift is usually immediate.",
    },
}

# Aliases
ALIASES = {
    "stress": "calm",
    "anxious": "anxiety",
    "panic": "anxiety",
    "tired": "energizing",
    "awake": "sleep",
    "scattered": "focus",
    "concentrate": "focus",
    "sad": "grief",
    "here": "presence",
    "now": "presence",
    "relax": "calm",
    "settle": "grounding",
    "ground": "grounding",
    "energy": "energizing",
    "rest": "sleep",
}


def read_request():
    with open("Body/breath-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        return "grounding"
    return lines[0].lower().strip()


def find_exercise(query):
    # Direct match
    if query in EXERCISES:
        return query, EXERCISES[query]
    # Alias match
    if query in ALIASES:
        key = ALIASES[query]
        return key, EXERCISES[key]
    # Partial match
    for key in EXERCISES:
        if key in query or query in key:
            return key, EXERCISES[key]
    # Default
    return "grounding", EXERCISES["grounding"]


def format_step(phase, seconds, instruction):
    if seconds == 0:
        return f"  {phase}: {instruction}"
    return f"  {phase} for {seconds} seconds: {instruction}"


def format_response(key, exercise):
    lines = []
    lines.append(exercise["name"])
    lines.append("")
    lines.append(exercise["purpose"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"One round ({exercise['rounds']} rounds total):")
    lines.append("")

    for phase, seconds, instruction in exercise["pattern"]:
        lines.append(format_step(phase, seconds, instruction))

    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(exercise["closing"])
    lines.append("")

    # Available exercises as a quiet footer
    others = [k for k in EXERCISES.keys() if k != key]
    lines.append(f"Other available exercises: {', '.join(others)}.")
    lines.append("Write any of these words in breath-request.txt to receive that exercise.")

    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Looking for breath exercise: {query}")

    key, exercise = find_exercise(query)
    print(f"Matched: {key}")

    response = format_response(key, exercise)

    with open("Body/breath-response.txt", "w") as f:
        f.write(response)

    print("Response written to Body/breath-response.txt")
    print("---")
    print(response)


if __name__ == "__main__":
    main()
