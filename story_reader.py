"""
Story reader — Grimm fairy tales (built-in) + DW Langsam gesprochene Nachrichten (live RSS).
"""
import urllib.request
import urllib.error
import json
import re

# Built-in simplified Grimm stories for A1 learners
GRIMM_STORIES = [
    {
        "id": "rotkäppchen",
        "title": "Rotkäppchen (Little Red Riding Hood)",
        "level": "A1",
        "text": """Es war einmal ein kleines Mädchen. Das Mädchen heißt Rotkäppchen.
Rotkäppchen hat eine rote Mütze. Die Mütze ist sehr schön.

Die Großmutter von Rotkäppchen ist krank. Sie wohnt im Wald.
Die Mutter sagt: "Geh zur Großmutter! Bring ihr Kuchen und Wein!"

Rotkäppchen geht durch den Wald. Im Wald trifft sie einen Wolf.
Der Wolf sagt: "Wohin gehst du, Rotkäppchen?"
Rotkäppchen sagt: "Ich gehe zur Großmutter. Sie ist krank."

Der Wolf läuft schnell zur Großmutter. Er isst die Großmutter!
Dann legt er sich ins Bett.

Rotkäppchen kommt an. Sie klopft an die Tür.
"Herein!", sagt der Wolf.
Rotkäppchen sagt: "Großmutter, du hast so große Augen!"
Der Wolf sagt: "Damit ich dich besser sehen kann!"
"Du hast so große Ohren!" — "Damit ich dich besser hören kann!"
"Du hast so einen großen Mund!" — "Damit ich dich besser essen kann!"

Der Wolf springt aus dem Bett! Rotkäppchen schreit.
Ein Jäger hört das. Er kommt und tötet den Wolf.
Er rettet die Großmutter.

Rotkäppchen ist sehr froh. Sie lernt: Sprich nicht mit fremden Leuten im Wald!""",
        "glossary": {
            "es war einmal": "once upon a time",
            "das Mädchen": "the girl",
            "die Mütze": "the hat/cap",
            "krank": "sick/ill",
            "der Wald": "the forest",
            "bringen": "to bring",
            "durch": "through",
            "treffen": "to meet",
            "der Wolf": "the wolf",
            "wohin": "where to",
            "schnell": "fast/quickly",
            "essen": "to eat",
            "das Bett": "the bed",
            "klopfen": "to knock",
            "die Augen": "the eyes",
            "die Ohren": "the ears",
            "der Mund": "the mouth",
            "springen": "to jump",
            "schreien": "to scream",
            "der Jäger": "the hunter",
            "retten": "to rescue",
            "froh": "happy/glad",
            "fremd": "foreign/strange",
        }
    },
    {
        "id": "hase_igel",
        "title": "Der Hase und der Igel",
        "level": "A1",
        "text": """Der Hase ist sehr schnell. Er läuft gern im Feld.
Der Igel ist langsam. Er geht langsam durch das Feld.

Der Hase lacht den Igel aus. "Du bist so langsam! Du hast so kurze Beine!"
Der Igel antwortet: "Wir können ein Rennen machen. Ich gewinne!"
Der Hase lacht sehr laut.

Das Rennen beginnt. Der Hase läuft sehr schnell.
Aber am Ende des Feldes — wartet der Igel!
"Ich bin schon hier!", sagt der Igel.

Wie ist das möglich? Der Igel hat einen Trick.
Seine Frau sieht genauso aus wie er! Sie wartet am Ende.

Der Hase läuft hin und her. Immer wartet ein Igel.
Nach 73 Rennen fällt der Hase um. Er ist sehr müde.

Die Moral: Man soll nicht über andere lachen.
Und: Manchmal ist Klugheit besser als Schnelligkeit.""",
        "glossary": {
            "der Hase": "the hare",
            "der Igel": "the hedgehog",
            "das Feld": "the field",
            "langsam": "slow",
            "auslachen": "to laugh at",
            "das Bein": "the leg",
            "antworten": "to answer",
            "das Rennen": "the race",
            "gewinnen": "to win",
            "beginnen": "to begin",
            "am Ende": "at the end",
            "warten": "to wait",
            "möglich": "possible",
            "der Trick": "the trick",
            "genauso": "just as",
            "hin und her": "back and forth",
            "umfallen": "to fall over",
            "die Moral": "the moral",
            "manchmal": "sometimes",
            "die Klugheit": "cleverness",
            "die Schnelligkeit": "speed",
        }
    },
    {
        "id": "goldene_gans",
        "title": "Die goldene Gans",
        "level": "A1-A2",
        "text": """Es war einmal drei Brüder. Der jüngste Bruder heißt Dummling.
Die anderen Brüder sind nicht nett zu ihm.

Eines Tages geht Dummling in den Wald. Er findet einen alten Mann.
Der Mann hat Hunger. Dummling gibt ihm sein Essen.

Als Dank gibt der alte Mann ihm eine goldene Gans!
Die Gans ist wunderschön. Sie glänzt wie Gold.

Im Dorf sieht ein Mädchen die Gans. Sie möchte eine Feder nehmen.
Aber sie bleibt an der Gans kleben! Sie kann nicht loslassen.

Ein zweites Mädchen versucht zu helfen. Auch sie bleibt kleben!
Dann ein drittes Mädchen — auch kleben!

So geht Dummling durch das Land. Hinter ihm gehen drei Mädchen.
Alle Menschen lachen.

Der König hat eine traurige Tochter. Sie lacht nie.
Der König sagt: "Wer meine Tochter zum Lachen bringt, heiratet sie!"

Die traurige Prinzessin sieht Dummling und die drei Mädchen.
Sie lacht laut! Dummling heiratet die Prinzessin.

Die Moral: Sei freundlich zu allen Menschen!""",
        "glossary": {
            "jüngste": "youngest",
            "Dummling": "simpleton (the hero's name)",
            "eines Tages": "one day",
            "finden": "to find",
            "als Dank": "as thanks",
            "die Gans": "the goose",
            "golden": "golden",
            "glänzen": "to shine",
            "die Feder": "the feather",
            "kleben": "to stick",
            "loslassen": "to let go",
            "versuchen": "to try",
            "traurig": "sad",
            "heiraten": "to marry",
            "die Prinzessin": "the princess",
            "freundlich": "friendly/kind",
        }
    },
]


