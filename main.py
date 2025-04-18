import streamlit as st

st.set_page_config(page_title="Outils de génération", page_icon="⚙️")

st.title("Bienvenue sur ton générateur !")

menu = st.selectbox("Choisis un outil 👇", [
    "🏷️ Générateur Markdown (.md)",
    "📝 Générateur Word Stylé (.docx)"
])

if menu == "🏷️ Générateur Markdown (.md)":
    st.header("Générateur Markdown")
    st.markdown("👉 [Clique ici pour lancer le générateur Markdown](https://md-generator.streamlit.app)")

elif menu == "📝 Générateur Word Stylé (.docx)":
    st.header("Générateur Word Stylé")
    st.markdown("👉 [Clique ici pour lancer le Generator Word Style](https://word-generator-style.streamlit.app)")
