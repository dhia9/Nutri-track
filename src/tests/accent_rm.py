import unicodedata


def enlever_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    resultat = ""
    for c in texte:
        if unicodedata.combining(c) == 0:
            resultat += c
    return resultat


print(enlever_accents("Pruneau, sans noyau, sec"))
print(enlever_accents("Âge"))
print(enlever_accents("Taïlle (cm)"))