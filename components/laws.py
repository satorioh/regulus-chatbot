import streamlit as st
from utils import get_abs_path
from config.global_config import (
    EMOJI,
)
from embeddings import save_embeddings

source_folder = get_abs_path('laws')


def laws_page():
    print("run laws page...")
    st.title(f"Regulus ChatDoc {EMOJI['law']}")
    save_embeddings(source_folder)
