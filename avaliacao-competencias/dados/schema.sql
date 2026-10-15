-- =============================================================================
-- Avaliação por competências · modelo de dados R2 Tech Consultoria
-- PostgreSQL 14+ (compatível com Supabase). Versão 1 · 13/10/2026
--
-- Multiempresa: toda tabela de cliente tem empresa_id. Linhas com empresa_id NULL
-- em competencia, indicador e politica_avaliacao são a biblioteca padrão da R2 Tech,
-- visível para todas as empresas.
--
-- Usuário logado: a função app.usuario_atual() lê current_setting('app.usuario_id').
-- No Supabase, troque o corpo dela por `select auth.uid()`.
-- =============================================================================

create schema if not exists app;

create or replace function app.usuario_atual() returns uuid
language sql stable as $$
  select nullif(current_setting('app.usuario_id', true), '')::uuid
$$;

-- ----------------------------------------------------------------------------- tipos
create type app.papel_membro      as enum ('admin', 'avaliador', 'colaborador');
create type app.tipo_vinculo      as enum ('clt', 'estagio', 'pj', 'socio', 'outro', 'nao_informado');
create type app.tipo_competencia  as enum ('comportamental', 'tecnica', 'lideranca');
create type app.tipo_indicador    as enum ('faltas_injustificadas', 'atrasos', 'percentual');
create type app.periodicidade     as enum ('semestral', 'anual', 'trimestral');
create type app.tipo_ciclo        as enum ('piloto', 'regular');
create type app.status_ciclo      as enum ('planejado', 'aberto', 'em_avaliacao', 'fechado');
create type app.status_avaliacao  as enum ('nao_iniciada', 'autoavaliacao', 'avaliacao_gestor', 'conversa', 'fechada');
create type app.status_pdi        as enum ('nao_iniciada', 'em_andamento', 'concluida');
create type app.participacao      as enum ('sim', 'nao', 'a_definir');
create type app.status_apuracao   as enum ('aberta', 'fechada', 'paga');

-- ----------------------------------------------------------------------------- acesso
create table app.usuario (
  id          uuid primary key default gen_random_uuid(),
  email       text not null unique,
  nome        text not null,
  criado_em   timestamptz not null default now()
);

create table app.empresa (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  cnpj        text,                       -- opcional
  ramo        text,                       -- ex.: contabilidade, advocacia
  criado_em   timestamptz not null default now()
);

-- Quem entra no site e com qual papel em cada empresa
create table app.membro_empresa (
  empresa_id  uuid not null references app.empresa(id) on delete cascade,
  usuario_id  uuid not null references app.usuario(id) on delete cascade,
  papel       app.papel_membro not null,
  primary key (empresa_id, usuario_id)
);

-- ----------------------------------------------------------------------------- organograma
create table app.area (
  id           uuid primary key default gen_random_uuid(),
  empresa_id   uuid not null references app.empresa(id) on delete cascade,
  nome         text not null,
  area_pai_id  uuid references app.area(id),
  ordem        int not null default 0,
  unique (empresa_id, nome)
);

create table app.cargo (
  id                 uuid primary key default gen_random_uuid(),
  empresa_id         uuid not null references app.empresa(id) on delete cascade,
  area_id            uuid references app.area(id),
  nome               text not null,
  missao             text,
  responsabilidades  text,
  ativo              boolean not null default true,
  unique (empresa_id, nome)
);

-- Funcionário (não precisa ter login). Sem CPF, salário ou dados de saúde.
create table app.pessoa (
  id           uuid primary key default gen_random_uuid(),
  empresa_id   uuid not null references app.empresa(id) on delete cascade,
  usuario_id   uuid references app.usuario(id),   -- preenchido quando a pessoa ganha login
  nome         text not null,
  email        text,
  ativo        boolean not null default true,
  observacoes  text
);

