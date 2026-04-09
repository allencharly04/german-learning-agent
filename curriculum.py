"""
A1 German curriculum — 20 lessons covering the full A1 standard.
Each lesson has vocabulary, grammar points, and quiz questions.
"""

LESSONS = [
    {
        "id": 1,
        "topic": "Greetings & Introductions",
        "grammar": "Basic sentence structure: Subject + Verb + Object",
        "explanation": """
## Grüß Gott! Hallo! Guten Tag!

German has different greetings depending on the time of day and formality.

**Formal greetings** (use with strangers, officials, older people):
- **Guten Morgen** — Good morning (before ~11am)
- **Guten Tag** — Good day (daytime)
- **Guten Abend** — Good evening (after ~6pm)
- **Auf Wiedersehen** — Goodbye (formal)

**Informal greetings** (friends, students, young people):
- **Hallo / Hi** — Hello
- **Hey** — Hey
- **Tschüss** — Bye
- **Ciao** — Bye (common in Germany too)

**In Aachen specifically**, you'll also hear the regional:
- **Grüß Gott** — common in the Rhineland region

**Introducing yourself:**
- Ich heiße Allen. → My name is Allen.
- Ich bin Allen. → I am Allen.
- Wie heißen Sie? → What's your name? (formal)
- Wie heißt du? → What's your name? (informal)
- Woher kommen Sie/kommst du? → Where are you from?
- Ich komme aus England/Nigeria/... → I come from...
- Ich wohne in Aachen. → I live in Aachen.
""",
        "vocabulary": [
            {"german": "Hallo", "english": "Hello", "article": "", "example_de": "Hallo! Wie geht es dir?", "example_en": "Hello! How are you?"},
            {"german": "Tschüss", "english": "Bye", "article": "", "example_de": "Tschüss! Bis morgen!", "example_en": "Bye! See you tomorrow!"},
            {"german": "Guten Morgen", "english": "Good morning", "article": "", "example_de": "Guten Morgen, Herr Müller!", "example_en": "Good morning, Mr Müller!"},
            {"german": "Guten Tag", "english": "Good day / Hello", "article": "", "example_de": "Guten Tag! Kann ich helfen?", "example_en": "Good day! Can I help?"},
            {"german": "Guten Abend", "english": "Good evening", "article": "", "example_de": "Guten Abend, willkommen!", "example_en": "Good evening, welcome!"},
            {"german": "Auf Wiedersehen", "english": "Goodbye (formal)", "article": "", "example_de": "Auf Wiedersehen und danke!", "example_en": "Goodbye and thank you!"},
            {"german": "Danke", "english": "Thank you", "article": "", "example_de": "Danke schön!", "example_en": "Thank you very much!"},
            {"german": "Bitte", "english": "Please / You're welcome", "article": "", "example_de": "Bitte sehr!", "example_en": "You're welcome!"},
            {"german": "Entschuldigung", "english": "Excuse me / Sorry", "article": "", "example_de": "Entschuldigung, wo ist der Bahnhof?", "example_en": "Excuse me, where is the station?"},
            {"german": "Ja", "english": "Yes", "article": "", "example_de": "Ja, natürlich!", "example_en": "Yes, of course!"},
            {"german": "Nein", "english": "No", "article": "", "example_de": "Nein, das stimmt nicht.", "example_en": "No, that's not right."},
            {"german": "ich", "english": "I", "article": "", "example_de": "Ich heiße Allen.", "example_en": "My name is Allen."},
            {"german": "heißen", "english": "to be named", "article": "", "example_de": "Wie heißt du?", "example_en": "What's your name?"},
            {"german": "kommen", "english": "to come (from)", "article": "", "example_de": "Ich komme aus Aachen.", "example_en": "I come from Aachen."},
            {"german": "wohnen", "english": "to live / reside", "article": "", "example_de": "Ich wohne in Aachen.", "example_en": "I live in Aachen."},
        ],
        "quiz": [
            {"q": "How do you say 'Good morning' in German?", "a": "Guten Morgen", "options": ["Guten Abend", "Guten Morgen", "Guten Tag", "Hallo"]},
            {"q": "Which greeting is formal?", "a": "Auf Wiedersehen", "options": ["Tschüss", "Ciao", "Auf Wiedersehen", "Hey"]},
            {"q": "Translate: 'Ich wohne in Aachen.'", "a": "I live in Aachen.", "options": ["I come from Aachen.", "I live in Aachen.", "I am in Aachen.", "I study in Aachen."]},
            {"q": "'Bitte' means:", "a": "Please / You're welcome", "options": ["Thank you", "Excuse me", "Please / You're welcome", "Sorry"]},
        ]
    },
    {
        "id": 2,
        "topic": "Articles: der, die, das",
        "grammar": "Definite articles in the nominative case",
        "explanation": """
## Der, Die, Das — The Most Important Thing in German

Every German noun has a grammatical gender: **masculine (der)**, **feminine (die)**, or **neuter (das)**. Unlike English, you must memorize the article with every noun.

**The golden rule: Always learn the article with the word.**
Don't learn: *Tisch* (table)
Do learn: *der Tisch* (the table)

**Definite articles (the):**
| Gender | Article | Example |
|--------|---------|---------|
| Masculine | **der** | der Mann (the man) |
| Feminine | **die** | die Frau (the woman) |
| Neuter | **das** | das Kind (the child) |
| Plural (all genders) | **die** | die Männer (the men) |

**Indefinite articles (a/an):**
| Gender | Article | Example |
|--------|---------|---------|
| Masculine | **ein** | ein Mann (a man) |
| Feminine | **eine** | eine Frau (a woman) |
| Neuter | **ein** | ein Kind (a child) |

**Tips for guessing gender:**
- Words ending in **-ung, -heit, -keit, -schaft** → usually **die**
- Words ending in **-chen, -lein** → always **das**
- Days, months, seasons → usually **der**
- Most words ending in **-er** (persons) → usually **der**
""",
        "vocabulary": [
            {"german": "der Mann", "english": "the man", "article": "der", "example_de": "Der Mann heißt Thomas.", "example_en": "The man's name is Thomas."},
            {"german": "die Frau", "english": "the woman", "article": "die", "example_de": "Die Frau kommt aus Berlin.", "example_en": "The woman comes from Berlin."},
            {"german": "das Kind", "english": "the child", "article": "das", "example_de": "Das Kind spielt im Park.", "example_en": "The child plays in the park."},
            {"german": "der Tisch", "english": "the table", "article": "der", "example_de": "Der Tisch ist groß.", "example_en": "The table is big."},
            {"german": "die Tür", "english": "the door", "article": "die", "example_de": "Die Tür ist offen.", "example_en": "The door is open."},
            {"german": "das Buch", "english": "the book", "article": "das", "example_de": "Das Buch ist interessant.", "example_en": "The book is interesting."},
            {"german": "der Hund", "english": "the dog", "article": "der", "example_de": "Der Hund ist süß.", "example_en": "The dog is cute."},
            {"german": "die Katze", "english": "the cat", "article": "die", "example_de": "Die Katze schläft.", "example_en": "The cat sleeps."},
            {"german": "das Haus", "english": "the house", "article": "das", "example_de": "Das Haus ist groß.", "example_en": "The house is big."},
            {"german": "der Stuhl", "english": "the chair", "article": "der", "example_de": "Der Stuhl ist alt.", "example_en": "The chair is old."},
            {"german": "die Stadt", "english": "the city", "article": "die", "example_de": "Aachen ist eine schöne Stadt.", "example_en": "Aachen is a beautiful city."},
            {"german": "das Auto", "english": "the car", "article": "das", "example_de": "Das Auto ist neu.", "example_en": "The car is new."},
        ],
        "quiz": [
            {"q": "What is the article for 'Hund' (dog)?", "a": "der", "options": ["der", "die", "das", "ein"]},
            {"q": "What is the article for 'Frau' (woman)?", "a": "die", "options": ["der", "die", "das", "eine"]},
            {"q": "What is the article for 'Buch' (book)?", "a": "das", "options": ["der", "die", "das", "ein"]},
            {"q": "Words ending in '-ung' are usually which gender?", "a": "feminine (die)", "options": ["masculine (der)", "feminine (die)", "neuter (das)", "plural (die)"]},
        ]
    },
    {
        "id": 3,
        "topic": "Numbers 1–100",
        "grammar": "Cardinal numbers and basic counting",
        "explanation": """
## Zahlen — Numbers

Numbers are essential for prices, addresses, phone numbers, and telling time.

**1–12 (memorize these):**
1 = **ein/eins**, 2 = **zwei**, 3 = **drei**, 4 = **vier**, 5 = **fünf**
6 = **sechs**, 7 = **sieben**, 8 = **acht**, 9 = **neun**, 10 = **zehn**
11 = **elf**, 12 = **zwölf**

**13–19 (add -zehn):**
13 = dreizehn, 14 = vierzehn, 15 = fünfzehn, 16 = sechzehn, 17 = siebzehn, 18 = achtzehn, 19 = neunzehn

**Tens:**
20 = **zwanzig**, 30 = **dreißig**, 40 = **vierzig**, 50 = **fünfzig**
60 = **sechzig**, 70 = **siebzig**, 80 = **achtzig**, 90 = **neunzig**, 100 = **hundert**

**Compound numbers (21–99):**
German says units BEFORE tens, joined with "und":
- 21 = **einundzwanzig** (one-and-twenty)
- 35 = **fünfunddreißig** (five-and-thirty)
- 48 = **achtundvierzig** (eight-and-forty)

**Useful phrases:**
- Das kostet **zwei Euro fünfzig**. → That costs €2.50.
- Ich bin **dreiundzwanzig** Jahre alt. → I am 23 years old.
- Meine Handynummer ist... → My mobile number is...
""",
        "vocabulary": [
            {"german": "eins", "english": "one (1)", "article": "", "example_de": "Ich habe einen Bruder.", "example_en": "I have one brother."},
            {"german": "zwei", "english": "two (2)", "article": "", "example_de": "Zwei Kaffee, bitte!", "example_en": "Two coffees, please!"},
            {"german": "drei", "english": "three (3)", "article": "", "example_de": "Drei Euro, bitte.", "example_en": "Three euros, please."},
            {"german": "zehn", "english": "ten (10)", "article": "", "example_de": "Es ist zehn Uhr.", "example_en": "It is ten o'clock."},
            {"german": "zwanzig", "english": "twenty (20)", "article": "", "example_de": "Ich bin zwanzig Jahre alt.", "example_en": "I am twenty years old."},
            {"german": "hundert", "english": "one hundred (100)", "article": "", "example_de": "Das kostet hundert Euro.", "example_en": "That costs one hundred euros."},
            {"german": "das Jahr", "english": "the year", "article": "das", "example_de": "Ich lerne seit einem Jahr Deutsch.", "example_en": "I have been learning German for a year."},
            {"german": "alt", "english": "old", "article": "", "example_de": "Wie alt bist du?", "example_en": "How old are you?"},
            {"german": "kosten", "english": "to cost", "article": "", "example_de": "Was kostet das?", "example_en": "How much does that cost?"},
            {"german": "der Euro", "english": "euro (currency)", "article": "der", "example_de": "Das kostet fünf Euro.", "example_en": "That costs five euros."},
        ],
        "quiz": [
            {"q": "How do you say 25 in German?", "a": "fünfundzwanzig", "options": ["zwanzigfünf", "fünfundzwanzig", "fünfzwanzig", "zwanzigundfünf"]},
            {"q": "What does 'dreißig' mean?", "a": "30", "options": ["13", "30", "33", "300"]},
            {"q": "Translate: 'Was kostet das?'", "a": "How much does that cost?", "options": ["What is that?", "How much does that cost?", "Do you have that?", "I want that."]},
            {"q": "How do you say 'I am 23 years old'?", "a": "Ich bin dreiundzwanzig Jahre alt.", "options": ["Ich bin zwanzigdrei Jahre alt.", "Ich bin dreiundzwanzig Jahre alt.", "Ich habe dreiundzwanzig Jahre.", "Ich bin dreiundzwanzig."]},
        ]
    },
    {
        "id": 4,
        "topic": "Present tense verbs (sein & haben)",
        "grammar": "Conjugation of sein (to be) and haben (to have)",
        "explanation": """
## Sein und Haben — To Be and To Have

These are the two most important verbs in German. You'll use them every single day.

**sein (to be):**
| Person | German | English |
|--------|--------|---------|
| ich | **bin** | I am |
| du | **bist** | you are |
| er/sie/es | **ist** | he/she/it is |
| wir | **sind** | we are |
| ihr | **seid** | you all are |
| sie/Sie | **sind** | they/you (formal) are |

**haben (to have):**
| Person | German | English |
|--------|--------|---------|
| ich | **habe** | I have |
| du | **hast** | you have |
| er/sie/es | **hat** | he/she/it has |
| wir | **haben** | we have |
| ihr | **habt** | you all have |
| sie/Sie | **haben** | they/you (formal) have |

**Examples:**
- Ich **bin** Student. → I am a student.
- Aachen **ist** in Deutschland. → Aachen is in Germany.
- Ich **habe** einen Laptop. → I have a laptop.
- Er **hat** keine Zeit. → He has no time.
- Wir **sind** müde. → We are tired.
""",
        "vocabulary": [
            {"german": "sein", "english": "to be", "article": "", "example_de": "Ich bin müde.", "example_en": "I am tired."},
            {"german": "haben", "english": "to have", "article": "", "example_de": "Ich habe Hunger.", "example_en": "I am hungry (I have hunger)."},
            {"german": "müde", "english": "tired", "article": "", "example_de": "Ich bin sehr müde.", "example_en": "I am very tired."},
            {"german": "hungrig", "english": "hungry", "article": "", "example_de": "Ich habe Hunger.", "example_en": "I am hungry."},
            {"german": "der Student", "english": "the (male) student", "article": "der", "example_de": "Ich bin Student an der RWTH.", "example_en": "I am a student at RWTH."},
            {"german": "die Studentin", "english": "the (female) student", "article": "die", "example_de": "Sie ist Studentin.", "example_en": "She is a student."},
            {"german": "Deutschland", "english": "Germany", "article": "", "example_de": "Aachen ist in Deutschland.", "example_en": "Aachen is in Germany."},
            {"german": "die Zeit", "english": "the time", "article": "die", "example_de": "Ich habe keine Zeit.", "example_en": "I have no time."},
            {"german": "kein/keine", "english": "no / not a", "article": "", "example_de": "Ich habe kein Auto.", "example_en": "I have no car."},
            {"german": "sehr", "english": "very", "article": "", "example_de": "Das ist sehr gut!", "example_en": "That is very good!"},
        ],
        "quiz": [
            {"q": "Ich ___ Student. (to be)", "a": "bin", "options": ["bist", "bin", "ist", "sind"]},
            {"q": "Er ___ keine Zeit. (to have)", "a": "hat", "options": ["habe", "hast", "hat", "haben"]},
            {"q": "Wir ___ müde. (to be)", "a": "sind", "options": ["bin", "bist", "ist", "sind"]},
            {"q": "Translate: 'Ich habe Hunger.'", "a": "I am hungry.", "options": ["I have hunger pains.", "I am hungry.", "I ate already.", "I want food."]},
        ]
    },
    {
        "id": 5,
        "topic": "Food & Ordering (Aachen Bäckerei)",
        "grammar": "Accusative case (basic), ordering phrases",
        "explanation": """
## Im Café und in der Bäckerei — At the Café and Bakery

Aachen has amazing bakeries (Bäckereien). This lesson covers everything you need to order food and drinks.

**Ordering phrases:**
- **Ich hätte gerne...** → I would like... (most polite)
- **Ich möchte...** → I would like...
- **Einmal..., bitte.** → One [item], please.
- **Zweimal..., bitte.** → Two [items], please.
- **Zum Mitnehmen oder hier essen?** → To take away or eat here?
- **Was darf es sein?** → What can I get you? (the shopkeeper says this)
- **Das macht X Euro.** → That comes to X euros.
- **Stimmt so.** → Keep the change.

**Common food items:**
- das Brötchen — bread roll (very common in Germany!)
- das Croissant — croissant
- der Kaffee — coffee
- der Tee — tea
- das Wasser — water
- die Brezel — pretzel
- der Kuchen — cake
- das Brot — bread

**Aachen tip:** The famous Aachener Printen (spiced gingerbread) is sold everywhere. Try asking for it!
- **Haben Sie Aachener Printen?** → Do you have Aachener Printen?
""",
        "vocabulary": [
            {"german": "das Brötchen", "english": "bread roll", "article": "das", "example_de": "Zwei Brötchen, bitte!", "example_en": "Two bread rolls, please!"},
            {"german": "der Kaffee", "english": "coffee", "article": "der", "example_de": "Einen Kaffee, bitte.", "example_en": "One coffee, please."},
            {"german": "der Tee", "english": "tea", "article": "der", "example_de": "Ich möchte einen Tee.", "example_en": "I would like a tea."},
            {"german": "das Wasser", "english": "water", "article": "das", "example_de": "Ein Wasser, bitte.", "example_en": "A water, please."},
            {"german": "das Brot", "english": "bread", "article": "das", "example_de": "Ich kaufe Brot.", "example_en": "I buy bread."},
            {"german": "der Kuchen", "english": "cake", "article": "der", "example_de": "Der Kuchen ist lecker!", "example_en": "The cake is delicious!"},
            {"german": "die Brezel", "english": "pretzel", "article": "die", "example_de": "Eine Brezel, bitte!", "example_en": "A pretzel, please!"},
            {"german": "lecker", "english": "delicious / tasty", "article": "", "example_de": "Das ist sehr lecker!", "example_en": "That is very delicious!"},
            {"german": "ich hätte gerne", "english": "I would like", "article": "", "example_de": "Ich hätte gerne einen Kaffee.", "example_en": "I would like a coffee."},
            {"german": "zum Mitnehmen", "english": "to take away", "article": "", "example_de": "Zum Mitnehmen, bitte.", "example_en": "To take away, please."},
            {"german": "bezahlen", "english": "to pay", "article": "", "example_de": "Ich möchte bezahlen.", "example_en": "I would like to pay."},
            {"german": "der Printen", "english": "Aachen gingerbread", "article": "der", "example_de": "Aachener Printen sind berühmt.", "example_en": "Aachen Printen are famous."},
        ],
        "quiz": [
            {"q": "How do you politely say 'I would like a coffee'?", "a": "Ich hätte gerne einen Kaffee.", "options": ["Ich will Kaffee.", "Ich hätte gerne einen Kaffee.", "Gib mir Kaffee.", "Kaffee, jetzt!"]},
            {"q": "What does 'Zum Mitnehmen?' mean?", "a": "To take away?", "options": ["For here?", "To take away?", "With milk?", "To go?... wait same thing"]},
            {"q": "What is a 'Brötchen'?", "a": "bread roll", "options": ["pretzel", "cake", "bread roll", "croissant"]},
            {"q": "'Stimmt so' means:", "a": "Keep the change.", "options": ["That's correct.", "Keep the change.", "How much?", "Thank you."]},
        ]
    },
    {
        "id": 6,
        "topic": "Days, Months & Time",
        "grammar": "Telling time, days of the week, months",
        "explanation": """
## Tage, Monate und Uhrzeit — Days, Months and Time

**Days of the week (Wochentage):**
Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag/Sonnabend, Sonntag

All days are **masculine (der)**. German weeks start on Monday.

**Months (Monate):**
Januar, Februar, März, April, Mai, Juni, Juli, August, September, Oktober, November, Dezember

All months are **masculine (der)**.

**Telling time:**
- **Wie spät ist es?** → What time is it?
- **Es ist...** → It is...
- Es ist **drei Uhr**. → It is 3 o'clock.
- Es ist **halb vier**. → It is half past three. ⚠️ (literally "half four" = 3:30!)
- Es ist **Viertel nach zwei**. → It is quarter past two.
- Es ist **Viertel vor sechs**. → It is quarter to six.

**⚠️ Important:** "halb vier" = 3:30, NOT 4:30! Germans say "half [of] four" meaning halfway to four.

**Useful time phrases:**
- heute — today
- morgen — tomorrow
- gestern — yesterday
- am Montag — on Monday
- um drei Uhr — at three o'clock
""",
        "vocabulary": [
            {"german": "der Montag", "english": "Monday", "article": "der", "example_de": "Am Montag habe ich Uni.", "example_en": "On Monday I have university."},
            {"german": "der Dienstag", "english": "Tuesday", "article": "der", "example_de": "Dienstag ist mein freier Tag.", "example_en": "Tuesday is my free day."},
            {"german": "der Mittwoch", "english": "Wednesday", "article": "der", "example_de": "Am Mittwoch gehe ich ins Gym.", "example_en": "On Wednesday I go to the gym."},
            {"german": "der Freitag", "english": "Friday", "article": "der", "example_de": "Freitags esse ich Pizza.", "example_en": "On Fridays I eat pizza."},
            {"german": "das Wochenende", "english": "weekend", "article": "das", "example_de": "Am Wochenende schlafe ich lang.", "example_en": "On the weekend I sleep in."},
            {"german": "heute", "english": "today", "article": "", "example_de": "Heute lerne ich Deutsch.", "example_en": "Today I am learning German."},
            {"german": "morgen", "english": "tomorrow", "article": "", "example_de": "Morgen habe ich einen Termin.", "example_en": "Tomorrow I have an appointment."},
            {"german": "gestern", "english": "yesterday", "article": "", "example_de": "Gestern war ich müde.", "example_en": "Yesterday I was tired."},
            {"german": "die Uhr", "english": "clock / o'clock", "article": "die", "example_de": "Es ist drei Uhr.", "example_en": "It is three o'clock."},
            {"german": "halb", "english": "half (past the previous hour)", "article": "", "example_de": "Es ist halb vier (= 3:30).", "example_en": "It is half past three (= 3:30)."},
        ],
        "quiz": [
            {"q": "What time is 'halb vier'?", "a": "3:30", "options": ["4:30", "3:30", "4:00", "3:00"]},
            {"q": "How do you say 'on Monday' in German?", "a": "am Montag", "options": ["in Montag", "am Montag", "bei Montag", "zu Montag"]},
            {"q": "What does 'morgen' mean?", "a": "tomorrow", "options": ["morning", "tomorrow", "today", "Monday"]},
            {"q": "Wie spät ist es? — What does this question mean?", "a": "What time is it?", "options": ["How late are you?", "What time is it?", "When do you finish?", "Are you late?"]},
        ]
    },
    {
        "id": 7,
        "topic": "Getting Around Aachen (Transport)",
        "grammar": "Prepositions of place: in, an, auf, bei, zu",
        "explanation": """
## Unterwegs in Aachen — Getting Around Aachen

Aachen has a great bus and tram system (ASEAG). This lesson teaches you everything you need to get around.

**Key phrases at the ticket machine / bus:**
- **Einmal zum Hauptbahnhof, bitte.** → One ticket to the main station, please.
- **Wo fährt der Bus nach...?** → Where does the bus to... leave from?
- **Wann kommt der nächste Bus?** → When does the next bus come?
- **Muss ich umsteigen?** → Do I need to change (buses/trains)?
- **Wie weit ist es bis...?** → How far is it to...?
- **Zu Fuß** → On foot / walking

**Prepositions of place:**
- **in** der Stadt — in the city
- **an** der Haltestelle — at the (bus) stop
- **auf** dem Marktplatz — on the market square
- **bei** der Uni — near the university
- **zu** Hause — at home
- **nach** Hause — (going) home

**Important Aachen locations:**
- der Hauptbahnhof (Hbf) — main train station
- der Dom — the cathedral (UNESCO heritage!)
- die Universität / RWTH — the university
- der Marktplatz — the market square
- die Bushaltestelle — the bus stop
- das Krankenhaus — hospital
""",
        "vocabulary": [
            {"german": "der Bahnhof", "english": "train station", "article": "der", "example_de": "Wo ist der Bahnhof?", "example_en": "Where is the train station?"},
            {"german": "der Bus", "english": "bus", "article": "der", "example_de": "Der Bus kommt um 10 Uhr.", "example_en": "The bus comes at 10 o'clock."},
            {"german": "die Haltestelle", "english": "bus/tram stop", "article": "die", "example_de": "Die Haltestelle ist dort.", "example_en": "The stop is there."},
            {"german": "das Ticket", "english": "ticket", "article": "das", "example_de": "Ich brauche ein Ticket.", "example_en": "I need a ticket."},
            {"german": "umsteigen", "english": "to change (transport)", "article": "", "example_de": "Muss ich umsteigen?", "example_en": "Do I need to change?"},
            {"german": "links", "english": "left", "article": "", "example_de": "Biegen Sie links ab.", "example_en": "Turn left."},
            {"german": "rechts", "english": "right", "article": "", "example_de": "Das ist rechts.", "example_en": "That is on the right."},
            {"german": "geradeaus", "english": "straight ahead", "article": "", "example_de": "Gehen Sie geradeaus.", "example_en": "Go straight ahead."},
            {"german": "der Dom", "english": "cathedral", "article": "der", "example_de": "Der Aachener Dom ist wunderschön.", "example_en": "Aachen Cathedral is beautiful."},
            {"german": "weit", "english": "far", "article": "", "example_de": "Ist es weit?", "example_en": "Is it far?"},
            {"german": "nah", "english": "near / close", "article": "", "example_de": "Die Uni ist nah.", "example_en": "The university is close."},
            {"german": "zu Fuß", "english": "on foot", "article": "", "example_de": "Ich gehe zu Fuß.", "example_en": "I go on foot."},
        ],
        "quiz": [
            {"q": "How do you ask 'Where is the train station?'", "a": "Wo ist der Bahnhof?", "options": ["Was ist der Bahnhof?", "Wo ist der Bahnhof?", "Wann ist der Bahnhof?", "Wie ist der Bahnhof?"]},
            {"q": "What does 'geradeaus' mean?", "a": "straight ahead", "options": ["left", "right", "straight ahead", "back"]},
            {"q": "'Muss ich umsteigen?' means:", "a": "Do I need to change?", "options": ["Where do I get off?", "Do I need to change?", "Is this the right bus?", "When does it arrive?"]},
            {"q": "What is 'die Haltestelle'?", "a": "bus/tram stop", "options": ["train station", "airport", "bus/tram stop", "bus ticket"]},
        ]
    },
    {
        "id": 8,
        "topic": "Family & People",
        "grammar": "Possessive pronouns: mein, dein, sein, ihr",
        "explanation": """
## Familie und Personen — Family and People

**Family vocabulary:**
- die Familie — family
- die Mutter / die Mama — mother / mum
- der Vater / der Papa — father / dad
- der Bruder — brother
- die Schwester — sister
- die Großmutter / die Oma — grandmother / granny
- der Großvater / der Opa — grandfather / grandad
- der Onkel — uncle
- die Tante — aunt
- das Baby — baby
- der Freund / die Freundin — boyfriend/male friend / girlfriend/female friend

**Possessive pronouns (my, your, his, her):**
| | masc. | fem. | neut. | plural |
|--|---|---|---|---|
| my | **mein** | **meine** | **mein** | **meine** |
| your (du) | **dein** | **deine** | **dein** | **deine** |
| his | **sein** | **seine** | **sein** | **seine** |
| her | **ihr** | **ihre** | **ihr** | **ihre** |

**Examples:**
- Das ist **mein** Bruder. → That is my brother. (Bruder = masc.)
- Das ist **meine** Mutter. → That is my mother. (Mutter = fem.)
- **Sein** Name ist Thomas. → His name is Thomas.
- **Ihre** Familie ist groß. → Her family is big.
""",
        "vocabulary": [
            {"german": "die Mutter", "english": "mother", "article": "die", "example_de": "Meine Mutter heißt Maria.", "example_en": "My mother's name is Maria."},
            {"german": "der Vater", "english": "father", "article": "der", "example_de": "Mein Vater kommt morgen.", "example_en": "My father comes tomorrow."},
            {"german": "der Bruder", "english": "brother", "article": "der", "example_de": "Ich habe einen Bruder.", "example_en": "I have one brother."},
            {"german": "die Schwester", "english": "sister", "article": "die", "example_de": "Meine Schwester ist älter.", "example_en": "My sister is older."},
            {"german": "die Familie", "english": "family", "article": "die", "example_de": "Meine Familie ist groß.", "example_en": "My family is big."},
            {"german": "der Freund", "english": "friend / boyfriend", "article": "der", "example_de": "Das ist mein Freund.", "example_en": "This is my friend / boyfriend."},
            {"german": "die Freundin", "english": "friend / girlfriend", "article": "die", "example_de": "Meine Freundin studiert Medizin.", "example_en": "My girlfriend studies medicine."},
            {"german": "mein/meine", "english": "my", "article": "", "example_de": "Das ist mein Buch.", "example_en": "That is my book."},
            {"german": "groß", "english": "big / tall", "article": "", "example_de": "Das Haus ist groß.", "example_en": "The house is big."},
            {"german": "klein", "english": "small / short", "article": "", "example_de": "Das Kind ist klein.", "example_en": "The child is small."},
        ],
        "quiz": [
            {"q": "How do you say 'my mother' in German?", "a": "meine Mutter", "options": ["mein Mutter", "meine Mutter", "seiner Mutter", "ihre Mutter"]},
            {"q": "What does 'der Freund' mean?", "a": "friend / boyfriend", "options": ["enemy", "stranger", "friend / boyfriend", "colleague"]},
            {"q": "'Meine Familie ist groß.' means:", "a": "My family is big.", "options": ["My family is small.", "My family is big.", "Her family is big.", "This family is big."]},
            {"q": "How do you say 'his name' in German?", "a": "sein Name", "options": ["ihr Name", "mein Name", "sein Name", "dein Name"]},
        ]
    },
    {
        "id": 9,
        "topic": "Shopping & Supermarket",
        "grammar": "Asking for things, prices, quantities",
        "explanation": """
## Einkaufen — Shopping

**At the supermarket (im Supermarkt):**
- **Wo finde ich...?** → Where can I find...?
- **Haben Sie...?** → Do you have...?
- **Was kostet das?** → How much does that cost?
- **Das ist zu teuer.** → That is too expensive.
- **Ich nehme das.** → I'll take that.
- **Ich zahle mit Karte.** → I'll pay by card.
- **Bar oder mit Karte?** → Cash or card?

**Quantities:**
- ein Kilo... — a kilo of...
- eine Flasche... — a bottle of...
- eine Packung... — a packet of...
- ein Stück... — a piece of...
- ein Liter... — a litre of...

**Important German shopping etiquette:**
- Bring your own bags (Bitte eine Tasche)
- At the till, items are scanned fast — have your money/card ready
- REWE, ALDI, LIDL, Kaufland are the main supermarkets
- Cash is still widely used in Germany — always have some!

**Common items:**
- die Milch — milk
- das Ei (pl: die Eier) — egg(s)
- das Fleisch — meat
- das Gemüse — vegetables
- das Obst — fruit
- der Käse — cheese
""",
        "vocabulary": [
            {"german": "die Milch", "english": "milk", "article": "die", "example_de": "Ich brauche Milch.", "example_en": "I need milk."},
            {"german": "das Ei", "english": "egg", "article": "das", "example_de": "Sechs Eier, bitte.", "example_en": "Six eggs, please."},
            {"german": "das Gemüse", "english": "vegetables", "article": "das", "example_de": "Ich esse viel Gemüse.", "example_en": "I eat a lot of vegetables."},
            {"german": "das Obst", "english": "fruit", "article": "das", "example_de": "Obst ist gesund.", "example_en": "Fruit is healthy."},
            {"german": "der Käse", "english": "cheese", "article": "der", "example_de": "Ich hätte gerne Käse.", "example_en": "I would like cheese."},
            {"german": "teuer", "english": "expensive", "article": "", "example_de": "Das ist zu teuer.", "example_en": "That is too expensive."},
            {"german": "billig", "english": "cheap", "article": "", "example_de": "ALDI ist sehr billig.", "example_en": "ALDI is very cheap."},
            {"german": "zahlen", "english": "to pay", "article": "", "example_de": "Ich zahle mit Karte.", "example_en": "I pay by card."},
            {"german": "die Tasche", "english": "bag / pocket", "article": "die", "example_de": "Haben Sie eine Tasche?", "example_en": "Do you have a bag?"},
            {"german": "brauchen", "english": "to need", "article": "", "example_de": "Ich brauche Hilfe.", "example_en": "I need help."},
        ],
        "quiz": [
            {"q": "How do you ask 'Where can I find the milk?'", "a": "Wo finde ich die Milch?", "options": ["Was ist die Milch?", "Wo finde ich die Milch?", "Haben Sie Milch?", "Ich will Milch."]},
            {"q": "'Bar oder mit Karte?' means:", "a": "Cash or card?", "options": ["With or without?", "Cash or card?", "Big or small?", "Here or to go?"]},
            {"q": "What does 'teuer' mean?", "a": "expensive", "options": ["cheap", "expensive", "good", "tasty"]},
            {"q": "How do you say 'I'll pay by card'?", "a": "Ich zahle mit Karte.", "options": ["Ich habe eine Karte.", "Ich zahle mit Karte.", "Ich will Karte.", "Karte, bitte."]},
        ]
    },
    {
        "id": 10,
        "topic": "At the University (RWTH Aachen)",
        "grammar": "Modal verbs: können, müssen, wollen",
        "explanation": """
## An der Uni — At University

This lesson covers academic vocabulary and the essential modal verbs.

**Modal verbs — the power words:**

**können** (can / to be able to):
ich kann, du kannst, er/sie kann, wir können, ihr könnt, sie können

**müssen** (must / to have to):
ich muss, du musst, er/sie muss, wir müssen, ihr müsst, sie müssen

**wollen** (to want to):
ich will, du willst, er/sie will, wir wollen, ihr wollt, sie wollen

**How they work:** Modal verb goes in position 2, main verb goes to the END as an infinitive.
- Ich **kann** Deutsch **sprechen**. → I can speak German.
- Ich **muss** zur Uni **gehen**. → I must go to the university.
- Ich **will** Deutsch **lernen**. → I want to learn German.

**University vocabulary:**
- die Vorlesung — lecture
- das Seminar — seminar
- die Hausarbeit — written assignment / essay
- die Prüfung — exam
- der Professor / die Professorin — professor
- die Bibliothek — library
- die Mensa — university canteen
- das Studium — studies / degree
""",
        "vocabulary": [
            {"german": "können", "english": "can / to be able to", "article": "", "example_de": "Ich kann Deutsch sprechen.", "example_en": "I can speak German."},
            {"german": "müssen", "english": "must / to have to", "article": "", "example_de": "Ich muss lernen.", "example_en": "I must study."},
            {"german": "wollen", "english": "to want to", "article": "", "example_de": "Ich will Arzt werden.", "example_en": "I want to become a doctor."},
            {"german": "die Vorlesung", "english": "lecture", "article": "die", "example_de": "Die Vorlesung beginnt um 9 Uhr.", "example_en": "The lecture starts at 9 o'clock."},
            {"german": "die Prüfung", "english": "exam", "article": "die", "example_de": "Ich habe morgen eine Prüfung.", "example_en": "I have an exam tomorrow."},
            {"german": "die Bibliothek", "english": "library", "article": "die", "example_de": "Ich lerne in der Bibliothek.", "example_en": "I study in the library."},
            {"german": "die Mensa", "english": "university canteen", "article": "die", "example_de": "Ich esse in der Mensa.", "example_en": "I eat in the canteen."},
            {"german": "lernen", "english": "to learn / study", "article": "", "example_de": "Ich lerne jeden Tag Deutsch.", "example_en": "I learn German every day."},
            {"german": "sprechen", "english": "to speak", "article": "", "example_de": "Ich spreche ein bisschen Deutsch.", "example_en": "I speak a little German."},
            {"german": "verstehen", "english": "to understand", "article": "", "example_de": "Ich verstehe das nicht.", "example_en": "I don't understand that."},
        ],
        "quiz": [
            {"q": "Where does the main verb go with a modal verb?", "a": "At the end of the sentence", "options": ["At the start", "After the modal", "At the end of the sentence", "In the middle"]},
            {"q": "'Ich muss lernen.' means:", "a": "I must study.", "options": ["I want to study.", "I can study.", "I must study.", "I should study."]},
            {"q": "How do you say 'I can speak German'?", "a": "Ich kann Deutsch sprechen.", "options": ["Ich sprechen Deutsch kann.", "Ich kann Deutsch sprechen.", "Deutsch ich kann sprechen.", "Ich spreche Deutsch kann."]},
            {"q": "What is 'die Mensa'?", "a": "university canteen", "options": ["library", "lecture hall", "university canteen", "exam room"]},
        ]
    },
]

