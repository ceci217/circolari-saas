import os
import sys
import streamlit as st
import json

# =========================
# FIX PATH (RENDER SAFE)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =========================
# IMPORT CONFIG
# =========================
from config import USE_OLLAMA, OPENAI_MODEL, OLLAMA_MODEL

# =========================
# IMPORT CORE MODULES
# =========================
from core.extract import extract_text
from core.chunker import chunk_text
from core.llm import call_llm
from core.db import init_db, save
from core.compare import compare
from export.word import export_word

# =========================
# INIT
# =========================
init_db()

# =========================
# UI CONFIG
# =========================
st.set_page_config(
    page_title="Circolari PRO SaaS",
    layout="wide"
)

st.title("🧾 Circolari PRO - Consulente del Lavoro")

st.write("Carica una circolare PDF e ottieni analisi strutturata AI.")

# =========================
# UPLOAD FILE
# =========================
file = st.file_uploader("Carica circolare PDF", type=["pdf"])

# =========================
# PROCESSING PIPELINE
# =========================
if file:

    with st.spinner("Estrazione testo in corso..."):
        text = extract_text(file)

    chunks = chunk_text(text)

    st.success(f"Testo estratto. Chunk generati: {len(chunks)}")

    if st.button("Analizza circolare"):

        results = []

        with st.spinner("Analisi AI in corso..."):

            for c in chunks:
                res = call_llm(c)

                try:
                    results.append(json.loads(res))
                except:
                    st.error("Errore: output LLM non è JSON valido")
                    st.stop()

        # salva primo risultato
        st.session_state["data"] = results[0]

        st.success("Analisi completata")

        st.subheader("Risultato AI")
        st.json(results[0])

# =========================
# DASHBOARD RISULTATI
# =========================
if "data" in st.session_state:

    data = st.session_state["data"]

    st.divider()

    st.subheader("📊 Azioni disponibili")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Salva su DB"):
            save("circolare", "ente", data)
            st.success("Salvato correttamente")

    with col2:
        if st.button("📄 Export Word"):
            export_word(data)
            st.success("Word generato")

    with col3:
        if st.button("🔎 Compare"):
            st.info("Funzione confronto in sviluppo")

# =========================
# RAG PLACEHOLDER
# =========================
st.divider()

st.subheader("💬 Chat normativa (RAG)")

st.info("Modulo RAG sarà attivato nella fase 2 del progetto")
