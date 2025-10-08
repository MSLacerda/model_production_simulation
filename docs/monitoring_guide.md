# Guia rápido de monitoramento de modelos
Ferramenta educacional para apoiar aulas sobre operação de modelos de machine learning em produção.

## Técnicas de monitoramento

### Detecção de Drift de Dados
**Objetivo:** Identificar mudanças na distribuição das variáveis de entrada antes que impactem o modelo.
Compara a distribuição dos dados de produção com uma referência (treinamento ou período estável) para descobrir se o modelo está recebendo exemplos diferentes do esperado.

**Sinais acompanhados:**
- Estatísticas agregadas das features
- Divergências de distribuição (PSI, KL, JS)
- Resultados de testes estatísticos (KS, Chi-quadrado)

**Algoritmos ou testes relevantes:**
- Population Stability Index (PSI) — Mede o deslocamento entre distribuições categorizadas usando bins fixos. (Uso indicado: Monitoramento recorrente com tolerância a ruídos e fácil interpretação por time de negócios.)
- Teste de Kolmogorov-Smirnov — Testa diferença entre distribuições contínuas considerando a maior distância entre CDFs. (Uso indicado: Features numéricas com histórico moderado de observações por janela.)
- Chi-quadrado — Compara frequências esperadas e observadas em variáveis categóricas. (Uso indicado: Features categóricas com cardinalidade baixa a moderada.)

**Boas práticas operacionais:**
- Definir janelas temporais alinhadas com o ritmo do negócio (diário, semanal, etc.)
- Armazenar os resultados para visualizar tendências e não apenas alertas isolados
- Usar múltiplas métricas para capturar diferentes tipos de desvios

**Problemas relacionados:** Drift de dados, Data quality

### Detecção de Drift de Conceito
**Objetivo:** Descobrir mudanças na relação entre features e target que degradam a performance.
Observa o desempenho do modelo ou distribuições condicionais para sinalizar quando o conceito previsto mudou. Normalmente exige feedback rotulado ou proxies de performance.

**Sinais acompanhados:**
- Métricas de performance ao longo do tempo
- Distribuição das previsões versus valores reais ou proxies
- Erros residuais agregados

**Algoritmos ou testes relevantes:**
- Drift Detection Method (DDM) — Monitora a taxa de erro e sua variância para identificar drifts súbitos. (Uso indicado: Classificação online com feedback frequente e rápido.)
- ADaptive WINdowing (ADWIN) — Mantém janelas dinâmicas e aplica testes de mudança na média para detectar drifts graduais. (Uso indicado: Fluxos contínuos de dados com necessidade de adaptação automática.)
- Teste de hipótese em métricas de performance — Aplica testes estatísticos (t-test, bootstrap) nas métricas para identificar quedas significativas. (Uso indicado: Cenários batch com ciclos de avaliação periódica e dados rotulados atrasados.)

**Boas práticas operacionais:**
- Planejar mecanismos de coleta de rótulos (humano ou automatizado)
- Utilizar métricas proxy quando rótulos forem caros (ex.: taxa de reclamação)
- Documentar estratégias de fallback caso o drift seja confirmado

**Problemas relacionados:** Drift de conceito, Modelo defasado

### Monitoramento de Performance
**Objetivo:** Acompanhar continuamente métricas de negócio e modelo para garantir aderência a SLAs.
Centraliza métricas como acurácia, ROC-AUC, precisão operacional e indicadores de custo/receita para detectar deteriorações relevantes.

**Sinais acompanhados:**
- Métricas de performance clássicas (acurácia, RMSE, F1)
- Indicadores de negócio (NPS, aprovação de crédito, ROI)
- SLA de latência e throughput

**Algoritmos ou testes relevantes:**
- Controle Estatístico de Processo (Shewhart, CUSUM) — Define limites superiores/inferiores e detecta variações fora de controle. (Uso indicado: Monitorar métricas contínuas com histórico suficiente para estimar limites.)
- Bootstrapping de métricas — Reamostra os dados para criar intervalos de confiança para as métricas monitoradas. (Uso indicado: Quando as distribuições das métricas são desconhecidas ou assimétricas.)

**Boas práticas operacionais:**
- Alinhar as métricas com stakeholders de negócio e tecnologia
- Definir limiares de alerta diferentes de limites de ação
- Registrar incidentes e aprendizados para calibrar limites futuros

**Problemas relacionados:** Degradação de performance, SLA violado

