/* ============================================================
   MC ASSOCIADOS — Camada de Dados (supabase.js)
   ------------------------------------------------------------
   Centraliza a leitura/gravação dos diagnósticos.
   Funciona em dois modos:
     1) SUPABASE  — se você preencher as credenciais abaixo.
     2) LOCAL     — fallback automático em localStorage do navegador,
                    útil para demonstração offline aos sócios.

   A API pública é a mesma nos dois modos:
     await MCData.salvar(registro)        -> grava um diagnóstico
     await MCData.listar()                -> retorna array (mais recente 1º)
     await MCData.remover(id)             -> apaga um registro
     MCData.modo                          -> 'supabase' | 'local'
   ============================================================ */

/* ---------- 1. CONFIGURAÇÃO DO SUPABASE ----------
   Substitua pelos dados do seu projeto (Project Settings → API).
   Enquanto estiverem vazios, o sistema usa o modo LOCAL. */
const SUPABASE_URL = "";            // ex.: "https://xxxxxxxx.supabase.co"
const SUPABASE_ANON_KEY = "";       // ex.: "eyJhbGciOi..."
const TABELA = "diagnostico_mc_associados";
const LS_KEY = "mc_diagnosticos_v1";

/* ---------- 2. Inicialização do cliente (carrega SDK só se preciso) ---------- */
let _client = null;
const _temSupabase = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);

async function _getClient() {
  if (_client) return _client;
  // Carrega o SDK do Supabase sob demanda via CDN.
  if (!window.supabase) {
    await new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2";
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }
  _client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  return _client;
}

/* ---------- 3. Helpers do modo LOCAL ---------- */
function _localLer() {
  try { return JSON.parse(localStorage.getItem(LS_KEY)) || []; }
  catch { return []; }
}
function _localGravar(lista) {
  localStorage.setItem(LS_KEY, JSON.stringify(lista));
}

/* ---------- 4. API pública ---------- */
const MCData = {
  modo: _temSupabase ? "supabase" : "local",

  /** Grava um diagnóstico e retorna o registro salvo. */
  async salvar(registro) {
    const payload = { ...registro, data_resposta: new Date().toISOString() };

    if (_temSupabase) {
      const sb = await _getClient();
      const { data, error } = await sb.from(TABELA).insert(payload).select().single();
      if (error) throw error;
      return data;
    }

    // Modo local
    const lista = _localLer();
    payload.id = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now());
    lista.push(payload);
    _localGravar(lista);
    return payload;
  },

  /** Retorna todos os diagnósticos, do mais recente para o mais antigo. */
  async listar() {
    if (_temSupabase) {
      const sb = await _getClient();
      const { data, error } = await sb.from(TABELA).select("*").order("data_resposta", { ascending: false });
      if (error) throw error;
      return data || [];
    }
    return _localLer().sort((a, b) => new Date(b.data_resposta) - new Date(a.data_resposta));
  },

  /** Remove um diagnóstico pelo id. */
  async remover(id) {
    if (_temSupabase) {
      const sb = await _getClient();
      const { error } = await sb.from(TABELA).delete().eq("id", id);
      if (error) throw error;
      return true;
    }
    _localGravar(_localLer().filter((r) => String(r.id) !== String(id)));
    return true;
  },
};

window.MCData = MCData;
