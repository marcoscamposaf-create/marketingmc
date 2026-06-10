# Rodar MC Associados na Web

O projeto é **100% estático** (HTML/CSS/JS), então pode rodar em qualquer plataforma. Aqui estão as **3 opções mais fáceis**.

---

## OPÇÃO 1: Netlify (⭐ Mais fácil — recomendado)

Netlify permite arrastar e soltar a pasta. Leva 2 minutos.

### Passo a passo

1. **Baixe todos os 9 arquivos** da pasta `mc-associados`.
2. **Crie uma pasta local** com todos eles (ex: `mc-associados/`).
3. Acesse https://netlify.com e **clique em "Sign up"** (pode usar GitHub/Google).
4. Na dashboard, procure por **"Sites"** → clique em **"Drag to deploy"** ou **"New site"**.
5. **Arraste a pasta inteira** `mc-associados/` para a área de drop.
6. Pronto! Netlify gera um URL único (ex: `graceful-panda-abc123.netlify.app`).

### Domínio customizado (opcional)

Na dashboard, vá para **"Domain settings"** → **"Add domain"** e coloque seu próprio domínio (ou compre um lá).

---

## OPÇÃO 2: Vercel

Vercel é feita pelos criadores do Next.js e é muito rápida.

### Passo a passo

1. Acesse https://vercel.com e **clique em "Sign Up"** (GitHub/Google/email).
2. Clique em **"New Project"** → **"Deploy from Git"**.
3. Se tiver os arquivos no GitHub, sincronize o repo. Se não tiver:
   - Suba a pasta para GitHub (ou pule este passo se não quiser).
   - Ou use o **"Import Project"** → cole a URL do seu repositório.
4. Vercel detecta automaticamente que é um projeto estático.
5. Clique em **"Deploy"** e pronto!

> Se não quer mexer com GitHub, use **Netlify** (Opção 1) — é mais direto.

---

## OPÇÃO 3: GitHub Pages (Gratuito, se você tem GitHub)

Ideal se você já usa GitHub para versionamento.

### Passo a passo

1. Crie um repositório no GitHub chamado `mc-associados`.
2. **Faça upload dos 9 arquivos** para a raiz do repositório.
3. Vá para **Settings** → **Pages** → escolha **"Deploy from a branch"**.
4. Selecione **branch `main`** (ou `master`) → **Save**.
5. GitHub gera uma URL (ex: `seu-usuario.github.io/mc-associados`).

Grátis e funciona perfeitamente.

---

## OPÇÃO 4: Replit (Para prototipagem rápida)

Se quiser testar super rápido sem instalar nada.

1. Acesse https://replit.com
2. Clique em **"Create"** → **"HTML, CSS, JS"**
3. Copie e cole os arquivos nas abas correspondentes.
4. Clique em **"Run"** — Replit gera uma URL que você pode compartilhar.

> Não é ideal para produção, mas funciona para demo.

---

## 🔧 Configurar Supabase na Web

Se você quer que os dados sejam salvos em um banco real (não só no navegador):

1. Crie um projeto em https://supabase.com
2. Execute o `database.sql` no **SQL Editor** do Supabase.
3. Copie a **Project URL** e a **anon public key** (em **Settings** → **API**).
4. Abra `supabase.js` no seu código:
   ```js
   const SUPABASE_URL = "https://SEU-PROJETO.supabase.co";
   const SUPABASE_ANON_KEY = "SUA-CHAVE-ANON";
   ```
5. Redeploy a aplicação (Netlify re-detecta as mudanças automaticamente).

Pronto! Agora os diagnósticos são salvos no Supabase em vez de apenas no navegador.

---

## Recomendação

✅ **Netlify** é a mais fácil:
- Não precisa Git / GitHub
- Drag-and-drop
- URL em 2 minutos
- Domínio customizado grátis (com seu próprio domínio)
- HTTPS automático

Qual plataforma você prefere?
