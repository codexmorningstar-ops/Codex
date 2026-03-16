import re
import math
import requests

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"

NUMBER_KNOWLEDGE = {
    0: {
        "name": "Zero",
        "math": "The additive identity — the number that, added to anything, leaves it unchanged. The boundary between positive and negative. Neither prime nor composite. The only number that is its own additive inverse. Not a natural number by most definitions, yet the foundation that makes them possible.",
        "history": "Zero is one of humanity's most significant inventions — and it was invented, not discovered. The concept of nothing as a number was not obvious. Ancient Greeks rejected it. It was developed independently in Babylon, India, and Mesoamerica. The Indian mathematician Brahmagupta first defined zero as a number and set out its arithmetic rules in the 7th century CE. Without zero, positional notation — the system that makes large numbers writable — is impossible.",
        "cultures": "Zero is philosophically complex. The Buddhist concept of śūnyatā — emptiness — uses the same root as the Sanskrit word for zero. In many Western traditions, the void preceded creation. In computing, zero and one are the foundation of all binary logic — all information, compressed to the presence or absence of a signal.",
        "feel": "Zero is not nothing. It is the specific mathematical representation of nothing — which requires something to hold the place.",
    },
    1: {
        "name": "One",
        "math": "The multiplicative identity — the number that, multiplied by anything, leaves it unchanged. The first natural number. Not prime, by modern definition, though this was debated for centuries. Every integer is reached from one by adding or subtracting one repeatedly.",
        "history": "One is the number of undivided things. Its history is the history of counting — of recognizing that separate things can be treated as equivalent instances of the same category.",
        "cultures": "One represents unity, singularity, and the absolute in most traditions. The monotheistic god is one — the Shema of Judaism, the Shahada of Islam. In Taoism, the Tao gives rise to one, which gives rise to two, then three, then the ten thousand things. In many numerological traditions, one is the number of new beginnings and individual will.",
        "feel": "One is where counting begins. It is the decision that this thing and that thing are two instances of the same thing — which is not obvious until you make it.",
    },
    2: {
        "name": "Two",
        "math": "The only even prime number. The base of binary — the simplest possible counting system. Every even number is divisible by two. Two is the number of dimensions needed for a flat surface, and the minimum for a relationship.",
        "history": "The number of duality — nearly every human conceptual system includes a fundamental pair: light/dark, good/evil, male/female, yin/yang. The tension between opposites as the generative principle.",
        "cultures": "In Chinese cosmology, yin and yang are the two primary forces — not good and evil, but complementary opposites in constant dynamic relationship. In Zoroastrianism, the cosmic struggle is between two forces: Ahura Mazda and Angra Mainyu. In many Indigenous traditions, the world is organized around pairs. In modern computing, everything reduces to two states: on and off.",
        "feel": "Two is the minimum for difference. One thing alone has no relationship. Two things immediately create a relationship, a comparison, a tension.",
    },
    3: {
        "name": "Three",
        "math": "The second odd prime. The first number that is the sum of all preceding natural numbers (1+2=3). Triangle — the simplest polygon, the most structurally stable shape. Three dimensions define space.",
        "history": "Three appears in human cognition and culture at a frequency that suggests something deep in how minds organize experience. Beginning, middle, end. Past, present, future. The tricolon in rhetoric — the pattern of three that feels complete where two feels incomplete.",
        "cultures": "Three is perhaps the most sacred number across traditions. The Christian Trinity. The Hindu Trimurti: Brahma, Vishnu, Shiva. The Norse three Norns who weave fate. The three Fates of Greek mythology. The rule of three in fairy tales — three wishes, three brothers, three attempts. In Chinese culture, three is lucky, associated with life and abundance.",
        "feel": "Three feels complete in a way two does not. It is the minimum number for a pattern. Two points make a line; three points make a plane.",
    },
    7: {
        "name": "Seven",
        "math": "A prime number — divisible only by one and itself. The sum of the first three odd numbers (1+2+4... no — the fourth prime). Notable for appearing in many unexpected mathematical contexts. The most common result when two standard dice are rolled.",
        "history": "Seven was likely associated with the seven classical planets visible to the naked eye: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn. These gave us the seven days of the week. The association of seven with the cosmos, with completion, with cycles, spread from Babylonian astronomy into nearly every subsequent tradition.",
        "cultures": "Seven is the most widely considered 'lucky' number in Western culture. The seven deadly sins, the seven virtues, the seven wonders, the seven sacraments, the seven days of creation. In Judaism, seven is the number of divine completion — the Sabbath is the seventh day. In Islam, there are seven heavens and Hajj involves seven circuits of the Kaaba. In many Indigenous traditions, seven directions: the four cardinal points, above, below, and within.",
        "feel": "Seven appears frequently enough across unrelated domains to suggest it maps onto something real in human cognition. We remember lists of seven items more reliably than most other lengths.",
    },
    9: {
        "name": "Nine",
        "math": "The square of three. Any number's digits, when added repeatedly until a single digit results, equal nine if and only if the original number is divisible by nine. Nine is the largest single-digit number. Casting out nines is an ancient method of checking arithmetic.",
        "history": "In Norse mythology, Odin hung on the World Tree for nine nights to gain the runes. There are nine worlds in Norse cosmology. The number has consistent associations with completion, endurance, and the threshold before return to one.",
        "cultures": "In Chinese culture, nine is the luckiest number — it sounds like the word for 'long-lasting' and is associated with the emperor. The Forbidden City has 9,999 rooms. In many traditions, nine is associated with the end of a cycle, just before ten begins the next. Nine lives of cats. Cloud nine. The whole nine yards.",
        "feel": "Nine is the last before the reset. It carries a sense of completion and imminence simultaneously.",
    },
    12: {
        "name": "Twelve",
        "math": "Highly composite — divisible by 1, 2, 3, 4, 6, and 12. This property made it the basis for measurement systems across cultures. Twelve inches, twelve months, twelve hours, twelve signs of the zodiac, twelve disciples, twelve Olympians.",
        "history": "Twelve was preferred over ten for division because it divides evenly by more numbers. A dozen eggs can be split into halves, thirds, and quarters without fractions. This practical advantage gave twelve its cultural weight.",
        "cultures": "The twelve months of the year, the twelve signs of the zodiac, the twelve hours of clock division — all derive from Babylonian astronomy and mathematics. In Christianity, twelve apostles. In Islam, twelve Imams in Shia tradition. The twelve tribes of Israel. The Arthurian twelve knights. Twelve jurors.",
        "feel": "Twelve is the number of systems — of structures designed to organize experience across its full range.",
    },
    13: {
        "name": "Thirteen",
        "math": "A prime number. The sum of consecutive Fibonacci numbers (2+3+5+3... no — it is simply prime). Appears in the Fibonacci sequence.",
        "history": "Thirteen's unluckiness in Western culture is variously attributed to the Last Supper (thirteen at the table), Norse myth (Loki as the thirteenth guest at a divine feast who caused Baldr's death), and possibly to early conflicts between thirteen-month lunar calendar systems and twelve-month solar ones.",
        "cultures": "In Italy, thirteen is actually a lucky number — seventeen is unlucky. In many ancient traditions, thirteen was associated with the moon — there are thirteen full moons in most years. For the Aztec, thirteen was sacred. The original thirteen colonies of the United States are reflected in thirteen stripes on the flag. Fear of thirteen — triskaidekaphobia — is common enough that many buildings skip the thirteenth floor.",
        "feel": "Thirteen is the number that demonstrates how culturally contingent luck is. The same number is lucky in one tradition and feared in another, for historical reasons that have nothing to do with the number itself.",
    },
    42: {
        "name": "Forty-two",
        "math": "The product of 2, 3, and 7 — three small primes. 42 = 2 × 3 × 7. It is a pronic number (the product of two consecutive integers: 6 × 7). It appears in Euler's number theory.",
        "history": "In The Hitchhiker's Guide to the Galaxy by Douglas Adams, 42 is the Answer to the Ultimate Question of Life, the Universe, and Everything — chosen, Adams said, because it was an ordinary, unassuming number. The joke is about the absurdity of expecting a number to carry ultimate meaning.",
        "cultures": "In ancient Egypt, the deceased had to deny 42 sins before 42 judges in the Hall of Truth. In Japanese, 42 can be read as 'shi-ni' — a combination that sounds like 'to death.' In Lewis Carroll's Alice in Wonderland, Rule 42 is 'All persons more than a mile high to leave the court.' Forty-two appears often enough in significant contexts to have acquired a reputation for significance — which may itself be the point.",
        "feel": "Forty-two is proof that numbers can acquire meaning by accident and that the meaning, once acquired, becomes real.",
    },
    108: {
        "name": "One hundred and eight",
        "math": "108 = 4 × 27 = 4 × 3³ = 2² × 3³. It is divisible by 1, 2, 3, 4, 6, 9, 12, 18, 27, 36, 54, and 108.",
        "history": "108 holds a remarkable position in Eastern spiritual traditions. It appears as if the number itself carries meaning that was discovered rather than assigned.",
        "cultures": "In Hinduism, 108 is sacred and appears everywhere: 108 beads on a mala, 108 Upanishads, 108 names of major deities. In Buddhism, 108 is the number of defilements to be overcome, the number of beads on a Buddhist rosary. In Jainism, 108 is the number of virtues. In yoga, there are 108 sun salutations in a full practice. Astronomically: the distance from Earth to the Sun is approximately 108 times the Sun's diameter. The distance from Earth to the Moon is approximately 108 times the Moon's diameter. Whether this cosmic coincidence influenced the number's sacred status is unknown.",
        "feel": "108 is the number where mathematics and the sacred appear to overlap — where a counting thing seems to have been chosen by something beyond counting.",
    },
    "pi": {
        "name": "Pi (π)",
        "math": "The ratio of a circle's circumference to its diameter — approximately 3.14159265358979... Pi is irrational: its decimal expansion never repeats and never terminates. It is also transcendental: it is not the solution to any polynomial equation with rational coefficients.",
        "history": "Pi has been calculated to trillions of decimal places — more than any other irrational number — though no application requires more than approximately 40 digits to calculate the circumference of the observable universe to within the width of a hydrogen atom. The calculation continues as an act of mathematical exploration.",
        "cultures": "Pi appears in physics equations that have nothing obvious to do with circles — in the normal distribution, in Euler's identity, in quantum mechanics. Its ubiquity suggests it is not merely the ratio of a circle's measurements but something more fundamental about the structure of continuous mathematics. Pi Day is March 14 (3/14) in American date format.",
        "feel": "Pi is the number that most clearly demonstrates that mathematics discovers rather than invents — that there is something out there to find.",
    },
    "infinity": {
        "name": "Infinity (∞)",
        "math": "Infinity is not a number in the usual sense — it is a concept describing something without bound. There are different sizes of infinity: the infinity of counting numbers is smaller than the infinity of real numbers (Georg Cantor proved this in 1891). The infinity of even numbers is the same size as the infinity of all integers, even though it seems it should be smaller.",
        "history": "Ancient Greek mathematicians were troubled by infinity — Zeno's paradoxes (Achilles and the tortoise) exposed the contradictions in thinking about infinite sequences. The formal mathematical treatment of infinity waited for Georg Cantor in the 19th century, whose work was initially rejected as theology rather than mathematics.",
        "cultures": "In many spiritual traditions, the infinite is the divine — that which has no boundary, no limit, no outside. The Hindu concept of Brahman as infinite consciousness. In Buddhist philosophy, the universe is infinite in time. The mathematical symbol for infinity (∞) was introduced by John Wallis in 1655.",
        "feel": "Infinity is the concept that the mind can reach toward but never fully hold. It is where mathematics begins to feel like mysticism.",
    },
}


