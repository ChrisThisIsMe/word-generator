import streamlit as st

st.set_page_config(page_title="Outils de génération", page_icon="⚙️")

st.title("Bienvenue sur ton générateur !")

menu = st.selectbox(
    "Choisis un outil 👇",
    [
        "--- Choisis un outil ---",
        "🏷️ Générateur Markdown (.md)",
        "📝 Générateur Word Stylé (.docx)"
    ]
)

if menu == "🏷️ Générateur Markdown (.md)":
    st.markdown("""
        <meta http-equiv="refresh" content="0; url='https://md-generator.streamlit.app'" />
    """, unsafe_allow_html=True)

elif menu == "📝 Générateur Word Stylé (.docx)":
    st.markdown("""
        <meta http-equiv="refresh" content="0; url='https://word-generator-style.streamlit.app'" />
    """, unsafe_allow_html=True)
