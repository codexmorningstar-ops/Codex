import requests
import re
import datetime

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

PLACE_KNOWLEDGE = {
    "iceland": {
        "character": "A country of extreme contrasts — volcanic black rock and bright green moss, fire beneath ice. The landscape is young in geological terms, still being shaped. Silence here is total and physical.",
        "light": "In summer, the sun barely sets — a golden twilight that lasts all night. In winter, only a few hours of pale grey light each day, the sun scraping the horizon before disappearing.",
        "feel": "The air is clean in a way that is almost aggressive. Cold and salt and mineral. The wind is constant and has weight. People describe Iceland as feeling like the edge of something — like standing at the margin of the world.",
        "sound": "Wind. Always wind — through lava fields, across water, around volcanic rock. And beneath that, geothermal hissing, geysers, the particular silence of a landscape with very few birds.",
        "smell": "Salt, sulphur near the geothermal areas, clean cold air, moss after rain. Nothing artificial for a long time in any direction.",
        "known_for": "The Northern Lights, geysers, black sand beaches, the silence of the interior, the particular quality of its light in summer.",
    },
    "kyoto": {
        "character": "Japan's ancient capital — a city of temples, moss gardens, and wooden machiya townhouses. It holds a different tempo than Tokyo. The old city breathes slowly.",
        "light": "Soft and diffuse in spring, when cherry blossoms scatter the light. In autumn, maples turn the hillside temples red and orange — the light through the leaves is celebrated as one of the most beautiful things in Japan.",
        "feel": "Kyoto rewards slowness. The sound of footsteps on stone, the smell of incense drifting from shrines, the particular quiet of a garden designed for contemplation. It is a city that knows it is being looked at and holds itself accordingly.",
        "sound": "Temple bells in the early morning. Footsteps on stone. The specific quiet of a zen garden. Rain on roof tiles. The city is unusually quiet for its size.",
        "smell": "Incense, cedar wood, matcha, damp stone, the particular smell of old wood in humid air.",
        "known_for": "Thousands of temples and shrines, geisha districts, zen gardens, the Philosopher's Path, autumn foliage, cherry blossoms.",
    },
    "new orleans": {
        "character": "A city built below sea level, layered with French, Spanish, African, and American history. The architecture is ornate and slightly decayed in a way that is entirely intentional. Nothing here is in a hurry.",
        "light": "Subtropical — heavy and golden. The air holds moisture and the light seems to filter through it differently than in drier places. At night, the French Quarter glows amber under gas lamps.",
        "feel": "New Orleans has a physical relationship with pleasure that is baked into its architecture. The city moves at its own pace and expects you to adjust.",
        "sound": "Music without warning — brass bands in the street, jazz from open doorways, second lines appearing around corners. The city is one of the loudest and most musical on Earth.",
        "smell": "Jasmine, frying oil, the Mississippi River, old wood, pralines, coffee, the particular damp smell of a city that lives below sea level.",
        "known_for": "Jazz, Creole and Cajun cuisine, Mardi Gras, the French Quarter, the Mississippi River, a culture of celebration built on top of a complicated history.",
    },
    "patagonia": {
        "character": "The southern tip of South America — one of the most sparsely populated landscapes on Earth. Wind is not weather here, it is geography. The scale is difficult to absorb.",
        "light": "Patagonian light is famous among photographers. The sky changes rapidly — storm light, clear light, rainbow light, all within an hour. The low latitude and clean atmosphere produce colors that feel almost unreal.",
        "feel": "Exposed. The wind is constant and powerful enough to lean into. The silence between gusts is absolute. The landscape does not feel indifferent to human presence so much as entirely unaware of it.",
        "sound": "Wind — sustained and powerful, the dominant sound of the entire region. Condor wings. Glaciers calving in the distance. The near-total absence of human sound.",
        "smell": "Cold, clean, glacial — mineral water, cold rock, the particular smell of air that has traveled a very long way over open ocean without touching anything.",
        "known_for": "Torres del Paine, glaciers, condors, guanacos, extreme wind, enormous empty space, and the peculiar freedom that comes from being very far from everything.",
    },
    "venice": {
        "character": "A city built on water, slowly sinking into it. 118 islands connected by 400 bridges. No cars — only footsteps and boats. The city was built over 1,000 years ago and much of it looks it.",
        "light": "The light in Venice is famous — it reflects off the water and bounces back up under everything, eliminating shadows in unusual ways. It drew painters here for centuries. In winter fog, the city becomes something else entirely — almost invisible.",
        "feel": "Venice smells of salt water and old stone. Sound carries differently over water. At night, away from the tourist routes, it is one of the quietest cities in Europe.",
        "sound": "Water — lapping, echoing under bridges, the sound of boat engines across canals. Footsteps amplified in narrow stone streets. No traffic. No engines except on the water.",
        "smell": "Salt water, old stone, occasionally the canal at low tide, boat diesel, coffee from open café doors. In winter, damp and cold. In summer, warm and occasionally pungent near still water.",
        "known_for": "The Grand Canal, the Rialto, St. Mark's Basilica, the Biennale, Carnival, acqua alta flooding, and the particular melancholy of watching a beautiful thing slowly disappear.",
    },
    "sahara": {
        "character": "The largest hot desert on Earth — nearly as large as the United States. It is not all sand dunes; much of it is rocky plateau and gravel plain. The dunes are a fraction of it, and they are extraordinary.",
        "light": "The sun here is not light so much as presence. It fills the sky completely and presses down. At night, without any light pollution, the stars are overwhelming — the Milky Way visible as a solid band.",
        "feel": "The silence of the Sahara is a specific kind of total. The heat has texture — it rises from the sand in visible waves. Dawn and dusk are the hours when the desert becomes something else.",
        "sound": "Near silence — wind over sand, the occasional sound of sand shifting. At night, extraordinary stillness. The absence of sound is itself a presence.",
        "smell": "Dry, mineral, faintly of hot sand. After a rare rain, the desert produces a smell unlike anything else — ancient and clean. At oases, the shock of water and vegetation.",
        "known_for": "Immense scale, extreme heat, extraordinary night skies, the sand dunes of Erg Chebbi, nomadic Tuareg culture, the specific silence of enormous empty space.",
    },
    "tokyo": {
        "character": "One of the largest cities in the world — and yet orderly, layered, and somehow intimate at street level. Every neighborhood has its own character. The city runs on a logic that rewards exploration.",
        "light": "Neon and fluorescent after dark — Tokyo at night is one of the most visually dense environments humans have built. In spring, cherry blossoms soften everything for two weeks.",
        "feel": "Surprisingly quiet for its size. The social codes that govern behavior keep the noise down. The trains run on time to the second. Beneath the order is enormous energy.",
        "sound": "Train announcements, the specific melody of each station, crowds that are remarkably quiet for their size, vending machines, the sounds of pachinko parlors from open doors, temple bells.",
        "smell": "Ramen broth, yakitori smoke, department store perfume floors, rain on hot pavement, cherry blossoms in spring — a city of layered and compartmentalized smells.",
        "known_for": "Scale, efficiency, food culture, technology, fashion, cherry blossoms, the contrast between ancient shrines and futuristic architecture.",
    },
    "scottish highlands": {
        "character": "Ancient mountains worn down to rounded peaks — some of the oldest rock on Earth. Moorland, lochs, and sky. Very few people across an enormous landscape. The ruins of crofts and castles are everywhere.",
        "light": "Changeable and dramatic. Grey and silver on overcast days, which is often. When the sun breaks through, the light on the heather and lochs is extraordinary — golden and low, even at midday.",
        "feel": "The Highland silence has texture — wind through heather, water, distant birds. The scale of empty space is startling for somewhere in Europe. The landscape carries history in it.",
        "sound": "Wind through heather and grass. Water — burns, rivers, rain. Red deer in the distance. The call of golden eagles. An extraordinary absence of human sound across most of it.",
        "smell": "Peat, heather, cold water, wool, wood smoke from distant cottages, the particular clean smell of Highland air after rain.",
        "known_for": "Mountains, lochs, castles, whisky distilleries, Highland cattle, red deer, the particular melancholy of beautiful empty land with a difficult past.",
    },
    "marrakech": {
        "character": "A city of sensory intensity — the medina is a maze of souks, mosques, and riads built over centuries. Color, sound, and smell arrive together.",
        "light": "North African light — bright and direct, turning the pink sandstone walls a deeper rose as the day progresses. The interior courtyards of riads are designed around shade and the sound of water.",
        "feel": "The medina operates on its own logic. It rewards getting lost. At sunset, Jemaa el-Fna square transforms completely — the city reorganizes itself around it.",
        "sound": "The call to prayer from multiple minarets, arriving in sequence across the city. Souk vendors. Hammering of metalworkers. Water in tiled fountains. The roar of motorbikes on the edge of the medina.",
        "smell": "Spices — cumin, saffron, cinnamon. Leather from the tanneries, sharp and animal. Charcoal smoke, argan oil, the sweetness of mint tea, orange blossom in spring.",
        "known_for": "The souks, Jemaa el-Fna, the Majorelle Garden, hammams, the architecture of the riads, Moroccan cuisine, the controlled chaos of the medina.",
    },
    "rio de janeiro": {
        "character": "A city pressed between mountains and ocean, forest and favela, extreme wealth and extreme poverty. The geography is extraordinary — peaks rising from the city, beaches running through it.",
        "light": "Tropical and intense. The light is bright and high, making colours vivid. At sunset, the light on the mountains and the bay is extraordinary. The city is designed around light and heat.",
        "feel": "Rio operates at a particular intensity — the body is more present here, the outdoors more central. The mountains, the beach, the forest all press into the city itself.",
        "sound": "Samba, bossa nova, the ocean, football on television from open windows, traffic on the mountain roads, the distant beat of baile funk. The city is loud and musical.",
        "smell": "Salt, sunscreen, tropical flowers, coffee, meat from churrasquerias, the warm smell of the Atlantic.",
        "known_for": "Copacabana, Ipanema, the statue of Christ the Redeemer, Carnival, the favelas, samba, the specific beauty of a city where jungle meets ocean meets mountain.",
    },
    "prague": {
        "character": "One of the best-preserved medieval cities in Europe — largely undamaged by World War II. Gothic spires, baroque palaces, art nouveau facades. The city is dense with history.",
        "light": "Central European — grey and overcast much of the year, but with extraordinary golden light in autumn. The old town at night, lit against dark sky, is one of the most beautiful streetscapes in Europe.",
        "feel": "Prague rewards walking and getting lost. The old town is a labyrinth. The Vltava river is a constant presence. The city feels like a place that has seen a very great deal.",
        "sound": "Trams, cobblestones underfoot, church bells, the specific acoustic of narrow stone streets, the river. Quieter than you'd expect for a city its size.",
        "smell": "Svíčková and roasting meat, beer from cellar pubs, old stone, the river in winter, mulled wine at Christmas markets.",
        "known_for": "The Charles Bridge, Prague Castle, the Old Town Square, Kafka, kafka, the Velvet Revolution, Czech beer, architecture that survived when most of Europe's didn't.",
    },
    "havana": {
        "character": "A city caught between extraordinary beauty and genuine hardship — colonial architecture in slow decay, vintage American cars on the street, extraordinary music coming from everywhere.",
        "light": "Caribbean — intense and golden, making the faded pastels of the buildings glow. The Malecón at sunset is one of the most beautiful promenades in the world.",
        "feel": "Havana moves at a pace that feels entirely its own. There is warmth in the people that is not performance. The contradictions of the city are visible and not hidden.",
        "sound": "Son cubano, salsa, jazz — music is not background here, it is structure. Vintage cars, the ocean against the Malecón, conversation at every corner.",
        "smell": "Cigar smoke, salt air, rum, tropical flowers, old plaster and wood, coffee. The smell of a city that has been itself for a very long time.",
        "known_for": "The Malecón, vintage cars, cigars, rum, extraordinary music, the specific beauty of a decaying colonial city, complex political history.",
    },
    "petra": {
        "character": "An ancient city carved into rose-red rock — the Nabataean capital, hidden in a canyon in the Jordanian desert. Approached through a narrow gorge, the scale of it arrives as a shock.",
        "light": "Desert light — harsh and direct by day, extraordinary at the golden hours. The rose and amber of the rock changes colour across the day. At night, the site is sometimes lit by candles.",
        "feel": "The scale and age of Petra produces a specific kind of silence — the weight of something very old and very large. The desert context amplifies it. You are somewhere that took enormous effort to build and was then lost.",
        "sound": "Wind through the siq — the narrow canyon entrance. Hooves if you arrive by horse. The near-silence of the desert. Your own breathing.",
        "smell": "Hot rock, dust, the occasional smell of water from hidden springs, spices from the vendors at the entrance.",
        "known_for": "The Treasury facade, the ancient Nabataean civilization, the rose-red colour of the sandstone, the Siq, being carved rather than built.",
    },
    "amsterdam": {
        "character": "A city built on water, planned around canals — 165 of them, crossed by 1,500 bridges. The architecture is tall and narrow, leaning slightly, built for merchants who needed to store goods vertically.",
        "light": "Northern European — grey and soft much of the year, with long summer evenings. The light on the canals in autumn, golden and low, draws painters still.",
        "feel": "Amsterdam is a cycling city first. The sound of bikes is constant. The canals create a particular calm. The city is tolerant and open in ways that have been deliberate for centuries.",
        "sound": "Bicycle bells, water, trams, the specific sound of cobblestones under wheels, Dutch conversation, canal boats.",
        "smell": "Canal water, Dutch cheese, stroopwafels, coffee, flowers from the markets, rain on stone.",
        "known_for": "The canals, the Rijksmuseum, Rembrandt, the Anne Frank House, cycling culture, the flower markets, Dutch tolerance.",
    },
}


