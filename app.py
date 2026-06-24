import sys
import os

# FIX PATH (Render-safe)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import json

from core.extract import extract_text
from core.chunker import chunk_text
from core.llm import call_llm
from core.db import init_db, save
from core.compare import compare
from export.word import export_word

init_db()

st.title("🧾 Circolari PRO - Consulente del Lavoro")

file = st.file_uploader("Carica circolare")

if file:

    text = extract_text(file)
    chunks = chunk_text(text)

    results = []

    if st.button("Analizza"):

        for c in chunks:
            res = call_llm(c)
            try:
                results.append(json.loads(res))
            except:
                st.error("JSON non valido")

        st.session_state["data"] = results[0]

        st.success("Analisi completata")
        st.json(results[0])

if "data" in st.session_state:

    data = st.session_state["data"]

    if st.button("Salva"):
        save("circolare", "ente", data)

    if st.button("Export Word"):
        export_word(data)
        st.success("Word generato")

    if st.button("Chat RAG"):
        st.write("Modalità chat da implementare sopra dataset")
