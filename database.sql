-- ============================================================
-- MC ASSOCIADOS — Estrutura de banco de dados (Supabase / PostgreSQL)
-- Tabela: diagnostico_mc_associados
-- Execute este script no SQL Editor do Supabase.
-- ============================================================

create extension if not exists "pgcrypto";   -- gera UUIDs

create table if not exists public.diagnostico_mc_associados (
  id                              uuid primary key default gen_random_uuid(),
  data_resposta                   timestamptz not null default now(),

  -- Identificação
  nome_respondente                text,
  cargo                           text,

  -- 1. Posicionamento estratégico
  missao                          text,
  visao_3_5_anos                  text,
  reconhecimento_mercado          text,
  diferenciais_competitivos       text,

  -- 2. Portfólio de serviços (múltipla escolha)
  servicos_oferecidos             text[],
  servicos_rentaveis              text[],
  servicos_crescimento            text[],
  servicos_prioridade_marketing   text[],

  -- 3. Clientes e mercado
  quantidade_clientes             text,
  segmentos_clientes              text,
  cliente_ideal                   text,
  dores_clientes                  text,
  segmentos_desejados             text,

  -- 4. Processo comercial
  origem_clientes                 text[],
  processo_comercial              text,         -- Sim | Parcialmente | Não
  funil_vendas                    text,         -- Sim | Não
  novos_clientes_mes              text,
  taxa_conversao                  text,

  -- 5. Marketing e presença digital
  canais_digitais                 text[],
  planejamento_marketing          text,         -- Sim | Parcialmente | Não
  nota_presenca_digital           text,         -- escala 0–10
  resultados_mensuraveis          text,         -- Sim | Parcialmente | Não
  desafios_marketing              text,

  -- 6. Tecnologia e inovação
  nota_maturidade_digital         text,         -- escala 0–10
  usa_ia_automacao                text,         -- Sim | Parcialmente | Não
  processos_automatizar           text,

  -- 7. Objetivos estratégicos
  prioridades_12_meses            text[],
  resultados_sucesso              text,
  riscos_crescimento              text[],

  -- 8. Expectativas da diretoria
  expectativas_diretoria          text,
  indicadores_mensais             text,
  iniciativas_futuras             text
);

-- Índice para ordenação por data (consultas do dashboard/relatório)
create index if not exists idx_diag_data on public.diagnostico_mc_associados (data_resposta desc);

-- ============================================================
-- Row Level Security (RLS)
-- Para um diagnóstico interno simples, liberamos insert/select com a chave
-- anônima. Em produção, restrinja conforme a política da empresa.
-- ============================================================
alter table public.diagnostico_mc_associados enable row level security;

create policy "permitir_insert_anon"
  on public.diagnostico_mc_associados
  for insert to anon
  with check (true);

create policy "permitir_select_anon"
  on public.diagnostico_mc_associados
  for select to anon
  using (true);

-- (Opcional) permitir exclusão pela chave anônima:
-- create policy "permitir_delete_anon"
--   on public.diagnostico_mc_associados
--   for delete to anon using (true);
