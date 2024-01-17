import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('airline-safety.csv')

# Titre de l'application
st.title('Visualisations sur la sécurité des compagnies aériennes')

# Expliquation des valeurs de la dataset
st.header("Description des colonnes")
with st.expander("Explication des valeurs de la dataset"):
    st.write("""
    - **airline :** Compagnie aérienne (l'astérisque indique que les filiales régionales sont incluses)
    - **avail_seat_km_per_week :** Sièges-kilomètres disponibles parcourus chaque semaine
    - **incidents_85_99 :** Nombre total d'incidents, 1985-1999
    - **fatal_accidents_85_99 :** Nombre total d'accidents mortels, 1985-1999
    - **fatalities_85_99 :** Nombre total de décès, 1985-1999
    - **incidents_00_14 :** Nombre total d'incidents, 2000-2014
    - **fatal_accidents_00_14 :** Nombre total d'accidents mortels, 2000-2014
    - **fatalities_00_14 :** Nombre total de décès, 2000-2014
    """)

# Visualisation 1 : Liste des compagnies n'ayant jamais fait d'accident
st.header("Liste des compagnies n'ayant jamais fait d'accident")
selected_years = st.radio("Sélectionnez la plage d'années", ["85_99", "00_14"])

# Filtrer le DataFrame en fonction de la plage d'années sélectionnée
if selected_years == "85_99":
    condition = (df['incidents_85_99'] == 0) & (df['incidents_00_14'] == 0)
    resultats = df.loc[condition, ['airline', 'incidents_85_99', 'incidents_00_14']]
    title = "entre 1985 et 2014"

elif selected_years == "00_14":
    condition = (df['incidents_00_14'] == 0)
    resultats = df.loc[condition, ['airline', 'incidents_00_14']]
    title = "entre 2000 et 2014"

# Afficher le résultat
st.subheader(f"Liste des compagnies n'ayant jamais fait d'accident {title}")
with st.expander(f"Liste des compagnies n'ayant jamais fait d'accident {title}"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    tbl = plt.table(cellText=resultats.values,
                    colLabels=resultats.columns,
                    loc='center',
                    colWidths=[0.2, 0.2, 0.2],
                    cellLoc='center',
                    bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 1.5)
    plt.subplots_adjust(left=0.2, right=0.8, bottom=0.2, top=0.8)
    st.pyplot(fig)

# Visualisation 2 : Liste des compagnies n'ayant pas fait d'accident en 1985-1999
st.header(f"Liste des compagnies n'ayant pas fait d'accident {selected_years}")
condition = (df[f'incidents_{selected_years}'] == 0)
resultats = df.loc[condition, ['airline', f'incidents_{selected_years}']]
st.table(resultats)

# Visualisation 3 : Liste des compagnies n'ayant jamais fait d'accident entre 2000 et 2014
st.header("Liste des compagnies n'ayant jamais fait d'accident entre 2000 et 2014")
condition = (df['incidents_00_14'] == 0)
resultats = df.loc[condition, ['airline', 'incidents_00_14']]
st.table(resultats)

# Visualisation 4 : Liste des compagnies n'ayant pas connu d'accident mortel
st.header("Liste des compagnies n'ayant pas connu d'accident mortel entre 1985 et 2014")
condition = (df['fatal_accidents_85_99'] == 0) & (df['fatal_accidents_00_14'] == 0)
resultats = df.loc[condition, ['airline', 'fatal_accidents_85_99', 'fatal_accidents_00_14']]
st.table(resultats)

# Visualisation 5 : Nombre d'accident mortel sur nombre d'accident total entre 1985 et 1999
st.header("Nombre d'accident mortel sur nombre d'accident total entre 1985 et 1999")
condition = (df['fatal_accidents_85_99'] == 0)
resultats = df[condition].copy()

plt.figure(figsize=(10, 6))
plt.plot(resultats['airline'], resultats['incidents_85_99'], label='incidents_85_99', color='blue', marker='o')
plt.plot(resultats['airline'], resultats['fatal_accidents_85_99'], label='fatal_accidents_85_99', color='red', marker='o')

plt.title("Nombre d'accident mortel sur nombre d'accident total entre 1985 et 1999")
plt.xlabel('Compagnies aériennes')
plt.ylabel("Nombre d'accident")
plt.xticks(rotation=45, ha='right')
for i, txt in enumerate(resultats['incidents_85_99']):
    plt.text(i, txt, f"{txt}", ha='center', va='bottom', fontsize=10, color='black')

for i, txt in enumerate(resultats['fatal_accidents_85_99']):
    plt.text(i, txt, f"{txt}", ha='center', va='bottom', fontsize=10, color='black')

plt.legend()
plt.grid(True)
st.pyplot(plt)


# Visualisation 7 : Top 5 des compagnies avec le plus grand nombre de décès entre 1985 et 2014
st.header("Top 5 des compagnies avec le plus grand nombre de décès entre 1985 et 2014")
df['total_fatalities'] = df['fatalities_85_99'] + df['fatalities_00_14']
top_companies = df.groupby('airline')['total_fatalities'].sum().nlargest(5)

plt.figure(figsize=(10, 6))
plt.bar(top_companies.index, top_companies.values, color='skyblue')
plt.xlabel('Compagnies aériennes')
plt.ylabel('Nombre total de décès')
plt.title('Top 5 des compagnies avec le plus grand nombre de décès entre 1985 et 2014')
plt.xticks(rotation=45, ha='right')

for i, value in enumerate(top_companies.values):
    plt.text(i, value, str(value), ha='center', va='bottom')
st.pyplot(plt)

# Visualisation 8 : Top 5 des compagnies avec le plus petit nombre de décès entre 1985 et 2014
st.header("Top 5 des compagnies avec le plus petit nombre de décès entre 1985 et 2014")
df['total_fatalities'] = df['fatalities_85_99'] + df['fatalities_00_14']
bottom_companies = df.groupby('airline')['total_fatalities'].sum().nsmallest(5)
plt.figure(figsize=(10, 6))
plt.bar(bottom_companies.index, bottom_companies.values, color='skyblue')
plt.xlabel('Compagnies aériennes')
plt.ylabel('Nombre total de décès')
plt.title('Top 5 des compagnies avec le plus petit nombre de décès entre 1985 et 2014')
plt.xticks(rotation=45, ha='right')

for i, value in enumerate(bottom_companies.values):
    plt.text(i, value, str(value), ha='center', va='bottom')
st.pyplot(plt)

# Visualisation 9 : Top 5 des compagnies avec le plus grand nombre de sièges-kilomètres disponibles par semaine
st.header("Top 5 des compagnies avec le plus grand nombre de sièges-kilomètres disponibles par semaine")
top_companies = df.nlargest(5, 'avail_seat_km_per_week')
top_companies = top_companies.sort_values(by='avail_seat_km_per_week', ascending=True)

colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral']
plt.barh(top_companies['airline'], top_companies['avail_seat_km_per_week'], color=colors)

plt.xlabel('Sièges-kilomètres parcourus par semaine')
plt.ylabel('Compagnies aériennes')
plt.title('Top 5 des compagnies avec le plus grand nombre de sièges-kilomètres disponibles par semaine')
for i, value in enumerate(top_companies['avail_seat_km_per_week']):
    plt.text(value, i, f"{value:,}", va='center', ha='left', color='black')

st.pyplot(plt)
