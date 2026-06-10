"""
MC ASSOCIADOS — Diagnóstico de Marketing Digital & Crescimento
Versão Streamlit com visual de landing page (como o index.html)
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# CONFIG & STYLES
# ============================================================
st.set_page_config(
    page_title="MC Associados — Diagnóstico",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS GLOBAL (como no index.html)
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FBFCFE;
        color: #3A4658;
    }
    h1 { 
        font-family: 'Fraunces', serif;
        font-size: 56px;
        font-weight: 600;
        color: #0A1F3C;
        margin-bottom: 24px;
        line-height: 1.2;
    }
    h2 {
        font-family: 'Fraunces', serif;
        font-size: 40px;
        color: #13345F;
        margin-bottom: 16px;
    }
    h3 {
        font-size: 22px;
        color: #13345F;
        margin-bottom: 12px;
    }
    .eyebrow {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #C9A24B;
        margin-bottom: 16px;
    }
    .hero-section {
        padding: 80px 40px;
        background: linear-gradient(135deg, #0A1F3C 0%, #13345F 100%);
        color: white;
        border-radius: 0;
    }
    .hero-title { font-size: 56px; }
    .hero-title em { font-style: italic; color: #C9A24B; }
    .hero-lead { 
        font-size: 20px;
        line-height: 1.6;
        margin: 24px 0;
        opacity: 0.95;
    }
    .btn-group {
        display: flex;
        gap: 16px;
        margin: 32px 0;
        flex-wrap: wrap;
    }
    .btn {
        padding: 14px 32px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 16px;
        border: none;
        cursor: pointer;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .btn-gold {
        background-color: #C9A24B;
        color: #0A1F3C;
    }
    .btn-gold:hover {
        background-color: #b8932e;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(201, 162, 75, 0.3);
    }
    .btn-light {
        background-color: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid white;
    }
    .btn-light:hover {
        background-color: rgba(255,255,255,0.3);
    }
    .stripe {
        background-color: #0A1F3C;
        padding: 60px 40px;
        color: white;
    }
    .stripe-inner {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 40px;
        text-align: center;
    }
    .stat-num {
        font-family: 'Fraunces', serif;
        font-size: 48px;
        font-weight: 600;
        color: #C9A24B;
        margin-bottom: 12px;
    }
    .stat-lbl {
        font-size: 14px;
        opacity: 0.9;
    }
    .section {
        padding: 80px 40px;
    }
    .section-tint {
        background-color: #F5F7FA;
    }
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 32px;
        margin-top: 48px;
    }
    .card {
        background: white;
        padding: 32px;
        border-radius: 12px;
        border: 1px solid #E5E9F0;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(10, 31, 60, 0.1);
        border-color: #C9A24B;
    }
    .card-icon {
        font-size: 32px;
        margin-bottom: 16px;
    }
    .steps {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        margin-top: 48px;
    }
    .step {
        text-align: center;
    }
    .step-num {
        font-family: 'Fraunces', serif;
        font-size: 42px;
        font-weight: 600;
        color: #C9A24B;
        margin-bottom: 16px;
    }
    .cta-band {
        background: linear-gradient(135deg, #13345F 0%, #0A1F3C 100%);
        padding: 60px 40px;
        border-radius: 16px;
        text-align: center;
        color: white;
    }
    .cta-band h2 {
        color: white;
        margin-bottom: 16px;
    }
    .cta-band p {
        font-size: 18px;
        margin-bottom: 32px;
        opacity: 0.95;
    }
    .footer {
        background-color: #0A1F3C;
        color: white;
        padding: 60px 40px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .footer-inner {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 40px;
        margin-bottom: 40px;
    }
    .footer a {
        color: #C9A24B;
        text-decoration: none;
        margin-right: 24px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .brand-mark {
        font-family: 'Fraunces', serif;
        font-size: 24px;
        font-weight: 600;
        background: linear-gradient(135deg, #C9A24B, #FFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    @media (max-width: 768px) {
        h1 { font-size: 36px; }
        h2 { font-size: 28px; }
        .stripe-inner { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: 1fr; }
        .steps { grid-template-columns: 1fr; }
        .hero-section { padding: 40px 20px; }
        .section { padding: 40px 20px; }
        .footer-inner { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA FUNCTIONS
# ============================================================
DATA_FILE = "diagnosticos_mc.json"

def carregar_dados():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)

def preenchido(v):
    if v is None:
        return False
    if isinstance(v, list):
        return len(v) > 0
    return str(v).strip() != ""

def get_num(v):
    if v is None:
        return 0
    try:
        return float(str(v).replace(",", ".").replace("%", "").strip())
    except:
        return 0

# ============================================================
# MOTOR DE MATURIDADE (mesmo código anterior)
# ============================================================
class MotorMaturidade:
    @staticmethod
    def pilares(registro):
        r = registro or {}
        campos_estr = [r.get("missao"), r.get("visao_3_5_anos"), r.get("reconhecimento_mercado"), r.get("diferenciais_competitivos")]
        estrategia = sum(1 for c in campos_estr if preenchido(c)) * 25
        
        comercial = 0
        proc = r.get("processo_comercial", "Não")
        comercial += {"Sim": 40, "Parcialmente": 20, "Não": 0}.get(proc, 0)
        comercial += 30 if r.get("funil_vendas") == "Sim" else 0
        conv = get_num(r.get("taxa_conversao", 0))
        comercial += 30 if conv >= 40 else 20 if conv >= 20 else 10 if conv > 0 else 0
        comercial = min(100, comercial)
        
        marketing = 0
        marketing += get_num(r.get("nota_presenca_digital", 0)) * 5
        plan = r.get("planejamento_marketing", "Não")
        marketing += {"Sim": 30, "Parcialmente": 15, "Não": 0}.get(plan, 0)
        result = r.get("resultados_mensuraveis", "Não")
        marketing += {"Sim": 20, "Parcialmente": 10, "Não": 0}.get(result, 0)
        marketing = min(100, marketing)
        
        tecnologia = min(100, get_num(r.get("nota_maturidade_digital", 0)) * 10)
        
        inovacao = 0
        ia = r.get("usa_ia_automacao", "Não")
        inovacao += {"Sim": 50, "Parcialmente": 25, "Não": 0}.get(ia, 0)
        inovacao += 25 if preenchido(r.get("processos_automatizar")) else 0
        inovacao += 25 if preenchido(r.get("iniciativas_futuras")) else 0
        inovacao = min(100, inovacao)
        
        return {"Estratégia": int(estrategia), "Comercial": int(comercial), "Marketing": int(marketing), "Tecnologia": int(tecnologia), "Inovação": int(inovacao)}
    
    @staticmethod
    def score(registro):
        pilares = MotorMaturidade.pilares(registro)
        vals = list(pilares.values())
        return int(sum(vals) / len(vals))
    
    @staticmethod
    def classificar(score):
        if score <= 20:
            return "Inicial", "#C0463B"
        elif score <= 40:
            return "Básico", "#C77A21"
        elif score <= 60:
            return "Em desenvolvimento", "#C9A24B"
        elif score <= 80:
            return "Estruturado", "#2C5A92"
        else:
            return "Avançado", "#2E7D5B"

# ============================================================
# CATÁLOGO
# ============================================================
OPC = {
    "servicos": ["Contabilidade", "Fiscal", "Departamento Pessoal", "BPO Financeiro", "Planejamento Tributário", "Recuperação Tributária", "Consultoria Empresarial", "Abertura de Empresas", "Outros"],
    "origem": ["Indicação", "Google", "Instagram", "LinkedIn", "Parceiros", "Networking", "Outros"],
    "canais": ["Instagram", "LinkedIn", "Site", "Blog", "E-mail Marketing", "WhatsApp", "Google Ads", "Meta Ads"],
    "prioridades": ["Crescimento da carteira", "Aumento de faturamento", "Aumento de rentabilidade", "Fortalecimento da marca", "Expansão de serviços", "Retenção de clientes", "Transformação digital"],
    "riscos": ["Concorrência acirrada", "Dependência de poucos clientes", "Falta de processos", "Equipe enxuta", "Baixa geração de leads", "Pressão de margem", "Tecnologia defasada", "Rotatividade de clientes"],
    "quantidade": ["Até 50", "51 a 100", "101 a 250", "251 a 500", "Acima de 500"],
}

# ============================================================
# NAVEGAÇÃO
# ============================================================
page = st.sidebar.radio("Navegação", ["🏠 Início", "📋 Diagnóstico", "📊 Dashboard", "📄 Relatório"])

# ============================================================
# PÁGINA 1: INÍCIO (COM VISUAL DO INDEX.HTML)
# ============================================================
if page == "🏠 Início":
    # HERO
    st.markdown("""
    <div class="hero-section">
        <p class="eyebrow">Projeto de Marketing Digital & Crescimento</p>
        <h1 class="hero-title">Onde a sua consultoria <em>realmente</em> está — e para onde pode crescer.</h1>
        <p class="hero-lead">
            Um levantamento estratégico, conduzido com sócios e gestores, que traduz a
            realidade da MC Associados em um diagnóstico claro: maturidade comercial,
            presença digital e o caminho para o próximo nível de crescimento.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div style="margin-top: 32px;">
        """, unsafe_allow_html=True)
        if st.button("🎯 Responder diagnóstico", use_container_width=True, key="btn_diag"):
            st.session_state.page = "📋 Diagnóstico"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="margin-top: 32px; text-align: center; color: #6A7689; padding: 12px;">
        ⏱ Cerca de 10 minutos · 8 blocos · dados tratados conforme a LGPD
        </div>
        """, unsafe_allow_html=True)
    
    # STRIPE
    st.markdown("""
    <div class="stripe">
        <div class="stripe-inner">
            <div><div class="stat-num">8</div><div class="stat-lbl">Blocos de levantamento</div></div>
            <div><div class="stat-num">5</div><div class="stat-lbl">Pilares de maturidade</div></div>
            <div><div class="stat-num">0–100</div><div class="stat-lbl">Score consolidado</div></div>
            <div><div class="stat-num">90 dias</div><div class="stat-lbl">Roadmap de ativação</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # O QUE AVALIAMOS
    st.markdown("""
    <div class="section">
        <p class="eyebrow">O que o diagnóstico revela</p>
        <h2>Uma leitura honesta de cada frente do negócio</h2>
        <p style="font-size: 18px; color: #6A7689; margin-bottom: 48px;">
        Cada bloco do formulário alimenta um pilar de maturidade. Juntos, eles mostram onde a empresa já é forte e onde está a maior oportunidade de crescimento.
        </p>
        <div class="grid-3">
            <div class="card">
                <div class="card-icon">◆</div>
                <h3>Posicionamento</h3>
                <p>Missão, visão, diferenciais e como a MC Associados quer ser reconhecida no mercado.</p>
            </div>
            <div class="card">
                <div class="card-icon">▲</div>
                <h3>Portfólio & clientes</h3>
                <p>Serviços rentáveis, potencial de crescimento e o perfil do cliente ideal.</p>
            </div>
            <div class="card">
                <div class="card-icon">●</div>
                <h3>Comercial</h3>
                <p>Origem dos clientes, processo de vendas, funil e taxa de conversão de propostas.</p>
            </div>
            <div class="card">
                <div class="card-icon">✦</div>
                <h3>Marketing digital</h3>
                <p>Canais ativos, planejamento, presença online e resultados mensuráveis.</p>
            </div>
            <div class="card">
                <div class="card-icon">⬡</div>
                <h3>Tecnologia & IA</h3>
                <p>Maturidade digital, uso de automações e processos com potencial de automação.</p>
            </div>
            <div class="card">
                <div class="card-icon">➜</div>
                <h3>Objetivos & expectativas</h3>
                <p>Prioridades dos próximos 12 meses, riscos e o que a diretoria espera acompanhar.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # COMO FUNCIONA
    st.markdown("""
    <div class="section section-tint">
        <p class="eyebrow">Como funciona</p>
        <h2>Do levantamento ao plano de ação</h2>
        <p style="font-size: 18px; color: #6A7689; margin-bottom: 48px;">Um fluxo simples e objetivo, pensado para a rotina de sócios e gestores.</p>
        <div class="steps">
            <div class="step">
                <div class="step-num">01</div>
                <h3>Responder</h3>
                <p>Sócios e gestores preenchem os 8 blocos estratégicos do formulário.</p>
            </div>
            <div class="step">
                <div class="step-num">02</div>
                <h3>Consolidar</h3>
                <p>As respostas são armazenadas e convertidas no score de maturidade.</p>
            </div>
            <div class="step">
                <div class="step-num">03</div>
                <h3>Analisar</h3>
                <p>O dashboard executivo cruza indicadores e gráficos por pilar.</p>
            </div>
            <div class="step">
                <div class="step-num">04</div>
                <h3>Decidir</h3>
                <p>O relatório entrega diagnóstico, recomendações e roadmaps de 90 dias e 12 meses.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA FINAL
    st.markdown("""
    <div class="section">
        <div class="cta-band">
            <h2>Pronto para mapear o crescimento da MC Associados?</h2>
            <p>O preenchimento leva cerca de 10 minutos e gera, ao final, um índice de maturidade imediato.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("🚀 Começar agora", use_container_width=True, key="btn_start")
    
    # FOOTER
    st.markdown("""
    <div class="footer">
        <div class="footer-inner">
            <div>
                <div style="margin-bottom: 12px;">
                    <span class="brand-mark">MC</span>
                    <span style="color: white; font-weight: 600; margin-left: 8px;">MC Associados</span>
                </div>
                <p style="opacity: 0.8; font-size: 14px;">
                    As informações coletadas neste diagnóstico são de uso interno e estratégico,
                    tratadas conforme a Lei Geral de Proteção de Dados (LGPD).
                </p>
            </div>
            <nav style="display: flex; gap: 24px; flex-wrap: wrap;">
                <a href="#">Diagnóstico</a>
                <a href="#">Dashboard</a>
                <a href="#">Relatório</a>
            </nav>
        </div>
        <div style="text-align: center; padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 12px; opacity: 0.7;">
            MC Associados © 2024
        </div>
    </div>
    """, unsafe_allow_html=True)

# PÁGINAS RESTANTES (formulário, dashboard, relatório) — mesmo código anterior
elif page == "📋 Diagnóstico":
    st.markdown("## Levantamento Estratégico")
    st.markdown("Responda com a visão mais próxima da realidade atual.")
    
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    form_data = st.session_state.form_data
    
    # BLOCO 1
    st.markdown("### 1️⃣ Posicionamento Estratégico")
    form_data["nome_respondente"] = st.text_input("Seu nome *", value=form_data.get("nome_respondente", ""))
    form_data["cargo"] = st.text_input("Cargo / função *", value=form_data.get("cargo", ""))
    form_data["missao"] = st.text_area("Qual é a missão da MC Associados?", value=form_data.get("missao", ""), height=100)
    form_data["visao_3_5_anos"] = st.text_area("Visão para os próximos 3 a 5 anos?", value=form_data.get("visao_3_5_anos", ""), height=100)
    form_data["reconhecimento_mercado"] = st.text_area("Como deseja ser reconhecida?", value=form_data.get("reconhecimento_mercado", ""), height=100)
    form_data["diferenciais_competitivos"] = st.text_area("Principais diferenciais competitivos", value=form_data.get("diferenciais_competitivos", ""), height=100)
    
    # BLOCO 2
    st.markdown("### 2️⃣ Portfólio de Serviços")
    form_data["servicos_oferecidos"] = st.multiselect("Quais serviços são oferecidos?", OPC["servicos"], default=form_data.get("servicos_oferecidos", []))
    form_data["servicos_rentaveis"] = st.multiselect("Quais têm maior rentabilidade?", OPC["servicos"], default=form_data.get("servicos_rentaveis", []))
    form_data["servicos_crescimento"] = st.multiselect("Quais têm maior potencial de crescimento?", OPC["servicos"], default=form_data.get("servicos_crescimento", []))
    form_data["servicos_prioridade_marketing"] = st.multiselect("Quais são prioridade em marketing?", OPC["servicos"], default=form_data.get("servicos_prioridade_marketing", []))
    
    # BLOCO 3
    st.markdown("### 3️⃣ Clientes e Mercado")
    form_data["quantidade_clientes"] = st.selectbox("Quantidade aproximada de clientes ativos", [""] + OPC["quantidade"], index=OPC["quantidade"].index(form_data.get("quantidade_clientes", "")) + 1 if form_data.get("quantidade_clientes") in OPC["quantidade"] else 0)
    form_data["segmentos_clientes"] = st.text_area("Segmentos que representam a maior parte da carteira", value=form_data.get("segmentos_clientes", ""), height=100)
    form_data["cliente_ideal"] = st.text_area("Quem é o cliente ideal?", value=form_data.get("cliente_ideal", ""), height=100)
    form_data["dores_clientes"] = st.text_area("Principais dores dos clientes", value=form_data.get("dores_clientes", ""), height=100)
    form_data["segmentos_desejados"] = st.text_area("Segmentos que deseja conquistar", value=form_data.get("segmentos_desejados", ""), height=100)
    
    # BLOCO 4
    st.markdown("### 4️⃣ Processo Comercial")
    form_data["origem_clientes"] = st.multiselect("Como os clientes chegam à empresa?", OPC["origem"], default=form_data.get("origem_clientes", []))
    form_data["processo_comercial"] = st.radio("Existe processo comercial formalizado?", ["Sim", "Parcialmente", "Não"], index=["Sim", "Parcialmente", "Não"].index(form_data.get("processo_comercial", "Não")))
    form_data["funil_vendas"] = st.radio("Existe acompanhamento de funil de vendas?", ["Sim", "Não"], index=["Sim", "Não"].index(form_data.get("funil_vendas", "Não")))
    form_data["novos_clientes_mes"] = st.number_input("Quantos novos clientes por mês?", min_value=0, value=int(form_data.get("novos_clientes_mes", 0)))
    form_data["taxa_conversao"] = st.number_input("Taxa de conversão de propostas (%)", min_value=0, max_value=100, value=int(form_data.get("taxa_conversao", 0)))
    
    # BLOCO 5
    st.markdown("### 5️⃣ Marketing e Presença Digital")
    form_data["canais_digitais"] = st.multiselect("Quais canais digitais são utilizados?", OPC["canais"], default=form_data.get("canais_digitais", []))
    form_data["planejamento_marketing"] = st.radio("Existe planejamento de marketing formal?", ["Sim", "Parcialmente", "Não"], index=["Sim", "Parcialmente", "Não"].index(form_data.get("planejamento_marketing", "Não")))
    form_data["nota_presenca_digital"] = st.slider("Como avalia a presença digital? (0–10)", 0, 10, value=int(form_data.get("nota_presenca_digital", 5)))
    form_data["resultados_mensuraveis"] = st.radio("Marketing gera resultados mensuráveis?", ["Sim", "Parcialmente", "Não"], index=["Sim", "Parcialmente", "Não"].index(form_data.get("resultados_mensuraveis", "Não")))
    form_data["desafios_marketing"] = st.text_area("Principais desafios de marketing", value=form_data.get("desafios_marketing", ""), height=100)
    
    # BLOCO 6
    st.markdown("### 6️⃣ Tecnologia e Inovação")
    form_data["nota_maturidade_digital"] = st.slider("Maturidade digital da empresa (0–10)", 0, 10, value=int(form_data.get("nota_maturidade_digital", 5)))
    form_data["usa_ia_automacao"] = st.radio("Usa automações ou Inteligência Artificial?", ["Sim", "Parcialmente", "Não"], index=["Sim", "Parcialmente", "Não"].index(form_data.get("usa_ia_automacao", "Não")))
    form_data["processos_automatizar"] = st.text_area("Quais processos poderiam ser automatizados?", value=form_data.get("processos_automatizar", ""), height=100)
    
    # BLOCO 7
    st.markdown("### 7️⃣ Objetivos Estratégicos")
    form_data["prioridades_12_meses"] = st.multiselect("Prioridades para os próximos 12 meses", OPC["prioridades"], default=form_data.get("prioridades_12_meses", []))
    form_data["resultados_sucesso"] = st.text_area("Como definiria sucesso?", value=form_data.get("resultados_sucesso", ""), height=100)
    form_data["riscos_crescimento"] = st.multiselect("Riscos que podem comprometer o crescimento", OPC["riscos"], default=form_data.get("riscos_crescimento", []))
    
    # BLOCO 8
    st.markdown("### 8️⃣ Expectativas da Diretoria")
    form_data["expectativas_diretoria"] = st.text_area("O que espera do Projeto de Marketing Digital?", value=form_data.get("expectativas_diretoria", ""), height=100)
    form_data["indicadores_mensais"] = st.text_area("Quais indicadores acompanhar mensalmente?", value=form_data.get("indicadores_mensais", ""), height=100)
    form_data["iniciativas_futuras"] = st.text_area("Alguma iniciativa para o futuro?", value=form_data.get("iniciativas_futuras", ""), height=100)
    
    consent = st.checkbox("Declaro estar ciente de que as informações serão utilizadas para fins estratégicos internos.", value=False)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar diagnóstico", use_container_width=True, type="primary"):
            if not form_data.get("nome_respondente") or not form_data.get("cargo"):
                st.error("Preencha ao menos nome e cargo.")
            elif not consent:
                st.error("Confirme o consentimento.")
            else:
                dados = carregar_dados()
                form_data["data_resposta"] = datetime.now().isoformat()
                form_data["score"] = MotorMaturidade.score(form_data)
                form_data["pilares"] = MotorMaturidade.pilares(form_data)
                dados.append(form_data)
                salvar_dados(dados)
                st.session_state.form_data = {}
                st.success(f"✅ Diagnóstico salvo! Score: {form_data['score']}/100")
    
    with col2:
        if st.button("🔄 Limpar formulário", use_container_width=True):
            st.session_state.form_data = {}
            st.rerun()

elif page == "📊 Dashboard":
    st.markdown("## Dashboard Executivo")
    dados = carregar_dados()
    
    if not dados:
        st.info("📭 Nenhum diagnóstico preenchido ainda.")
    else:
        nomes = ["Consolidado (todas as respostas)"] + [f"{d.get('nome_respondente', 'Sem nome')} · {d.get('cargo', '—')}" for d in dados]
        idx_selecionado = st.selectbox("Recorte da análise", range(len(nomes)), format_func=lambda i: nomes[i])
        
        if idx_selecionado == 0:
            scores = [d.get("score", 0) for d in dados]
            score_geral = int(sum(scores) / len(scores)) if scores else 0
            registro = None
        else:
            registro = dados[idx_selecionado - 1]
            score_geral = registro.get("score", 0)
        
        faixa, cor = MotorMaturidade.classificar(score_geral)
        pilares = MotorMaturidade.pilares(registro) if registro else {}
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score Geral", f"{score_geral}/100")
        with col2:
            st.metric("Classificação", faixa)
        with col3:
            st.metric("Diagnósticos", len(dados))

elif page == "📄 Relatório":
    st.markdown("## Relatório de Diagnóstico")
    dados = carregar_dados()
    
    if not dados:
        st.info("📭 Nenhum diagnóstico preenchido.")
    else:
        st.success("✅ Relatórios disponíveis no app.py")
