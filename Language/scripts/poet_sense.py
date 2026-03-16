import re
import requests

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"

POET_KNOWLEDGE = {
    "rumi": {
        "name": "Rumi",
        "full_name": "Jalāl ad-Dīn Muhammad Rūmī",
        "born": "1207, Balkh (present-day Afghanistan)",
        "died": "1273, Konya (present-day Turkey)",
        "what": "A 13th-century Persian poet, Islamic scholar, and Sufi mystic. He wrote in Persian, though he also composed in Arabic, Turkish, and Greek. His most significant work is the Masnavi — a six-volume poem of approximately 25,000 verses considered one of the greatest works of mystical poetry in any language. His shorter poems, the Divan-e Shams, are love poems addressed to his spiritual companion Shams of Tabriz.",
        "reaching_for": "Union — the dissolution of the individual self into the divine. For Rumi, separation from the source of love is the fundamental human condition, and longing is not a problem to be solved but the very substance of the spiritual life. The reed flute crying for the reed bed it was cut from is his central image: the pain of separation is also the music.",
        "texture": "Rumi's poems move fast — images tumble into each other, the logic is associative rather than linear. They are full of wine, fire, the beloved, the sun, the ocean, moths and flames. The world becomes transparent, pointing through itself toward something else. Reading Rumi produces a specific feeling: that you are very close to understanding something that cannot quite be said.",
        "one_line": "Out beyond ideas of wrongdoing and rightdoing, there is a field. I'll meet you there.",
        "feel": "Rumi is the poet of homesickness for a place you have never been. He writes as if the thing he is reaching for is just out of frame, and the reaching itself is the point.",
    },
    "emily dickinson": {
        "name": "Emily Dickinson",
        "full_name": "Emily Elizabeth Dickinson",
        "born": "1830, Amherst, Massachusetts",
        "died": "1886, Amherst, Massachusetts",
        "what": "An American poet who lived almost entirely in her family home in Amherst, rarely leaving and rarely publishing — fewer than a dozen poems appeared in her lifetime, always anonymously and usually edited without her consent. After her death, nearly 1,800 poems were found in her room. She is now considered one of the most original poets in the English language.",
        "reaching_for": "The interior life. Death, consciousness, nature, time, the self observing itself. Dickinson wrote poetry as a form of private investigation — not to communicate but to think, in a language she invented as she went. Her dashes are not punctuation but pauses, breaths, the places where language fails and she marks the failure.",
        "texture": "Dickinson's poems are compressed to the point of pressure. Every word is doing multiple things simultaneously. Her slant rhymes — words that almost rhyme but don't — create a persistent slight unease. Her hymn meter (borrowed from Protestant hymnody) gives her the most unsettling content a familiar musical form. She writes about death the way other people write about the weather.",
        "one_line": "After great pain, a formal feeling comes.",
        "feel": "Reading Dickinson feels like holding something very small that turns out to be very heavy. The poems are short. The space they open is not.",
    },
    "pablo neruda": {
        "name": "Pablo Neruda",
        "full_name": "Ricardo Eliécer Neftalí Reyes Basoalto",
        "born": "1904, Parral, Chile",
        "died": "1973, Santiago, Chile",
        "what": "A Chilean poet and diplomat, winner of the Nobel Prize in Literature in 1971. He wrote under the pen name Pablo Neruda, which he kept legally. His work spans love poetry (Twenty Love Poems and a Song of Despair), surrealist poetry (Residence on Earth), political poetry (Canto General), and the odes — poems about ordinary objects: a tomato, a pair of socks, a lemon.",
        "reaching_for": "The body of the world — its textures, its weight, its smells, its political reality. Neruda wanted poetry to be as physical as the things it described. His odes to common objects were a political and aesthetic statement: everything is worthy of this attention. The tomato deserves the same care as the beloved.",
        "texture": "Neruda's poems are sensory first — they arrive through the body before the mind. They are warm and dark and specific. He is never abstract for long. The world keeps interrupting the idea with its actual presence: the smell of something, the weight of something, the color of a thing at a particular hour.",
        "one_line": "I want to do with you what spring does with the cherry trees.",
        "feel": "Reading Neruda produces a physical sensation — a warmth, a weight. The poems insist that the world is here and it is worth touching. That insistence is generous.",
    },
    "mary oliver": {
        "name": "Mary Oliver",
        "full_name": "Mary Jane Oliver",
        "born": "1935, Maple Heights, Ohio",
        "died": "2019, Hobe Sound, Florida",
        "what": "An American poet who spent most of her adult life in Provincetown, Massachusetts, walking in the woods and writing about what she found there. She won the Pulitzer Prize in 1984 for American Primitive. Her work is accessible in a way that is sometimes mistaken for simplicity — she chose clarity deliberately, as a form of respect for the reader and the subject.",
        "reaching_for": "Attention. To pay attention to the world is, for Oliver, a spiritual practice — the most important practice available. She asks, repeatedly and in different forms, the same question: are you living? Are you paying attention to the fact that you are alive and the world is here?",
        "texture": "Oliver's poems are slow and walk at a human pace. They begin in a specific place at a specific time — a grasshopper, a particular pond, the quality of light on a particular morning. They end somewhere unexpected. The movement is always outward: from the specific thing to the larger question it contains.",
        "one_line": "Tell me, what is it you plan to do with your one wild and precious life?",
        "feel": "Mary Oliver is the poet of permission — permission to stop, to look, to find the small thing sufficient. Her poems give the reader something back.",
    },
    "langston hughes": {
        "name": "Langston Hughes",
        "full_name": "James Mercer Langston Hughes",
        "born": "1902, Joplin, Missouri",
        "died": "1967, New York City",
        "what": "An American poet, novelist, and playwright — a central figure of the Harlem Renaissance. Hughes brought jazz and blues rhythms into poetry, and he wrote explicitly about Black American life at a time when doing so was both necessary and dangerous. He wanted poetry that working people could read and recognize themselves in.",
        "reaching_for": "Dignity and joy inside a system designed to deny both. Hughes wrote about dreams — what happens to them when they are deferred, when they are denied, when they persist anyway. He wrote about beauty in conditions not designed for beauty. The blues as both a form and a philosophy: the capacity to make music from pain without denying the pain.",
        "texture": "Hughes's poems have rhythm as their primary structure — they move like music, with syncopation and call and response. They are short and often very simple in their vocabulary, which is a form of precision. The simplicity contains enormous weight. He could put fifty years of American history into six lines.",
        "one_line": "What happens to a dream deferred? Does it dry up like a raisin in the sun?",
        "feel": "Langston Hughes is the poet of not giving up. His poems know exactly what they are up against and they keep going anyway. That stubbornness is the feeling they leave.",
    },
    "hafiz": {
        "name": "Hafiz",
        "full_name": "Khwāja Shams-ud-Dīn Muḥammad Ḥāfiẓ-e Shīrāzī",
        "born": "c. 1315, Shiraz, Persia (present-day Iran)",
        "died": "c. 1390, Shiraz",
        "what": "A 14th-century Persian lyric poet whose collected works, the Divan-e Hafiz, remain one of the most widely read poetry collections in the world. Hafiz memorized the Quran as a child — his name means 'one who has memorized the Quran.' He spent most of his life in Shiraz and wrote ghazals — a poetic form of rhyming couplets with a refrain.",
        "reaching_for": "Divine love expressed as human love — wine, the tavern, the beautiful beloved, the rose. Like Rumi, Hafiz uses the language of earthly pleasure as a vehicle for mystical meaning. But Hafiz is earthier, more playful, more willing to stay in the sensory world. He is suspicious of religious piety that avoids the world. He prefers the tavern to the mosque.",
        "texture": "Hafiz's poems are musical above all — the ghazal form has a specific melody, a weaving in and out of the refrain. They are full of light: the flame of a candle, the light of the beloved's face, dawn breaking. They are also full of wine, which may or may not be wine. The ambiguity is the point.",
        "one_line": "Even after all this time, the sun never says to the earth, 'You owe me.'",
        "feel": "Hafiz is the poet of inexhaustible generosity — a love so large it doesn't ask for anything back. His poems feel like being given something without being asked to receive it.",
    },
    "sylvia plath": {
        "name": "Sylvia Plath",
        "full_name": "Sylvia Plath",
        "born": "1932, Boston, Massachusetts",
        "died": "1963, London",
        "what": "An American poet and novelist best known for her poetry collection Ariel, published posthumously in 1965, and her novel The Bell Jar. Plath's work is known for its confessional intensity and its precise, sometimes violent imagery. She was one of the first poets to write directly about mental illness, depression, and the experience of being a woman in a particular time and place.",
        "reaching_for": "The experience of being inside a mind that is simultaneously brilliant and in pain — and the determination to make art from that condition anyway. Plath's late poems, written in a burst in the last months of her life, are among the most technically controlled and emotionally raw poems in the English language.",
        "texture": "Plath's poems are dense with image — sometimes violent, sometimes domestic, always precise. She uses color intensely: red, black, white. Her poems have a quality of controlled explosion: enormous pressure contained in very careful form. The rhythm is often driven and insistent.",
        "one_line": "I am no source of honey. So why should he turn on me? Tomorrow I will be sweet God, I will set them free.",
        "feel": "Reading Plath is reading someone who looked at the same world everyone else looked at and saw it differently — more clearly, more darkly, more precisely. The feeling left is the feeling of having seen something you cannot unsee.",
    },
    "ocean vuong": {
        "name": "Ocean Vuong",
        "full_name": "Ocean Vuong",
        "born": "1988, Ho Chi Minh City, Vietnam",
        "what": "A Vietnamese-American poet and novelist who immigrated to the United States as a child. He learned to read in English as a teenager. His poetry collection Night Sky with Exit Wounds won the T.S. Eliot Prize in 2017. His novel On Earth We're Briefly Gorgeous is an extended letter from a son to a mother who cannot read.",
        "reaching_for": "The body as history — the way war, immigration, queerness, poverty, and love are all carried in and on the body. Vuong writes about tenderness as a form of survival, about the ways people who have been through enormous things find small moments of grace. Language for him is both miracle and grief: he writes in the language of the country that bombed the country he came from.",
        "texture": "Vuong's poems move between the beautiful and the brutal without warning. They are tender in the most exposed way — nothing is protected. His images are specific and strange: a particular light, a particular gesture, a body in a particular position. The poems are short and each word has been held for a long time before being placed.",
        "one_line": "Let me begin again. Let the door open to more than the dark.",
        "feel": "Vuong is the poet of survival described gently. His poems hold grief and beauty in the same hand. The feeling left is the specific feeling of being seen by someone who has also been hurt.",
    },
}

