import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rentabilité École d'Arts Vivants", layout="wide")

# === Données de base ===
frais_fixes = 25000
cout_prof_par_h = 35
cout_par_slot = cout_prof_par_h * 4  # 1 cours/semaine × 4 semaines

activites = {
    "Bien-être":     {"tarif": 52, "slots": 7,  "capacite": 4},
    "Danse":         {"tarif": 46, "slots": 36, "capacite": 15},
    "Arts":          {"tarif": 46, "slots": 5,  "capacite": 15},
    "Chant/Éveil":   {"tarif": 46, "slots": 14, "capacite": 15},
    "Musique":       {"tarif": 77, "slots": 36, "capacite": 4},
    "Théâtre":       {"tarif": 50, "slots": 3,  "capacite": 15},
}

# === Calculs ===
rows = []
total_recette = 0
total_cout = 0
total_marge = 0
total_capacite = 0

for nom, data in activites.items():
    capacite_max = data["slots"] * data["capacite"]
    recette = data["tarif"] * capacite_max
    cout = data["slots"] * cout_par_slot
    marge = recette - cout

    rows.append({
        "Activité": nom,
        "Tarif (€)": data["tarif"],
        "Slots": data["slots"],
        "Capacité/slot": data["capacite"],
        "Capacité totale": capacite_max,
        "Recette (€)": recette,
        "Coût prof (€)": cout,
        "Marge (€)": marge
    })

    total_recette += recette
    total_cout += cout
    total_marge += marge
    total_capacite += capacite_max

# === DataFrame et affichage ===
df = pd.DataFrame(rows)

st.title("📊 Analyse de rentabilité - École d'Arts Vivants")
st.subheader("📌 Données par activité")
st.dataframe(df, use_container_width=True)

# === Résumé global ===
seuil_rentabilite = frais_fixes / total_marge if total_marge != 0 else 0
eleves_min = seuil_rentabilite * total_capacite
marge_par_eleve = total_marge / total_capacite

col1, col2, col3 = st.columns(3)
col1.metric("Marge totale", f"{total_marge:,.0f} €")
col2.metric("Capacité totale", f"{total_capacite} élèves")
col3.metric("Marge unitaire moyenne", f"{marge_par_eleve:.2f} € / élève")

st.markdown("---")
st.subheader("📈 Seuil de rentabilité")
col4, col5 = st.columns(2)
col4.metric("Taux de remplissage nécessaire", f"{seuil_rentabilite*100:.1f} %")
col5.metric("Élèves nécessaires", f"{int(eleves_min)}")

st.markdown("> Ce tableau est basé sur un remplissage à 100% pour tous les cours.")
