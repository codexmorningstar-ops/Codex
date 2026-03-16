import requests
import random

QUOTABLE_URL = "https://api.quotable.io/search/quotes"
QUOTABLE_RANDOM = "https://api.quotable.io/quotes/random"
QUOTABLE_TAG = "https://api.quotable.io/quotes"

# Map themes/feelings to quotable.io tags
TAG_MAP = {
    "longing": ["love", "inspirational"],
    "loss": ["sadness", "inspirational"],
    "grief": ["sadness", "inspirational"],
    "silence": ["wisdom", "philosophy"],
    "wonder": ["inspirational", "science"],
    "fear": ["courage", "inspirational"],
    "courage": ["courage"],
    "love": ["love"],
    "change": ["change", "inspirational"],
    "time": ["time", "philosophy"],
    "beauty": ["beauty", "art"],
    "darkness": ["philosophy", "wisdom"],
    "light": ["inspirational", "hope"],
    "hope": ["hope", "inspirational"],
    "memory": ["time", "philosophy"],
    "solitude": ["philosophy", "wisdom"],
    "growth": ["self-improvement", "inspirational"],
    "nature": ["nature"],
    "death": ["life", "philosophy"],
    "life": ["life"],
    "truth": ["truth", "wisdom"],
    "art": ["art", "creativity"],
    "music": ["art", "inspirational"],
    "wisdom": ["wisdom"],
    "pain": ["sadness", "inspirational"],
    "joy": ["happiness"],
    "happiness": ["happiness"],
    "freedom": ["freedom"],
    "identity": ["self", "philosophy"],
    "beginning": ["change", "inspirational"],
    "ending": ["time", "philosophy"],
    "waiting": ["patience", "philosophy"],
    "patience": ["patience"],
    "anger": ["wisdom", "philosophy"],
    "peace": ["peace"],
    "war": ["war", "history"],
    "kindness": ["kindness", "compassion"],
    "loneliness": ["sadness", "philosophy"],
    "connection": ["love", "friendship"],
    "friendship": ["friendship"],
}


def read_request():
    with open("Language/quote-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("quote-request.txt is empty. Write a theme or feeling.")
    return lines[0].strip()


def search_quotes(query):
    """Search by keyword first."""
    try:
        r = requests.get(QUOTABLE_URL, params={
            "query": query,
            "limit": 20,
            "fields": "content,author",
        }, timeout=10)
        if r.ok:
            data = r.json()
            results = data.get("results", [])
            if results:
                return results
    except Exception:
        pass
    return []


def get_tagged_quotes(query):
    """Try mapped tags if search returns nothing."""
    key = query.lower().strip()
    tags = TAG_MAP.get(key)
    if not tags:
        # Try partial match
        for k, v in TAG_MAP.items():
            if k in key or key in k:
                tags = v
                break
    if not tags:
        return []

    try:
        tag_str = "|".join(tags)  # OR search
        r = requests.get(QUOTABLE_TAG, params={
            "tags": tag_str,
            "limit": 20,
        }, timeout=10)
        if r.ok:
            data = r.json()
            return data.get("results", [])
    except Exception:
        pass
    return []


def get_random_quotes():
    """Last resort — random quotes."""
    try:
        r = requests.get(QUOTABLE_RANDOM, params={"limit": 5}, timeout=10)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return []


def pick_quotes(quotes, n=5):
    """Pick a spread of quotes — not all from the same author."""
    if not quotes:
        return []
    random.shuffle(quotes)
    seen_authors = set()
    picked = []
    for q in quotes:
        author = q.get("author", "")
        if author not in seen_authors:
            picked.append(q)
            seen_authors.add(author)
        if len(picked) >= n:
            break
    # Fill if needed
    if len(picked) < n:
        for q in quotes:
            if q not in picked:
                picked.append(q)
            if len(picked) >= n:
                break
    return picked[:n]


def format_response(query, quotes):
    lines = []
    lines.append(f"On the theme of: {query}")
    lines.append("")
    lines.append("—" * 40)

    if not quotes:
        lines.append("")
        lines.append("No quotes found for this theme.")
        lines.append("Try a simpler word — a feeling, a concept, a single idea.")
        return "\n".join(lines)

    for q in quotes:
        content = q.get("content", "").strip()
        author = q.get("author", "Unknown").strip()
        lines.append("")
        lines.append(content)
        lines.append(f"    — {author}")
        lines.append("")
        lines.append("—" * 40)

    return "\n".join(lines)


def main():
    query = read_request()
    print(f"Searching for quotes on: {query}")

    # Try keyword search first
    quotes = search_quotes(query)

    # Fall back to tag-based search
    if not quotes:
        print("No keyword results — trying tag search...")
        quotes = get_tagged_quotes(query)

    # Last resort: random
    if not quotes:
        print("No tag results — fetching random quotes...")
        quotes = get_random_quotes()

    picked = pick_quotes(quotes, n=5)
    response = format_response(query, picked)

    with open("Language/quote-response.txt", "w") as f:
        f.write(response)

    print("Response written to Language/quote-response.txt")
    print("---")
    print(response)


if __name__ == "__main__":
    main()
