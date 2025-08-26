import os
from textblob import TextBlob
from difflib import SequenceMatcher

POSITIVE_THRESHOLD = float(os.getenv("POSITIVE_THRESHOLD", "0.1"))
NEGATIVE_THRESHOLD = float(os.getenv("NEGATIVE_THRESHOLD", "-0.1"))

# Geavanceerde Nederlandse sentiment woordenboek
STRONG_NEGATIVE = [
    'kk', 'kanker', 'racist', 'racistisch', 'kut', 'shit', 'klote', 'kak',
    'verschrikkelijk', 'afschuwelijk', 'vreselijk', 'waardeloos', 'idioot',
    'tering', 'godverdomme', 'klootzak', 'lul', 'eikel', 'hoer', 'hoeren'
]

NEGATIVE_WORDS = [
    'slecht', 'dom', 'stom', 'achterlijk', 'debiel', 'mongool', 'lui', 
    'nutteloos', 'irritant', 'vervelend', 'rot', 'sukkel', 'saai',
    'onnozel', 'zinloos', 'onzin', 'belachelijk', 'idioot', 'stom',
    'verkeerd', 'fout', 'mislukt', 'teleurstellend', 'zwak', 'slap'
]

NEGATIVE_PHRASES = [
    'niet goed', 'niet leuk', 'niet fijn', 'niet prettig', 'niet duidelijk',
    'niet handig', 'niet nuttig', 'niet interessant', 'niet boeiend',
    'niet makkelijk', 'niet begrijpelijk', 'niet overzichtelijk', 'niet leerrijk',
    'beetje onnozel', 'niet zo', 'weinig leerrijk', 'te simpel', 'te makkelijk',
    'geen zin', 'geen nut', 'geen waarde', 'verspilling van tijd'
]

POSITIVE_WORDS = [
    'geweldig', 'fantastisch', 'super', 'excellent', 'perfect', 'mooi',
    'goed', 'goeie', 'goede', 'leuk', 'fijn', 'prettig', 'duidelijk', 'helder', 'inspirerend',
    'top', 'prima', 'uitstekend', 'cool', 'nice', 'lief', 'aardig',
    'vriendelijk', 'behulpzaam', 'interessant', 'boeiend', 'nuttig',
    'handig', 'makkelijk', 'begrijpelijk', 'overzichtelijk', 'leerrijk',
    'knap', 'slim', 'intelligent', 'vakkundig', 'professioneel', 'deskundig',
    'gemotiveerd', 'enthousiast', 'energiek', 'actief', 'betrokken', 'toegewijd',
    'gepassioneerd', 'gedreven', 'zorgzaam', 'attent', 'geduldig', 'ondersteunend',
    'creatief', 'innovatief', 'flexibel', 'aanpasbaar', 'betrouwbaar', 'punctueel',
    'georganiseerd', 'gestructureerd', 'systematisch', 'efficiënt', 'effectief'
]

# Context modifiers - woorden die sentiment kunnen veranderen
INTENSIFIERS = ['heel', 'zeer', 'erg', 'super', 'enorm', 'extreem', 'echt', 'hartstikke', 'ontzettend', 'verschrikkelijk', 'geweldig', 'fantastisch', 'buitengewoon', 'uitzonderlijk']
DIMINISHERS = ['beetje', 'een beetje', 'iets', 'enigszins', 'redelijk', 'tamelijk', 'vrij', 'nogal', 'best', 'wel']
NEGATORS = ['niet', 'geen', 'nooit', 'niemand', 'niets', 'nergens']

# Nederlandse positieve uitroepen en bevestigingen
POSITIVE_EXCLAMATIONS = ['ja!', 'top!', 'geweldig!', 'perfect!', 'prima!', 'mooi!', 'goed zo!', 'precies!', 'klopt!', 'helemaal goed!']

def fuzzy_match(word: str, target_list: list, threshold: float = 0.8) -> tuple[bool, str]:
    """
    Fuzzy matching voor schrijffouten.
    Returns (match_found, matched_word)
    """
    for target in target_list:
        # Simpele Levenshtein-achtige matching
        similarity = SequenceMatcher(None, word.lower(), target.lower()).ratio()
        if similarity >= threshold:
            return True, target
    return False, ""

