/* ============================================================
   MC ASSOCIADOS — script.js
   Lógica de formulário, motor de maturidade, dashboard e relatório.
   Cada módulo só roda na página correspondente (detecção por DOM).
   ============================================================ */

/* ============================================================
   0. UTILITÁRIOS COMPARTILHADOS
   ============================================================ */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/* Menu mobile */
(function navToggle() {
  const t = $(".nav__toggle");
  if (t) t.addEventListener("click", () => $(".nav__links")?.classList.toggle("is-open"));
})();

/* Converte valor em número seguro (aceita "35%", "R$ 10", "12") */
function getNum(v) {
  if (v == null) return 0;
  const n = parseFloat(String(v).replace(",", ".").replace(/[^\d.]/g, ""));
  return isNaN(n) ? 0 : n;
}
function preenchido(v) {
  if (Array.isArray(v)) return v.length > 0;
  return v != null && String(v).trim() !== "";
}

/* Desenha um medidor radial (gauge) em SVG dentro de `mount`.
   value 0–100. opts: {size, stroke, track, fill, label} */
function drawGauge(mount, value, opts = {}) {
  const size = opts.size || 150;
  const stroke = opts.stroke || 13;
  const r = (size - stroke) / 2;
  const cx = size / 2, cy = size / 2;
  const start = 135, sweep = 270;                 // gauge de 270°
  const circ = 2 * Math.PI * r;
  const arcLen = circ * (sweep / 360);
  const pct = Math.max(0, Math.min(100, value)) / 100;

  const trackColor = opts.track || "rgba(255,255,255,.14)";
  const fillColor = opts.fill || "#C9A24B";
  const valColor = opts.label || "#fff";
  const subColor = opts.sub || "rgba(255,255,255,.6)";

  mount.innerHTML = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="Pontuação ${Math.round(value)} de 100">
      <g transform="rotate(${start} ${cx} ${cy})">
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${trackColor}"
          stroke-width="${stroke}" stroke-linecap="round"
          stroke-dasharray="${arcLen} ${circ}" />
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${fillColor}"
          stroke-width="${stroke}" stroke-linecap="round"
          stroke-dasharray="${arcLen * pct} ${circ}"
          style="transition: stroke-dasharray 1s cubic-bezier(.4,0,.2,1)" />
      </g>
      <text x="${cx}" y="${cy - 2}" text-anchor="middle" dominant-baseline="middle"
        font-family="Fraunces, serif" font-size="${size * 0.3}" font-weight="600" fill="${valColor}">${Math.round(value)}</text>
      <text x="${cx}" y="${cy + size * 0.17}" text-anchor="middle"
        font-family="Inter, sans-serif" font-size="${size * 0.085}" fill="${subColor}" letter-spacing="1">/ 100</text>
    </svg>`;
}

/* ============================================================
   1. MOTOR DE MATURIDADE (compartilhado: form, dashboard, relatório)
   ============================================================ */
const Maturidade = {
  /* Calcula os 5 pilares (0–100) e o score geral de um registro. */
  pilares(r) {
    r = r || {};

    // -- Estratégia: completude do posicionamento
    const estrCampos = [r.missao, r.visao_3_5_anos, r.reconhecimento_mercado, r.diferenciais_competitivos];
    const estrategia = estrCampos.filter(preenchido).length * 25;

    // -- Comercial: processo + funil + conversão
    let comercial = 0;
    comercial += ({ Sim: 40, Parcialmente: 20, "Não": 0 }[r.processo_comercial] ?? 0);
    comercial += (r.funil_vendas === "Sim" ? 30 : 0);
    const conv = getNum(r.taxa_conversao);
    comercial += conv >= 40 ? 30 : conv >= 20 ? 20 : conv > 0 ? 10 : (preenchido(r.taxa_conversao) ? 8 : 0);
    comercial = Math.min(100, comercial);

    // -- Marketing: presença + planejamento + resultados
    let marketing = 0;
    marketing += getNum(r.nota_presenca_digital) * 5;                 // 0–50
    marketing += ({ Sim: 30, Parcialmente: 15, "Não": 0 }[r.planejamento_marketing] ?? 0);
    marketing += ({ Sim: 20, Parcialmente: 10, "Não": 0 }[r.resultados_mensuraveis] ?? 0);
    marketing = Math.min(100, marketing);

    // -- Tecnologia: maturidade digital declarada
    const tecnologia = Math.min(100, getNum(r.nota_maturidade_digital) * 10);

    // -- Inovação: IA + automação + visão de futuro
    let inovacao = 0;
    inovacao += ({ Sim: 50, Parcialmente: 25, "Não": 0 }[r.usa_ia_automacao] ?? 0);
    inovacao += preenchido(r.processos_automatizar) ? 25 : 0;
    inovacao += preenchido(r.iniciativas_futuras) ? 25 : 0;
    inovacao = Math.min(100, inovacao);

    return {
      Estratégia: Math.round(estrategia),
      Comercial: Math.round(comercial),
      Marketing: Math.round(marketing),
      Tecnologia: Math.round(tecnologia),
      Inovação: Math.round(inovacao),
    };
  },

  score(r) {
    const p = this.pilares(r);
    const vals = Object.values(p);
    return Math.round(vals.reduce((a, b) => a + b, 0) / vals.length);
  },

  /* Média de pilares e score para um conjunto de registros (consolidado). */
  pilaresMedia(lista) {
    if (!lista.length) return { Estratégia: 0, Comercial: 0, Marketing: 0, Tecnologia: 0, Inovação: 0 };
    const soma = { Estratégia: 0, Comercial: 0, Marketing: 0, Tecnologia: 0, Inovação: 0 };
    lista.forEach((r) => {
      const p = this.pilares(r);
      for (const k in soma) soma[k] += p[k];
    });
    for (const k in soma) soma[k] = Math.round(soma[k] / lista.length);
    return soma;
  },

  classificar(score) {
    if (score <= 20) return { faixa: "Inicial", cor: "#C0463B" };
    if (score <= 40) return { faixa: "Básico", cor: "#C77A21" };
    if (score <= 60) return { faixa: "Em desenvolvimento", cor: "#C9A24B" };
    if (score <= 80) return { faixa: "Estruturado", cor: "#2C5A92" };
    return { faixa: "Avançado", cor: "#2E7D5B" };
  },
};
window.Maturidade = Maturidade;

/* ============================================================
   2. CATÁLOGO DE OPÇÕES (reaproveitado em form e gráficos)
   ============================================================ */
const OPC = {
  servicos: ["Contabilidade", "Fiscal", "Departamento Pessoal", "BPO Financeiro",
    "Planejamento Tributário", "Recuperação Tributária", "Consultoria Empresarial",
    "Abertura de Empresas", "Outros"],
  origem: ["Indicação", "Google", "Instagram", "LinkedIn", "Parceiros", "Networking", "Outros"],
  canais: ["Instagram", "LinkedIn", "Site", "Blog", "E-mail Marketing", "WhatsApp", "Google Ads", "Meta Ads"],
  prioridades: ["Crescimento da carteira", "Aumento de faturamento", "Aumento de rentabilidade",
    "Fortalecimento da marca", "Expansão de serviços", "Retenção de clientes", "Transformação digital"],
  riscos: ["Concorrência acirrada", "Dependência de poucos clientes", "Falta de processos",
    "Equipe enxuta", "Baixa geração de leads", "Pressão de margem", "Tecnologia defasada", "Rotatividade de clientes"],
  quantidade: ["Até 50", "51 a 100", "101 a 250", "251 a 500", "Acima de 500"],
};
window.OPC = OPC;

/* ============================================================
   3. MÓDULO FORMULÁRIO  (formulario.html)
   ============================================================ */
(function formModule() {
  const form = $("#diagnostico");
  if (!form) return;

  const blocos = $$(".fblock");
  const total = blocos.length;
  let atual = 0;

  const fill = $("#progressFill");
  const stepLbl = $("#progressStep");
  const pctLbl = $("#progressPct");
  const btnPrev = $("#btnPrev");
  const btnNext = $("#btnNext");
  const btnSubmit = $("#btnSubmit");
  const erro = $("#formError");

  function render() {
    blocos.forEach((b, i) => b.classList.toggle("is-active", i === atual));
    const pct = Math.round(((atual + 1) / total) * 100);
    fill.style.width = pct + "%";
    stepLbl.innerHTML = `Etapa <b>${atual + 1}</b> de ${total} · ${blocos[atual].dataset.titulo}`;
    pctLbl.textContent = pct + "%";
    btnPrev.style.visibility = atual === 0 ? "hidden" : "visible";
    btnNext.style.display = atual === total - 1 ? "none" : "inline-flex";
    btnSubmit.style.display = atual === total - 1 ? "inline-flex" : "none";
    erro.classList.remove("is-on");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* Validação leve: campos com [required] e o consentimento na última etapa */
  function validaBloco(i) {
    const bloco = blocos[i];
    const obrigatorios = $$("[required]", bloco);
    for (const campo of obrigatorios) {
      if (campo.type === "checkbox") {
        if (!campo.checked) return campo;
      } else if (!preenchido(campo.value)) {
        return campo;
      }
    }
    return null;
  }

  btnNext.addEventListener("click", () => {
    const falta = validaBloco(atual);
    if (falta) {
      erro.textContent = "Preencha os campos obrigatórios desta etapa antes de avançar.";
      erro.classList.add("is-on");
      falta.focus();
      return;
    }
    if (atual < total - 1) { atual++; render(); }
  });

  btnPrev.addEventListener("click", () => { if (atual > 0) { atual--; render(); } });

  /* Escala 0–10 (clique nos botões) */
  $$(".scale").forEach((scale) => {
    const hidden = $("input[type=hidden]", scale);
    $$(".scale__btn", scale).forEach((btn) => {
      btn.addEventListener("click", () => {
        $$(".scale__btn", scale).forEach((b) => b.classList.remove("is-on"));
        btn.classList.add("is-on");
        hidden.value = btn.dataset.val;
      });
    });
  });

  /* Coleta os dados do formulário no formato do banco */
  function coletar() {
    const fd = new FormData(form);
    const reg = {};
    // Campos simples
    for (const [k, v] of fd.entries()) {
      if (reg[k] === undefined) reg[k] = v;
      else if (Array.isArray(reg[k])) reg[k].push(v);
      else reg[k] = [reg[k], v];
    }
    // Garante arrays para os multi-select declarados
    ["servicos_oferecidos", "servicos_rentaveis", "servicos_crescimento", "servicos_prioridade_marketing",
      "origem_clientes", "canais_digitais", "prioridades_12_meses", "riscos_crescimento"].forEach((k) => {
      const vals = fd.getAll(k);
      reg[k] = vals;
    });
    return reg;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const falta = validaBloco(atual);
    if (falta) {
      erro.textContent = "Confirme o consentimento e os campos obrigatórios para concluir.";
      erro.classList.add("is-on");
      falta.focus();
      return;
    }
    btnSubmit.disabled = true;
    btnSubmit.textContent = "Enviando…";
    try {
      const registro = coletar();
      delete registro.consentimento; // não persistimos o checkbox
      const salvo = await MCData.salvar(registro);

      // Tela de conclusão
      $("#formCard").style.display = "none";
      $("#progress").style.display = "none";
      const done = $("#done");
      done.classList.add("is-on");
      const sc = Maturidade.score(salvo);
      const cls = Maturidade.classificar(sc);
      $("#doneScore").textContent = sc;
      $("#doneBand").textContent = cls.faixa;
      $("#doneBand").style.color = cls.cor;
    } catch (err) {
      console.error(err);
      erro.textContent = "Não foi possível enviar agora. Verifique a conexão e tente novamente.";
      erro.classList.add("is-on");
      btnSubmit.disabled = false;
      btnSubmit.textContent = "Concluir diagnóstico";
    }
  });

  render();
})();

/* ============================================================
   4. MÓDULO DASHBOARD  (dashboard.html)
   ============================================================ */
(function dashboardModule() {
  const dash = $("#dashRoot");
  if (!dash) return;

  let dados = [];
  let charts = [];

  function destruirCharts() { charts.forEach((c) => c.destroy()); charts = []; }

  /* contagem de frequência de opções em um campo multi-select */
  function freq(lista, campo, universo) {
    const cont = {};
    universo.forEach((o) => (cont[o] = 0));
    lista.forEach((r) => {
      const arr = Array.isArray(r[campo]) ? r[campo] : (r[campo] ? [r[campo]] : []);
      arr.forEach((v) => { if (v in cont) cont[v]++; else cont[v] = (cont[v] || 0) + 1; });
    });
    return cont;
  }

  const PAL = ["#13345F", "#2C5A92", "#C9A24B", "#1C4374", "#6A7689", "#2E7D5B", "#C77A21", "#95A0B1"];

  function baseOpts(extra = {}) {
    return Object.assign({
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
    }, extra);
  }

  function render() {
    destruirCharts();
    const sel = $("#respSelect").value;
    const registro = sel === "__all__" ? null : dados.find((d) => String(d.id) === sel);

    // ---- KPIs + Score (dependem da seleção) ----
    const pilares = registro ? Maturidade.pilares(registro) : Maturidade.pilaresMedia(dados);
    const score = registro ? Maturidade.score(registro) : Math.round(Object.values(pilares).reduce((a, b) => a + b, 0) / 5);
    const cls = Maturidade.classificar(score);

    drawGauge($("#scoreGauge"), score, { size: 168, fill: "#D8B86A" });
    $("#scoreBand").textContent = cls.faixa;

    // Pilares
    const pilarWrap = $("#pillars");
    pilarWrap.innerHTML = Object.entries(pilares).map(([nome, v]) => `
      <div class="pillar">
        <span class="pillar__name">${nome}</span>
        <span class="pillar__track"><span class="pillar__fill" style="width:${v}%"></span></span>
        <span class="pillar__val">${v}</span>
      </div>`).join("");

    // KPIs — quando consolidado, usamos o registro mais recente para valores categóricos
    const ref = registro || dados[0] || {};
    function tag(cond, ok, warn, danger) {
      return cond === "ok" ? `<span class="kpi__foot tag-ok">${ok}</span>`
        : cond === "warn" ? `<span class="kpi__foot tag-warn">${warn}</span>`
        : cond === "danger" ? `<span class="kpi__foot tag-danger">${danger}</span>`
        : `<span class="kpi__foot tag-neutral">—</span>`;
    }
    const presenca = registro ? getNum(registro.nota_presenca_digital) : media(dados, "nota_presenca_digital");
    const matur = registro ? getNum(registro.nota_maturidade_digital) : media(dados, "nota_maturidade_digital");

    $("#kpis").innerHTML = `
      ${kpi("Presença digital", presenca.toFixed(1), "<small>/10</small>", tag(presenca >= 7 ? "ok" : presenca >= 4 ? "warn" : "danger", "Forte", "Mediana", "Frágil"))}
      ${kpi("Maturidade digital", matur.toFixed(1), "<small>/10</small>", tag(matur >= 7 ? "ok" : matur >= 4 ? "warn" : "danger", "Madura", "Em evolução", "Inicial"))}
      ${kpi("Clientes ativos", ref.quantidade_clientes || "—", "", tag("neutral"))}
      ${kpi("Novos clientes/mês", ref.novos_clientes_mes ? getNum(ref.novos_clientes_mes) : "—", "", tag("neutral"))}
      ${kpi("Taxa de conversão", ref.taxa_conversao || "—", "", tag(getNum(ref.taxa_conversao) >= 30 ? "ok" : getNum(ref.taxa_conversao) >= 15 ? "warn" : "danger", "Saudável", "Atenção", "Baixa"))}
      ${kpi("Estrutura comercial", ref.processo_comercial || "—", "", tag(ref.processo_comercial === "Sim" ? "ok" : ref.processo_comercial === "Parcialmente" ? "warn" : "danger", "Formalizada", "Parcial", "Inexistente"))}
      ${kpi("Planejamento de mkt", ref.planejamento_marketing || "—", "", tag(ref.planejamento_marketing === "Sim" ? "ok" : ref.planejamento_marketing === "Parcialmente" ? "warn" : "danger", "Estruturado", "Parcial", "Ausente"))}
      ${kpi("IA & automação", ref.usa_ia_automacao || "—", "", tag(ref.usa_ia_automacao === "Sim" ? "ok" : ref.usa_ia_automacao === "Parcialmente" ? "warn" : "danger", "Em uso", "Inicial", "Não usa"))}
    `;

    // ---- Gráficos (sempre consolidados sobre todas as respostas) ----
    const c1 = freq(dados, "canais_digitais", OPC.canais);
    charts.push(new Chart($("#chCanais"), {
      type: "bar",
      data: { labels: Object.keys(c1), datasets: [{ data: Object.values(c1), backgroundColor: "#13345F", borderRadius: 6 }] },
      options: baseOpts({ scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }),
    }));

    const c2 = freq(dados, "origem_clientes", OPC.origem);
    charts.push(new Chart($("#chOrigem"), {
      type: "doughnut",
      data: { labels: Object.keys(c2), datasets: [{ data: Object.values(c2), backgroundColor: PAL }] },
      options: baseOpts({ cutout: "60%", plugins: { legend: { display: true, position: "right", labels: { boxWidth: 12, font: { size: 11 } } } } }),
    }));

    const c3 = freq(dados, "prioridades_12_meses", OPC.prioridades);
    charts.push(new Chart($("#chPrioridades"), {
      type: "bar",
      data: { labels: Object.keys(c3), datasets: [{ data: Object.values(c3), backgroundColor: "#C9A24B", borderRadius: 6 }] },
      options: baseOpts({ indexAxis: "y", scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } }),
    }));

    charts.push(new Chart($("#chMaturidade"), {
      type: "radar",
      data: {
        labels: Object.keys(pilares),
        datasets: [{ data: Object.values(pilares), backgroundColor: "rgba(44,90,146,.18)", borderColor: "#2C5A92", pointBackgroundColor: "#C9A24B", borderWidth: 2 }],
      },
      options: baseOpts({ scales: { r: { suggestedMin: 0, suggestedMax: 100, ticks: { stepSize: 20, font: { size: 10 } } } } }),
    }));

    const c5 = freq(dados, "servicos_prioridade_marketing", OPC.servicos);
    charts.push(new Chart($("#chServicos"), {
      type: "bar",
      data: { labels: Object.keys(c5), datasets: [{ data: Object.values(c5), backgroundColor: "#1C4374", borderRadius: 6 }] },
      options: baseOpts({ indexAxis: "y", scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } }),
    }));

    const c6 = freq(dados, "riscos_crescimento", OPC.riscos);
    charts.push(new Chart($("#chRiscos"), {
      type: "bar",
      data: { labels: Object.keys(c6), datasets: [{ data: Object.values(c6), backgroundColor: "#C0463B", borderRadius: 6 }] },
      options: baseOpts({ indexAxis: "y", scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } }),
    }));
  }

  function media(lista, campo) {
    if (!lista.length) return 0;
    return lista.reduce((a, r) => a + getNum(r[campo]), 0) / lista.length;
  }
  function kpi(lbl, val, suf, tagHtml) {
    return `<div class="kpi"><div class="kpi__lbl">${lbl}</div><div class="kpi__val">${val}${suf}</div>${tagHtml}</div>`;
  }

  async function init() {
    try { dados = await MCData.listar(); }
    catch (e) { console.error(e); dados = []; }

    $("#modeTag").textContent = MCData.modo === "supabase" ? "Supabase" : "Local";

    if (!dados.length) {
      $("#dashContent").style.display = "none";
      $("#dashEmpty").style.display = "block";
      return;
    }
    // Popular seletor de respondentes
    const sel = $("#respSelect");
    sel.innerHTML = `<option value="__all__">Consolidado · todas as respostas (${dados.length})</option>` +
      dados.map((d) => `<option value="${d.id}">${d.nome_respondente || "Sem nome"}${d.cargo ? " · " + d.cargo : ""}</option>`).join("");
    sel.addEventListener("change", render);
    render();
  }

  init();
})();

/* ============================================================
   5. MÓDULO RELATÓRIO  (relatorio.html)
   ============================================================ */
(function reportModule() {
  const root = $("#reportRoot");
  if (!root) return;

  function txt(v, fallback = "Não informado.") { return preenchido(v) ? (Array.isArray(v) ? v.join(", ") : v) : fallback; }

  async function init() {
    let dados = [];
    try { dados = await MCData.listar(); } catch (e) { console.error(e); }

    if (!dados.length) {
      $("#reportContent").style.display = "none";
      $("#reportEmpty").style.display = "block";
      return;
    }

    // Seletor
    const sel = $("#repSelect");
    sel.innerHTML = `<option value="__all__">Consolidado · todas as respostas</option>` +
      dados.map((d) => `<option value="${d.id}">${d.nome_respondente || "Sem nome"}${d.cargo ? " · " + d.cargo : ""}</option>`).join("");
    sel.addEventListener("change", () => build(dados, sel.value));
    build(dados, "__all__");
  }

  function build(dados, selId) {
    const reg = selId === "__all__" ? null : dados.find((d) => String(d.id) === selId);
    const base = reg || dados[0];
    const pilares = reg ? Maturidade.pilares(reg) : Maturidade.pilaresMedia(dados);
    const score = reg ? Maturidade.score(reg) : Math.round(Object.values(pilares).reduce((a, b) => a + b, 0) / 5);
    const cls = Maturidade.classificar(score);

    $("#repScore").textContent = score;
    $("#repBand").textContent = cls.faixa;
    $("#repBand").style.color = cls.cor;
    $("#repMeta").textContent = reg
      ? `${reg.nome_respondente || "Respondente"}${reg.cargo ? " · " + reg.cargo : ""} · ${new Date(reg.data_resposta).toLocaleDateString("pt-BR")}`
      : `Visão consolidada · ${dados.length} resposta(s) · ${new Date().toLocaleDateString("pt-BR")}`;

    // ---- Resumo executivo (gerado a partir dos dados) ----
    const pares = Object.entries(pilares).sort((a, b) => b[1] - a[1]);
    const forte = pares[0], fraco = pares[pares.length - 1];
    $("#repResumo").textContent =
      `O diagnóstico posiciona a MC Associados no nível "${cls.faixa}", com pontuação geral de ${score}/100. ` +
      `O pilar mais desenvolvido é ${forte[0]} (${forte[1]}/100), enquanto ${fraco[0]} (${fraco[1]}/100) concentra a maior oportunidade de evolução. ` +
      `As recomendações a seguir priorizam ganhos de curto prazo em geração de demanda e estruturação comercial, ` +
      `sustentados por uma base de marca e tecnologia consistente com o posicionamento premium da consultoria.`;

    // ---- Oportunidades / gargalos (regras simples sobre os dados) ----
    const oport = [], gargalo = [];
    if (getNum(base.nota_presenca_digital) < 7) oport.push("Elevar a presença digital com conteúdo técnico de autoridade (tributário e contábil).");
    if (!arrTem(base.canais_digitais, "LinkedIn")) oport.push("Ativar o LinkedIn como canal B2B para captação de empresas e gestores.");
    if (!arrTem(base.canais_digitais, "Google Ads") && !arrTem(base.canais_digitais, "Meta Ads")) oport.push("Iniciar mídia paga segmentada para gerar fluxo previsível de leads qualificados.");
    if (base.usa_ia_automacao !== "Sim") oport.push("Implantar automações de marketing e atendimento (CRM + IA) para escalar sem aumentar custo.");
    if (preenchido(base.segmentos_desejados)) oport.push(`Construir oferta dedicada para os segmentos-alvo: ${txt(base.segmentos_desejados)}.`);
    if (!oport.length) oport.push("Consolidar e otimizar as iniciativas já existentes, ampliando investimento nos canais de melhor retorno.");

    if (base.processo_comercial !== "Sim") gargalo.push("Processo comercial não totalmente formalizado — risco de perda de oportunidades por falta de padrão.");
    if (base.funil_vendas !== "Sim") gargalo.push("Ausência de funil de vendas estruturado dificulta previsibilidade e gestão de conversão.");
    if (getNum(base.taxa_conversao) > 0 && getNum(base.taxa_conversao) < 20) gargalo.push("Taxa de conversão de propostas abaixo do ideal — revisar abordagem e qualificação.");
    if (base.planejamento_marketing !== "Sim") gargalo.push("Marketing sem planejamento formal reduz consistência e mensuração de resultados.");
    if (base.resultados_mensuraveis === "Não") gargalo.push("Falta de métricas claras impede avaliar o retorno das ações de marketing.");
    arrEach(base.riscos_crescimento, (rk) => gargalo.push("Risco percebido pela diretoria: " + rk + "."));
    if (!gargalo.length) gargalo.push("Sem gargalos críticos identificados — foco em otimização contínua.");

    // ---- Serviços com maior potencial ----
    const servPot = (Array.isArray(base.servicos_crescimento) && base.servicos_crescimento.length)
      ? base.servicos_crescimento
      : (Array.isArray(base.servicos_prioridade_marketing) ? base.servicos_prioridade_marketing : []);

    // ---- Recomendações ----
    const recs = [
      "Definir posicionamento e proposta de valor por segmento prioritário, traduzindo diferenciais técnicos em benefícios de negócio.",
      "Estruturar funil comercial com etapas, responsáveis e metas; integrar a um CRM para acompanhamento da conversão.",
      "Criar calendário editorial de autoridade (artigos, LinkedIn, e-mail) focado nas dores reais dos clientes.",
      "Implementar mídia paga de captação com landing pages e mensuração de custo por lead e por cliente.",
      "Adotar automações e IA para nutrição de leads, atendimento e relatórios gerenciais mensais.",
    ];

    $("#repOport").innerHTML = oport.map((o) => `<li class="pos">${o}</li>`).join("");
    $("#repGargalos").innerHTML = gargalo.map((g) => `<li class="neg">${g}</li>`).join("");
    $("#repServicos").innerHTML = servPot.length
      ? servPot.map((s) => `<li class="pos">${s}</li>`).join("")
      : `<li>Definir, junto à diretoria, os serviços de maior margem e escalabilidade.</li>`;
    $("#repRecs").innerHTML = recs.map((r) => `<li>${r}</li>`).join("");

    // ---- Próximos passos ----
    $("#repPassos").innerHTML = [
      "Validar este diagnóstico com a diretoria e alinhar prioridades.",
      "Aprovar orçamento e metas (leads, conversão, faturamento).",
      "Iniciar o roadmap de 90 dias descrito abaixo.",
    ].map((p, i) => `<li>${p}</li>`).join("");

    // ---- Roadmaps ----
    $("#rm90").innerHTML = [
      ["Mês 1 — Fundamentos", "Posicionamento por segmento, identidade de marca, CRM e funil comercial básico."],
      ["Mês 2 — Presença & conteúdo", "Site/landing pages, perfis ativos (LinkedIn/Instagram), calendário editorial técnico."],
      ["Mês 3 — Geração de demanda", "Campanhas de mídia paga, automação de leads e primeiros relatórios de performance."],
    ].map(([t, d]) => `<div class="rmstep"><b>${t}</b>${d}</div>`).join("");

    $("#rm12").innerHTML = [
      ["Trim. 1 — Estruturar", "Bases de marketing e comercial operando com métricas mensais."],
      ["Trim. 2 — Escalar", "Otimização de campanhas, expansão de canais e ampliação de leads qualificados."],
      ["Trim. 3 — Rentabilizar", "Foco nos serviços de maior potencial e aumento da taxa de conversão."],
      ["Trim. 4 — Consolidar", "Marca de autoridade, previsibilidade comercial e cultura de dados consolidadas."],
    ].map(([t, d]) => `<div class="rmstep"><b>${t}</b>${d}</div>`).join("");

    // Pilares no rodapé do relatório
    $("#repPilares").innerHTML = Object.entries(pilares).map(([n, v]) => `
      <div class="pillar">
        <span class="pillar__name">${n}</span>
        <span class="pillar__track"><span class="pillar__fill" style="width:${v}%"></span></span>
        <span class="pillar__val">${v}</span>
      </div>`).join("");
  }

  function arrTem(arr, val) { return Array.isArray(arr) ? arr.includes(val) : arr === val; }
  function arrEach(arr, fn) { (Array.isArray(arr) ? arr : (arr ? [arr] : [])).forEach(fn); }

  init();
})();

/* ============================================================
   6. DEMO DO HERO (index.html) — barras de pilar ilustrativas
   ============================================================ */
(function heroDemo() {
  const wrap = $("#heroGauge");
  if (!wrap) return;
  drawGauge(wrap, 58, { size: 150, fill: "#D8B86A", track: "rgba(255,255,255,.14)" });
})();