def get_grimm_stories():
    return GRIMM_STORIES

def get_grimm_story(story_id):
    for s in GRIMM_STORIES:
        if s["id"] == story_id:
            return s
    return None

def fetch_dw_news():
    """Fetch DW Langsam gesprochene Nachrichten RSS feed."""
    try:
        url = "https://rss.dw.com/xml/podcast-slow-german"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")

        # Parse RSS items
        items = []
        pattern = r'<item>(.*?)</item>'
        matches = re.findall(pattern, content, re.DOTALL)

        for m in matches[:5]:
            title = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', m)
            desc = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', m)
            link = re.search(r'<link>(.*?)</link>', m)

            if title and desc:
                # Clean HTML from description
                clean_desc = re.sub(r'<[^>]+>', '', desc.group(1))
                clean_desc = clean_desc.strip()[:800]
                items.append({
                    "title": title.group(1).strip(),
                    "text": clean_desc,
                    "link": link.group(1).strip() if link else "",
                    "level": "A2-B1",
                    "source": "DW Langsam"
                })
        return items
    except Exception:
        return []

def get_sample_dw_news():
    """Fallback sample DW-style news when offline."""
    return [
        {
            "title": "Das Wetter in Deutschland",
            "text": """In Deutschland ist das Wetter im Winter oft kalt und grau.
Im Norden regnet es viel. Im Süden, in den Alpen, gibt es viel Schnee.

Aachen liegt im Westen von Deutschland. Hier ist das Wetter oft mild, aber es regnet häufig.
Im Sommer kann es warm werden — bis zu 30 Grad.

Die Deutschen sprechen sehr gern über das Wetter.
"Schönes Wetter heute!" oder "Typisch deutsches Wetter!" hört man oft.

Klimawandel ist ein wichtiges Thema in Deutschland.
Die Temperaturen steigen. Die Sommer werden heißer und trockener.
Das ist ein großes Problem für die Landwirtschaft.""",
            "level": "A2",
            "source": "Sample News",
            "link": ""
        },
        {
            "title": "Die RWTH Aachen — Eine der besten Universitäten",
            "text": """Die RWTH Aachen University ist eine der besten technischen Universitäten in Europa.
RWTH steht für "Rheinisch-Westfälische Technische Hochschule".

Über 45.000 Studenten studieren hier. Sie kommen aus der ganzen Welt.
Besonders beliebt sind Ingenieurswissenschaften, Informatik und Naturwissenschaften.

Die Universität hat viele Forschungsprojekte. Ein wichtiges Thema ist die Elektromobilität.
Aachen forscht auch an Robotern und Künstlicher Intelligenz.

In Aachen gibt es auch das Deutsche Zentrum für Luft- und Raumfahrt (DLR).
Viele Wissenschaftler arbeiten dort an wichtigen Projekten.

Die Stadt und die Universität arbeiten eng zusammen.
Das macht Aachen zu einem wichtigen Wissenschaftsstandort in Deutschland.""",
            "level": "A2-B1",
            "source": "Sample News",
            "link": ""
        },
    ]
