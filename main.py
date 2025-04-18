import streamlit as st

st.set_page_config(page_title="Outils de génération", page_icon="⚙️")

st.title("Bienvenue sur ton générateur personnel ⚙️")

st.markdown("---")

st.subheader("📄 Générateur Markdown (.md)")
st.markdown(
    """
    🔹 Crée ton fichier Markdown stylé automatiquement à partir de règles simples.<br>
    👉 [Lancer le générateur Markdown](https://md-generator.streamlit.app)
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("📝 Générateur Word Stylé (.docx)")
st.markdown(
    """
    🔹 Transforme un fichier Markdown en un document Word stylisé avec tes préférences.<br>
    👉 [Lancer le générateur Word Stylé](https://word-generator-style.streamlit.app)
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.info("Choisis ton outil ci-dessus et laisse la magie opérer ✨")
