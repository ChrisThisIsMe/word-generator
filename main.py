import streamlit as st

st.set_page_config(page_title="Outils de génération", page_icon="⚙️")

st.title("Bienvenue sur ton générateur !")

menu = st.selectbox("Choisis un outil 👇", [
    "--- Choisis un outil ---",
    "🏷️ Générateur Markdown (.md)",
    "📝 Générateur Word Stylé (.docx)"
])

# Ne redirige que si un vrai choix est fait
if menu == "🏷️ Générateur Markdown (.md)":
    st.write("Redirection en cours...")
    st.markdown(
        "<meta http-equiv='refresh' content='0;url=https://md-generator.streamlit.app'>",
        unsafe_allow_html=True
    )

elif menu == "📝 Générateur Word Stylé (.docx)":
    st.write("Redirection en cours...")
    st.markdown(
        "<meta http-equiv='refresh' content='0;url=https://word-generator-style.streamlit.app'>",
        unsafe_allow_html=True
    )
