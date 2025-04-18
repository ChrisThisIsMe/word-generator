import streamlit as st
from docx import Document
from docx.shared import Pt, Cm, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def customize_style(style, font_name, font_size, spacing_before, spacing_after, line_spacing):
    style.font.name = font_name
    style.font.size = Pt(font_size)
    style.paragraph_format.space_before = Pt(spacing_before)
    style.paragraph_format.space_after = Pt(spacing_after)
    style.paragraph_format.line_spacing = line_spacing

def process_markdown(md_lines, doc, config):
    buffer = []
    marker_found = False

    for _ in range(config['blank_pages']):
        doc.add_paragraph("")
        doc.add_page_break()

    for line in md_lines:
        stripped = line.strip()
        if stripped.lower() == config['marker_keyword']:
            marker_found = True
            p = doc.add_paragraph(stripped, style="Heading 1")
            p.alignment = config['align_h1']
            for _ in range(config['blank_after_marker']):
                doc.add_paragraph("")
                doc.add_page_break()
            continue
        elif stripped.startswith("# "):
            if config['add_page_break_h1']:
                doc.add_page_break()
            text = stripped[2:].upper() if config['uppercase_h1'] else stripped[2:]
            p = doc.add_paragraph(text, style="Heading 1")
            p.alignment = config['align_h1']
        elif stripped.startswith("## "):
            if config['add_page_break_h2']:
                doc.add_page_break()
            text = stripped[3:].upper() if config['uppercase_h2'] else stripped[3:]
            p = doc.add_paragraph(text, style="Heading 2")
            p.alignment = config['align_h2']
        elif stripped.startswith("### "):
            text = stripped[4:]
            p = doc.add_paragraph(text, style="Heading 3")
            p.alignment = config['align_h3']
        elif stripped == "":
            if buffer:
                paragraph = " ".join(buffer).strip()
                if paragraph:
                    p = doc.add_paragraph(paragraph, style="Normal")
                    p.alignment = config['align_normal']
                buffer = []
        else:
            buffer.append(stripped)

    for _ in range(config['blank_end']):
        doc.add_paragraph("")
        doc.add_page_break()

    return doc

st.title("Générateur Word à partir de Markdown")

uploaded_file = st.file_uploader("Choisir un fichier Markdown (.md ou .txt)", type=["md", "txt"])

with st.expander("Paramètres du document"):

    col1, col2 = st.columns(2)

    with col1:
        h1_font = st.text_input("Police H1", "Garamond")
        h2_font = st.text_input("Police H2", "Garamond")
        h3_font = st.text_input("Police H3", "Garamond")
        normal_font = st.text_input("Police texte normal", "Garamond")

        h1_size = st.number_input("Taille H1", 8, 72, 24)
        h2_size = st.number_input("Taille H2", 8, 72, 16)
        h3_size = st.number_input("Taille H3", 8, 72, 13)
        normal_size = st.number_input("Taille texte normal", 8, 72, 11)

        h1_before = st.number_input("Espace avant H1", 0, 100, 0)
        h1_after = st.number_input("Espace après H1", 0, 100, 12)
        h1_spacing = st.number_input("Interligne H1", 1.0, 3.0, 2.0)

        h2_before = st.number_input("Espace avant H2", 0, 100, 0)
        h2_after = st.number_input("Espace après H2", 0, 100, 9)
        h2_spacing = st.number_input("Interligne H2", 1.0, 3.0, 1.15)

        h3_before = st.number_input("Espace avant H3", 0, 100, 0)
        h3_after = st.number_input("Espace après H3", 0, 100, 9)
        h3_spacing = st.number_input("Interligne H3", 1.0, 3.0, 1.15)

        normal_before = st.number_input("Espace avant texte", 0, 100, 0)
        normal_after = st.number_input("Espace après texte", 0, 100, 6)
        normal_spacing = st.number_input("Interligne texte", 1.0, 3.0, 1.15)

        marker_keyword = st.text_input("Mot-clé repère (ex. Page Légale)", "Page Légale")
        blank_after_marker = st.number_input("Pages après repère", 0, 10, 1)
        blank_pages = st.number_input("Pages blanches au début", 0, 10, 2)
        blank_end = st.number_input("Pages blanches à la fin", 0, 10, 1)

    with col2:
        page_width = st.number_input("Largeur page (mm)", 100, 200, 120)
        page_height = st.number_input("Hauteur page (mm)", 100, 300, 190)

        margin_top = st.number_input("Marge haut (cm)", 0.0, 10.0, 1.8)
        margin_bottom = st.number_input("Marge bas (cm)", 0.0, 10.0, 1.8)
        margin_left = st.number_input("Marge gauche (cm)", 0.0, 10.0, 2.0)
        margin_right = st.number_input("Marge droite (cm)", 0.0, 10.0, 2.0)

        align_map = {"Gauche": WD_ALIGN_PARAGRAPH.LEFT, "Centré": WD_ALIGN_PARAGRAPH.CENTER,
                    "Droite": WD_ALIGN_PARAGRAPH.RIGHT, "Justifié": WD_ALIGN_PARAGRAPH.JUSTIFY}

        align_h1 = align_map[st.selectbox("Alignement H1", list(align_map.keys()), index=1)]
        align_h2 = align_map[st.selectbox("Alignement H2", list(align_map.keys()), index=0)]
        align_h3 = align_map[st.selectbox("Alignement H3", list(align_map.keys()), index=0)]
        align_normal = align_map[st.selectbox("Alignement Texte", list(align_map.keys()), index=3)]

        uppercase_h1 = st.checkbox("Mettre H1 en MAJUSCULES", True)
        uppercase_h2 = st.checkbox("Mettre H2 en MAJUSCULES")
        add_page_break_h1 = st.checkbox("Saut de page avant H1", True)
        add_page_break_h2 = st.checkbox("Saut de page avant H2", True)

if uploaded_file and st.button("Générer le fichier Word"):
    doc = Document()

    section = doc.sections[0]
    section.page_width = Mm(page_width)
    section.page_height = Mm(page_height)
    section.top_margin = Cm(margin_top)
    section.bottom_margin = Cm(margin_bottom)
    section.left_margin = Cm(margin_left)
    section.right_margin = Cm(margin_right)

    # Styles
    customize_style(doc.styles['Heading 1'], h1_font, h1_size, h1_before, h1_after, h1_spacing)
    customize_style(doc.styles['Heading 2'], h2_font, h2_size, h2_before, h2_after, h2_spacing)
    customize_style(doc.styles['Heading 3'], h3_font, h3_size, h3_before, h3_after, h3_spacing)
    customize_style(doc.styles['Normal'], normal_font, normal_size, normal_before, normal_after, normal_spacing)

    content = uploaded_file.read().decode("utf-8").splitlines()

    config = {
        "marker_keyword": marker_keyword.lower(),
        "blank_after_marker": blank_after_marker,
        "blank_pages": blank_pages,
        "blank_end": blank_end,
        "uppercase_h1": uppercase_h1,
        "uppercase_h2": uppercase_h2,
        "add_page_break_h1": add_page_break_h1,
        "add_page_break_h2": add_page_break_h2,
        "align_h1": align_h1,
        "align_h2": align_h2,
        "align_h3": align_h3,
        "align_normal": align_normal
    }

    doc = process_markdown(content, doc, config)

    output_path = "/tmp/generated_word_style.docx"
    doc.save(output_path)

    with open(output_path, "rb") as file:
        btn = st.download_button(
            label="📥 Télécharger le fichier Word",
            data=file,
            file_name="styled_output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