-- Ocupação de cargo e subordinação, com histórico. Organograma = vínculos sem data_fim.
create table app.vinculo (
  id                uuid primary key default gen_random_uuid(),
  empresa_id        uuid not null references app.empresa(id) on delete cascade,
  pessoa_id         uuid not null references app.pessoa(id) on delete cascade,
  cargo_id          uuid not null references app.cargo(id),
  gestor_pessoa_id  uuid references app.pessoa(id),
  tipo              app.tipo_vinculo not null default 'nao_informado',
  jornada           text,                   -- ex.: "dois dias por semana"
  data_inicio       date,
  data_fim          date,
  check (gestor_pessoa_id is distinct from pessoa_id),
  check (data_fim is null or data_inicio is null or data_fim >= data_inicio)
);
create unique index vinculo_um_ativo_por_pessoa on app.vinculo (pessoa_id) where data_fim is null;

-- ----------------------------------------------------------------------------- competências e indicadores
create table app.competencia (
  id                   uuid primary key default gen_random_uuid(),
  empresa_id           uuid references app.empresa(id) on delete cascade,  -- NULL = biblioteca R2 Tech
  tipo                 app.tipo_competencia not null,
  area_biblioteca      text,             -- área da biblioteca (técnicas), ex.: "Fiscal"
  codigo               text,             -- C1..C8, L1..L5; técnicas recebem código no cargo
  nome                 text not null,
  definicao            text,
  nivel_1              text,
  nivel_3              text not null,    -- para técnicas: "o que é atender"
  nivel_5              text,
  evidencia_sugerida   text,
  origem               text,             -- de onde veio (ex.: "Briefing, seção 10")
  ativo                boolean not null default true
);

-- Competências técnicas de cada cargo (as comportamentais valem para todos os cargos)
create table app.cargo_competencia (
  cargo_id        uuid not null references app.cargo(id) on delete cascade,
  competencia_id  uuid not null references app.competencia(id),
  codigo          text not null,         -- T1..T6
  ordem           int not null default 0,
  texto_atender   text,                  -- ajuste ao processo do cliente; NULL usa competencia.nivel_3
  evidencia       text,
  primary key (cargo_id, competencia_id),
  unique (cargo_id, codigo)
);

create table app.indicador (
  id                 uuid primary key default gen_random_uuid(),
  empresa_id         uuid references app.empresa(id) on delete cascade,  -- NULL = padrão R2 Tech
  tipo               app.tipo_indicador not null,
  nome               text not null,
  fonte              text,
  tabela_conversao   jsonb   -- opcional; NULL usa a tabela da política. [{"a_partir_de":0,"nota":5}, ...]
);

-- Indicadores de resultado de cada cargo (faltas e atrasos valem para todos)
create table app.cargo_indicador (
  cargo_id      uuid not null references app.cargo(id) on delete cascade,
  indicador_id  uuid not null references app.indicador(id),
  ordem         int not null default 0,
  primary key (cargo_id, indicador_id)
);

-- ----------------------------------------------------------------------------- regras
create table app.politica_avaliacao (
  id                     uuid primary key default gen_random_uuid(),
  empresa_id             uuid references app.empresa(id) on delete cascade,  -- NULL = padrão R2 Tech
  nome                   text not null,
  peso_comportamental    numeric(4,3) not null,
  peso_tecnico           numeric(4,3) not null,
  peso_indicadores       numeric(4,3) not null,
  conversao_faltas       jsonb not null,  -- [{"a_partir_de":0,"nota":5},{"a_partir_de":1,"nota":4},...]
  conversao_atrasos      jsonb not null,
  conversao_percentual   jsonb not null,  -- a_partir_de em fração (0.95 = 95%)
  faixas_gratificacao    jsonb not null,  -- [{"a_partir_de":3.5,"percentual":1.0,"faixa":"Atende"}, ...]
  periodicidade          app.periodicidade not null default 'semestral',
  atestado_reduz_nota    boolean not null default false,
  validada_em            date,            -- NULL = proposta ainda não validada pela direção
  check (peso_comportamental + peso_tecnico + peso_indicadores = 1)
);