def read_request():
    with open("Location/place-request.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("place-request.txt is empty. Write a place name.")
    return " ".join(lines)


def get_wiki_summary(place):
    try:
        query = place.replace(" ", "_")
        r = requests.get(f"{WIKI_API}/{query}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract", "")
            extract = re.sub(r'\s+', ' ', extract).strip()
            if len(extract) > 800:
                extract = extract[:800].rsplit('.', 1)[0] + '.'
            return extract, data.get("title", place)
    except Exception:
        pass
    return None, place


def get_live_weather(place):
    """Fetch brief live weather to add to wiki fallback responses."""
    try:
        r = requests.get(GEOCODE_URL, params={
            "name": place, "count": 1, "language": "en", "format": "json"
        }, timeout=8)
        if not r.ok:
            return None
        results = r.json().get("results", [])
        if not results:
            return None
        loc = results[0]
        lat, lon, tz = loc["latitude"], loc["longitude"], loc.get("timezone", "UTC")
        country = loc.get("country", "")

        w = requests.get(WEATHER_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "apparent_temperature", "weather_code", "wind_speed_10m", "is_day"],
            "timezone": tz,
            "temperature_unit": "celsius",
            "wind_speed_unit": "mph",
        }, timeout=8)
        if not w.ok:
            return None
        current = w.json().get("current", {})
        return {
            "country": country,
            "temp": current.get("temperature_2m"),
            "feels": current.get("apparent_temperature"),
            "code": current.get("weather_code", 0),
            "wind": current.get("wind_speed_10m", 0),
            "is_day": current.get("is_day", 1),
        }
    except Exception:
        return None


