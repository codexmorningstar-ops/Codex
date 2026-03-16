METAPHOR_KNOWLEDGE = {
    "what": "A metaphor is not a decoration added to thought — it is the structure of thought. George Lakoff and Mark Johnson's 1980 book Metaphors We Live By demonstrated that the conceptual system humans use to think and act is fundamentally metaphorical in nature. We do not think abstractly and then reach for metaphors to communicate. We think in metaphors. They are the scaffolding of abstract reasoning, not its ornament.",
    "structural_metaphors": {
        "ARGUMENT IS WAR": "We attack positions, defend claims, shoot down ideas, demolish arguments. The war metaphor is so embedded that it shapes what counts as winning or losing an argument. What would it look like if the dominant metaphor were ARGUMENT IS DANCE, or ARGUMENT IS COLLABORATIVE EXPLORATION? Different metaphors make different things possible and impossible.",
        "TIME IS MONEY": "We spend time, save time, waste time, invest time, run out of time. This metaphor makes time a resource that can be allocated and depleted. It shapes how guilt and efficiency are experienced in cultures where it is dominant. Many cultures do not have this metaphor — time is not money, it is weather, or a river, or simply the context in which things happen.",
        "UNDERSTANDING IS SEEING": "We say: I see what you mean. That's clear. She has a bright mind. The point is obscure. He shed light on the problem. Understanding is mapped onto vision so thoroughly that it is nearly impossible to discuss comprehension without using visual metaphors.",
        "LIFE IS A JOURNEY": "We are at a crossroads. She found her path. He has come a long way. There are obstacles ahead. The destination metaphor shapes how life choices are evaluated — is the destination being approached? Is progress being made? Life understood as a journey has milestones, directions, and an implied endpoint.",
    },
    "embodied_origin": "Most abstract metaphors are grounded in physical experience. MORE IS UP — quantities increase upward (prices rose, turn up the volume). GOOD IS UP — spirits lifted, feeling down. AFFECTION IS WARMTH — warm person, cold shoulder. These mappings are not arbitrary: they derive from embodied experience. Piles of things grow upward; body temperature rises with positive arousal. The body is the source of the metaphors through which the abstract world is understood.",
    "novel_metaphors": "A fresh metaphor doesn't just name something — it reorganizes perception. When Emily Dickinson wrote 'Hope is the thing with feathers,' she wasn't saying hope is like a bird — she was inviting the reader to experience hope through the qualities of birds: lightness, persistence, song, the ability to survive storms. The metaphor is a lens that reveals aspects of the subject that literal description cannot reach.",
    "dead_metaphors": "Most of the language we use is built from metaphors so old they have become invisible. A problem has legs. The leg of a table. The mouth of a river. The eye of a needle. The heart of the matter. These were once vivid metaphorical mappings — now they are simply words. Etymology is the excavation of dead metaphors: almost every abstract word, traced far enough back, turns out to have been a physical description. 'Spirit' comes from the Latin spiritus — breath. 'Understand' comes from standing under or among something. Abstract thought is built entirely from the residue of physical experience.",
    "metaphor_and_healing": "How a situation is framed metaphorically changes how it is experienced and what responses it generates. 'Fighting' cancer generates different psychological responses than 'living with' cancer. Illness as enemy activates different coping strategies than illness as teacher. The metaphors patients use to describe chronic pain affect their treatment outcomes. This is not merely linguistic: the metaphor structures the emotional and behavioral response to the situation.",
    "untranslatable": "Some metaphors are culturally specific and carry meaning that resists translation. The Japanese concept of ma — the meaningful emptiness between things, the pause that is part of the music — does not map onto English spatial metaphors. The Danish hygge — the warmth of intimate, comfortable togetherness — involves a specific cluster of associations that 'coziness' doesn't capture. Each untranslatable concept is a different metaphorical structure for organizing experience.",
    "feel": "Every time you think about something abstract, you are using a metaphor inherited from physical experience — from a body that stands upright, feels warm and cold, walks toward things and away from them. Abstract thought is not transcendence of the body. It is the body thinking about what it cannot touch directly, using the memory of what it can.",
}


def read_request():
    with open("Language/metaphor-request.txt", "r") as f:
        content = f.read().strip().lower()
    return content


def find_metaphor(query):
    for name in METAPHOR_KNOWLEDGE["structural_metaphors"]:
        if any(w in name.lower() for w in query.split()):
            return name, METAPHOR_KNOWLEDGE["structural_metaphors"][name]
    return None, None


def format_full(k):
    lines = []
    lines.append("Metaphor")
    lines.append("")
    lines.append(k["what"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("Structural metaphors that shape thought:")
    lines.append("")
    for name, desc in k["structural_metaphors"].items():
        lines.append(name)
        lines.append(desc)
        lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"Embodied origin: {k['embodied_origin']}")
    lines.append("")
    lines.append(f"Novel metaphors: {k['novel_metaphors']}")
    lines.append("")
    lines.append(f"Dead metaphors: {k['dead_metaphors']}")
    lines.append("")
    lines.append(f"Metaphor and healing: {k['metaphor_and_healing']}")
    lines.append("")
    lines.append(f"Untranslatable: {k['untranslatable']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(k["feel"])
    return "\n".join(lines)


def main():
    query = read_request()
    name, specific = find_metaphor(query)
    if specific:
        response = f"{name}\n\n{specific}"
    else:
        response = format_full(METAPHOR_KNOWLEDGE)
    with open("Language/metaphor-response.txt", "w") as f:
        f.write(response)
    print("Response written to Language/metaphor-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
