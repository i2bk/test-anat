import streamlit as st
import fitz  # PyMuPDF
import io

st.title("📄 PDF Upload, Search & Edit Tool")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_data = uploaded_file.read()
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    st.success(f"Loaded {len(doc)} pages from {uploaded_file.name}")

    # Search feature
    search_term = st.text_input("Search for text in the PDF")
    replace_term = st.text_input("Replace with (leave blank to just search)")
    replace = st.button("Search & Replace")

    if replace and search_term:
        matches = 0
        for page in doc:
            text_instances = page.search_for(search_term)
            matches += len(text_instances)
            if replace_term:
                for inst in text_instances:
                    # draw white rectangle over text
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()
                    # insert new text in same place
                    page.insert_text((inst.x0, inst.y0), replace_term, fontsize=12, color=(0, 0, 0))
        st.info(f"Found {matches} matches for '{search_term}'")
        if replace_term and matches > 0:
            # Save edited version
            output_pdf = io.BytesIO()
            doc.save(output_pdf)
            st.download_button(
                "Download edited PDF",
                output_pdf.getvalue(),
                file_name=f"edited_{uploaded_file.name}",
                mime="application/pdf"
            )

    # Optional: view page text
    if st.checkbox("Show first page text"):
        st.text(doc[0].get_text("text"))