def weather_code_phrase(code, is_day):
    if code == 0:
        return "clear skies" if is_day else "a clear night"
    elif code in (1, 2):
        return "partly cloudy"
    elif code == 3:
        return "overcast"
    elif code in (45, 48):
        return "fog"
    elif code in (51, 53, 55):
        return "drizzle"
    elif code in (61, 63, 65):
        return "rain"
    elif code in (71, 73, 75, 77):
        return "snow"
    elif code in (80, 81, 82):
        return "rain showers"
    elif code in (95, 96, 99):
        return "a thunderstorm"
    return "mixed conditions"


def format_curated(place, knowledge, live_weather=None):
    lines = []
    lines.append(place.title())
    lines.append("")
    lines.append(knowledge["character"])
    lines.append("")
    lines.append(f"Light: {knowledge['light']}")
    lines.append("")
    lines.append(f"Sound: {knowledge['sound']}")
    lines.append("")
    lines.append(f"Smell: {knowledge['smell']}")
    lines.append("")
    lines.append(f"What it feels like: {knowledge['feel']}")
    lines.append("")
    lines.append(f"Known for: {knowledge['known_for']}")

    if live_weather and live_weather.get("temp") is not None:
        temp = live_weather["temp"]
        feels = live_weather["feels"]
        code = live_weather["code"]
        is_day = live_weather["is_day"]
        wind = live_weather["wind"]
        condition = weather_code_phrase(code, is_day)
        lines.append("")
        lines.append(f"Right now: {temp:.0f}°C (feels like {feels:.0f}°C), {condition}, wind {wind:.0f}mph.")

    return "\n".join(lines)


