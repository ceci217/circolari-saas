import streamlit as st
import json

# =========================
# CORE IMPORT (ORA CORRETTO)
# =========================
from core.extract import extract_text
from core.chunker import chunk_text
from core.llm import call_llm
from core.db import init_db, save
from core.compare import compare
from export.word import export_word

# =========================
# INIT DB
# =========================
init_db()

# =========================
# UI
# =========================
st.set_page_config(page_title="Circolari PRO", layout="wide")

st.title("🧾 Circolari PRO - Consulente del Lavoro")

file = st.file_uploader("Carica circolare PDF", type=["pdf"])

# =========================
# PROCESSO FILE
# =========================
if file:

    text = extract_text(file)
    chunks = chunk_text(text)

    st.write(f"Chunk generati: {len(chunks)}")

    if st.button("Analizza circolare"):

        results = []

        for c in chunks:
            res = call_llm(c)

            try:
                results.append(json.loads(res))
            except:
                st.error("Errore: output LLM non è JSON valido")
                st.stop()

        st.session_state["data"] = results[0]

        st.success("Analisi completata")
        st.json(results[0])

# =========================
# DASHBOARD RISULTATI
# =========================
if "data" in st.session_state:

    data = st.session_state["data"]

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Salva"):
            save("circolare", "ente", data)
            st.success("Salvato")

    with col2:
        if st.button("📄 Export Word"):
            export_word(data)
            st.success("Word generato")

    with col3:
        if st.button("🔎 Compare"):
            st.info("Funzione confronto attualmente in sviluppo")

# =========================
# CHAT PLACEHOLDER
# =========================
st.divider()

st.subheader("💬 Chat RAG")

st.info("Funzione RAG in arrivo (fase 2)")