-- ----------------------------------------------------------------------------- ciclos e avaliações
create table app.ciclo_avaliacao (
  id                  uuid primary key default gen_random_uuid(),
  empresa_id          uuid not null references app.empresa(id) on delete cascade,
  politica_id         uuid not null references app.politica_avaliacao(id),
  nome                text not null,
  tipo                app.tipo_ciclo not null default 'regular',
  data_inicio         date not null,
  data_fim            date not null,
  status              app.status_ciclo not null default 'planejado',
  efeito_financeiro   boolean not null default true,
  check (data_fim >= data_inicio)
);

create table app.avaliacao (
  id                       uuid primary key default gen_random_uuid(),
  empresa_id               uuid not null references app.empresa(id) on delete cascade,
  ciclo_id                 uuid not null references app.ciclo_avaliacao(id) on delete cascade,
  pessoa_id                uuid not null references app.pessoa(id),
  cargo_id                 uuid not null references app.cargo(id),       -- cargo no ciclo (fica no histórico)
  avaliador_pessoa_id      uuid references app.pessoa(id),
  status                   app.status_avaliacao not null default 'nao_iniciada',
  inclui_trilha_lideranca  boolean not null default false,
  data_conversa            date,
  comentario_geral         text,
  -- notas gravadas no fechamento (antes disso, usar a view app.v_avaliacao_notas)
  nota_comportamental      numeric(3,2),
  nota_tecnica             numeric(3,2),
  nota_indicadores         numeric(3,2),
  nota_final               numeric(3,2),
  unique (ciclo_id, pessoa_id)
);

create table app.avaliacao_item (
  avaliacao_id    uuid not null references app.avaliacao(id) on delete cascade,
  competencia_id  uuid not null references app.competencia(id),
  nota_auto       smallint check (nota_auto between 1 and 5),
  nota_gestor     smallint check (nota_gestor between 1 and 5),
  nota_final      smallint check (nota_final between 1 and 5),   -- acordada na conversa
  evidencias      text,
  primary key (avaliacao_id, competencia_id)
);

create table app.avaliacao_indicador (
  avaliacao_id  uuid not null references app.avaliacao(id) on delete cascade,
  indicador_id  uuid not null references app.indicador(id),
  valor         numeric,          -- contagem (faltas, atrasos) ou fração (0.96)
  observacao    text,
  primary key (avaliacao_id, indicador_id)
);

-- Contagens mensais. Não guardar atestado, CID ou motivo de saúde: só a quantidade.
create table app.registro_assiduidade (
  id                     uuid primary key default gen_random_uuid(),
  empresa_id             uuid not null references app.empresa(id) on delete cascade,
  pessoa_id              uuid not null references app.pessoa(id) on delete cascade,
  mes                    date not null check (extract(day from mes) = 1),
  faltas_injustificadas  int not null default 0 check (faltas_injustificadas >= 0),
  atrasos                int not null default 0 check (atrasos >= 0),
  faltas_justificadas    int not null default 0 check (faltas_justificadas >= 0),
  observacao             text,
  unique (pessoa_id, mes)
);

create table app.pdi_acao (
  id              uuid primary key default gen_random_uuid(),
  avaliacao_id    uuid not null references app.avaliacao(id) on delete cascade,
  competencia_id  uuid references app.competencia(id),
  acao            text not null,
  apoio_empresa   text,
  prazo           date,
  status          app.status_pdi not null default 'nao_iniciada',
  comentario      text
);

-- ----------------------------------------------------------------------------- gratificação
create table app.gratificacao_apuracao (
  id              uuid primary key default gen_random_uuid(),
  empresa_id      uuid not null references app.empresa(id) on delete cascade,
  ano             int not null,
  reserva_mensal  numeric(12,2),
  meses_reserva   int not null default 12,
  fundo           numeric(12,2) generated always as (reserva_mensal * meses_reserva) stored,
  status          app.status_apuracao not null default 'aberta',
  unique (empresa_id, ano)
);

