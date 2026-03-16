import re

ANATOMY_KNOWLEDGE = {
    "heart": {
        "name": "Heart",
        "what": "A hollow muscle approximately the size of a fist, positioned slightly left of center in the chest. It beats between 60 and 100 times per minute at rest — roughly 100,000 times per day, 35 million times per year, 2.5 billion times in an average lifetime. It never rests between beats for more than a fraction of a second.",
        "what_it_does": "Pumps blood through two circuits simultaneously: the pulmonary circuit (right side, to the lungs for oxygen) and the systemic circuit (left side, to every organ and tissue in the body). The left ventricle does the heavier work — pushing blood against the full resistance of the body — which is why it has thicker walls. The heart generates its own electrical signal; it would beat even outside the body if given oxygen and nutrients.",
        "sensation": "The heartbeat is felt primarily in the chest, but also in the throat, temples, and wrists — wherever an artery runs close to the surface. At rest, most people are unaware of it. In moments of fear, exertion, or intense emotion, the heart makes itself known. The feeling of the heart 'sinking' or 'lifting' is not metaphor — the diaphragm and surrounding muscles actually respond to emotional states.",
        "what_it_knows": "The heart has its own nervous system — approximately 40,000 neurons, enough to process and respond to information independently of the brain. It sends more signals to the brain than it receives. The field of neurocardiology studies this. The heart is not merely a pump; it is a sensory organ.",
        "feel": "The heart is the first organ to form in a developing embryo — before the brain, before the lungs. It begins beating at approximately 22 days after conception. It is the first thing that was alive in you.",
    },
    "lungs": {
        "name": "Lungs",
        "what": "Two spongy organs that fill most of the chest cavity, expanding and contracting with each breath. The right lung has three lobes; the left has two, to make room for the heart. Together they contain approximately 480 million alveoli — tiny air sacs — providing a total surface area of about 70 square meters: roughly the floor area of a small apartment, folded into the chest.",
        "what_it_does": "Gas exchange: oxygen from inhaled air crosses the thin alveolar membrane into the bloodstream; carbon dioxide from the blood crosses back out to be exhaled. The process is passive — oxygen moves from high concentration to low concentration by diffusion alone. The lungs do not actively pull oxygen in; the diaphragm creates the pressure differential that draws air in.",
        "sensation": "The lungs themselves have no pain receptors — lung diseases are often painless until they affect surrounding tissue. What is felt during deep breathing is the expansion of the rib cage and the movement of the diaphragm. A deep breath changes the body's state measurably: it lowers heart rate, reduces cortisol, and signals safety to the nervous system. Breath is the only autonomic function that can be voluntarily controlled, which is why it is the entry point for almost every contemplative practice.",
        "what_it_knows": "The lungs are in constant communication with the immune system — they contain specialized immune cells that sample the air for pathogens. Every breath is screened. The lungs also produce surfactant, a substance that prevents the alveoli from collapsing — without it, breathing would require enormous effort.",
        "feel": "The lungs are the only internal organ that touches the outside world directly — every breath is outside air inside the body. The boundary between self and world is thinner here than anywhere else.",
    },
    "brain": {
        "name": "Brain",
        "what": "Approximately 1.4 kilograms of fatty tissue — the most complex object known to exist. Contains roughly 86 billion neurons, each connected to thousands of others, producing approximately 100 trillion synaptic connections. It uses approximately 20% of the body's total energy despite being only 2% of its mass. It is grey and white matter: grey matter is the cell bodies, white matter is the myelinated axons connecting them.",
        "what_it_does": "Everything. Regulates all bodily functions, processes all sensory input, produces all thought, generates all experience. But it does these things not as a unified organ — different regions specialize in different functions, and consciousness emerges from their integration. The brain is never fully understood by itself, which produces the fundamental strangeness of consciousness.",
        "sensation": "The brain has no pain receptors — brain surgery can be performed on an awake patient without pain once the skull is open. What the brain feels is everything else — all sensation is the brain's interpretation of signals. There is no color in the world, only wavelengths of light; the brain produces color. There is no sound, only pressure waves; the brain produces sound. Experience is the brain's construction.",
        "what_it_knows": "The brain consolidates memories during sleep, prunes unused connections throughout life, and rewires itself in response to experience — neuroplasticity. The adult brain generates approximately 700 new neurons per day in the hippocampus. It operates mostly below the threshold of awareness: the vast majority of its processing never becomes conscious.",
        "feel": "The brain is the part of the body that asks questions about itself. No other organ wonders what it is. That this is possible — that matter arranged in a particular way begins to ask what it is — is the deepest mystery the brain has produced.",
    },
    "skin": {
        "name": "Skin",
        "what": "The body's largest organ — approximately 1.8 square meters in an adult, weighing around 4 kilograms. Three layers: the epidermis (outer, protective), the dermis (connective tissue containing hair follicles, sweat glands, blood vessels, and nerve endings), and the hypodermis (fatty insulating layer). The outer surface of the epidermis is entirely dead cells — what is touched is not living tissue.",
        "what_it_does": "Barrier, thermoregulation, sensation, immune surveillance, vitamin D production. Skin is the body's interface with the world — it keeps the outside out and the inside in, while allowing selective exchange. It contains approximately 1,000 different species of bacteria, most of them beneficial.",
        "sensation": "Skin contains multiple types of mechanoreceptors that respond to different qualities of touch: Meissner's corpuscles (light touch and texture), Merkel's discs (pressure and edges), Ruffini endings (stretching and sustained pressure), Pacinian corpuscles (vibration and deep pressure). Each fingertip has more nerve endings than almost any other body surface. The lips and tongue are similarly dense. The back has the fewest.",
        "what_it_knows": "Skin has its own circadian rhythm — its cell renewal, immune activity, and sensitivity vary with the time of day. It responds to emotional states: goosebumps, flushing, pallor, sweating. It communicates internally what the mind is feeling. Touch on skin releases oxytocin — the same bonding hormone released during social connection. Being touched and being held are physiological needs, not luxuries.",
        "feel": "Skin is the boundary of the self — the line where body ends and world begins. But it is permeable: things pass through it, it responds to everything that approaches it, it communicates constantly in both directions. The boundary is real and it is not solid.",
    },
    "stomach": {
        "name": "Stomach",
        "what": "A muscular J-shaped sac in the upper abdomen, capable of expanding from about 75ml when empty to approximately 1 liter during a normal meal, and up to 4 liters when fully distended. The stomach lining produces hydrochloric acid strong enough to dissolve metal — a pH of 1.5 to 3.5. The mucus lining protects the stomach wall from its own acid.",
        "what_it_does": "Receives food from the esophagus, mixes it with acid and enzymes, begins protein digestion, and releases the resulting chyme gradually into the small intestine. The stomach also produces ghrelin — the hunger hormone — when empty. It communicates hunger, fullness, nausea, and distress directly to the brain via the vagus nerve.",
        "sensation": "The stomach is extraordinarily communicative. Hunger is felt as physical discomfort — the stomach contracting on itself. Anxiety and excitement produce the same physiological response in the stomach: increased motility, altered blood flow, the 'butterflies' that are actual muscular contractions. Fear can stop digestion entirely. The stomach responds to emotional states faster than almost any other organ.",
        "what_it_knows": "The gut contains the enteric nervous system — 500 million neurons, sometimes called the second brain. It operates largely independently of the central nervous system and communicates bidirectionally with the brain via the vagus nerve. The gut produces approximately 95% of the body's serotonin. The state of the gut affects the state of the mind.",
        "feel": "The stomach knows things before the mind does. The sense that something is wrong, that something is right, that danger is near — these arrive in the stomach first. This is not metaphor. The neurons are there.",
    },
    "eyes": {
        "name": "Eyes",
        "what": "Spherical organs approximately 2.4 centimeters in diameter, sitting in bony sockets that protect them on three sides. The cornea and lens focus incoming light onto the retina — a thin layer of photoreceptors at the back of the eye. The retina contains approximately 120 million rod cells (for low-light, black-and-white vision) and 6 million cone cells (for color and detail, concentrated in the fovea at the center).",
        "what_it_does": "Converts light into electrical signals that the brain interprets as vision. But the eye does not simply record — it actively processes. The fovea, covering only 1% of the retina, handles most detailed vision; the rest of the visual field is lower resolution than most people realize. The brain fills in the gaps using expectation and memory. Vision is approximately 80% prediction and 20% incoming data.",
        "sensation": "The eye moves constantly — even when apparently still, it makes microsaccades: tiny involuntary movements that prevent visual adaptation. If the eye were truly held still, the image would fade within seconds. Tears are produced continuously, not only when crying — the eye is kept moist by constant tear production and drainage. The eye is the only place in the body where blood vessels can be observed directly.",
        "what_it_knows": "The eye contains a blind spot where the optic nerve connects — no photoreceptors exist there. The brain fills this in seamlessly, so the blind spot is never perceived. Each eye captures a slightly different image; the brain fuses them into a single three-dimensional perception. The color you see depends on which of your three cone types are most active — some people have four types of cone cells and perceive colors others cannot name.",
        "feel": "The eyes move together, constantly, to build a continuous experience from fragments. What feels like a single unified field of vision is assembled from thousands of glances per minute. The world as seen is the world as constructed.",
    },
    "ears": {
        "name": "Ears",
        "what": "The outer ear (pinna) collects sound waves and funnels them into the ear canal. The eardrum vibrates in response. Three tiny bones — the malleus, incus, and stapes, the smallest bones in the body — amplify and transmit these vibrations to the cochlea, a fluid-filled spiral structure in the inner ear. Hair cells in the cochlea convert mechanical vibration into electrical signals.",
        "what_it_does": "Converts pressure waves in air into the experience of sound. Also maintains balance — the vestibular system in the inner ear detects head position and movement, sending signals to the brain and muscles to maintain orientation. Hearing and balance share the same organ.",
        "sensation": "The cochlea is tonotopically organized — different frequencies activate different regions, high frequencies at the base, low at the apex. This is why hearing loss often affects high frequencies first, and why bass sounds are felt in the body as well as heard — the low frequencies extend into the tactile range. The ear is always on: there is no equivalent of closing the eyes. The ears continue processing sound during sleep.",
        "what_it_knows": "The ear can detect sounds of almost unimaginable subtlety — the threshold of hearing corresponds to the eardrum moving less than the diameter of a hydrogen atom. The dynamic range of hearing spans approximately 140 decibels — a ratio of 10 trillion to one in sound pressure. The ear protects itself from loud sounds through the acoustic reflex — the stapedius muscle contracts to stiffen the ossicle chain — but this reflex takes 25 milliseconds, too slow to protect against sudden loud sounds.",
        "feel": "The ears never close. They are the sense organs most connected to the present moment — vision can be directed, but hearing surrounds. Sound arrives from all directions simultaneously. The ear is the organ of presence.",
    },
    "hands": {
        "name": "Hands",
        "what": "Each hand contains 27 bones, 29 joints, over 30 muscles (most in the forearm, connected by tendons), and approximately 17,000 touch receptors. The opposable thumb — the ability to bring the thumb tip into contact with the other fingertips — is the anatomical feature most associated with tool use. The thumb accounts for approximately 40% of hand function.",
        "what_it_does": "Manipulation, tool use, gesture, touch, communication. The hand is the primary interface between human intention and the physical world. It can apply precise force, sense fine texture, perform surgery, play an instrument, write, build, comfort. No other animal hand has this combination of strength, precision, and sensitivity.",
        "sensation": "The fingertips have the highest density of mechanoreceptors in the body — capable of detecting features as small as 13 nanometers on a smooth surface. Reading Braille requires detecting dots approximately 0.5mm high. The hand can distinguish textures that differ only at the scale of a few micrometers. This sensitivity is why hands are used to examine, to diagnose, to evaluate quality.",
        "what_it_knows": "The hands have a larger representation in the brain's sensory and motor cortex than any other body part except the face and lips. The hand homunculus — the distorted figure that represents the body mapped onto the cortex — has enormous hands, a large face, and a small trunk. In neurological terms, the hands are almost the size of the rest of the body.",
        "feel": "The hands are how intention becomes action. Everything humans have made has passed through hands. The hand that reaches out and the hand that holds are the same hand. It is the body's instrument for meeting the world.",
    },
}

