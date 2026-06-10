"""
MC ASSOCIADOS — Diagnóstico de Marketing Digital & Crescimento
Aplicação Streamlit com formulário, dashboard e relatório
Salva dados em JSON (ou Supabase opcionalmente)
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
# Nota: Removemos pandas para evitar erro de compilacao no Windows
# Usamos estruturas nativas do Python em vez disso

# ============================================================
# CONFIGURAÇÃO STREAMLIT
# ============================================================
st.set_page_config(
    page_title="MC Associados — Diagnóstico",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado (azul-marinho, branco, cinza)
st.markdown("""
<style>
    :root {
        --navy-900: #0A1F3C;
        --navy-700: #13345F;
        --gold-500: #C9A24B;
        --gray-700: #3A4658;
        --gray-500: #6A7689;
    }
    
    .main { background-color: #FBFCFE; }
    h1 { color: #0A1F3C; }
    h2 { color: #13345F; }
    .css-1d391kg { background: linear-gradient(150deg, #0A1F3C, #13345F); color: white; padding: 20px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# UTILITÁRIOS
# ============================================================
DATA_FILE = "diagnosticos_mc.json"

def carregar_dados():
    """Carrega diagnósticos salvos em JSON."""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    """Salva diagnósticos em JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)

def preenchido(v):
    """Verifica se um campo está preenchido."""
    if v is None:
        return False
    if isinstance(v, list):
        return len(v) > 0
    return str(v).strip() != ""

def get_num(v):
    """Converte valor em número seguro."""
    if v is None:
        return 0
    try:
        return float(str(v).replace(",", ".").replace("%", "").strip())
    except:
        return 0

# ============================================================
# MOTOR DE MATURIDADE
# ============================================================
class MotorMaturidade:
    """Calcula score de maturidade e pilares."""
    
    @staticmethod
    def pilares(registro):
        """Calcula os 5 pilares (0–100)."""
        r = registro or {}
        
        # Estratégia: completude do posicionamento
        campos_estr = [
            r.get("missao"),
            r.get("visao_3_5_anos"),
            r.get("reconhecimento_mercado"),
            r.get("diferenciais_competitivos"),
        ]
        estrategia = sum(1 for c in campos_estr if preenchido(c)) * 25
        
        # Comercial: processo + funil + conversão
        comercial = 0
        proc = r.get("processo_comercial", "Não")
        comercial += {"Sim": 40, "Parcialmente": 20, "Não": 0}.get(proc, 0)
        comercial += 30 if r.get("funil_vendas") == "Sim" else 0
        conv = get_num(r.get("taxa_conversao", 0))
        comercial += 30 if conv >= 40 else 20 if conv >= 20 else 10 if conv > 0 else 0
        comercial = min(100, comercial)
        
        # Marketing: presença + planejamento + resultados
        marketing = 0
        marketing += get_num(r.get("nota_presenca_digital", 0)) * 5  # 0–50
        plan = r.get("planejamento_marketing", "Não")
        marketing += {"Sim": 30, "Parcialmente": 15, "Não": 0}.get(plan, 0)
        result = r.get("resultados_mensuraveis", "Não")
        marketing += {"Sim": 20, "Parcialmente": 10, "Não": 0}.get(result, 0)
        marketing = min(100, marketing)
        
        # Tecnologia: maturidade digital
        tecnologia = min(100, get_num(r.get("nota_maturidade_digital", 0)) * 10)
        
        # Inovação: IA + automação + futuro
        inovacao = 0
        ia = r.get("usa_ia_automacao", "Não")
        inovacao += {"Sim": 50, "Parcialmente": 25, "Não": 0}.get(ia, 0)
        inovacao += 25 if preenchido(r.get("processos_automatizar")) else 0
        inovacao += 25 if preenchido(r.get("iniciativas_futuras")) else 0
        inovacao = min(100, inovacao)
        
        return {
            "Estratégia": int(estrategia),
            "Comercial": int(comercial),
            "Marketing": int(marketing),
            "Tecnologia": int(tecnologia),
            "Inovação": int(inovacao),
        }
    
    @staticmethod
    def score(registro):
        """Score geral (média dos pilares)."""
        pilares = MotorMaturidade.pilares(registro)
        vals = list(pilares.values())
        return int(sum(vals) / len(vals))
    
    @staticmethod
    def classificar(score):
        """Classifica o score em faixa."""
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
# CATÁLOGO DE OPÇÕES
# ============================================================
OPC = {
    "servicos": ["Contabilidade", "Fiscal", "Departamento Pessoal", "BPO Financeiro",
                 "Planejamento Tributário", "Recuperação Tributária", "Consultoria Empresarial",
                 "Abertura de Empresas", "Outros"],
    "origem": ["Indicação", "Google", "Instagram", "LinkedIn", "Parceiros", "Networking", "Outros"],
    "canais": ["Instagram", "LinkedIn", "Site", "Blog", "E-mail Marketing", "WhatsApp", "Google Ads", "Meta Ads"],
    "prioridades": ["Crescimento da carteira", "Aumento de faturamento", "Aumento de rentabilidade",
                    "Fortalecimento da marca", "Expansão de serviços", "Retenção de clientes", "Transformação digital"],
    "riscos": ["Concorrência acirrada", "Dependência de poucos clientes", "Falta de processos",
               "Equipe enxuta", "Baixa geração de leads", "Pressão de margem", "Tecnologia defasada", "Rotatividade de clientes"],
    "quantidade": ["Até 50", "51 a 100", "101 a 250", "251 a 500", "Acima de 500"],
}

# ============================================================
# NAVEGAÇÃO (Sidebar)
# ============================================================
st.sidebar.markdown("### 🏢 MC Associados")
st.sidebar.markdown("Consultoria Contábil e Tributária")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegação",
    ["🏠 Início", "📋 Diagnóstico", "📊 Dashboard", "📄 Relatório"],
)

# ============================================================
# PÁGINA 1: INÍCIO
# ============================================================
if page == "🏠 Início":
    st.markdown("## 💼 Diagnóstico de Marketing Digital & Crescimento")
    st.markdown(
        """
        Bem-vindo à plataforma de diagnóstico estratégico da **MC Associados**.
        
        Esta ferramenta coleta informações de sócios e gestores para estruturar um 
        **plano de marketing digital e crescimento comercial** baseado em dados reais.
        
        ### Como funciona
        
        1. **Preencha o diagnóstico** (8 blocos, ~10 minutos)
        2. **Veja o score de maturidade** (0–100) gerado automaticamente
        3. **Analise os dados** no dashboard executivo
        4. **Leia as recomendações** no relatório final
        
        ### Os 5 pilares de maturidade
        
        - **Estratégia**: posicionamento, visão e diferenciais
        - **Comercial**: processo de vendas, funil e conversão
        - **Marketing**: presença digital, planejamento e resultados
        - **Tecnologia**: grau de digitalização
        - **Inovação**: automação e visão de futuro
        
        ---
        """
    )
    
    # Estatísticas
    dados = carregar_dados()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Diagnósticos", len(dados))
    with col2:
        if dados:
            scores = [MotorMaturidade.score(d) for d in dados]
            st.metric("Score médio", f"{int(sum(scores)/len(scores))}/100")
        else:
            st.metric("Score médio", "—")
    with col3:
        st.metric("Modo de dados", "Local (JSON)")
    with col4:
        st.metric("LGPD", "✅ Conformidade")
    
    st.markdown("---")
    st.markdown("### Comece agora")
    if st.button("▶ Abrir formulário de diagnóstico", use_container_width=True):
        st.session_state.page = "📋 Diagnóstico"
        st.rerun()

# ============================================================
# PÁGINA 2: FORMULÁRIO
# ============================================================
elif page == "📋 Diagnóstico":
    st.markdown("## Levantamento Estratégico")
    st.markdown("Responda com a visão mais próxima da realidade atual.")
    
    # AVISO LGPD
    with st.expander("⚖️ Uso das informações (LGPD)", expanded=False):
        st.warning(
            """
            As informações coletadas serão utilizadas exclusivamente para fins de 
            diagnóstico estratégico, planejamento de marketing digital e desenvolvimento 
            comercial da MC Associados. Os dados não serão utilizados para avaliação 
            individual de desempenho, exposição pública ou qualquer finalidade não 
            autorizada pela diretoria.
            """
        )
    
    # Usar session_state para manter os dados entre reloads
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    form_data = st.session_state.form_data
    
    # ---- BLOCO 1 ----
    st.markdown("### 1️⃣ Posicionamento Estratégico")
    form_data["nome_respondente"] = st.text_input("Seu nome *", value=form_data.get("nome_respondente", ""))
    form_data["cargo"] = st.text_input("Cargo / função *", value=form_data.get("cargo", ""))
    form_data["missao"] = st.text_area("Qual é a missão da MC Associados?", value=form_data.get("missao", ""), height=80)
    form_data["visao_3_5_anos"] = st.text_area("Visão para os próximos 3 a 5 anos?", value=form_data.get("visao_3_5_anos", ""), height=80)
    form_data["reconhecimento_mercado"] = st.text_area("Como deseja ser reconhecida?", value=form_data.get("reconhecimento_mercado", ""), height=80)
    form_data["diferenciais_competitivos"] = st.text_area("Principais diferenciais competitivos", value=form_data.get("diferenciais_competitivos", ""), height=80)
    
    # ---- BLOCO 2 ----
    st.markdown("### 2️⃣ Portfólio de Serviços")
    form_data["servicos_oferecidos"] = st.multiselect(
        "Quais serviços são oferecidos?",
        OPC["servicos"],
        default=form_data.get("servicos_oferecidos", [])
    )
    form_data["servicos_rentaveis"] = st.multiselect(
        "Quais têm maior rentabilidade?",
        OPC["servicos"],
        default=form_data.get("servicos_rentaveis", [])
    )
    form_data["servicos_crescimento"] = st.multiselect(
        "Quais têm maior potencial de crescimento?",
        OPC["servicos"],
        default=form_data.get("servicos_crescimento", [])
    )
    form_data["servicos_prioridade_marketing"] = st.multiselect(
        "Quais são prioridade em marketing?",
        OPC["servicos"],
        default=form_data.get("servicos_prioridade_marketing", [])
    )
    
    # ---- BLOCO 3 ----
    st.markdown("### 3️⃣ Clientes e Mercado")
    form_data["quantidade_clientes"] = st.selectbox(
        "Quantidade aproximada de clientes ativos",
        [""] + OPC["quantidade"],
        index=OPC["quantidade"].index(form_data.get("quantidade_clientes", "")) + 1 if form_data.get("quantidade_clientes") in OPC["quantidade"] else 0
    )
    form_data["segmentos_clientes"] = st.text_area("Segmentos que representam a maior parte da carteira", value=form_data.get("segmentos_clientes", ""), height=100)
    form_data["cliente_ideal"] = st.text_area("Quem é o cliente ideal?", value=form_data.get("cliente_ideal", ""), height=100)
    form_data["dores_clientes"] = st.text_area("Principais dores dos clientes", value=form_data.get("dores_clientes", ""), height=100)
    form_data["segmentos_desejados"] = st.text_area("Segmentos que deseja conquistar", value=form_data.get("segmentos_desejados", ""), height=100)
    
    # ---- BLOCO 4 ----
    st.markdown("### 4️⃣ Processo Comercial")
    form_data["origem_clientes"] = st.multiselect(
        "Como os clientes chegam à empresa?",
        OPC["origem"],
        default=form_data.get("origem_clientes", [])
    )
    form_data["processo_comercial"] = st.radio(
        "Existe processo comercial formalizado?",
        ["Sim", "Parcialmente", "Não"],
        index=["Sim", "Parcialmente", "Não"].index(form_data.get("processo_comercial", "Não"))
    )
    form_data["funil_vendas"] = st.radio(
        "Existe acompanhamento de funil de vendas?",
        ["Sim", "Não"],
        index=["Sim", "Não"].index(form_data.get("funil_vendas", "Não"))
    )
    form_data["novos_clientes_mes"] = st.number_input("Quantos novos clientes por mês?", min_value=0, value=int(form_data.get("novos_clientes_mes", 0)))
    form_data["taxa_conversao"] = st.number_input("Taxa de conversão de propostas (%)", min_value=0, max_value=100, value=int(form_data.get("taxa_conversao", 0)))
    
    # ---- BLOCO 5 ----
    st.markdown("### 5️⃣ Marketing e Presença Digital")
    form_data["canais_digitais"] = st.multiselect(
        "Quais canais digitais são utilizados?",
        OPC["canais"],
        default=form_data.get("canais_digitais", [])
    )
    form_data["planejamento_marketing"] = st.radio(
        "Existe planejamento de marketing formal?",
        ["Sim", "Parcialmente", "Não"],
        index=["Sim", "Parcialmente", "Não"].index(form_data.get("planejamento_marketing", "Não"))
    )
    form_data["nota_presenca_digital"] = st.slider(
        "Como avalia a presença digital? (0–10)",
        0, 10,
        value=int(form_data.get("nota_presenca_digital", 5))
    )
    form_data["resultados_mensuraveis"] = st.radio(
        "Marketing gera resultados mensuráveis?",
        ["Sim", "Parcialmente", "Não"],
        index=["Sim", "Parcialmente", "Não"].index(form_data.get("resultados_mensuraveis", "Não"))
    )
    form_data["desafios_marketing"] = st.text_area("Principais desafios de marketing", value=form_data.get("desafios_marketing", ""), height=60)
    
    # ---- BLOCO 6 ----
    st.markdown("### 6️⃣ Tecnologia e Inovação")
    form_data["nota_maturidade_digital"] = st.slider(
        "Maturidade digital da empresa (0–10)",
        0, 10,
        value=int(form_data.get("nota_maturidade_digital", 5))
    )
    form_data["usa_ia_automacao"] = st.radio(
        "Usa automações ou Inteligência Artificial?",
        ["Sim", "Parcialmente", "Não"],
        index=["Sim", "Parcialmente", "Não"].index(form_data.get("usa_ia_automacao", "Não"))
    )
    form_data["processos_automatizar"] = st.text_area("Quais processos poderiam ser automatizados?", value=form_data.get("processos_automatizar", ""), height=60)
    
    # ---- BLOCO 7 ----
    st.markdown("### 7️⃣ Objetivos Estratégicos")
    form_data["prioridades_12_meses"] = st.multiselect(
        "Prioridades para os próximos 12 meses",
        OPC["prioridades"],
        default=form_data.get("prioridades_12_meses", [])
    )
    form_data["resultados_sucesso"] = st.text_area("Como definiria sucesso?", value=form_data.get("resultados_sucesso", ""), height=60)
    form_data["riscos_crescimento"] = st.multiselect(
        "Riscos que podem comprometer o crescimento",
        OPC["riscos"],
        default=form_data.get("riscos_crescimento", [])
    )
    
    # ---- BLOCO 8 ----
    st.markdown("### 8️⃣ Expectativas da Diretoria")
    form_data["expectativas_diretoria"] = st.text_area("O que espera do Projeto de Marketing Digital?", value=form_data.get("expectativas_diretoria", ""), height=60)
    form_data["indicadores_mensais"] = st.text_area("Quais indicadores acompanhar mensalmente?", value=form_data.get("indicadores_mensais", ""), height=60)
    form_data["iniciativas_futuras"] = st.text_area("Alguma iniciativa para o futuro?", value=form_data.get("iniciativas_futuras", ""), height=60)
    
    # Consentimento
    consent = st.checkbox("Declaro estar ciente de que as informações serão utilizadas para fins estratégicos internos.", value=False)
    
    # Salvar
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
                st.session_state.show_score = True
    
    with col2:
        if st.button("🔄 Limpar formulário", use_container_width=True):
            st.session_state.form_data = {}
            st.rerun()
    
    # Mostrar score ao salvar
    if st.session_state.get("show_score") and form_data.get("score"):
        st.markdown("---")
        score = form_data.get("score")
        faixa, cor = MotorMaturidade.classificar(score)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### 📊 Índice de Maturidade: **{score}/100**")
            st.markdown(f"**Classificação:** {faixa}")
        with col2:
            pilares = form_data.get("pilares", {})
            for nome, valor in pilares.items():
                st.markdown(f"• **{nome}**: {valor}/100")

# ============================================================
# PÁGINA 3: DASHBOARD
# ============================================================
elif page == "📊 Dashboard":
    st.markdown("## Dashboard Executivo")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("📭 Nenhum diagnóstico preenchido ainda. Acesse a aba **Diagnóstico** para começar.")
    else:
        # Seletor de recorte
        nomes = ["Consolidado (todas as respostas)"] + [
            f"{d.get('nome_respondente', 'Sem nome')} · {d.get('cargo', '—')}"
            for d in dados
        ]
        idx_selecionado = st.selectbox("Recorte da análise", range(len(nomes)), format_func=lambda i: nomes[i])
        
        if idx_selecionado == 0:
            # Consolidado
            scores = [d.get("score", 0) for d in dados]
            score_geral = int(sum(scores) / len(scores)) if scores else 0
            registro = None
        else:
            # Individual
            registro = dados[idx_selecionado - 1]
            score_geral = registro.get("score", 0)
        
        # Score e pilares
        faixa, cor = MotorMaturidade.classificar(score_geral)
        pilares = MotorMaturidade.pilares(registro) if registro else MotorMaturidade.pilares({})
        if not registro and dados:
            # Média dos pilares
            pilares_todos = [d.get("pilares", {}) for d in dados]
            pilares = {
                k: int(sum(p.get(k, 0) for p in pilares_todos) / len(pilares_todos))
                for k in ["Estratégia", "Comercial", "Marketing", "Tecnologia", "Inovação"]
            }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score Geral", f"{score_geral}/100")
            st.metric("Classificação", faixa)
        with col2:
            # Gauge (Plotly)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_geral,
                title={"text": "Índice"},
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#C9A24B"},
                    "steps": [
                        {"range": [0, 20], "color": "#f0f0f0"},
                        {"range": [20, 40], "color": "#f8f8f8"},
                        {"range": [40, 60], "color": "#fafafa"},
                        {"range": [60, 80], "color": "#fcfcfc"},
                        {"range": [80, 100], "color": "#fefefe"},
                    ],
                }
            ))
            fig.update_layout(height=300, font={"size": 14})
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            st.markdown("### Pilares")
            for nome, valor in pilares.items():
                st.progress(valor / 100, text=f"{nome}: {valor}/100")
        
        # Gráficos
        st.markdown("---")
        st.markdown("### Gráficos Consolidados")
        
        col1, col2 = st.columns(2)
        
        # Canais digitais
        with col1:
            canais_freq = {}
            for d in dados:
                for canal in d.get("canais_digitais", []):
                    canais_freq[canal] = canais_freq.get(canal, 0) + 1
            if canais_freq:
                fig = px.bar(
                    x=list(canais_freq.keys()),
                    y=list(canais_freq.values()),
                    title="Canais digitais utilizados",
                    labels={"x": "Canal", "y": "Frequência"},
                    color_discrete_sequence=["#13345F"]
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Origem dos clientes
        with col2:
            origem_freq = {}
            for d in dados:
                for orig in d.get("origem_clientes", []):
                    origem_freq[orig] = origem_freq.get(orig, 0) + 1
            if origem_freq:
                fig = px.pie(
                    values=list(origem_freq.values()),
                    names=list(origem_freq.keys()),
                    title="Origem dos clientes"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        # Prioridades
        with col1:
            prio_freq = {}
            for d in dados:
                for p in d.get("prioridades_12_meses", []):
                    prio_freq[p] = prio_freq.get(p, 0) + 1
            if prio_freq:
                fig = px.bar(
                    y=list(prio_freq.keys()),
                    x=list(prio_freq.values()),
                    orientation="h",
                    title="Prioridades estratégicas",
                    labels={"x": "Frequência", "y": "Prioridade"},
                    color_discrete_sequence=["#C9A24B"]
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Riscos
        with col2:
            risco_freq = {}
            for d in dados:
                for r in d.get("riscos_crescimento", []):
                    risco_freq[r] = risco_freq.get(r, 0) + 1
            if risco_freq:
                fig = px.bar(
                    y=list(risco_freq.keys()),
                    x=list(risco_freq.values()),
                    orientation="h",
                    title="Riscos percebidos",
                    labels={"x": "Frequência", "y": "Risco"},
                    color_discrete_sequence=["#C0463B"]
                )
                st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PÁGINA 4: RELATÓRIO
# ============================================================
elif page == "📄 Relatório":
    st.markdown("## Relatório de Diagnóstico")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("📭 Nenhum diagnóstico preenchido. Acesse a aba **Diagnóstico** para começar.")
    else:
        # Seletor
        nomes = ["Consolidado (todas as respostas)"] + [
            f"{d.get('nome_respondente', 'Sem nome')} · {d.get('cargo', '—')}"
            for d in dados
        ]
        idx = st.selectbox("Recorte para o relatório", range(len(nomes)), format_func=lambda i: nomes[i])
        
        if idx == 0:
            # Consolidado
            scores = [d.get("score", 0) for d in dados]
            score_geral = int(sum(scores) / len(scores)) if scores else 0
            registro = None
            meta = f"Visão consolidada · {len(dados)} resposta(s)"
        else:
            registro = dados[idx - 1]
            score_geral = registro.get("score", 0)
            meta = f"{registro.get('nome_respondente', '—')} · {registro.get('cargo', '—')}"
        
        faixa, cor = MotorMaturidade.classificar(score_geral)
        pilares = MotorMaturidade.pilares(registro) if registro else MotorMaturidade.pilares({})
        if not registro and dados:
            pilares_todos = [d.get("pilares", {}) for d in dados]
            pilares = {
                k: int(sum(p.get(k, 0) for p in pilares_todos) / len(pilares_todos))
                for k in ["Estratégia", "Comercial", "Marketing", "Tecnologia", "Inovação"]
            }
        
        # Cabeçalho
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### Diagnóstico Estratégico")
            st.markdown(f"**{meta}**")
        with col2:
            st.markdown(f"### 📊 {score_geral}/100")
            st.markdown(f"**{faixa}**")
        
        st.markdown("---")
        
        # Resumo executivo
        st.markdown("### 📋 Resumo Executivo")
        pares = sorted(pilares.items(), key=lambda x: x[1], reverse=True)
        forte, fraco = pares[0], pares[-1]
        st.markdown(f"""
        O diagnóstico posiciona a MC Associados no nível **"{faixa}"**, com pontuação geral de **{score_geral}/100**.
        
        O pilar mais desenvolvido é **{forte[0]}** ({forte[1]}/100), enquanto **{fraco[0]}** ({fraco[1]}/100) 
        concentra a maior oportunidade de evolução.
        
        As recomendações a seguir priorizam ganhos de curto prazo em geração de demanda e estruturação comercial.
        """)
        
        # Oportunidades
        st.markdown("### 💡 Oportunidades")
        oport = []
        ref = registro or dados[0] if dados else {}
        
        if get_num(ref.get("nota_presenca_digital", 0)) < 7:
            oport.append("Elevar a presença digital com conteúdo técnico de autoridade.")
        if "LinkedIn" not in ref.get("canais_digitais", []):
            oport.append("Ativar o LinkedIn como canal B2B para captação.")
        if "Google Ads" not in ref.get("canais_digitais", []) and "Meta Ads" not in ref.get("canais_digitais", []):
            oport.append("Iniciar mídia paga segmentada para gerar fluxo previsível de leads.")
        if ref.get("usa_ia_automacao") != "Sim":
            oport.append("Implantar automações de marketing e atendimento (CRM + IA).")
        if preenchido(ref.get("segmentos_desejados")):
            oport.append(f"Construir oferta dedicada para: {ref.get('segmentos_desejados')}.")
        
        if not oport:
            oport = ["Consolidar e otimizar as iniciativas já existentes."]
        
        for item in oport:
            st.markdown(f"✓ {item}")
        
        # Gargalos
        st.markdown("### ⚠️ Gargalos")
        gargalo = []
        if ref.get("processo_comercial") != "Sim":
            gargalo.append("Processo comercial não totalmente formalizado.")
        if ref.get("funil_vendas") != "Sim":
            gargalo.append("Ausência de funil de vendas estruturado.")
        if get_num(ref.get("taxa_conversao", 0)) > 0 and get_num(ref.get("taxa_conversao", 0)) < 20:
            gargalo.append("Taxa de conversão de propostas abaixo do ideal.")
        if ref.get("planejamento_marketing") != "Sim":
            gargalo.append("Marketing sem planejamento formal.")
        if ref.get("resultados_mensuraveis") == "Não":
            gargalo.append("Falta de métricas claras de resultado.")
        
        for item in gargalo or ["Sem gargalos críticos identificados."]:
            st.markdown(f"• {item}")
        
        # Recomendações
        st.markdown("### 🎯 Recomendações Estratégicas")
        recs = [
            "Definir posicionamento e proposta de valor por segmento prioritário.",
            "Estruturar funil comercial com etapas, responsáveis e metas.",
            "Criar calendário editorial de autoridade focado nas dores reais.",
            "Implementar mídia paga de captação com mensuração de custo.",
            "Adotar automações e IA para nutrição de leads e relatórios.",
        ]
        for i, item in enumerate(recs, 1):
            st.markdown(f"{i}. {item}")
        
        # Próximos passos
        st.markdown("### 📍 Próximos Passos")
        passos = [
            "Validar este diagnóstico com a diretoria.",
            "Aprovar orçamento e metas.",
            "Iniciar o roadmap de 90 dias.",
        ]
        for item in passos:
            st.markdown(f"→ {item}")
        
        # Roadmaps
        st.markdown("### 🗺️ Roadmap")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 90 dias")
            st.markdown("""
            **Mês 1 — Fundamentos**
            - Posicionamento, CRM, funil
            
            **Mês 2 — Presença & conteúdo**
            - Site, landing pages, calendário editorial
            
            **Mês 3 — Geração de demanda**
            - Campanhas, automação, primeiros relatórios
            """)
        with col2:
            st.markdown("#### 12 meses")
            st.markdown("""
            **Trim. 1** — Estruturação
            **Trim. 2** — Escalação
            **Trim. 3** — Rentabilização
            **Trim. 4** — Consolidação
            """)
        
        # Botão para download
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            # Exportar como texto
            texto_relatorio = f"""MC ASSOCIADOS — Relatório de Diagnóstico
{meta}
Score: {score_geral}/100 · {faixa}

PILARES:
{chr(10).join(f"{k}: {v}/100" for k, v in pilares.items())}

OPORTUNIDADES:
{chr(10).join(f"- {o}" for o in oport)}

GARGALOS:
{chr(10).join(f"- {g}" for g in gargalo)}

RECOMENDAÇÕES:
{chr(10).join(f"{i}. {r}" for i, r in enumerate(recs, 1))}"""
            
            st.download_button(
                "📥 Baixar relatório (TXT)",
                texto_relatorio,
                file_name=f"relatorio_mc_{datetime.now().strftime('%Y%m%d')}.txt",
                use_container_width=True
            )

# ============================================================
# RODAPÉ
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
**MC Associados**  
Consultoria Contábil e Tributária  
[Diagnóstico 2024]
""")
