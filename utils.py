import re, unicodedata

def normalize_urdu(text):
    text = unicodedata.normalize("NFC", text)
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"[\u0617-\u061A\u064B-\u0652]", "", text)  # remove diacritics
    text = re.sub(r"[\"“”\(\)\[\]\*<>…•]", " ", text)
    return " ".join(text.split())

def normalize_roman(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-\']", " ", text)
    return " ".join(text.split())

# simple transliteration table (extend as needed)
MAP_TABLE = {"ا":"a","ب":"b","پ":"p","ت":"t","ٹ":"t","ج":"j","چ":"ch","خ":"kh","د":"d","ڈ":"d",
             "ر":"r","ڑ":"r","ز":"z","س":"s","ش":"sh","ف":"f","ق":"q","ک":"k","گ":"g","ل":"l",
             "م":"m","ن":"n","و":"o","ہ":"h","ی":"y","ع":"’","غ":"gh"}

def transliterate_urdu_to_roman(urd):
    out = []
    for ch in urd:
        out.append(MAP_TABLE.get(ch, ch))
    return "".join(out)
