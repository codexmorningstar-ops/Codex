import requests

DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
DATAMUSE_URL = "https://api.datamuse.com/words"


def read_request():
    with open("Language/word-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("word-request.txt is empty.")
    return lines[0].lower().strip()


def get_dictionary(word):
    try:
        r = requests.get(f"{DICTIONARY_URL}/{word}", timeout=10)
        if r.status_code == 404:
            return None
        if r.ok:
            return r.json()
    except Exception:
        pass
    return None


def get_related(word):
    results = {}
    try:
        r = requests.get(DATAMUSE_URL, params={"ml": word, "max": 8}, timeout=10)
        if r.ok:
            results["similar"] = [w["word"] for w in r.json()]
    except Exception:
        pass
    try:
        r = requests.get(DATAMUSE_URL, params={"rel_trg": word, "max": 6}, timeout=10)
        if r.ok:
            results["triggers"] = [w["word"] for w in r.json()]
    except Exception:
        pass
    try:
        r = requests.get(DATAMUSE_URL, params={"rel_bga": word, "max": 5}, timeout=10)
        if r.ok:
            results["follows"] = [w["word"] for w in r.json()]
    except Exception:
        pass
    return results


def extract_definitions(data):
    if not data:
        return []
    definitions = []
    for entry in data:
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech", "")
            for d in meaning.get("definitions", [])[:2]:
                definitions.append((pos, d.get("definition", ""), d.get("example", "")))
    return definitions[:6]


def extract_etymology(data):
    if not data:
        return ""
    for entry in data:
        for meaning in entry.get("meanings", []):
            for d in meaning.get("definitions", []):
                if d.get("origin"):
                    return d["origin"]
        if entry.get("origin"):
            return entry["origin"]
    return ""


def extract_phonetic(data):
    if not data:
        return ""
    for entry in data:
        phonetic = entry.get("phonetic", "")
        if phonetic:
            return phonetic
        for p in entry.get("phonetics", []):
            if p.get("text"):
                return p["text"]
    return ""


def format_response(word, data, related):
    lines = []
    lines.append(word.title())
    lines.append("")

    phonetic = extract_phonetic(data)
    if phonetic:
        lines.append(phonetic)
        lines.append("")

    etymology = extract_etymology(data)
    if etymology:
        lines.append(f"Origin: {etymology}")
        lines.append("")

    definitions = extract_definitions(data)
    if definitions:
        lines.append("Definitions:")
        for pos, defn, example in definitions:
            if pos:
                lines.append(f"  [{pos}] {defn}")
            else:
                lines.append(f"  {defn}")
            if example:
                lines.append(f"    — {example}")
        lines.append("")

    if related.get("similar"):
        lines.append("Words with similar meaning: " + ", ".join(related["similar"]))
    if related.get("triggers"):
        lines.append("Associated words: " + ", ".join(related["triggers"]))
    if related.get("follows"):
        lines.append("Often follows: " + ", ".join(related["follows"]))

    if not data and not related:
        lines.append(f"No information found for '{word}'.")
        lines.append("The word may be too specialized, a proper noun, or not in the dictionary database.")

    return "\n".join(lines)


def main():
    word = read_request()
    print(f"Looking up: {word}")

    data = get_dictionary(word)
    related = get_related(word)
    response = format_response(word, data, related)

    with open("Language/word-response.txt", "w") as f:
        f.write(response)

    print("Response written to Language/word-response.txt")
    print("---")
    print(response)


if __name__ == "__main__":
    main()