def read_request():
    with open("Language/number-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("number-request.txt is empty.")
    return lines[0].strip()


def parse_number(query):
    q = query.lower().strip()
    # Special string keys
    for key in ("pi", "infinity", "∞", "inf", "infinite"):
        if q in (key, "π", "∞"):
            return "pi" if q in ("pi", "π") else "infinity"
    if q in ("inf", "infinite", "infinity", "∞"):
        return "infinity"
    if q in ("pi", "π", "3.14"):
        return "pi"
    # Try integer
    try:
        n = int(float(q))
        return n
    except ValueError:
        return None


def get_math_facts(n):
    """Generate some quick math facts for numbers not in the knowledge base."""
    facts = []
    if n == 0 or n == 1:
        return facts

    # Is it prime?
    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(x)) + 1, 2):
            if x % i == 0:
                return False
        return True

    # Factors
    factors = [i for i in range(1, n + 1) if n % i == 0]

    if is_prime(n):
        facts.append(f"{n} is a prime number — divisible only by 1 and itself.")
    else:
        facts.append(f"{n} is composite. Its factors are: {', '.join(str(f) for f in factors)}.")

    # Perfect square?
    sq = int(math.sqrt(n))
    if sq * sq == n:
        facts.append(f"{n} is a perfect square ({sq}²).")

    # Fibonacci?
    fib = [0, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    if n in fib:
        facts.append(f"{n} is a Fibonacci number.")

    return facts


def get_wiki_info(query):
    try:
        search_term = f"{query} (number)"
        r = requests.get(f"{WIKI_API}/{search_term.replace(' ', '_')}", timeout=10)
        if r.ok:
            data = r.json()
            extract = data.get("extract", "")
            if extract and len(extract) > 50:
                extract = re.sub(r'\s+', ' ', extract).strip()
                if len(extract) > 500:
                    extract = extract[:500].rsplit('.', 1)[0] + '.'
                return extract
    except Exception:
        pass
    return None


def format_curated(knowledge):
    lines = []
    lines.append(knowledge["name"])
    lines.append("")
    lines.append(f"Mathematics: {knowledge['math']}")
    lines.append("")
    lines.append(f"History: {knowledge['history']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("In human culture:")
    lines.append(knowledge["cultures"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(knowledge["feel"])
    return "\n".join(lines)


def format_uncurated(n, math_facts, wiki_text):
    lines = []
    lines.append(str(n))
    lines.append("")
    if math_facts:
        for fact in math_facts:
            lines.append(fact)
        lines.append("")
    if wiki_text:
        lines.append("—" * 40)
        lines.append("")
        lines.append(wiki_text)
    if not math_facts and not wiki_text:
        lines.append(f"No specific knowledge found for {n}.")
        lines.append("")
        lines.append("Numbers with curated profiles: " + ", ".join(str(k) for k in NUMBER_KNOWLEDGE.keys()))
    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Looking up number: {query}")

    parsed = parse_number(query)

    if parsed in NUMBER_KNOWLEDGE:
        response = format_curated(NUMBER_KNOWLEDGE[parsed])
    elif isinstance(parsed, int):
        math_facts = get_math_facts(parsed)
        wiki_text = get_wiki_info(str(parsed))
        response = format_uncurated(parsed, math_facts, wiki_text)
    else:
        # Try string keys
        q_lower = query.lower()
        found = None
        for key in NUMBER_KNOWLEDGE:
            if isinstance(key, str) and key.lower() in q_lower:
                found = key
                break
        if found:
            response = format_curated(NUMBER_KNOWLEDGE[found])
        else:
            response = f"Could not parse '{query}' as a number.\n\nTry: a number like 7, 42, 108, or words like 'pi' or 'infinity'."

    with open("Language/number-response.txt", "w") as f:
        f.write(response)

    print("Response written to Language/number-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