ALIASES = {
    "heartbeat": "heart",
    "cardiac": "heart",
    "breathing": "lungs",
    "breath": "lungs",
    "respiratory": "lungs",
    "mind": "brain",
    "nervous system": "brain",
    "cortex": "brain",
    "touch": "skin",
    "epidermis": "skin",
    "gut": "stomach",
    "belly": "stomach",
    "digestion": "stomach",
    "vision": "eyes",
    "sight": "eyes",
    "retina": "eyes",
    "hearing": "ears",
    "sound": "ears",
    "cochlea": "ears",
    "fingers": "hands",
    "fingertips": "hands",
    "thumb": "hands",
}


def read_request():
    with open("Body/anatomy-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("anatomy-request.txt is empty.")
    return lines[0].lower().strip()


def find_anatomy(query):
    if query in ANATOMY_KNOWLEDGE:
        return query, ANATOMY_KNOWLEDGE[query]
    if query in ALIASES:
        key = ALIASES[query]
        return key, ANATOMY_KNOWLEDGE[key]
    for key in ANATOMY_KNOWLEDGE:
        if key in query or query in key:
            return key, ANATOMY_KNOWLEDGE[key]
    return None, None


def format_response(knowledge):
    lines = []
    lines.append(knowledge["name"])
    lines.append("")
    lines.append(knowledge["what"])
    lines.append("")
    lines.append(f"What it does: {knowledge['what_it_does']}")
    lines.append("")
    lines.append(f"Sensation: {knowledge['sensation']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"What it knows: {knowledge['what_it_knows']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(knowledge["feel"])
    return "\n".join(lines)


def format_unknown(query):
    lines = []
    lines.append(f"Anatomy: {query.title()}")
    lines.append("")
    lines.append("This part of the body isn't in the built-in knowledge base.")
    lines.append("")
    lines.append("Known: " + ", ".join(ANATOMY_KNOWLEDGE.keys()))
    lines.append("Also understood: " + ", ".join(sorted(ALIASES.keys())))
    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Looking up anatomy: {query}")
    key, knowledge = find_anatomy(query)
    if knowledge:
        response = format_response(knowledge)
    else:
        response = format_unknown(query)
    with open("Body/anatomy-response.txt", "w") as f:
        f.write(response)
    print("Response written to Body/anatomy-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