create table app.gratificacao_item (
  apuracao_id       uuid not null references app.gratificacao_apuracao(id) on delete cascade,
  pessoa_id         uuid not null references app.pessoa(id),
  participa         app.participacao not null default 'a_definir',
  valor_referencia  numeric(12,2),
  nota_ano          numeric(3,2),
  percentual        numeric(4,3),
  valor_calculado   numeric(12,2),
  valor_ajustado    numeric(12,2),     -- após limitar ao fundo
  primary key (apuracao_id, pessoa_id)
);

-- ----------------------------------------------------------------------------- regras de cálculo
-- Converte um valor em nota pela tabela [{"a_partir_de":x,"nota":n}] (mesma lógica do LOOKUP da planilha)
create or replace function app.nota_por_faixa(valor numeric, tabela jsonb) returns smallint
language sql immutable as $$
  select (x->>'nota')::smallint
  from jsonb_array_elements(tabela) x
  where valor is not null and (x->>'a_partir_de')::numeric <= valor
  order by (x->>'a_partir_de')::numeric desc
  limit 1
$$;

-- Organograma compartilhado com a equipe
create view app.v_organograma with (security_invoker = true) as
select v.empresa_id, p.id as pessoa_id, p.nome as pessoa, c.nome as cargo, a.nome as area,
       g.id as gestor_id, g.nome as gestor, v.tipo, v.jornada
from app.vinculo v
join app.pessoa p on p.id = v.pessoa_id
join app.cargo c on c.id = v.cargo_id
left join app.area a on a.id = c.area_id
left join app.pessoa g on g.id = v.gestor_pessoa_id
where v.data_fim is null and p.ativo;

-- Soma da assiduidade de cada pessoa no período do ciclo
create view app.v_assiduidade_ciclo with (security_invoker = true) as
select av.id as avaliacao_id,
       coalesce(sum(r.faltas_injustificadas), 0) as faltas_injustificadas,
       coalesce(sum(r.atrasos), 0) as atrasos,
       coalesce(sum(r.faltas_justificadas), 0) as faltas_justificadas
from app.avaliacao av
join app.ciclo_avaliacao ci on ci.id = av.ciclo_id
left join app.registro_assiduidade r
       on r.pessoa_id = av.pessoa_id and r.mes between date_trunc('month', ci.data_inicio) and ci.data_fim
group by av.id;

-- Notas calculadas (mesma regra da planilha): nota considerada = final acordada, senão a do gestor;
-- média por bloco; faltas e atrasos vêm da assiduidade; nota final só quando os três blocos existem.
create view app.v_avaliacao_notas with (security_invoker = true) as
with itens as (
  select ai.avaliacao_id, c.tipo, coalesce(ai.nota_final, ai.nota_gestor) as nota
  from app.avaliacao_item ai join app.competencia c on c.id = ai.competencia_id
),
blocos as (
  select avaliacao_id,
         round(avg(nota) filter (where tipo = 'comportamental'), 2) as comportamental,
         round(avg(nota) filter (where tipo = 'tecnica'), 2) as tecnica,
         round(avg(nota) filter (where tipo = 'lideranca'), 2) as lideranca_fora_da_nota
  from itens group by avaliacao_id
),
ind as (
  select av.id as avaliacao_id, app.nota_por_faixa(asd.faltas_injustificadas, po.conversao_faltas) as nota
  from app.avaliacao av join app.ciclo_avaliacao ci on ci.id = av.ciclo_id
  join app.politica_avaliacao po on po.id = ci.politica_id
  join app.v_assiduidade_ciclo asd on asd.avaliacao_id = av.id
  union all
  select av.id, app.nota_por_faixa(asd.atrasos, po.conversao_atrasos)
  from app.avaliacao av join app.ciclo_avaliacao ci on ci.id = av.ciclo_id
  join app.politica_avaliacao po on po.id = ci.politica_id
  join app.v_assiduidade_ciclo asd on asd.avaliacao_id = av.id
  union all
  select aind.avaliacao_id, app.nota_por_faixa(aind.valor, coalesce(i.tabela_conversao, po.conversao_percentual))
  from app.avaliacao_indicador aind
  join app.indicador i on i.id = aind.indicador_id and i.tipo = 'percentual'
  join app.avaliacao av on av.id = aind.avaliacao_id
  join app.ciclo_avaliacao ci on ci.id = av.ciclo_id
  join app.politica_avaliacao po on po.id = ci.politica_id
),
ind_media as (
  select avaliacao_id, round(avg(nota), 2) as indicadores from ind group by avaliacao_id
)
select av.id as avaliacao_id, av.empresa_id, av.ciclo_id, av.pessoa_id,
       b.comportamental, b.tecnica, im.indicadores, b.lideranca_fora_da_nota,
       round(b.comportamental * po.peso_comportamental + b.tecnica * po.peso_tecnico
             + im.indicadores * po.peso_indicadores, 2) as nota_final
