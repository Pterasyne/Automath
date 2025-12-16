import pandas as pd
import random

def create_excel(file_name):
    operandes = [(a, b) for a in range(1, 10) for b in range(1, 10)]

    additions = [(a, b, a + b, "Addition", "+") for a, b in operandes if a + b < 10]
    soustractions = [(a, b, a - b, "Soustraction", "-") for a, b in operandes if a - b > 0]

    random.shuffle(additions)
    random.shuffle(soustractions)

    data = []
    for a, b, r, op_type, signe in additions:
        data.append([
            op_type,#Type
            a,#Opérande 1
            signe,#signe
            b,#Opérande 2
            r,#Résultat attendu
            "", #Réponse enfant
            ""#Match
        ] + [""] * 10)#0 à 9

    for a, b, r, op_type, signe in soustractions: #not very efficient code oops
        data.append([
            op_type,#Type
            a,#Opérande 1
            signe,#signe
            b,#Opérande 2
            r,#Résultat attendu
            "", #Réponse enfant
            ""#Match
        ] + [""] * 10)#0 à 9

    columns = [
        "Type", "Opérande 1", "signe", "Opérande 2", "Résultat attendu",
        "Réponse enfant", "Match"
    ] + [str(i) for i in range(10)]

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f"{file_name}.xlsx", index=False)

# Génération des 26 fichiers
for i in range(1,27):
    create_excel(f"Strat_{i:02d}")