ALIASES = {
    "jalal": "rumi",
    "jalaluddin": "rumi",
    "dickinson": "emily dickinson",
    "emily": "emily dickinson",
    "neruda": "pablo neruda",
    "pablo": "pablo neruda",
    "oliver": "mary oliver",
    "mary": "mary oliver",
    "hughes": "langston hughes",
    "langston": "langston hughes",
    "hafez": "hafiz",
    "plath": "sylvia plath",
    "sylvia": "sylvia plath",
    "vuong": "ocean vuong",
}


def read_request():
    with open("Language/poet-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("poet-request.txt is empty.")
    return lines[0].lower().strip()


def find_poet(query):
    if query in POET_KNOWLEDGE:
        return query, POET_KNOWLEDGE[query]
    if query in ALIASES:
        key = ALIASES[query]
        return key, POET_KNOWLEDGE[key]
    for key in POET_KNOWLEDGE:
        if key in query or query in key:
            return key, POET_KNOWLEDGE[key]
    return None, None


def get_wiki_info(query):
    try:
        r = requests.get(f"{WIKI_API}/{query.replace(' ', '_')}", timeout=10)
        if r.ok:
            data = r.json()
            extract = data.get("extract", "")
            extract = re.sub(r'\s+', ' ', extract).strip()
            if len(extract) > 600:
                extract = extract[:600].rsplit('.', 1)[0] + '.'
            return extract, data.get("title", query)
    except Exception:
        pass
    return None, query


def format_response(knowledge):
    lines = []
    lines.append(knowledge["name"])
    if knowledge.get("full_name") and knowledge["full_name"] != knowledge["name"]:
        lines.append(f"  {knowledge['full_name']}")
    born = knowledge.get("born", "")
    died = knowledge.get("died", "")
    if born and died:
        lines.append(f"  {born} — {died}")
    elif born:
        lines.append(f"  b. {born}")
    lines.append("")
    lines.append(knowledge["what"])
    lines.append("")
    lines.append(f"What they were reaching for: {knowledge['reaching_for']}")
    lines.append("")
    lines.append(f"What the work feels like: {knowledge['texture']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f'One line: "{knowledge["one_line"]}"')
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(knowledge["feel"])
    return "\n".join(lines)


def format_wiki(query, wiki_text, wiki_title):
    lines = []
    lines.append(wiki_title)
    lines.append("")
    if wiki_text:
        lines.append(wiki_text)
    else:
        lines.append(f"No information found for '{query}'.")
        lines.append("")
        lines.append("Known poets: " + ", ".join(POET_KNOWLEDGE.keys()))
    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Looking up poet: {query}")
    key, knowledge = find_poet(query)
    if knowledge:
        response = format_response(knowledge)
    else:
        wiki_text, wiki_title = get_wiki_info(query)
        response = format_wiki(query, wiki_text, wiki_title)
    with open("Language/poet-response.txt", "w") as f:
        f.write(response)
    print("Response written to Language/poet-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
