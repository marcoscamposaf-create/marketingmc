# Rodar a Aplicação Streamlit

A versão **Streamlit** da aplicação oferece uma interface web completa, sem necessidade de compilação.

---

## 1. Rodar localmente (desenvolvimento)

### Pré-requisitos
- **Python 3.8+** instalado
- Uma pasta com os seguintes arquivos:
  - `app.py`
  - `requirements.txt`
  - (Opcionalmente: `index.html`, `formulario.html`, etc., se quiser também a versão HTML)

### Passo a passo

#### Windows (PowerShell ou CMD)

```powershell
# Navegar até a pasta do projeto
cd C:\Caminho\para\mc-associados

# (Opcional) Criar um ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```

#### macOS / Linux

```bash
# Navegar até a pasta do projeto
cd /caminho/para/mc-associados

# (Opcional) Criar um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```

Streamlit abrirá automaticamente a aplicação no navegador em `http://localhost:8501`.

---

## 2. Rodar na web

### Opção A: Streamlit Cloud (Gratuito)

**Streamlit Cloud** é a forma mais fácil de publicar uma aplicação Streamlit.

#### Setup

1. **Crie um repositório GitHub** com os arquivos:
   - `app.py`
   - `requirements.txt`

2. Acesse **https://share.streamlit.io** e clique em **"Deploy an app"**.

3. Autentique com sua conta GitHub.

4. Selecione o repositório, branch e arquivo (`app.py`).

5. Clique em **"Deploy"** — Streamlit gera uma URL pública em segundos.

A aplicação estará disponível em um URL como: `https://seu-usuario-mc-associados-app.streamlit.app`

#### Vantagens
- ✅ Gratuito
- ✅ Deploy automático (cada push no GitHub redeploy)
- ✅ HTTPS automático
- ✅ Dados salvos em JSON local (ou Supabase, se configurado)

---

### Opção B: Render / Railway / Heroku (com custo mínimo)

Se preferir mais controle ou um domínio customizado:

#### Render

1. Crie conta em **https://render.com**
2. Novo **Web Service** → conecte seu repo GitHub
3. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=10000 --server.address=0.0.0.0
   ```
4. Deploy automático.

#### Railway

1. Crie conta em **https://railway.app**
2. Connect repositório GitHub
3. Railway detecta `requirements.txt` automaticamente
4. Deploy em alguns segundos.

---

## 3. Dados persistidos

Por padrão, os diagnósticos são salvos em um arquivo `diagnosticos_mc.json` na mesma pasta.

### Onde os dados são armazenados

- **Ambiente local**: Arquivo `diagnosticos_mc.json` no diretório da aplicação.
- **Streamlit Cloud**: Arquivo persiste no servidor do Streamlit (mantém histórico).
- **Supabase** (opcional): Se você quiser um banco real, configure as credenciais no `app.py` (adicione a lógica de conexão).

### Backup dos dados

Para fazer backup, baixe o arquivo `diagnosticos_mc.json` a qualquer momento.

---

## 4. Customizações

### Alterar porta (se precisar)

```bash
streamlit run app.py --server.port 9000
```

### Desabilitar confirmação de upload

```bash
streamlit run app.py --logger.level=error
```

### Configurar arquivo de config

Crie um `.streamlit/config.toml` na pasta raiz:

```toml
[theme]
primaryColor = "#C9A24B"
backgroundColor = "#FBFCFE"
secondaryBackgroundColor = "#E4E9F0"
textColor = "#0A1F3C"

[browser]
gatherUsageStats = false
```

---

## 5. Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

Instale as dependências:
```bash
pip install -r requirements.txt
```

### "Port 8501 is already in use"

Use outra porta:
```bash
streamlit run app.py --server.port 8502
```

### Dados não persistem no Streamlit Cloud

Os dados salvos em arquivo local (`diagnosticos_mc.json`) funcionam no Cloud, mas:
- Se você faz redeploy, cria uma nova instância.
- Para persistência garantida, use **Supabase** ou outro banco externo.

---

## 6. Próximos passos

1. **Rodar localmente** para testar.
2. **Publicar no Streamlit Cloud** para compartilhar com os sócios.
3. **(Opcional) Integrar com Supabase** para banco de dados persistente em produção.

---

## Comparação: HTML/JS vs Streamlit

| Aspecto | HTML/JS | Streamlit |
|--------|---------|-----------|
| Deploy | Netlify, Vercel, GitHub Pages | Streamlit Cloud (mais fácil) |
| Dados | localStorage + Supabase | JSON local + Supabase |
| Customização | Total (CSS) | Moderada (Streamlit config) |
| Performance | Muito rápida | Rápida (Python backend) |
| Melhor para | Marketing, público geral | Dados internos, análise |

**Use HTML** se quer máxima customização visual.  
**Use Streamlit** se quer rapidez de deploy e análise de dados interativa.
