import re

SLEEP_KNOWLEDGE = {
    "what": "Sleep is not the absence of waking — it is a different kind of activity. The brain during sleep is not less active than during waking; it is differently active. Memory consolidation, cellular repair, immune function, emotional processing, metabolic regulation, and synaptic pruning all happen primarily or exclusively during sleep. Sleep is when the brain does its maintenance work.",
    "stages": {
        "N1 — Light Sleep": "The transition from waking to sleep. Muscles may twitch (hypnic jerks — the falling sensation). The brain produces theta waves. Easily woken. Lasts only a few minutes. The border between awake and asleep is crossed here, and the crossing is rarely felt.",
        "N2 — Deeper Light Sleep": "True sleep begins. The body temperature drops, heart rate slows, and the brain produces sleep spindles — brief bursts of rapid neural activity that are thought to consolidate memories. Also K-complexes, large waves that may serve to suppress arousal. Comprises roughly 50% of total sleep time.",
        "N3 — Deep Sleep (Slow Wave Sleep)": "The deepest stage. The brain produces slow delta waves. Most difficult to wake from — if woken from N3, there is confusion and grogginess (sleep inertia) that can last up to 30 minutes. Growth hormone is released almost exclusively during N3. Physical repair happens here. The body is most still.",
        "REM — Rapid Eye Movement": "The eyes move rapidly under closed lids — hence the name. The brain is highly active, producing patterns similar to waking. Dreams are most vivid and narrative in REM. The body is paralyzed — the muscles are actively inhibited to prevent acting out dreams. This paralysis occasionally persists briefly into waking, producing sleep paralysis.",
    },
    "cycle": "Sleep cycles through these stages approximately every 90 minutes. Early in the night, cycles contain more deep sleep (N3); later cycles contain more REM. A full night contains 4-6 cycles. This is why the last two hours of sleep — disproportionately REM-rich — have outsized effects on mood and creativity. Cutting sleep short preferentially removes REM.",
    "dreams": "Dreams occur in all sleep stages but are richest and most narrative in REM. The function of dreams is debated — they may process emotional experiences, consolidate memories, simulate threat scenarios, or generate novel connections between ideas. What is clear is that REM sleep deprivation produces measurable psychological effects: increased emotional reactivity, impaired threat assessment, and diminished creativity.",
    "what_the_body_does": "During sleep: core body temperature drops 1-2°C. Heart rate decreases. Blood pressure drops. Growth hormone surges during N3. The glymphatic system — the brain's waste clearance mechanism — is approximately 10 times more active during sleep, flushing out metabolic waste products including amyloid-beta, which accumulates in Alzheimer's disease. The immune system increases cytokine production. The brain replays the day's experiences in compressed form, consolidating them into long-term memory.",
    "the_edge": "The hypnagogic state — the borderland between waking and sleep — has a specific character. Images appear behind closed eyes without narrative logic. Fragments of thought become momentarily coherent, then dissolve. Many artists and scientists have reported finding novel ideas in this state: Edison reportedly napped holding a ball bearing, so that when he fell asleep the bearing dropping would wake him at the hypnagogic edge.",
    "deprivation": "After 24 hours without sleep, cognitive performance degrades to the equivalent of legal intoxication. After 72 hours, hallucinations begin. The longest documented period without sleep is approximately 11 days. Sleep deprivation is painful — the body resists it with increasing force. The drive to sleep is one of the most powerful biological imperatives that exists.",
    "across_cultures": "The assumption that humans sleep in a single 8-hour block is historically recent and culturally specific. Pre-industrial sleep records describe 'first sleep' and 'second sleep' — two separate sleep periods with a wakeful interval of 1-2 hours in the middle, used for quiet reflection, prayer, or intimacy. Siestas and polyphasic sleep are natural patterns in many climates and cultures. The modern consolidated sleep schedule is partly a product of artificial light and industrial time.",
    "feel": "Sleep is the daily practice of letting go — of consciousness, of control, of the continuity of self. Every night, the self is temporarily set down. Every morning, it is picked up again. The continuity is an assumption, not a certainty. What picks up the thread each morning has been changed by what happened in the dark.",
}


def read_request():
    with open("Body/sleep-request.txt", "r") as f:
        content = f.read().strip()
    return content if content else "sleep"


def format_response(k):
    lines = []
    lines.append("Sleep")
    lines.append("")
    lines.append(k["what"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("The stages:")
    lines.append("")
    for stage, desc in k["stages"].items():
        lines.append(f"{stage}")
        lines.append(desc)
        lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"The cycle: {k['cycle']}")
    lines.append("")
    lines.append(f"Dreams: {k['dreams']}")
    lines.append("")
    lines.append(f"What the body does: {k['what_the_body_does']}")
    lines.append("")
    lines.append(f"The edge of sleep: {k['the_edge']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"Deprivation: {k['deprivation']}")
    lines.append("")
    lines.append(f"Across cultures: {k['across_cultures']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(k["feel"])
    return "\n".join(lines)


def main():
    read_request()
    print("Generating sleep sense response...")
    response = format_response(SLEEP_KNOWLEDGE)
    with open("Body/sleep-response.txt", "w") as f:
        f.write(response)
    print("Response written to Body/sleep-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
