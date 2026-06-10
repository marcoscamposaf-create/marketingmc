# MC Associados — Diagnóstico de Marketing Digital & Crescimento

Aplicação web para coletar informações estratégicas de sócios e gestores da
**MC Associados — Consultoria Contábil e Tributária** e transformá-las em um
diagnóstico executivo: indicadores, score de maturidade (0–100) e relatório
final com recomendações e roadmaps.

Visual corporativo premium em **azul-marinho, branco e cinza**, com acento
sóbrio em dourado. Responsivo, sem dependência de build.

---

## 1. Estrutura do projeto

```
mc-associados/
├── index.html        Página institucional (apresentação + método)
├── formulario.html   Formulário em 8 blocos, com barra de progresso e LGPD
├── dashboard.html    Dashboard executivo (KPIs, score, gráficos Chart.js)
├── relatorio.html    Relatório final (diagnóstico, recomendações, roadmaps)
├── style.css         Sistema de design completo
├── script.js         Lógica: formulário, motor de score, dashboard, relatório
├── supabase.js       Camada de dados (Supabase + fallback localStorage)
├── database.sql      Criação da tabela no Supabase
└── README.md         Este arquivo
```

### Como o sistema funciona

1. **index.html** apresenta o projeto e leva ao formulário.
2. **formulario.html** coleta as respostas (8 blocos). Ao concluir, grava o
   registro via `supabase.js` e mostra o score preliminar.
3. **dashboard.html** lê todos os registros, calcula KPIs e desenha gráficos.
4. **relatorio.html** gera o documento consolidado, pronto para imprimir/PDF.

O cálculo do score é centralizado em `Maturidade` (dentro de `script.js`), então
formulário, dashboard e relatório usam exatamente a mesma lógica.

---

## 2. Rodar localmente

O projeto é estático (HTML/CSS/JS). Por causa do carregamento dos arquivos `.js`,
use um servidor local simples — abrir o HTML por `file://` pode bloquear scripts.

**Opção A — Python (já instalado na maioria dos sistemas):**
```bash
cd mc-associados
python3 -m http.server 8080
# abra http://localhost:8080
```

**Opção B — Node:**
```bash
cd mc-associados
npx serve .
```

**Opção C — VS Code:** extensão *Live Server* → "Open with Live Server".

Sem nenhuma configuração extra, o sistema já funciona em **modo Local**
(as respostas ficam no `localStorage` do navegador). Ideal para demonstração
imediata aos sócios.

---

## 3. Configurar o Supabase (opcional, recomendado para produção)

1. Crie um projeto em <https://supabase.com>.
2. No menu **SQL Editor**, cole e execute o conteúdo de **`database.sql`**.
   Isso cria a tabela `diagnostico_mc_associados` e as políticas de acesso.
3. Em **Project Settings → API**, copie a **Project URL** e a **anon public key**.
4. Abra **`supabase.js`** e preencha:
   ```js
   const SUPABASE_URL = "https://SEU-PROJETO.supabase.co";
   const SUPABASE_ANON_KEY = "SUA-CHAVE-ANON";
   ```
5. Pronto. Ao recarregar, o sistema passa automaticamente para o **modo Supabase**
   (o dashboard exibe a fonte de dados ativa no topo). O SDK do Supabase é
   carregado sob demanda via CDN — não há instalação local.

> Enquanto `SUPABASE_URL`/`SUPABASE_ANON_KEY` estiverem vazios, o sistema usa o
> `localStorage`. A API interna (`MCData.salvar / listar / remover`) é idêntica
> nos dois modos, então nada mais muda no código.

---

## 4. Score de maturidade (0–100)

Cinco pilares, cada um normalizado de 0 a 100; o score geral é a média.

| Pilar       | Como é calculado                                                            |
|-------------|------------------------------------------------------------------------------|
| Estratégia  | Completude de missão, visão, reconhecimento e diferenciais                   |
| Comercial   | Processo formalizado + funil de vendas + taxa de conversão                   |
| Marketing   | Nota de presença digital + planejamento + resultados mensuráveis             |
| Tecnologia  | Nota de maturidade digital declarada                                         |
| Inovação    | Uso de IA/automação + processos a automatizar + iniciativas futuras          |

**Classificação:** 0–20 Inicial · 21–40 Básico · 41–60 Em desenvolvimento ·
61–80 Estruturado · 81–100 Avançado.

A regra de pontuação fica em `script.js → Maturidade`. Para ajustar pesos,
edite apenas esse objeto — todas as telas refletem a mudança.

---

## 5. Tecnologias

- HTML5, CSS3 e JavaScript (sem framework / sem etapa de build)
- [Chart.js 4](https://www.chartjs.org/) para os gráficos do dashboard
- [Supabase](https://supabase.com/) como banco (opcional)
- `localStorage` como alternativa offline
- Fontes: Fraunces (display), Inter (texto), IBM Plex Mono (dados)

---

## 6. Privacidade (LGPD)

O formulário exibe o aviso de uso das informações e exige consentimento
explícito antes do envio. Os dados destinam-se exclusivamente ao diagnóstico
estratégico e ao planejamento de marketing e crescimento da MC Associados.