### Monitoramento de Qualidade de Dados
**Objetivo:** Garantir que os dados ingeridos atendam padrões de completude, consistência e validade.
Aplica regras automáticas ou modelos de detecção de anomalia em features, integridade de schemas, faixas válidas, valores nulos e consistência entre sistemas.

**Sinais acompanhados:**
- Percentual de valores faltantes
- Faixas e limites (mínimo, máximo, média)
- Relacionamentos e chaves entre tabelas

**Algoritmos ou testes relevantes:**
- Regras declarativas (Great Expectations, Deequ) — Permitem definir expectativas sobre estatísticas e valida-las automaticamente. (Uso indicado: Pipeline batch ou streaming com regras bem definidas e audíveis.)
- Isolation Forest — Detecta outliers ao isolar observações em árvores aleatórias. (Uso indicado: Features contínuas com anomalias raras que fogem das regras tradicionais.)
- Autoencoders — Modelos não supervisionados que aprendem representação e apontam reconstruções ruins como anomalias. (Uso indicado: Datasets de alta dimensionalidade com correlações complexas entre features.)

**Boas práticas operacionais:**
- Integrar validações na esteira de dados para bloquear pipelines quebrados
- Criar dashboards que mostrem histórico e sazonalidade dos indicadores
- Combinar regras de negócio com métodos estatísticos para maior robustez

**Problemas relacionados:** Data quality, Pipeline quebrado

### Monitoramento de Fairness e Bias
**Objetivo:** Identificar disparidades de tratamento entre grupos sensíveis e garantir conformidade ética.
Analisa métricas de equidade, taxas de aprovação/rejeição e impactos diferenciados para cada grupo protegido, com alertas quando limites são violados.

**Sinais acompanhados:**
- Disparidade de impacto (impact ratio)
- Diferença de taxas de aprovação/rejeição
- Métricas de igualdade de oportunidade ou odds

**Algoritmos ou testes relevantes:**
- Demographic Parity — Compara a taxa de decisões positivas entre grupos. (Uso indicado: Quando a política exige proporcionalidade independente do outcome.)
- Equalized Odds — Analisa taxa de verdadeiros positivos e falsos positivos por grupo. (Uso indicado: Aplicações com necessidade de equilíbrio em erros do tipo I e II.)
- Threshold Moving ou Reweighting — Ajusta limiares ou pesos para reduzir disparidades detectadas. (Uso indicado: Mitigação rápida enquanto soluções estruturais são implementadas.)

**Boas práticas operacionais:**
- Definir limites e políticas em conjunto com jurídico e compliance
- Monitorar a evolução após qualquer ajuste ou re-treinamento
- Registrar as justificativas das decisões em relatórios de governança

**Problemas relacionados:** Viés algorítmico, Problemas regulatórios


## Problemas recorrentes em produção

### Drift de dados
**Sintomas:**
- Queda gradual na performance sem mudanças no código
- Features com distribuições diferentes das observadas no treinamento
- Alertas frequentes de outliers em variáveis chave

**Causas comuns:**
- Mudança de comportamento dos usuários
- Atualização em sistemas upstream
- Entrada de novos segmentos ou produtos

**Como detectar:**
- PSI ou JS divergence acima de limites
- Testes estatísticos com p-valor abaixo do limiar
- Modelos de detecção de anomalias nas features

**Ações de mitigação:**
- Rever a amostra de treinamento e considerar re-treinamento
- Criar modelos especializados por segmento
- Implementar filtros ou transformações adicionais nas features

### Drift de conceito
**Sintomas:**
- Queda brusca de métricas de performance
- Feedback humano indicando previsões inconsistentes
- Incremento de reclamações de clientes

**Causas comuns:**
- Mudança na dinâmica do mercado
- Alteração nas políticas internas de decisão
- Mudanças externas (regulação, pandemia)

**Como detectar:**
- Monitoramento de métricas com controle estatístico
- Testes de mudança em taxas de erro (DDM, ADWIN)
- Comparação de distribuições condicionais

**Ações de mitigação:**
- Re-treinar ou ajustar hiperparâmetros
- Criar modelos adaptativos ou ensemble com pesos dinâmicos
- Rever features e incluir novas variáveis contextuais

### Data quality
**Sintomas:**
- Valores faltantes acima do normal
- Mudança inesperada em estatísticas básicas
- Falhas em validações de schema

