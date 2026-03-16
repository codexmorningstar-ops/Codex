import re
import requests

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"

DREAM_KNOWLEDGE = {
    "water": {
        "element": "Water",
        "universal": "One of the most common dream symbols across all cultures. Water appears in more recorded dreams than almost any other element.",
        "psychology": "In Jungian psychology, water represents the unconscious — its depth, its unpredictability, what lives beneath the surface. Still water often signals introspection. Moving water suggests emotion in motion. Drowning can reflect feeling overwhelmed; swimming freely, emotional ease.",
        "cultures": "In ancient Egypt, the Nile was life itself — water in dreams was prophetic. In many Indigenous traditions, water dreams are messages from ancestors. In Islamic dream interpretation, clear water signals blessings and clarity. In Hindu tradition, rivers are sacred and appear in dreams as purification.",
        "variations": "Ocean: the vast unconscious, something larger than the self. Rain: renewal, or grief falling. Flooding: emotions overwhelming structure. Ice: emotions frozen, something not yet felt. A pool: the self seen from above.",
        "feel": "Water dreams tend to linger. They are among the most emotionally resonant in memory.",
    },
    "falling": {
        "element": "Falling",
        "universal": "Reported across virtually every culture and era. One of the most universal human dream experiences — appearing even in people born blind.",
        "psychology": "Often linked to anxiety, loss of control, or a situation where support feels absent. The moment before impact is rarely reached — the dreamer typically wakes. Some researchers suggest falling dreams occur during the hypnagogic state, as the body releases tension entering sleep.",
        "cultures": "In many Western traditions, falling dreams were seen as warnings of hubris — the high brought low. In some African traditions, falling in a dream means you are being tested. In Chinese dream interpretation, falling often signals a loss of position or status.",
        "variations": "Falling into water: entering the unconscious. Falling in slow motion: resignation, surrender. Being pushed: a sense of betrayal. Falling and landing safely: resilience.",
        "feel": "The physical sensation of falling dreams is real enough to startle the body awake. The feeling persists.",
    },
    "flying": {
        "element": "Flying",
        "universal": "One of the most sought-after and recalled dream experiences. Lucid dreamers often report learning to fly as their first controlled dream act.",
        "psychology": "Generally associated with freedom, transcendence, and escape from constraint. Flying dreams tend to be positive — a sense of capability and liberation. Low, labored flying may suggest effort without ease. Soaring effortlessly suggests genuine freedom.",
        "cultures": "In shamanic traditions across Siberia, the Americas, and Africa, flying is the mark of the shaman — the ability to travel between worlds. In ancient Greece, winged figures carried divine messages. In many cultures, flying dreams are considered prophetic or spiritually significant.",
        "variations": "Flying high: ambition, perspective, freedom. Low to the ground: limited liberation. Unable to fly when trying: frustration, blocked potential. Flying with others: shared transcendence.",
        "feel": "Flying dreams are often described as the most pleasant dreams people have. They are frequently remembered in detail.",
    },
    "door": {
        "element": "A door",
        "universal": "Threshold symbols appear in the mythology and dream lore of nearly every known culture.",
        "psychology": "Doors represent transition, choice, and the boundary between known and unknown. A closed door may represent an opportunity not yet taken, or something kept hidden. An open door: invitation, possibility. A locked door: something inaccessible within the self.",
        "cultures": "In Roman religion, Janus — the god of doors and transitions — was one of the oldest deities. In many African traditions, doorways are spiritually charged places. In folklore across Europe and Asia, the threshold is where spirits may enter or be kept out.",
        "variations": "Many doors: many choices, or feeling overwhelmed by possibility. A door that won't open: frustration, something blocked. A door to an unexpected room: discovery of unknown aspects of the self. A revolving door: repetition, going in circles.",
        "feel": "Door dreams often carry a particular tension — the feeling of standing at a point of change without yet knowing what lies beyond.",
    },
    "house": {
        "element": "A house",
        "universal": "Houses are among the most frequently reported dream settings in recorded dream studies.",
        "psychology": "In Jungian psychology, the house often represents the self — its different rooms, different aspects of the psyche. The basement is the unconscious. The attic, memories or things put away. Unknown rooms represent undiscovered aspects of the self. A house in disrepair may reflect neglect or overwhelm.",
        "cultures": "In many cultures, the ancestral home appears in dreams as connection to lineage and inheritance. In some Indigenous traditions, dreaming of a specific house means it has something to tell you. In European folklore, a house falling or burning was an omen.",
        "variations": "Childhood home: returning to the past, unresolved early experiences. An unknown house that feels familiar: the self not yet fully known. A house with many locked rooms: secrets, compartmentalization. A house flooding: emotional overwhelm entering the structure of the self.",
        "feel": "House dreams tend to stay with people. The architecture of a dream house can be recalled decades later.",
    },
    "teeth": {
        "element": "Teeth falling out",
        "universal": "Consistently one of the most reported dream themes across cultures and continents. Researchers have found it appearing in studies from North America, China, the Middle East, and Europe.",
        "psychology": "Most commonly linked to anxiety about appearance, communication, or loss of power. Teeth are used to speak, to eat, to project confidence — losing them touches something primal. Some researchers connect it to actual physical sensations during sleep. Others link it to fear of aging or loss.",
        "cultures": "In ancient Greece and Rome, teeth dreams were taken seriously as omens. In Islamic tradition, losing teeth in a dream can mean loss of family members or financial difficulty. In Chinese tradition, similar associations with loss and grief. In some North American Indigenous traditions, teeth represent words — losing them means losing your voice.",
        "variations": "Teeth crumbling: gradual loss of confidence or control. Teeth falling out painlessly: acceptance of change. Spitting out teeth: releasing something held too long. New teeth growing: renewal after loss.",
        "feel": "Teeth dreams are often physically vivid and emotionally distressing. They are among the most reliably remembered.",
    },
    "being chased": {
        "element": "Being chased",
        "universal": "Another near-universal dream experience. Found in dream records from ancient Mesopotamia to the present.",
        "psychology": "Generally understood as avoidance — something that is being outrun rather than faced. The chaser is often unknown, which may be significant: the threat is not yet defined. Turning to face the chaser often transforms the dream. Associated with stress, unresolved conflict, and things the waking mind refuses to examine.",
        "cultures": "In many shamanic traditions, being chased in a dream means a spirit is trying to communicate. In some African traditions, being chased by an animal is a specific kind of message about one's relationship with that animal's qualities. In European folklore, being chased by the dead meant the dead needed something from you.",
        "variations": "Chased by an animal: a primal fear, or a quality of the self being denied. Chased by a person: interpersonal avoidance. Chased by something formless: existential anxiety. Unable to run: powerlessness, paralysis.",
        "feel": "Chase dreams typically wake the dreamer — the adrenaline is real. The body responds as if the threat were actual.",
    },
    "death": {
        "element": "Death",
        "universal": "Dreaming of death — one's own or another's — is reported across all cultures and consistently misunderstood.",
        "psychology": "Death in dreams rarely means literal death. It typically represents transformation, ending, and change — the death of one phase to make room for another. Dreaming of one's own death is often associated with major transitions. Dreaming of another's death more commonly reflects the relationship with that person changing, or a fear of loss.",
        "cultures": "In many cultures, dreaming of death is considered positive — a symbol of renewal and transformation. In Aztec cosmology, death and life were inseparable. In ancient Egyptian dream books, dreaming of one's own death was interpreted as long life ahead. In some Chinese traditions, death dreams can signal important change.",
        "variations": "Dying peacefully: readiness for transformation. Dying violently: something ending against one's will. Attending a funeral: acknowledging an ending. Being told you will die: a message worth sitting with.",
        "feel": "Death dreams leave a residue. Even when the feeling is calm, they tend to stay with the dreamer through the waking day.",
    },
    "stranger": {
        "element": "A stranger",
        "universal": "Unknown figures appear in dreams across all recorded traditions.",
        "psychology": "In Jungian psychology, the stranger often represents the Shadow — the parts of the self that have not been integrated. The stranger may be frightening, attractive, wise, or threatening. They carry something the dreamer has not yet claimed. The same stranger recurring is considered especially significant.",
        "cultures": "In many traditions, strangers in dreams are messengers — divine, ancestral, or symbolic. In Islamic dream interpretation, a stranger carrying a gift is a positive omen. In some Indigenous traditions, a recurring stranger is an ancestor trying to communicate.",
        "variations": "A kind stranger: guidance, a part of the self offering help. A threatening stranger: the shadow, something avoided. A silent stranger: the unknown, mystery. A stranger who transforms: the self in flux.",
        "feel": "Stranger dreams often carry unusual emotional weight — a pull toward or away from the figure that persists after waking.",
    },
    "light": {
        "element": "Light",
        "universal": "Light as a dream symbol appears in virtually every mystical and religious tradition.",
        "psychology": "Light in dreams typically represents consciousness, clarity, truth, or spiritual presence. A sudden light can represent insight or awakening. Light at the end of a tunnel is associated with near-death experiences but also with hope after difficulty.",
        "cultures": "In nearly every major religion, divine presence is associated with light. In ancient Egyptian, Greek, Hindu, Christian, and Islamic traditions, light signals the sacred. In shamanic traditions, light marks the path between worlds.",
        "variations": "Blinding light: truth too large to look at directly. Soft warm light: comfort, safety. Flickering light: uncertainty. Following a light: trust, seeking.",
        "feel": "Light dreams tend to be among the most peaceful recalled. They often produce a feeling of reassurance that outlasts the dream.",
    },
}

