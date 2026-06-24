import streamlit as st
import json
import fitz  # PyMuPDF

# =========================
# PDF EXTRACT
# =========================
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text


# =========================
# CHUNKING SEMPLICE
# =========================
def chunk_text(text, size=1200):
    return [text[i:i+size] for i in range(0, len(text), size)]


# =========================
# LLM MOCK (SOSTITUIBILE CON OPENAI)
# =========================
def call_llm(text):
    return json.dumps({
        "sintesi": "Analisi automatica circolare",
        "obblighi": ["Verifica normativa", "Aggiornamento contrattuale"],
        "scadenze": ["30 giorni"],
        "criticita": ["Interpretazione ambigua"]
    })


# =========================
# APP UI
# =========================
st.set_page_config(page_title="Circolari PRO", layout="wide")

st.title("🧾 Circolari PRO - SaaS stabile")

file = st.file_uploader("Carica circolare PDF")

if file:

    text = extract_text(file)
    chunks = chunk_text(text)

    st.write(f"Chunk generati: {len(chunks)}")

    if st.button("Analizza circolare"):

        results = []

        for c in chunks:
            res = call_llm(c)
            results.append(json.loads(res))

        st.session_state["data"] = results[0]

        st.success("Analisi completata")
        st.json(results[0])


if "data" in st.session_state:

    data = st.session_state["data"]

    if st.button("Salva"):
        st.success("Salvato (mock)")

    if st.button("Export Word"):
        st.success("Export pronto (da integrare)")

    if st.button("Chat RAG"):
        st.info("Chat RAG nel prossimo step")