**Causas comuns:**
- Pipelines upstream instáveis
- Falhas de integração entre sistemas
- Erro humano em cadastros ou ETLs

**Como detectar:**
- Regras de qualidade automatizadas
- Dashboards com limites aceitáveis
- Alarmes de anomalia em features críticas

**Ações de mitigação:**
- Acionar times responsáveis pelos dados
- Criar processos de backfill ou correção
- Introduzir validações obrigatórias antes da inferência

### Modelo defasado
**Sintomas:**
- Métricas de negócio não batendo com projeções
- Comparação com modelos de benchmark mostra perda
- Equipe operacional relata decisões desatualizadas

**Causas comuns:**
- Modelo treinado com dados antigos
- Falta de agilidade no ciclo de re-treinamento
- Mudanças sazonais não capturadas

**Como detectar:**
- Monitoramento de performance com limites temporais
- Comparações A/B com versões atualizadas
- Avaliação offline periódica

**Ações de mitigação:**
- Planejar calendário de re-treinamento
- Automatizar pipelines de dados e validação
- Adotar arquitetura champion/challenger

### Viés algorítmico
**Sintomas:**
- Diferença significativa em taxas de aprovação entre grupos
- Incidência desproporcional de falsos positivos/negativos
- Alertas de compliance ou auditoria

**Causas comuns:**
- Dados históricos enviesados
- Proxy de variáveis sensíveis
- Configuração de limiares sem análise de equidade

**Como detectar:**
- Cálculo periódico de métricas de fairness
- Dashboards segmentados por atributos sensíveis
- Testes contrafactuais

**Ações de mitigação:**
- Ajustar limiares ou reponderar amostras
- Coletar dados adicionais para grupos sub-representados
- Aplicar técnicas de pós-processamento para equalizar erros


## Casos de uso

### Concessão de crédito
Instituição financeira avaliando risco de crédito para novos clientes.

**Riscos de produção:**
- Drift de dados devido a novos segmentos
- Aumento de inadimplência sem detecção
- Pressão regulatória sobre fairness

**Foco de monitoramento:**
- PSI por feature relevante
- Taxa de aprovação e inadimplência por grupo
- Acompanhamento de F1 e AUC semanal

**KPIs recomendados:**
- Taxa de default
- Tempo médio de decisão
- Impact ratio entre grupos sensíveis

### Detecção de fraude
Empresa de pagamentos analisando transações em tempo real.

**Riscos de produção:**
- Ataques coordenados gerando drifts súbitos
- Latência elevada comprometendo a experiência
- Atualização frequente de padrões de fraude

**Foco de monitoramento:**
- Taxa de falsos positivos e falsos negativos
- Latência de inferência e throughput
- Alertas de ADWIN ou DDM em taxa de erro

**KPIs recomendados:**
- Custo evitado por bloqueio
- Tempo de resposta por decisão
- Taxa de investigação manual

### Manutenção preditiva
Indústria monitorando sensores para prever falhas em equipamentos.

**Riscos de produção:**
- Sensores descalibrados gerando dados inválidos
- Mudança na operação com novos regimes
- Feedback rótulo atrasado

**Foco de monitoramento:**
- Integridade de dados de sensores
- Monitoramento de drift em variáveis de condição
- Avaliação pós-falha com controle estatístico

**KPIs recomendados:**
- Tempo médio entre falhas
- Taxa de falsos alarmes
- Disponibilidade dos equipamentos

### Recomendação de conteúdo
Plataforma digital sugerindo conteúdos personalizados.

**Riscos de produção:**
- Mudanças de comportamento de usuários
- Conteúdos novos sem histórico
- Efeito bolha ou viés em recomendações

**Foco de monitoramento:**
- Diversidade e novidade das recomendações
- Engajamento (CTR, tempo de sessão)
- Fairness para criadores ou grupos específicos

**KPIs recomendados:**
- Click-through rate
- Tempo médio de consumo
- Distribuição de exposição por criador

### Previsão de demanda
Varejista prevendo vendas para otimizar estoque e logística.

**Riscos de produção:**
- Sazonalidade extrema e eventos inesperados
- Dados de estoque incorretos ou atrasados
- Mudanças externas (clima, economia)

**Foco de monitoramento:**
- Erros de previsão por SKU e região
- Drift em variáveis macroeconômicas
- Integridade de dados de vendas

**KPIs recomendados:**
- WAPE (Weighted Absolute Percentage Error)
- Cobertura de estoque
- Custo de ruptura