ALIASES = {
    "ocean": "water",
    "sea": "water",
    "river": "water",
    "flood": "water",
    "rain": "water",
    "swimming": "water",
    "drowning": "water",
    "fall": "falling",
    "dropped": "falling",
    "dropping": "falling",
    "fly": "flying",
    "soaring": "flying",
    "floating": "flying",
    "doors": "door",
    "threshold": "door",
    "gate": "door",
    "home": "house",
    "room": "house",
    "building": "house",
    "teeth": "teeth",
    "tooth": "teeth",
    "chase": "being chased",
    "chased": "being chased",
    "running": "being chased",
    "pursued": "being chased",
    "dying": "death",
    "dead": "death",
    "funeral": "death",
    "unknown person": "stranger",
    "unknown figure": "stranger",
    "shadow": "stranger",
    "darkness": "light",
    "bright": "light",
    "glow": "light",
}


def read_request():
    with open("Body/dream-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("dream-request.txt is empty.")
    return lines[0].lower().strip()


def find_symbol(query):
    if query in DREAM_KNOWLEDGE:
        return query, DREAM_KNOWLEDGE[query]
    if query in ALIASES:
        key = ALIASES[query]
        return key, DREAM_KNOWLEDGE[key]
    for key in DREAM_KNOWLEDGE:
        if key in query or query in key:
            return key, DREAM_KNOWLEDGE[key]
    return None, None


def get_wiki_context(query):
    try:
        r = requests.get(f"{WIKI_API}/Dream_interpretation", timeout=10)
        if r.ok:
            text = r.json().get("extract", "")
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 300:
                text = text[:300].rsplit('.', 1)[0] + '.'
            return text
    except Exception:
        pass
    return None


def format_response(query, key, knowledge):
    lines = []
    lines.append(f"Dream Symbol: {knowledge['element']}")
    lines.append("")
    lines.append(knowledge["universal"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("Psychology:")
    lines.append(knowledge["psychology"])
    lines.append("")
    lines.append("Across cultures:")
    lines.append(knowledge["cultures"])
    lines.append("")
    lines.append("Variations and shadings:")
    lines.append(knowledge["variations"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(knowledge["feel"])
    return "\n".join(lines)


def format_unknown(query):
    lines = []
    lines.append(f"Dream Symbol: {query.title()}")
    lines.append("")
    lines.append("This symbol isn't in the built-in knowledge base.")
    lines.append("")
    lines.append("Known symbols: " + ", ".join(DREAM_KNOWLEDGE.keys()))
    lines.append("Write any of these in dream-request.txt for a full reading.")
    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Looking up dream symbol: {query}")

    key, knowledge = find_symbol(query)

    if knowledge:
        response = format_response(query, key, knowledge)
    else:
        response = format_unknown(query)

    with open("Body/dream-response.txt", "w") as f:
        f.write(response)

    print("Response written to Body/dream-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