from app.avaliacao av
join app.ciclo_avaliacao ci on ci.id = av.ciclo_id
join app.politica_avaliacao po on po.id = ci.politica_id
left join blocos b on b.avaliacao_id = av.id
left join ind_media im on im.avaliacao_id = av.id;

-- =============================================================================
-- Segurança por linha (RLS)
--   admin       : tudo da empresa
--   avaliador   : lê o organograma; lê e escreve as avaliações em que é avaliador
--   colaborador : lê o organograma; lê a própria avaliação, a própria assiduidade e o próprio PDI
-- A restrição de colunas (colaborador só grava nota_auto e evidencias) fica na API do site.
-- =============================================================================
create or replace function app.eh_membro(emp uuid) returns boolean
language sql stable security definer set search_path = app as $$
  select exists (select 1 from membro_empresa m where m.empresa_id = emp and m.usuario_id = usuario_atual())
$$;

create or replace function app.eh_admin(emp uuid) returns boolean
language sql stable security definer set search_path = app as $$
  select exists (select 1 from membro_empresa m
                 where m.empresa_id = emp and m.usuario_id = usuario_atual() and m.papel = 'admin')
$$;

-- pessoa ligada ao usuário logado nesta empresa
create or replace function app.minha_pessoa(emp uuid) returns uuid
language sql stable security definer set search_path = app as $$
  select p.id from pessoa p where p.empresa_id = emp and p.usuario_id = usuario_atual() limit 1
$$;

create or replace function app.pode_ver_avaliacao(av_id uuid) returns boolean
language sql stable security definer set search_path = app as $$
  select exists (select 1 from avaliacao a where a.id = av_id and (
           eh_admin(a.empresa_id)
           or a.avaliador_pessoa_id = minha_pessoa(a.empresa_id)
           or a.pessoa_id = minha_pessoa(a.empresa_id)))
$$;

alter table app.empresa               enable row level security;
alter table app.membro_empresa        enable row level security;
alter table app.area                  enable row level security;
alter table app.cargo                 enable row level security;
alter table app.pessoa                enable row level security;
alter table app.vinculo               enable row level security;
alter table app.competencia           enable row level security;
alter table app.cargo_competencia     enable row level security;
alter table app.indicador             enable row level security;
alter table app.cargo_indicador       enable row level security;
alter table app.politica_avaliacao    enable row level security;
alter table app.ciclo_avaliacao       enable row level security;
alter table app.avaliacao             enable row level security;
alter table app.avaliacao_item        enable row level security;
alter table app.avaliacao_indicador   enable row level security;
alter table app.registro_assiduidade  enable row level security;
alter table app.pdi_acao              enable row level security;
alter table app.gratificacao_apuracao enable row level security;
alter table app.gratificacao_item     enable row level security;

create policy empresa_ler on app.empresa for select using (app.eh_membro(id));
create policy empresa_admin on app.empresa for update using (app.eh_admin(id));
create policy membro_ler on app.membro_empresa for select using (app.eh_membro(empresa_id));
create policy membro_admin on app.membro_empresa for all using (app.eh_admin(empresa_id));

