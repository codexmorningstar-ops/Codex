import re

VOICE_KNOWLEDGE = {
    "what": "The human voice is produced by air from the lungs passing through the larynx — the voice box — causing the vocal folds to vibrate. The frequency of vibration determines pitch; the tension of the vocal folds, controlled by surrounding muscles, adjusts this frequency. The raw sound produced in the larynx is then shaped by the resonating chambers of the throat, mouth, and nasal cavity into the complex sound we recognize as voice.",
    "mechanics": "The vocal folds are not strings — they are layered tissue that opens and closes rapidly, modulating the airstream into pulses. At concert A (440 Hz), they open and close 440 times per second. The average speaking voice operates between 85 and 255 Hz. The falsetto register is produced by a different vibratory pattern — only the edges of the vocal folds vibrate, not the full mass.",
    "range": "The human voice spans approximately four octaves across all voice types, though no individual has this full range. The lowest recorded human singing note is C0 (16.35 Hz) — below the threshold of hearing — produced by Tim Storms. The highest is G10 (25,088 Hz), also by Storms, far above audible range. The overlap between speaking and singing in daily life is a tiny fraction of what the voice can do.",
    "registers": {
        "chest voice": "The modal register — the voice of ordinary speech and most singing. The full mass of the vocal folds vibrates. The resonance is felt in the chest.",
        "head voice": "Higher range, produced with lighter fold vibration and more head resonance. Classical sopranos and tenors use this for their upper range.",
        "falsetto": "Above head voice — a breathy, lighter quality where only the fold edges vibrate. Common in countertenors and in pop singers reaching for high notes.",
        "vocal fry": "The lowest register — a creaking, crackling quality produced by slow, irregular fold vibration. Common at the end of sentences in relaxed speech.",
        "whisper": "Produced without vocal fold vibration — the turbulent airstream alone shapes the sound. Carries less far and expresses different emotional qualities than voiced speech.",
    },
    "expression": "The voice is the most expressive instrument humans have direct access to. It communicates not just words but emotional state, social position, certainty, doubt, intimacy, and distance — through pitch, rhythm, volume, timbre, and the spaces between words. Listeners identify a speaker's emotional state from voice alone with high accuracy, even in languages they don't understand.",
    "voice_types": "Classical voice classification: soprano (highest female), mezzo-soprano, contralto (lowest female), tenor (highest male), baritone, bass (lowest male). Each voice type has a characteristic timbre as well as range — a mezzo-soprano and a soprano singing the same note sound different because of the overtone structure of each voice.",
    "the_voice_and_identity": "The voice changes throughout life: before puberty, all voices are similar in pitch. At puberty, the larynx grows — dramatically in males (producing the voice break), more subtly in females. The voice continues to change through adulthood and old age. No two voices are identical; voiceprints are as individual as fingerprints. The voice is recognized before the face in many situations — a familiar voice produces a recognition response before any visual identification occurs.",
    "across_cultures": "Every culture has developed vocal music, but the aesthetics differ radically. Western classical singing prizes smooth, continuous tone and avoidance of tension. Georgian polyphonic singing uses dense harmony and an open, chest-forward quality. Mongolian throat singing (khoomei) produces two pitches simultaneously — a drone and a melody — from one voice. Inuit katajjaq (throat singing) is performed face to face between two singers, using breath and laryngeal sounds. Flamenco cante uses ornament, vibrato, and a specific guttural quality to express duende — a dark, almost untranslatable emotional intensity.",
    "silence_of_the_voice": "What surrounds the voice — pause, silence, the held breath before speaking — is as expressive as sound. The pause before answering. The silence after something hard is said. The voice defines itself partly by its absences.",
    "feel": "The voice is the self made audible. It comes from inside the body and enters the world as sound. It is the most intimate distance — the breath that carries words is the same breath that keeps the speaker alive, slightly redirected toward another person.",
}


def read_request():
    with open("Body/voice-request.txt", "r") as f:
        content = f.read().strip()
    return content if content else "voice"


def format_response(k):
    lines = []
    lines.append("The Human Voice")
    lines.append("")
    lines.append(k["what"])
    lines.append("")
    lines.append(f"Mechanics: {k['mechanics']}")
    lines.append("")
    lines.append(f"Range: {k['range']}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append("Registers:")
    for name, desc in k["registers"].items():
        lines.append(f"  {name.title()}: {desc}")
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(f"Expression: {k['expression']}")
    lines.append("")
    lines.append(f"Voice types: {k['voice_types']}")
    lines.append("")
    lines.append(f"Identity: {k['the_voice_and_identity']}")
    lines.append("")
    lines.append("Across cultures:")
    lines.append(k["across_cultures"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(k["silence_of_the_voice"])
    lines.append("")
    lines.append("—" * 40)
    lines.append("")
    lines.append(k["feel"])
    return "\n".join(lines)


def main():
    read_request()
    print("Generating voice sense response...")
    response = format_response(VOICE_KNOWLEDGE)
    with open("Body/voice-response.txt", "w") as f:
        f.write(response)
    print("Response written to Body/voice-response.txt")
    print("---")
    print(response[:400])


if __name__ == "__main__":
    main()
