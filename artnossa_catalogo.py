import json
import os
import uuid
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# ============================================================
# ARTNOSSA ESTOFADOS - CATÁLOGO DIGITAL
# Execute com: streamlit run artnossa_catalogo.py
# ============================================================

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "artnossa_dados.json"
UPLOAD_DIR = APP_DIR / "imagens"
UPLOAD_DIR.mkdir(exist_ok=True)

# IMPORTANTE: troque esta senha antes de publicar o catálogo.
ADMIN_PASSWORD = os.getenv("ARTNOSSA_ADMIN_PASSWORD", "troque123")

DEFAULT_DATA = {
    "company": "ArtNossa Estofados",
    "subtitle": "Conforto e elegância em cada detalhe",
    "whatsapp": "",  # Ex.: 5517999999999 (país + DDD + número, só números)
    "instagram": "",
    "products": []
}


def load_data():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in DEFAULT_DATA.items():
                data.setdefault(key, value)
            return data
        except (json.JSONDecodeError, OSError):
            st.error("Não foi possível ler o arquivo de dados. Verifique artnossa_dados.json.")
    return DEFAULT_DATA.copy()


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()

st.set_page_config(
    page_title="ArtNossa Estofados | Catálogo",
    page_icon="🛏️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --ink:#24211f; --muted:#77716b; --cream:#f7f4ef; --gold:#ad895d; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#fbfaf8; color:var(--ink); }
.block-container { padding-top:1.5rem; max-width:1200px; }
.hero {
  background:linear-gradient(115deg,rgba(28,25,23,.92),rgba(60,49,40,.82)),
             radial-gradient(circle at 80% 20%,#ad895d,transparent 45%);
  color:#fff; padding:3.2rem 2.4rem; border-radius:18px; margin:1rem 0 2rem;
}
.hero h1 { font-family:'Playfair Display',serif; font-size:clamp(2.3rem,5vw,4rem); margin:0; color:#fff; }
.hero p { color:#eee6dc; font-size:1.05rem; margin:.6rem 0 0; }
.eyebrow { color:#d7b88f; text-transform:uppercase; letter-spacing:.22em; font-size:.72rem; font-weight:700; }
.section-title { font-family:'Playfair Display',serif; font-size:2rem; margin:1.2rem 0 .2rem; }
.section-sub { color:#77716b; margin-bottom:1.2rem; }
.product-card {
  background:white; border:1px solid #eee9e2; border-radius:14px;
  padding:12px; height:100%; box-shadow:0 5px 18px rgba(35,28,20,.045);
}
.product-name { font-family:'Playfair Display',serif; font-size:1.22rem; font-weight:600; margin:.65rem 0 .2rem; }
.product-desc { color:#77716b; font-size:.9rem; min-height:2.6rem; }
.product-price { font-size:1.1rem; font-weight:700; color:#8c6945; margin:.7rem 0; }
.pill { display:inline-block; padding:4px 10px; background:#f3eee7; color:#806344;
        border-radius:99px; font-size:.72rem; font-weight:700; }
.footer { margin-top:3rem; padding:1.5rem; text-align:center; color:#817a72;
          border-top:1px solid #eee9e2; font-size:.85rem; }
div.stButton > button, div.stDownloadButton > button {
  border-radius:9px; border:1px solid #ad895d; min-height:2.6rem;
}
a { color:#8c6945 !important; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">Móveis estofados • Design • Conforto</div>
  <h1>{data['company']}</h1>
  <p>{data['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Navegação e filtros
products = data.get("products", [])
categories = ["Todos", "Cabeceiras", "Recamiers"]
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<div class="section-title">Nosso catálogo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Encontre o modelo ideal para transformar seu ambiente.</div>', unsafe_allow_html=True)
with c2:
    selected_category = st.selectbox("Categoria", categories, label_visibility="collapsed")

search = st.text_input("⌕  Buscar produto", placeholder="Digite o nome de uma cabeceira ou recamier...")
visible = [
    p for p in products
    if (selected_category == "Todos" or p.get("category") == selected_category)
    and search.lower() in (p.get("name", "") + " " + p.get("description", "")).lower()
]

if not visible:
    st.info("Ainda não há produtos nesta seleção. Volte em breve ou fale com a ArtNossa pelo WhatsApp.")
else:
    cols_per_row = 3
    for start in range(0, len(visible), cols_per_row):
        cols = st.columns(cols_per_row, gap="large")
        for col, product in zip(cols, visible[start:start + cols_per_row]):
            with col:
                with st.container(border=False):
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    image_path = product.get("image", "")
                    if image_path and Path(image_path).exists():
                        st.image(image_path, use_container_width=True)
                    else:
                        st.markdown(
                            '<div style="height:210px;background:#f1ede7;border-radius:9px;'
                            'display:flex;align-items:center;justify-content:center;color:#9a8b7a;'
                            'font-size:3rem;">✧</div>', unsafe_allow_html=True
                        )
                    st.markdown(f'<span class="pill">{product.get("category", "")}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-name">{product.get("name", "Produto")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-desc">{product.get("description", "")}</div>', unsafe_allow_html=True)
                    price = product.get("price", "").strip()
                    if price:
                        st.markdown(f'<div class="product-price">{price}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="product-price">Consulte o preço</div>', unsafe_allow_html=True)

                    whatsapp = data.get("whatsapp", "").strip()
                    if whatsapp:
                        msg = quote(f"Olá! Tenho interesse no produto {product.get('name', '')}. Poderia me passar mais informações?")
                        st.markdown(
                            f'<a href="https://wa.me/{whatsapp}?text={msg}" target="_blank">'
                            '<button style="width:100%;background:#8c6945;color:white;padding:10px;'
                            'border:0;border-radius:8px;font-weight:700;cursor:pointer;">'
                            'Consultar pelo WhatsApp</button></a>', unsafe_allow_html=True
                        )
                    else:
                        st.caption("WhatsApp ainda não configurado.")
                    st.markdown('</div>', unsafe_allow_html=True)

# Contato
st.markdown("---")
contact_col1, contact_col2 = st.columns(2)
with contact_col1:
    st.subheader("Fale com a ArtNossa")
    if data.get("whatsapp"):
        st.link_button("Conversar pelo WhatsApp", f"https://wa.me/{data['whatsapp']}", use_container_width=True)
    else:
        st.caption("Configure seu WhatsApp na área administrativa.")
with contact_col2:
    if data.get("instagram"):
        st.link_button("Acompanhar no Instagram", data["instagram"], use_container_width=True)

st.markdown('<div class="footer">ArtNossa Estofados · Cabeceiras e Recamiers</div>', unsafe_allow_html=True)

# Administração
st.markdown("---")
with st.expander("🔐 Área administrativa | Gerenciar catálogo"):
    if "admin_ok" not in st.session_state:
        st.session_state.admin_ok = False

    if not st.session_state.admin_ok:
        password = st.text_input("Senha de administrador", type="password")
        if st.button("Entrar na administração"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    else:
        st.success("Acesso administrativo liberado.")
        if st.button("Sair da administração"):
            st.session_state.admin_ok = False
            st.rerun()

        st.subheader("Dados da empresa")
        with st.form("company_form"):
            company_name = st.text_input("Nome da empresa", value=data["company"])
            subtitle = st.text_input("Frase de apresentação", value=data["subtitle"])
            whatsapp = st.text_input("WhatsApp (com código do país e DDD, só números)", value=data["whatsapp"])
            instagram = st.text_input("Link do Instagram (opcional)", value=data["instagram"])
            save_company = st.form_submit_button("Salvar dados da empresa")
        if save_company:
            data.update(company=company_name, subtitle=subtitle, whatsapp=whatsapp, instagram=instagram)
            save_data(data)
            st.success("Dados da empresa salvos!")
            st.rerun()

        st.subheader("Adicionar produto")
        with st.form("product_form", clear_on_submit=True):
            product_name = st.text_input("Nome do produto")
            category = st.selectbox("Categoria do produto", ["Cabeceiras", "Recamiers"])
            description = st.text_area("Descrição", placeholder="Descreva o modelo, tecido, medidas ou opções de cores.")
            price = st.text_input("Preço (opcional)", placeholder="Ex.: R$ 899,00 ou Sob consulta")
            uploaded_image = st.file_uploader("Foto do produto", type=["png", "jpg", "jpeg", "webp"])
            add_product = st.form_submit_button("Adicionar ao catálogo")
        if add_product:
            if not product_name.strip():
                st.error("Digite o nome do produto.")
            else:
                image_name = ""
                if uploaded_image:
                    suffix = Path(uploaded_image.name).suffix.lower() or ".jpg"
                    image_name = str(UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}")
                    with open(image_name, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                data["products"].append({
                    "id": uuid.uuid4().hex,
                    "name": product_name.strip(),
                    "category": category,
                    "description": description.strip(),
                    "price": price.strip(),
                    "image": image_name,
                })
                save_data(data)
                st.success("Produto adicionado ao catálogo!")
                st.rerun()

        st.subheader("Produtos cadastrados")
        if not data["products"]:
            st.caption("Nenhum produto cadastrado ainda.")
        for product in list(data["products"]):
            left, right = st.columns([4, 1])
            with left:
                st.write(f"**{product['name']}** · {product['category']} · {product.get('price') or 'Sem preço'}")
            with right:
                if st.button("Excluir", key=f"delete_{product['id']}"):
                    data["products"] = [p for p in data["products"] if p["id"] != product["id"]]
                    save_data(data)
                    st.rerun()

        st.caption("Os produtos e configurações ficam salvos nos arquivos artnossa_dados.json e na pasta imagens, ao lado deste programa.")
