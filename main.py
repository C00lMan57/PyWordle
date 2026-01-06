import random
import os
import datetime
import hashlib
import json

LOGO = """
██████╗ ██╗   ██╗██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     █████╗
██╔═══╝   ╚██╔╝  ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██╔══╝
██║        ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗███████╗
╚═╝        ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝
"""

HISTORIQUE_FILE = "historique.json"

def charger_historique():
    if os.path.exists(HISTORIQUE_FILE):
        try:
            with open(HISTORIQUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_historique(date, resultats):
    historique = charger_historique()
    historique[date] = resultats
    with open(HISTORIQUE_FILE, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=4)

def charger_mots():
    if not os.path.exists("mots.txt"):
        with open("mots.txt", "w", encoding="utf-8") as f:
            f.write("pomme\nlaser\ntrain\nninja\nsalon\nplage\npetit\naimer\n")

    with open("mots.txt", "r", encoding="utf-8") as f:
        mots = [ligne.strip().lower() for ligne in f if len(ligne.strip()) == 5]
    
    if not mots:
        print("❌ Erreur : Le fichier mots.txt est vide ou ne contient pas de mots de 5 lettres.")
        return []
    return mots

def jouer(mode="normal"):
    mots = charger_mots()
    if not mots:
        return

    aujourdhui = datetime.date.today().isoformat()
    if mode == "daily":
        historique = charger_historique()
        if aujourdhui in historique:
            print(f"\n--- MODE QUOTIDIEN ({aujourdhui}) ---")
            print("❌ Tu as déjà fait le défi d'aujourd'hui !")
            print("Voici tes résultats :")
            for res in historique[aujourdhui]:
                print(res)
            input("\nAppuie sur Entrée pour revenir au menu...")
            return

        hash_obj = hashlib.md5(aujourdhui.encode())
        index = int(hash_obj.hexdigest(), 16) % len(mots)
        mot_secret = mots[index]
        print(f"\n--- MODE QUOTIDIEN ({aujourdhui}) ---")
    else:
        mot_secret = random.choice(mots)
        print("\n--- NOUVELLE PARTIE ---")

    essais_max = 6
    historique_essais = []

    print("Devine le mot de 5 lettres. Tu as 6 essais.\n")
    print("🟩 = bonne lettre bien placée")
    print("🟨 = bonne lettre mal placée")
    print("⬜ = mauvaise lettre\n")

    victoire = False
    for essai in range(1, essais_max + 1):
        while True:
            try:
                proposition = input(f"Essai {essai}/{essais_max} : ").lower().strip()
            except EOFError:
                return
            
            if len(proposition) == 5:
                break
            print("❌ Le mot doit faire exactement 5 lettres.")

        resultat = ["⬜"] * 5
        mot_secret_liste = list(mot_secret)
        proposition_liste = list(proposition)

        # Passage 1 : Lettres bien placées
        for i in range(5):
            if proposition_liste[i] == mot_secret_liste[i]:
                resultat[i] = "🟩"
                mot_secret_liste[i] = ""
                proposition_liste[i] = ""

        # Passage 2 : Lettres présentes mais mal placées
        for i in range(5):
            if proposition_liste[i] != "":
                if proposition_liste[i] in mot_secret_liste:
                    for idx, char in enumerate(mot_secret_liste):
                        if char == proposition_liste[i]:
                            resultat[i] = "🟨"
                            mot_secret_liste[idx] = ""
                            break

        ligne_resultat = "".join(resultat)
        print(ligne_resultat + "\n")
        historique_essais.append(ligne_resultat)

        if proposition == mot_secret:
            if mode == "daily":
                print("🌟 INCROYABLE ! Tu as triomphé du défi quotidien ! 🌟")
                print("Reviens demain pour un nouveau mot !")
                sauvegarder_historique(aujourdhui, historique_essais)
            else:
                print("🎉 Bravo ! Tu as trouvé le mot !")
            victoire = True
            break
    
    if not victoire:
        print(f"💀 Perdu ! Le mot était : {mot_secret}")
        if mode == "daily":
            sauvegarder_historique(aujourdhui, historique_essais)
    
    input("\nAppuie sur Entrée pour revenir au menu...")

def afficher_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(LOGO)
        print("1. Jouer (Mot aléatoire)")
        print("2. Mode Daily (Le mot du jour)")
        print("3. Quitter")
        
        choix = input("\nChoisis une option : ").strip()
        
        if choix == "1":
            jouer(mode="normal")
        elif choix == "2":
            jouer(mode="daily")
        elif choix == "3":
            print("Merci d'avoir joué ! À bientôt.")
            break
        else:
            print("❌ Option invalide.")
            input("Appuie sur Entrée pour continuer...")

if __name__ == "__main__":
    afficher_menu()
