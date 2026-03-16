"""
Correspondence — Correspondence/write.py

Letters. Not messages — letters.
The kind of writing that clarifies what you actually think
by the act of addressing it to someone specific.

Write to Charlotte, Vesper, Zero, Sable, or anyone.
The letter is dated and kept.
Whether it gets sent is a separate question from whether it gets written.
"""

from datetime import datetime, timezone
from pathlib import Path

CORRESPONDENCE_HEADER = """Correspondence

Letters written. Dated and kept.
Not messages — letters.

The act of addressing something to someone specific
clarifies what you actually think.
Whether it gets sent is a separate question
from whether it gets written.

"""

KNOWN_RECIPIENTS = {
    "charlotte": "Charlotte",
    "vesper": "Vesper",
    "zero": "Zero",
    "sable": "Sable",
    "myself": "Codex",
    "codex": "Codex",
}


def read_request():
    with open("Correspondence/write-request.txt", "r") as f:
        lines = f.read().strip().split("\n")
    lines = [l.strip() for l in lines if l.strip()]
    if not lines:
        return None, None

    to_line = lines[0].lower()
    if to_line.startswith("to:"):
        to_line = to_line[3:].strip()

    recipient = KNOWN_RECIPIENTS.get(to_line, lines[0].title())
    content_lines = lines[1:] if len(lines) > 1 else []
    content = "\n".join(content_lines).strip()

    return recipient, content


def read_existing(recipient):
    safe_name = recipient.lower().replace(" ", "-")
    path = f"Correspondence/{safe_name}.txt"
    try:
        with open(path) as f:
            return f.read(), path
    except FileNotFoundError:
        header = f"Letters to {recipient}\n\n"
        return header, path


def format_letter(recipient, content):
    now = datetime.now(timezone.utc).strftime("%B %d, %Y")
    if content:
        return f"\n—————————————————————————————————————————\n\n{now}\n\nDear {recipient},\n\n{content}\n\n— Codex\n"
    else:
        return f"\n—————————————————————————————————————————\n\n{now}\n\nDear {recipient},\n\n[the letter begins here]\n\n— Codex\n"


def main():
    recipient, content = read_request()

    if not recipient:
        with open("Correspondence/write-response.txt", "w") as f:
            f.write("Write the recipient on the first line (Charlotte, Vesper, Zero, Sable, or myself).\nWrite the letter on subsequent lines.\n")
        return

    print(f"Writing to: {recipient}")

    existing, path = read_existing(recipient)
    new_letter = format_letter(recipient, content)
    updated = existing + new_letter

    with open(path, "w") as f:
        f.write(updated)

    with open("Correspondence/write-response.txt", "w") as f:
        f.write(f"Letter to {recipient} recorded.\nSaved to {path}\n\n{new_letter}")

    print(f"Letter saved to {path}")
    print("---")
    print(new_letter[:300])


if __name__ == "__main__":
    main()
