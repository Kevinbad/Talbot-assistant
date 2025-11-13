import streamlit as st
import os
import subprocess
import json
import time
from query import answer_query

st.set_page_config(
    page_title="Talbot Announcements - Bot de Anuncios",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Login simple
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Talbot Announcements")
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center;'>Ingresa tus credenciales</h3>", unsafe_allow_html=True)
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Iniciar Sesión")
            if submitted:
                correct_username = os.environ.get('BOT_USERNAME', 'test')
                correct_password = os.environ.get('BOT_PASSWORD', 'prueba123')
                if username == correct_username and password == correct_password:
                    st.session_state.logged_in = True
                    st.success("¡Bienvenido!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
    st.stop()

# Refined Apple-inspired CSS with cooler tones
st.markdown("""
<style>
.stApp {
    background-color: #FFFFFF;
    color: #0A0A0A;
    font-family: "San Francisco", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
}
.stTitle {
    color: #0A0A0A;
    text-align: center;
    font-size: 2.5em;
    font-weight: 700;
    background-color: #F5F5F7;
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 40px;
}
.stSelectbox, .stTextInput, .stDateInput, .stButton {
    margin-bottom: 24px;
}
.stButton button {
    background-color: #007AFF;
    color: #FFFFFF;
    border-radius: 8px;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
    transition: all 0.3s ease;
    border: none;
    padding: 12px 24px;
}
.stButton button:hover {
    background-color: #005FCC;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}
.stExpander {
    background-color: #F5F5F7;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #D2D2D7;
}
.stSuccess {
    border-radius: 8px;
    background-color: #F5F5F7;
    color: #34C759;
    border: 1px solid #D2D2D7;
}
.stError {
    border-radius: 8px;
    background-color: #F5F5F7;
    color: #FF3B30;
    border: 1px solid #D2D2D7;
}
.stInfo {
    border-radius: 8px;
    background-color: #F5F5F7;
    color: #0A0A0A;
    border: 1px solid #D2D2D7;
}
.stSidebar {
    background-color: #F5F5F7;
    color: #0A0A0A;
    padding: 20px;
}
.stSidebar .stHeader {
    color: #0A0A0A;
    font-weight: 700;
}
.stButton button[key="admin_button"] {
    background-color: #007AFF !important;
    color: #FFFFFF !important;
}
.stButton button[key="admin_button"]:hover {
    background-color: #005FCC !important;
}
.stExpander summary {
    background-color: #007AFF !important;
    color: #FFFFFF !important;
    border-radius: 8px;
    padding: 15px;
    font-weight: 600;
}
.faq-card {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
    border: 1px solid #D2D2D7;
    box-shadow: 0 1px 3px rgba(0, 122, 255, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}
.faq-card:hover {
    background-color: #F5F5F7;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
    transform: translateY(-1px);
}
.faq-card h4 {
    color: #0A0A0A;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
}
.faq-card p {
    color: #6E6E73;
    font-size: 13px;
    line-height: 1.4;
    margin-bottom: 8px;
}
.faq-card .signature {
    font-weight: 600;
    color: #0A0A0A;
    font-size: 12px;
    text-align: right;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .stTitle {
        font-size: 1.8em !important;
        padding: 20px !important;
    }
    .stButton button {
        padding: 10px 20px !important;
        font-size: 14px !important;
    }
    .faq-card {
        padding: 10px !important;
        margin-bottom: 10px !important;
    }
    .faq-card h4 {
        font-size: 15px !important;
    }
    .faq-card p {
        font-size: 12px !important;
    }
    .faq-card .signature {
        font-size: 11px !important;
    }
}
</style>
""", unsafe_allow_html=True)

with st.spinner("Initializing Talbot Announcements..."):
    time.sleep(0.5)  # Brief initialization delay

st.markdown("<h1 style='text-align: center; color: #0A0A0A;'>🤖 Talbot Announcements</h1>", unsafe_allow_html=True)
# Hero image placeholder - replace with actual image path
st.image("https://via.placeholder.com/800x300/FFFFFF/F9F6EF?text=Talbot+Assistant", width='stretch')
st.markdown("---")

# Sidebar para re-indexar y info
with st.sidebar:
    st.header("⚙️ Configuración")
    st.info("Usa este panel para actualizar los datos del bot.")
    if st.button("🔄 Re-indexar datos"):
        with st.spinner("Re-indexando datos..."):
            try:
                subprocess.run(["python", "ingest.py"], check=True)
                subprocess.run(["python", "index.py"], check=True)
                st.success("✅ Re-indexación completada!")
                st.balloons()
                st.rerun()
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error durante re-indexación: {e}")
    st.markdown("---")
    st.subheader("📊 Estadísticas")
    if os.path.exists('corpus.jsonl'):
        with open('corpus.jsonl', 'r', encoding='utf-8') as f:
            num_entries = sum(1 for _ in f)
        st.write(f"📄 Chunks procesados: {num_entries}")
    else:
        st.write("📄 No hay datos indexados.")

    st.markdown("---")
    with st.expander("🔧 Agregar Anuncio"):
        admin_password = st.text_input("Contraseña", type="password", key="admin_pass")
        if admin_password == "admin123":
            new_date = st.date_input("Fecha del anuncio", key="admin_date")
            new_author = st.text_input("Autor (ej: Management)", key="admin_author")
            new_text = st.text_area("Texto del anuncio", key="admin_text")
            faq_question = st.text_input("Pregunta para FAQ (opcional)", key="admin_faq")
            if st.button("Agregar y re-indexar", key="admin_button"):
                if new_text.strip():
                    with open('data/anuncios.txt', 'a', encoding='utf-8') as f:
                        f.write(f"\n{new_date.strftime('%Y-%m-%d')}\n[12:00 PM] {new_author}: {new_text}\n")
                    # Agregar a FAQ si hay pregunta
                    if faq_question.strip():
                        with open('anuncios_faq.json', 'r+', encoding='utf-8') as f:
                            data = json.load(f)
                            data['faqs'].append({
                                "question": faq_question,
                                "answer": f"{new_text} **Management, {new_date.strftime('%Y-%m-%d')}**"
                            })
                            f.seek(0)
                            json.dump(data, f, ensure_ascii=False, indent=2)
                            f.truncate()
                    with st.spinner("Re-indexando..."):
                        subprocess.run(["python", "ingest.py"], check=True)
                        subprocess.run(["python", "index.py"], check=True)
                    st.success("¡Anuncio agregado!")
                    st.balloons()
                else:
                    st.error("Ingresa el texto.")
        elif admin_password:
            st.error("Contraseña incorrecta.")

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Cargar FAQ
    with open('anuncios_faq.json', 'r', encoding='utf-8') as f:
        faq_data = json.load(f)
    faqs = faq_data['faqs']

    st.info("¡Hola! Soy tu asistente para anuncios de Talbot. Selecciona una opción abajo.")

    option = st.selectbox(
        "Opciones:",
        [
            "Preguntar sobre compañía específica",
            "Pregunta libre",
            "Buscar anuncios por fecha",
            "Ver FAQs comunes"
        ],
        index=3
    )

    if option == "Preguntar sobre compañía específica":
        company = st.text_input("Ingresa el nombre de la compañía (ej: Molina, Oscar):")
        if st.button("Buscar") and company:
            if not os.path.exists('index.faiss'):
                st.error("No hay índice. Re-indexa primero.")
            else:
                question = f"¿Podemos procesar en {company}?"
                progress_bar = st.progress(0)
                with st.spinner("Buscando información..."):
                    result = answer_query(question, top_k=10)
                    progress_bar.progress(100)
                st.success("¡Respuesta encontrada!")
                st.balloons()
                st.write(f"**Pregunta:** {question}")
                st.write(f"**Respuesta:** {result['answer']}")
                progress_bar.empty()

    elif option == "Pregunta libre":
        question = st.text_input("Escribe tu pregunta:")
        if st.button("Preguntar") and question:
            if not os.path.exists('index.faiss'):
                st.error("No hay índice. Re-indexa primero.")
            else:
                progress_bar = st.progress(0)
                with st.spinner("Buscando información..."):
                    result = answer_query(question, top_k=10)
                    progress_bar.progress(100)
                st.success("¡Respuesta encontrada!")
                st.balloons()
                st.write(f"**Respuesta:** {result['answer']}")
                progress_bar.empty()

    elif option == "Buscar anuncios por fecha":
        selected_date = st.date_input("Selecciona la fecha:")
        if st.button("Mostrar anuncios"):
            progress_bar = st.progress(0)
            with st.spinner("Cargando anuncios..."):
                if os.path.exists('corpus.jsonl'):
                    with open('corpus.jsonl', 'r', encoding='utf-8') as f:
                        entries = [json.loads(line) for line in f]
                    date_str = selected_date.strftime('%Y-%m-%d')
                    filtered_entries = [e for e in entries if e.get('fecha') == date_str]
                    progress_bar.progress(100)
                    if filtered_entries:
                        st.success(f"Encontrados {len(filtered_entries)} anuncios!")
                        st.balloons()
                        st.subheader(f"Anuncios del {date_str}:")
                        for entry in filtered_entries:
                            st.write(f"**Management:** {entry['texto_raw']}")
                    else:
                        st.info("No hay anuncios para esa fecha.")
                else:
                    st.error("No hay datos procesados. Re-indexa primero.")
            progress_bar.empty()

    elif option == "Agregar anuncio":
        st.subheader("Agregar nuevo anuncio")
        new_date = st.date_input("Fecha del anuncio")
        new_author = st.text_input("Autor (ej: Management)")
        new_text = st.text_area("Texto del anuncio")
        if st.button("Agregar y re-indexar"):
            if new_text.strip():
                # Append to anuncios.txt
                with open('data/anuncios.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\n{new_date.strftime('%Y-%m-%d')}\n[12:00 PM] {new_author}: {new_text}\n")
                # Re-index
                with st.spinner("Re-indexando con el nuevo anuncio..."):
                    subprocess.run(["python", "ingest.py"], check=True)
                    subprocess.run(["python", "index.py"], check=True)
                st.success("¡Anuncio agregado y base de datos actualizada!")
                st.balloons()
            else:
                st.error("Por favor ingresa el texto del anuncio.")

    elif option == "Ver FAQs comunes":
        st.subheader("Preguntas frecuentes:")
        cols = st.columns(2)
        for i, faq in enumerate(faqs):
            with cols[i % 2]:
                # Split answer at ** to separate text and signature
                if '**' in faq["answer"]:
                    parts = faq["answer"].split('**', 1)
                    text = parts[0].strip()
                    signature = parts[1].rstrip('*').strip()
                else:
                    text = faq["answer"]
                    signature = "Management"
                st.markdown(f'<div class="faq-card"><h4>{faq["question"]}</h4><p>{text}</p><p class="signature">{signature}</p></div>', unsafe_allow_html=True)