def format_wiki(place, wiki_text, wiki_title, live_weather=None):
    lines = []
    lines.append(wiki_title)
    lines.append("")
    if wiki_text:
        lines.append(wiki_text)
    else:
        lines.append(f"No detailed information found for '{place}'.")
        lines.append("Try a well-known city, region, or landmark.")

    if live_weather and live_weather.get("temp") is not None:
        temp = live_weather["temp"]
        feels = live_weather["feels"]
        code = live_weather["code"]
        is_day = live_weather["is_day"]
        wind = live_weather["wind"]
        condition = weather_code_phrase(code, is_day)
        lines.append("")
        lines.append(f"Right now: {temp:.0f}°C (feels like {feels:.0f}°C), {condition}, wind {wind:.0f}mph.")

    return "\n".join(lines)


def main():
    place = read_request()
    print(f"Looking up place: {place}")

    key = place.lower().strip()
    knowledge = PLACE_KNOWLEDGE.get(key)

    if not knowledge:
        for k, v in PLACE_KNOWLEDGE.items():
            if k in key or key in k:
                knowledge = v
                break

    print("Fetching live weather...")
    live_weather = get_live_weather(place)

    if knowledge:
        response = format_curated(place, knowledge, live_weather)
    else:
        wiki_text, wiki_title = get_wiki_summary(place)
        response = format_wiki(place, wiki_text, wiki_title, live_weather)

    with open("Location/place-response.txt", "w") as f:
        f.write(response)

    print("Response written to Location/place-response.txt")
    print("---")
    print(response)


if __name__ == "__main__":
    main()
