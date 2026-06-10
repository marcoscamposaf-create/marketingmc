# 📦 MC ASSOCIADOS — Projeto Completo Entregue

Aplicação web **dual-stack** para diagnóstico estratégico de marketing digital:
- **Versão HTML/JS**: Static, sem build, roda em qualquer servidor web.
- **Versão Streamlit**: Python, deploy em 1 clique no Streamlit Cloud.

---

## 📁 Arquivos entregues (14 arquivos + 3.282 linhas)

### 🎨 **Versão HTML/JS** (estática, pronta para web)

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| **index.html** | Página institucional com hero e método | 178 |
| **formulario.html** | Formulário em 8 blocos com validação | 369 |
| **dashboard.html** | Dashboard executivo com seletor de recorte | 121 |
| **relatorio.html** | Relatório consolidado (diagnóstico + roadmap) | 132 |
| **style.css** | Sistema de design completo (azul/branco/cinza) | 453 |
| **script.js** | Motor de score, gráficos, lógica do formulário | 567 |
| **supabase.js** | Camada de dados (Supabase + localStorage) | 101 |
| **database.sql** | Criação de tabela no Supabase | 89 |

### 🐍 **Versão Streamlit** (Python, deploy 1-clique)

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| **app.py** | Aplicação Streamlit completa (4 páginas) | 650+ |
| **requirements.txt** | Dependências Python | 3 |

### 📖 **Documentação**

| Arquivo | Descrição |
|---------|-----------|
| **README.md** | Como usar, estrutura, Supabase setup |
| **COMECE_AQUI.md** | Guia rápido para Windows (PowerShell) |
| **RODAR_NA_WEB.md** | 4 opções de deploy (Netlify, Vercel, GitHub Pages, Replit) |
| **STREAMLIT_GUIDE.md** | Como rodar o app.py localmente e na web |

---

## 🚀 Quick Start (escolha uma opção)

### Opção 1️⃣: HTML na Web (2 minutos)

```bash
# Baixe os 8 arquivos HTML/CSS/JS
# Arraste a pasta para Netlify.com
# ✅ Pronto — aplicação no ar
```

**URL gerada:** `seu-site.netlify.app`

### Opção 2️⃣: Streamlit Cloud (2 minutos)

```bash
# Suba app.py + requirements.txt para GitHub
# Acesse https://share.streamlit.io
# Selecione o repositório
# ✅ Pronto — deploy automático
```

**URL gerada:** `seu-usuario-app.streamlit.app`

### Opção 3️⃣: Rodar localmente (Windows)

```powershell
cd C:\Projetos\mc-associados
python3 -m http.server 8080  # (versão HTML)
# ou
pip install -r requirements.txt && streamlit run app.py  # (versão Streamlit)
```

---

## 🎯 O que cada versão oferece

### **HTML/JS** — Visual Premium, Deploy Simples

✅ Design corporativo totalmente customizável  
✅ Sem dependências (funciona em qualquer servidor)  
✅ Ideal para apresentação aos sócios  
✅ Gráficos com Chart.js  
✅ Dados em localStorage (offline) ou Supabase  

### **Streamlit** — Python, Análise Interativa

✅ Deploy 1-clique no Streamlit Cloud  
✅ Backend Python (fácil expandir com análise avançada)  
✅ Dados em JSON (persistem no servidor)  
✅ Gráficos com Plotly (interativos)  
✅ Ideal para equipe interna analisar dados  

---

## 💾 Dados & Persistência

Ambas as versões salvam diagnósticos em:

1. **localStorage** (HTML) — navegador local
2. **JSON** (Streamlit) — arquivo no servidor
3. **Supabase** (opcional) — banco PostgreSQL real

Para usar Supabase:
1. Crie conta em https://supabase.com
2. Execute o `database.sql`
3. Preencha as credenciais em `supabase.js` (HTML) ou `app.py` (Streamlit)

---

## 🎓 O que foi implementado

✅ **Formulário em 8 blocos** exatamente como pedido  
✅ **Motor de maturidade** com 5 pilares (Estratégia, Comercial, Marketing, Tecnologia, Inovação)  
✅ **Score automático** 0–100 com classificação (Inicial → Avançado)  
✅ **Dashboard executivo** com KPIs e 6 gráficos  
✅ **Relatório consolidado** com diagnóstico, oportunidades, gargalos, roadmaps (90 dias + 12 meses)  
✅ **Aviso de LGPD** obrigatório  
✅ **Design corporativo** azul-marinho/branco/cinza com acento dourado  
✅ **Responsivo** (mobile, tablet, desktop)  
✅ **Sem build/npm** (versão HTML)  
✅ **Código limpo** comentado e organizado  

---

## 📊 Dados salvos

Cada diagnóstico armazena:
- Identificação (nome, cargo)
- 8 blocos estratégicos (32 campos)
- Score e pilares calculados automaticamente
- Data/hora da resposta
- Tudo pronto para análise consolidada

---

## 🔧 Suporte & Customizações

**Fácil de customizar:**
- Perguntas do formulário → edite em `formulario.html`
- Peso dos pilares → ajuste em `Maturidade.pilares()` em `script.js`
- Paleta de cores → mude as variáveis CSS em `style.css`
- Domínio customizado → configure no Netlify/Vercel

---

## ✅ Checklist Final

- ✅ 8 arquivos HTML/CSS/JS prontos para deploy
- ✅ 1 arquivo `app.py` Streamlit completo
- ✅ SQL para criar banco no Supabase
- ✅ 4 guias de setup em português
- ✅ Sem erros de syntax
- ✅ Validado e testado
- ✅ Pronto para apresentação aos sócios da MC Associados

---

## 🎉 Próximas ações

1. **Escolha a versão** (HTML ou Streamlit)
2. **Deploy na web** (Netlify / Streamlit Cloud — 2 minutos)
3. **Compartilhe o link** com os sócios
4. **Colete respostas** e veja os scores gerados em tempo real
5. **(Opcional) Configure Supabase** para banco persistente

---

**Tudo pronto para a MC Associados!** 🚀
