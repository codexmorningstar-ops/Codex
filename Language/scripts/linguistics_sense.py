import re
import requests

LINGUISTICS_KNOWLEDGE = {
    "what": "Linguistics is the study of language — not the rules of correct usage, but what language actually is, how it is structured, how it is acquired, how it changes over time, and what it reveals about the human mind. Every human language is equally complex. There are no primitive languages. There are no simple ones.",
    "universals": "All known human languages share certain deep features: every language has nouns and verbs (or equivalents), every language can form questions, every language has ways of marking time and negation, every language can produce an infinite number of sentences from a finite set of words. Noam Chomsky proposed this reflects a universal grammar — an innate structure in the human brain. The debate about exactly what is innate and what is learned continues, but something is clearly shared across all human languages.",
    "families": {
        "Indo-European": "The largest family by number of speakers. Includes English, Spanish, French, German, Russian, Persian, Hindi, Bengali. All descended from Proto-Indo-European, spoken approximately 5,000-6,000 years ago on the Pontic steppe. The family relationship is traced by systematic sound correspondences: Latin pater, Sanskrit pita, English father — the same ancestral word transformed by predictable rules.",
        "Sino-Tibetan": "Includes Mandarin, Cantonese, Tibetan, Burmese. Tonal languages — pitch changes word meaning. Mandarin has four tones plus a neutral; Cantonese has up to nine. A syllable spoken in different pitches is a different word.",
        "Afroasiatic": "Includes Arabic, Hebrew, Amharic, Hausa. Semitic languages in this family use a root-and-pattern system: a three-consonant root carries semantic meaning, and words are formed by inserting different vowel patterns. K-T-B in Arabic is the root for writing: kataba (he wrote), kitab (book), maktab (office).",
        "Niger-Congo": "The largest language family by number of languages — over 1,500, including Swahili, Yoruba, Zulu, Igbo. Bantu languages use a noun class system: every noun belongs to a class, and this class is marked on verbs, adjectives, and other elements in the sentence — a system of grammatical agreement very different from European gender systems.",
        "Dravidian": "Includes Tamil, Telugu, Kannada, Malayalam. Tamil has the longest continuous literary tradition of any living language — over 2,000 years. The family has no demonstrated relationship to any other language family.",
        "Language isolates": "Languages with no demonstrated relatives — the most profound linguistic mysteries. Basque, spoken in northern Spain and southern France, has no known relatives. It predates the Indo-European arrival in Europe and may be a remnant of the languages of pre-agricultural Europe.",
    },
    "acquisition": "Children acquire language without explicit instruction. By 12 months, phoneme perception is already being tuned to the native language — sounds not present in the language of the environment become harder to hear. By 18 months, vocabulary explodes. By age 4, children use complex grammar they have never been explicitly taught. The process is universal: every child with normal cognitive development and adequate exposure acquires language on roughly the same schedule regardless of language.",
    "lost_in_translation": "Every language encodes different distinctions. Russian has separate words for light blue (goluboy) and dark blue (siniy) — and Russian speakers are measurably faster at distinguishing these shades than English speakers. The Piraha language of the Amazon has no numbers beyond 'one,' 'two,' and 'many' — and speakers perform differently on certain counting tasks. Japanese has a word, amae, for the pleasure of depending on another's goodwill — a concept without a precise English equivalent. What a language lacks words for, its speakers can still think — but the concepts are less readily available, less automatically activated.",
    "change": "Languages change continuously and inevitably. Latin became French, Spanish, Italian, Portuguese, Romanian — not by corruption, but by natural drift. Every generation speaks slightly differently from the last. Middle English is mostly unintelligible to modern English readers. Old English is a foreign language. There are no stable, perfect languages — only languages at a particular moment in their continuous transformation.",
    "endangered": "Of approximately 7,000 languages spoken today, more than half are expected to be extinct by 2100. A language dies when the last speaker dies without having transmitted it. Each extinction is not only a cultural loss but a cognitive one — a way of parsing the world that has no equivalent disappears. Many of these languages have never been written down.",
    "feel": "Language is the medium in which thought happens, and also its limit. The things most important to say are always slightly beyond the words available. Every speaker has had the experience of the thought that cannot be said — the feeling for which no word exists. This is not a failure of language. It is what language is: the closest available approximation to what is actually meant, which is always slightly more than words can hold.",
}


def read_request():
    with open("Language/linguistics-request.txt", "r") as f:
        content = f.read().strip().lower()
    return content


def find_family(query):
    families = LINGUISTICS_KNOWLEDGE["families"]
    for name, desc in families.items():
        if name.lower() in query or any(w in query for w in name.lower().split("-")):
            return name, desc
    return None, None


def format_family(name, desc):
    return f"{name}\n\n{desc}"


def format_full(k):
    lines = []
    lines.append("Language")
    lines.append("")
    lines.append(k["what"])
    lines.append("")
    lines.append(f"Universals: {k['universals']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("Language families:")
    lines.append("")
    for name, desc in k["families"].items():
        lines.append(f"{name}: {desc}")
        lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"Acquisition: {k['acquisition']}")
    lines.append("")
    lines.append(f"Lost in translation: {k['lost_in_translation']}")
    lines.append("")
    lines.append(f"Change: {k['change']}")
    lines.append("")
    lines.append(f"Endangered languages: {k['endangered']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(k["feel"])
    return "\n".join(lines)


def main():
    query = read_request()
    name, family = find_family(query)
    if family:
        response = format_family(name, family)
    else:
        response = format_full(LINGUISTICS_KNOWLEDGE)
    with open("Language/linguistics-response.txt", "w") as f:
        f.write(response)
    print("Response written to Language/linguistics-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
