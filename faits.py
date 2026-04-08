# faits.py - Gestion des faits connus

faits = []

def ajouter_fait(fait):
    if fait not in faits:
        faits.append(fait)

def fait_existe(fait):
    return fait in faits

def reinitialiser():
    faits.clear()

def afficher_faits():
    print("Faits connus:", faits)