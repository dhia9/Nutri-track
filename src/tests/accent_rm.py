import unicodedata


def enlever_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    resultat = ""
    for c in texte:
        if unicodedata.combining(c) == 0:
            resultat += c
    return resultat


def test_enlever_accents_simple():
    print(enlever_accents("Pruneau, sans noyau, sec") == "Pruneau, sans noyau, sec")


def test_enlever_accents_circumflex():
    print(enlever_accents("Âge") == "Age")


def test_enlever_accents_diaeresis():
    print(enlever_accents("Taïlle (cm)") == "Taille (cm)")