-- organograma: toda a equipe lê, só admin altera
create policy area_ler   on app.area    for select using (app.eh_membro(empresa_id));
create policy area_admin on app.area    for all    using (app.eh_admin(empresa_id));
create policy cargo_ler   on app.cargo  for select using (app.eh_membro(empresa_id));
create policy cargo_admin on app.cargo  for all    using (app.eh_admin(empresa_id));
create policy pessoa_ler   on app.pessoa for select using (app.eh_membro(empresa_id));
create policy pessoa_admin on app.pessoa for all    using (app.eh_admin(empresa_id));
create policy vinculo_ler   on app.vinculo for select using (app.eh_membro(empresa_id));
create policy vinculo_admin on app.vinculo for all    using (app.eh_admin(empresa_id));

-- biblioteca R2 Tech (empresa_id NULL) é visível a todos; as da empresa, aos membros
create policy competencia_ler on app.competencia for select using (empresa_id is null or app.eh_membro(empresa_id));
create policy competencia_admin on app.competencia for all using (app.eh_admin(empresa_id));
create policy indicador_ler on app.indicador for select using (empresa_id is null or app.eh_membro(empresa_id));
create policy indicador_admin on app.indicador for all using (app.eh_admin(empresa_id));
create policy politica_ler on app.politica_avaliacao for select using (empresa_id is null or app.eh_membro(empresa_id));
create policy politica_admin on app.politica_avaliacao for all using (app.eh_admin(empresa_id));
create policy cc_ler on app.cargo_competencia for select
  using (exists (select 1 from app.cargo c where c.id = cargo_id and app.eh_membro(c.empresa_id)));
create policy cc_admin on app.cargo_competencia for all
  using (exists (select 1 from app.cargo c where c.id = cargo_id and app.eh_admin(c.empresa_id)));
create policy ci_ler on app.cargo_indicador for select
  using (exists (select 1 from app.cargo c where c.id = cargo_id and app.eh_membro(c.empresa_id)));
create policy ci_admin on app.cargo_indicador for all
  using (exists (select 1 from app.cargo c where c.id = cargo_id and app.eh_admin(c.empresa_id)));

create policy ciclo_ler on app.ciclo_avaliacao for select using (app.eh_membro(empresa_id));
create policy ciclo_admin on app.ciclo_avaliacao for all using (app.eh_admin(empresa_id));

-- avaliações: admin, avaliador da pessoa e a própria pessoa
create policy avaliacao_ver on app.avaliacao for select using (app.pode_ver_avaliacao(id));
create policy avaliacao_admin on app.avaliacao for all using (app.eh_admin(empresa_id));
create policy avaliacao_avaliador on app.avaliacao for update
  using (avaliador_pessoa_id = app.minha_pessoa(empresa_id));
create policy item_ver on app.avaliacao_item for select using (app.pode_ver_avaliacao(avaliacao_id));
create policy item_escrever on app.avaliacao_item for all using (app.pode_ver_avaliacao(avaliacao_id));
create policy aind_ver on app.avaliacao_indicador for select using (app.pode_ver_avaliacao(avaliacao_id));
create policy aind_escrever on app.avaliacao_indicador for all using (
  exists (select 1 from app.avaliacao a where a.id = avaliacao_id and
          (app.eh_admin(a.empresa_id) or a.avaliador_pessoa_id = app.minha_pessoa(a.empresa_id))));
create policy pdi_ver on app.pdi_acao for select using (app.pode_ver_avaliacao(avaliacao_id));
create policy pdi_escrever on app.pdi_acao for all using (app.pode_ver_avaliacao(avaliacao_id));

-- assiduidade: admin; a própria pessoa só lê
create policy assid_admin on app.registro_assiduidade for all using (app.eh_admin(empresa_id));
create policy assid_propria on app.registro_assiduidade for select using (pessoa_id = app.minha_pessoa(empresa_id));

-- gratificação: só admin
create policy grat_admin on app.gratificacao_apuracao for all using (app.eh_admin(empresa_id));
create policy grat_item_admin on app.gratificacao_item for all using (
  exists (select 1 from app.gratificacao_apuracao g where g.id = apuracao_id and app.eh_admin(g.empresa_id)));
