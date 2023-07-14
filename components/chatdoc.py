import streamlit as st
from config.global_config import (
    MAX_CONTEXT,
    EMOJI,
    ERROR_RESPONSE,
    DISCLAIMER
)


def chatdoc_page():
    print("run chatdoc page...")
    st.title(f"Regulus ChatDoc {EMOJI['doc']}")

    uploaded_file = st.file_uploader(
        "Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt"],
        help="Scanned documents are not supported yet!",
    )
