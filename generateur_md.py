import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Générateur Markdown", layout="wide")
st.title("📝 Générateur Markdown multi-règles")

# Champ pour le titre du livre
title = st.text_input("Titre du livre")

# Section pour les règles
st.subheader("Règles de transformation")
col1, col2 = st.columns([2, 1])
with col1:
    keyword_input = st.text_input("Mot-clé", key="keyword")
with col2:
    style_input = st.text_input("Style (ex: ##)", key="style")

# Initialiser la liste des règles
if "all_rules" not in st.session_state:
    st.session_state.all_rules = []

# Ajouter une règle
if st.button("➕ Ajouter la règle"):
    if keyword_input.strip() and style_input.strip():
        st.session_state.all_rules.append((keyword_input.strip(), style_input.strip()))
    else:
        st.warning("Les deux champs doivent être remplis.")

# Affichage des règles
if st.session_state.all_rules:
    st.markdown("**Règles ajoutées :**")
    for idx, (k, s) in enumerate(st.session_state.all_rules, 1):
        st.write(f"{idx}. `{k}` → `{s}`")

# Zone de texte
st.subheader("Colle ici ton texte brut :")
raw_text = st.text_area("Texte à transformer", height=300)

# Fonction de transformation
def detect_markdown_from_text(text, title, rules):
    lines = text.strip().split('\n')
    output = [f"# {title.strip()}"] if title.strip() else []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        matched = False
        for keyword, style_tag in rules:
            if clean.lower().startswith(keyword.lower()):
                output.append(f"{style_tag} {clean}")
                matched = True
                break
        if not matched:
            output.append(clean)
    return "\n\n".join(output)

# Génération du fichier
if st.button("💾 Générer le fichier .md"):
    if not raw_text:
        st.warning("Le champ de texte est vide.")
    elif not st.session_state.all_rules:
        st.warning("Ajoute au moins une règle.")
    else:
        processed_text = detect_markdown_from_text(raw_text, title, st.session_state.all_rules)
        st.download_button("📥 Télécharger le Markdown", data=processed_text, file_name="output.md", mime="text/markdown")