# Schrijffout varianten van belangrijke woorden
SPELLING_VARIANTS = {
    'racist': ['rassist', 'rasist', 'racis', 'rassis'],
    'racistisch': ['rassistisch', 'rasistisch', 'racistich', 'rassistich'],
    'leerkrachten': ['kleerkrachten', 'lerkrachten', 'leerkrachte', 'kleerkrachte'],
    'onnozel': ['onozzel', 'onozel', 'onnosel', 'onozzel'],
    'slecht': ['slegt', 'sleght', 'slech'],
    'verschrikkelijk': ['verschrikelijk', 'verschrikkeljk', 'verschrikeljk'],
    'waardeloos': ['waardeloss', 'waardelos', 'waardeloze'],
    'motivatie': ['motivasie', 'motivacie', 'motivati']
}

def analyze_sentiment(text: str) -> tuple[str, float, float]:
    """
    Nederlandse sentiment analyse met verbeterde negatie detectie.
    Detecteert constructieve kritiek en subtiele negatieve patronen.
    
    Returns:
        tuple: (label, score, confidence)
    """
    text_lower = text.lower().strip()
    
    print(f"\n=== ANALYZING: '{text}' ===")

    # DIRECT NEGATIVE DETECTION - INCLUSIEF SUBTIELE KRITIEK
    SUPER_NEGATIVE_TRIGGERS = [
        'racist', 'racistisch', 'kk', 'kanker', 'kut', 'shit', 'klote',
        'onnozel', 'dom', 'stom', 'waardeloos', 'verschrikkelijk',
        'niet goed', 'niet leuk', 'niet leerrijk', 'beetje onnozel',
        'hebben nood aan', 'moeten beter', 'kunnen beter', 'missen',
        'ontbreekt', 'tekort', 'probleem', 'klacht', 'verbetering nodig',
        'onnodige', 'onnodig', 'moeilijker te volgen', 'moeilijk te volgen',
        'te moeilijk', 'verwarrend', 'onduidelijk', 'chaotisch'
    ]
    
    # NEGATION NEUTRALIZERS - "niet + negatief woord" = NEUTRAAL
    NEGATION_NEUTRALIZERS = [
        'niet slecht', 'niet zo slecht', 'niet erg slecht', 'niet heel slecht',
        'niet verschrikkelijk', 'niet waardeloos', 'niet zo erg'
    ]

    # NEGATION NEGATIVE - "niet + positief woord" = NEGATIEF
    NEGATION_NEGATIVE = [
        'niet goed', 'niet zo goed', 'niet erg goed', 'niet heel goed',
        'niet leuk', 'niet zo leuk', 'niet erg leuk', 'niet heel leuk',
        'niet fijn', 'niet zo fijn', 'niet prettig', 'niet zo prettig',
        'niet duidelijk', 'niet zo duidelijk', 'niet helder', 'niet zo helder',
        'niet interessant', 'niet zo interessant', 'niet boeiend', 'niet zo boeiend',
        'niet nuttig', 'niet zo nuttig', 'niet handig', 'niet zo handig',
        'niet makkelijk', 'niet zo makkelijk', 'niet begrijpelijk', 'niet zo begrijpelijk',
        'niet overzichtelijk', 'niet zo overzichtelijk', 'niet leerrijk', 'niet zo leerrijk',
        'niet georganiseerd', 'niet goed georganiseerd', 'niet zo goed georganiseerd',
        'niet gemotiveerd', 'niet zo gemotiveerd', 'niet erg gemotiveerd', 'niet heel gemotiveerd',
        'niet enthousiast', 'niet zo enthousiast', 'niet energiek', 'niet zo energiek',
        'niet actief', 'niet zo actief', 'niet betrokken', 'niet zo betrokken',
        'niet toegewijd', 'niet zo toegewijd', 'niet gedreven', 'niet zo gedreven',
        'niet zorgzaam', 'niet zo zorgzaam', 'niet geduldig', 'niet zo geduldig',
        'niet ondersteunend', 'niet zo ondersteunend', 'niet behulpzaam', 'niet zo behulpzaam',
        'niet creatief', 'niet zo creatief', 'niet flexibel', 'niet zo flexibel',
        'niet betrouwbaar', 'niet zo betrouwbaar', 'niet punctueel', 'niet zo punctueel',
        'niet gestructureerd', 'niet zo gestructureerd', 'niet efficiënt', 'niet zo efficiënt'
    ]
    
    # NEUTRAL/OK INDICATORS
    NEUTRAL_INDICATORS = [
        'het is ok', 'is ok', 'gaat wel', 'kan ermee door', 'redelijk',
        'niet slecht', 'wel ok', 'prima zo', 'acceptabel'
    ]
    
    SUPER_POSITIVE_TRIGGERS = [
        'geweldig', 'fantastisch', 'super', 'perfect', 'excellent',
        'heel goed', 'erg leuk', 'zeer interessant', 'goeie leerkracht',
        'goede leerkracht', 'goeie docent', 'goede docent', 'top docent',
        'prima leerkracht', 'uitstekende', 'knap', 'slim', 'vakkundig'
    ]

    # NEDERLANDSE POSITIEVE PATRONEN
    POSITIVE_PATTERNS = [
        'heel goed', 'erg goed', 'zeer goed', 'super goed', 'ontzettend goed',
        'heel leuk', 'erg leuk', 'zeer leuk', 'super leuk', 'ontzettend leuk',
        'heel fijn', 'erg fijn', 'zeer fijn', 'super fijn', 'ontzettend fijn',
        'heel duidelijk', 'erg duidelijk', 'zeer duidelijk', 'super duidelijk',
        'heel interessant', 'erg interessant', 'zeer interessant', 'super interessant',
        'heel nuttig', 'erg nuttig', 'zeer nuttig', 'super nuttig',
        'heel handig', 'erg handig', 'zeer handig', 'super handig',
        'heel behulpzaam', 'erg behulpzaam', 'zeer behulpzaam', 'super behulpzaam',
        'heel gemotiveerd', 'erg gemotiveerd', 'zeer gemotiveerd', 'super gemotiveerd',
        'heel enthousiast', 'erg enthousiast', 'zeer enthousiast', 'super enthousiast',
        'heel betrokken', 'erg betrokken', 'zeer betrokken', 'super betrokken',
        'heel geduldig', 'erg geduldig', 'zeer geduldig', 'super geduldig',
        'heel creatief', 'erg creatief', 'zeer creatief', 'super creatief',
        'heel professioneel', 'erg professioneel', 'zeer professioneel', 'super professioneel',
        'goed uitgelegd', 'duidelijk uitgelegd', 'helder uitgelegd', 'prima uitgelegd',
        'goed georganiseerd', 'prima georganiseerd', 'netjes georganiseerd',
        'fijne leerkracht', 'aardige leerkracht', 'lieve leerkracht', 'vriendelijke leerkracht',
        'fijne docent', 'aardige docent', 'lieve docent', 'vriendelijke docent',
        'goede begeleiding', 'fijne begeleiding', 'prima begeleiding', 'uitstekende begeleiding',
        'leuke lessen', 'interessante lessen', 'boeiende lessen', 'leerzame lessen',
        'goed tempo', 'fijn tempo', 'prima tempo', 'geschikt tempo',
        'duidelijke uitleg', 'heldere uitleg', 'goede uitleg', 'prima uitleg',
        'nuttige feedback', 'goede feedback', 'constructieve feedback', 'waardevolle feedback',
        'prettige sfeer', 'goede sfeer', 'fijne sfeer', 'ontspannen sfeer',
        'goed bereikbaar', 'makkelijk bereikbaar', 'altijd bereikbaar',
        'snel antwoord', 'snelle reactie', 'goede communicatie', 'duidelijke communicatie',
        'ben tevreden', 'ben blij', 'vind het fijn', 'vind het leuk', 'vind het goed',
        'ben positief', 'ben enthousiast', 'raad aan', 'beveel aan', 'zou aanraden',
        'hou van', 'vind leuk', 'vind goed', 'vind fijn', 'vind interessant',
        'goede ervaring', 'positieve ervaring', 'fijne ervaring', 'leuke ervaring',
        'tevreden over', 'blij met', 'content met', 'happy met', 'dankbaar voor',
        'waardeer het', 'stel op prijs', 'ben dankbaar', 'appreciate',
        'goed gedaan', 'knap gedaan', 'mooi gedaan', 'prima gedaan', 'netjes gedaan',
        'chapeau', 'petje af', 'respect', 'waardering', 'complimenten'
    ]
    
    # EERST: CHECK VOOR NEGATION NEGATIVE - "niet goed" = NEGATIEF
    for negation_neg in NEGATION_NEGATIVE:
        if negation_neg in text_lower:
            print(f"NEGATION NEGATIVE FOUND: '{negation_neg}' - FORCING NEGATIVE")
            return "Negative", -0.7, 0.8

    # TWEEDE: CHECK VOOR NEUTRALIZERS - "niet slecht" = NEUTRAAL
    for neutralizer in NEGATION_NEUTRALIZERS:
        if neutralizer in text_lower:
            print(f"NEUTRALIZER FOUND: '{neutralizer}' - FORCING NEUTRAL")
            return "Neutral", 0.0, 0.8
    
    # TWEEDE: CHECK VOOR NEUTRAL INDICATORS
    for indicator in NEUTRAL_INDICATORS:
        if indicator in text_lower:
            print(f"NEUTRAL INDICATOR FOUND: '{indicator}' - FORCING NEUTRAL")
            return "Neutral", 0.0, 0.8
    
    # DERDE: CHECK FOR IMMEDIATE NEGATIVE TRIGGERS (EXACT + FUZZY)
    for trigger in SUPER_NEGATIVE_TRIGGERS:
        if trigger in text_lower:
            print(f"NEGATIVE TRIGGER FOUND (EXACT): '{trigger}'")
            return "Negative", -0.8, 0.9
    
    # CHECK FOR SPELLING VARIANTS OF TRIGGERS
    spelling_trigger_variants = {
        'racistisch': ['rassistisch', 'rasistisch', 'racistich'],
        'racist': ['rassist', 'rasist'],
        'onnozel': ['onozzel', 'onozel'],
        'verschrikkelijk': ['verschrikelijk', 'verschrikkeljk']
    }
    
    for correct_trigger, variants in spelling_trigger_variants.items():
        for variant in variants:
            if variant in text_lower:
                print(f"NEGATIVE TRIGGER FOUND (SPELLING): '{variant}' -> '{correct_trigger}'")
                return "Negative", -0.8, 0.9
    
    # CHECK FOR IMMEDIATE POSITIVE TRIGGERS
    for trigger in SUPER_POSITIVE_TRIGGERS:
        if trigger in text_lower:
            print(f"POSITIVE TRIGGER FOUND (EXACT): '{trigger}'")
            return "Positive", 0.8, 0.9

    # CHECK FOR POSITIVE PATTERNS
    for pattern in POSITIVE_PATTERNS:
        if pattern in text_lower:
            print(f"POSITIVE PATTERN FOUND: '{pattern}'")
            return "Positive", 0.7, 0.8

    # CHECK FOR POSITIVE EXCLAMATIONS
    for exclamation in POSITIVE_EXCLAMATIONS:
        if exclamation in text_lower:
            print(f"POSITIVE EXCLAMATION FOUND: '{exclamation}'")
            return "Positive", 0.8, 0.9
    
    # SPECIAL PATTERNS - SUBTLE NEGATIVITY + CONSTRUCTIEVE KRITIEK
    SUBTLE_NEGATIVE_PATTERNS = [
        'hebben nood aan', 'hebben behoefte aan', 'zouden moeten', 'kunnen beter',
        'missen nog', 'ontbreekt nog', 'zou fijn zijn als', 'hopelijk wordt',
        'jammer dat', 'spijtig dat', 'zou helpen als', 'meer aandacht voor',
        'vaak onnodige', 'te veel', 'te weinig', 'moeilijker maakt',
        'maakt het moeilijk', 'zorgt voor verwarring', 'leidt tot problemen',
        'veroorzaakt', 'hindert', 'stoort', 'belemmert', 'bemoeilijkt',
        'slecht georganiseerd', 'niet georganiseerd', 'chaotisch', 'rommelig',
        'door elkaar', 'onduidelijke structuur', 'geen structuur', 'warrig',
        'verwarrende opzet', 'slechte planning', 'geen planning', 'ongestructureerd'
    ]
    
    for pattern in SUBTLE_NEGATIVE_PATTERNS:
        if pattern in text_lower:
            print(f"SUBTLE NEGATIVE PATTERN FOUND: '{pattern}'")
            return "Negative", -0.6, 0.8
    
    # EXTRA: PROBLEEM-VEROORZAKENDE PATRONEN
    PROBLEM_CAUSING_PATTERNS = [
        'maakt moeilijker', 'maakt het moeilijk', 'maakt verwarrend',
        'zorgt voor problemen', 'leidt tot verwarring', 'veroorzaakt problemen',
        'commentaren wat', 'gedrag wat', 'houding die'
    ]
    
    for pattern in PROBLEM_CAUSING_PATTERNS:
        if pattern in text_lower:
            print(f"PROBLEM-CAUSING PATTERN FOUND: '{pattern}'")
            return "Negative", -0.7, 0.8
    
    # SLIMME WORD-BY-WORD ANALYSE MET NEGATIE CONTEXT
    words = text_lower.split()
    negative_count = 0
    positive_count = 0

    for i, word in enumerate(words):
        clean_word = word.strip('.,!?;:"()[]{}')
        
        # CHECK VOOR NEGATIE CONTEXT
        if i > 0 and words[i-1] == 'niet':
            # "niet + negatief woord" = NEUTRAAL (skip)
            if clean_word in ['slecht', 'verschrikkelijk', 'waardeloos', 'dom', 'stom']:
                print(f"NEGATION NEUTRALIZER: 'niet {clean_word}' - SKIPPING NEGATIVE")
                continue  # Skip deze negatieve woord omdat het geneutraliseerd is

            # "niet + positief woord" = NEGATIEF (count as negative)
            if clean_word in ['goed', 'goeie', 'goede', 'leuk', 'fijn', 'prettig', 'duidelijk', 'helder', 'interessant', 'boeiend', 'nuttig', 'handig', 'makkelijk', 'begrijpelijk', 'overzichtelijk', 'leerrijk', 'georganiseerd', 'gemotiveerd', 'enthousiast', 'energiek', 'actief', 'betrokken', 'toegewijd', 'gedreven', 'zorgzaam', 'geduldig', 'ondersteunend', 'creatief', 'flexibel', 'betrouwbaar', 'punctueel', 'gestructureerd', 'efficiënt']:
                negative_count += 1
                print(f"NEGATION NEGATIVE: 'niet {clean_word}' - COUNTING AS NEGATIVE")
                continue  # Skip de normale positieve verwerking

        # CHECK VOOR "NIET ZO" CONTEXT
        if i > 1 and words[i-2] == 'niet' and words[i-1] == 'zo':
            # "niet zo + positief woord" = NEGATIEF
            if clean_word in ['goed', 'goeie', 'goede', 'leuk', 'fijn', 'prettig', 'duidelijk', 'helder', 'interessant', 'boeiend', 'nuttig', 'handig', 'makkelijk', 'begrijpelijk', 'overzichtelijk', 'leerrijk', 'georganiseerd', 'gemotiveerd', 'enthousiast', 'energiek', 'actief', 'betrokken', 'toegewijd', 'gedreven', 'zorgzaam', 'geduldig', 'ondersteunend', 'creatief', 'flexibel', 'betrouwbaar', 'punctueel', 'gestructureerd', 'efficiënt']:
                negative_count += 1
                print(f"NEGATION NEGATIVE: 'niet zo {clean_word}' - COUNTING AS NEGATIVE")
                continue  # Skip de normale positieve verwerking
        
        # EXACT MATCH - NEGATIVE WORDS (alleen als niet geneutraliseerd)
        if clean_word in ['racist', 'racistisch', 'kk', 'kanker', 'kut', 'shit', 'klote', 'onnozel', 'dom', 'stom', 'slecht', 'waardeloos', 'verschrikkelijk', 'idioot', 'debiel']:
            negative_count += 2
            print(f"STRONG NEGATIVE WORD (EXACT): '{clean_word}'")
        elif clean_word in ['saai', 'vervelend', 'irritant', 'nood', 'tekort', 'missen', 'ontbreekt', 'probleem', 'klacht', 'beter', 'verbetering', 'onnodige', 'onnodig', 'moeilijker', 'moeilijk', 'verwarrend', 'onduidelijk', 'chaotisch', 'hinderlijk', 'storend']:
            negative_count += 1
            print(f"NEGATIVE WORD (EXACT): '{clean_word}'")
        
        # FUZZY MATCH - SCHRIJFFOUTEN
        else:
            # Check spelling variants
            for correct_word, variants in SPELLING_VARIANTS.items():
                if clean_word in variants:
                    if correct_word in ['racist', 'racistisch', 'onnozel', 'slecht', 'verschrikkelijk', 'waardeloos']:
                        negative_count += 2
                        print(f"STRONG NEGATIVE WORD (SPELLING): '{clean_word}' -> '{correct_word}'")
                    break
            
            # Fuzzy match against strong negative words
            strong_negatives = ['racist', 'racistisch', 'onnozel', 'verschrikkelijk', 'waardeloos']
            match_found, matched_word = fuzzy_match(clean_word, strong_negatives, 0.75)
            if match_found:
                negative_count += 2
                print(f"STRONG NEGATIVE WORD (FUZZY): '{clean_word}' -> '{matched_word}'")
        
        # POSITIVE WORDS (EXACT MATCH) - met intensifier check
        if clean_word in ['geweldig', 'fantastisch', 'super', 'perfect', 'excellent', 'goed', 'goeie', 'goede', 'leuk', 'mooi', 'fijn', 'top', 'prima', 'uitstekend', 'knap', 'slim', 'vakkundig', 'professioneel', 'gemotiveerd', 'enthousiast', 'energiek', 'actief', 'betrokken', 'toegewijd', 'gedreven', 'zorgzaam', 'geduldig', 'ondersteunend', 'creatief', 'flexibel', 'betrouwbaar', 'punctueel', 'georganiseerd', 'gestructureerd', 'efficiënt']:
            # Check for intensifier before this word
            intensifier_boost = 0
            if i > 0 and words[i-1].strip('.,!?;:"()[]{}') in ['heel', 'zeer', 'erg', 'super', 'ontzettend', 'hartstikke']:
                intensifier_boost = 1
                print(f"INTENSIFIER FOUND: '{words[i-1]} {clean_word}' - EXTRA BOOST")

            positive_count += 1 + intensifier_boost
            print(f"POSITIVE WORD: '{clean_word}' (boost: {intensifier_boost})")

    print(f"NEGATIVE COUNT: {negative_count}, POSITIVE COUNT: {positive_count}")
    
    # AGGRESSIVE DECISION MAKING
    if negative_count > 0:
        score = -0.7 - (negative_count * 0.2)
        print(f"FORCING NEGATIVE: score = {score}")
        return "Negative", score, 0.8
    elif positive_count > 0:
        score = 0.7 + (positive_count * 0.1)
        print(f"FORCING POSITIVE: score = {score}")
        return "Positive", score, 0.8
    else:
        # FALLBACK TO TEXTBLOB BUT STILL AGGRESSIVE
        blob = TextBlob(text)
        textblob_score = float(blob.sentiment.polarity)
        
        if textblob_score > 0.1:
            print(f"TEXTBLOB POSITIVE: {textblob_score}")
            return "Positive", textblob_score, 0.6
        elif textblob_score < -0.1:
            print(f"TEXTBLOB NEGATIVE: {textblob_score}")
            return "Negative", textblob_score, 0.6
        else:
            print(f"TRULY NEUTRAL: {textblob_score}")
            return "Neutral", textblob_score, 0.5