# A1 vocabulary topics for initial seeding
STARTER_VOCABULARY = [
    # Colors
    {"german": "rot", "english": "red", "article": "", "topic": "colors", "example_de": "Das Auto ist rot.", "example_en": "The car is red."},
    {"german": "blau", "english": "blue", "article": "", "topic": "colors", "example_de": "Der Himmel ist blau.", "example_en": "The sky is blue."},
    {"german": "grün", "english": "green", "article": "", "topic": "colors", "example_de": "Das Gras ist grün.", "example_en": "The grass is green."},
    {"german": "schwarz", "english": "black", "article": "", "topic": "colors", "example_de": "Die Katze ist schwarz.", "example_en": "The cat is black."},
    {"german": "weiß", "english": "white", "article": "", "topic": "colors", "example_de": "Der Schnee ist weiß.", "example_en": "The snow is white."},
    # Weather (useful in Aachen - it rains a lot!)
    {"german": "das Wetter", "english": "the weather", "article": "das", "topic": "weather", "example_de": "Das Wetter ist schlecht.", "example_en": "The weather is bad."},
    {"german": "der Regen", "english": "rain", "article": "der", "topic": "weather", "example_de": "Es regnet in Aachen oft.", "example_en": "It rains often in Aachen."},
    {"german": "die Sonne", "english": "sun", "article": "die", "topic": "weather", "example_de": "Die Sonne scheint!", "example_en": "The sun is shining!"},
    {"german": "kalt", "english": "cold", "article": "", "topic": "weather", "example_de": "Im Winter ist es kalt.", "example_en": "In winter it is cold."},
    {"german": "warm", "english": "warm", "article": "", "topic": "weather", "example_de": "Im Sommer ist es warm.", "example_en": "In summer it is warm."},
]

def get_lesson(lesson_id):
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    return None

def get_total_lessons():
    return len(LESSONS)
