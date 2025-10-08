"""Structured knowledge base about monitoring ML models in production."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Algorithm:
    """Algorithm or statistical test applied in a monitoring technique."""

    name: str
    summary: str
    when_to_use: str


@dataclass(frozen=True)
class Technique:
    """Monitoring technique with practical information for practitioners."""

    name: str
    objective: str
    description: str
    monitoring_signals: List[str]
    algorithms: List[Algorithm]
    operational_tips: List[str]
    related_problems: List[str]


@dataclass(frozen=True)
class ProductionProblem:
    """Common issues faced by machine learning systems in production."""

    name: str
    symptoms: List[str]
    causes: List[str]
    detection_methods: List[str]
    mitigation_actions: List[str]


@dataclass(frozen=True)
class UseCase:
    """Representative scenario that benefits from robust monitoring."""

    name: str
    context: str
    risks: List[str]
    monitoring_focus: List[str]
    example_kpis: List[str]


MONITORING_TECHNIQUES: List[Technique] = [
    Technique(
        name="Detecção de Drift de Dados",
        objective="Identificar mudanças na distribuição das variáveis de entrada antes que impactem o modelo.",
        description=(
            "Compara a distribuição dos dados de produção com uma referência (treinamento ou período estável) "
            "para descobrir se o modelo está recebendo exemplos diferentes do esperado."
        ),
        monitoring_signals=[
            "Estatísticas agregadas das features",
            "Divergências de distribuição (PSI, KL, JS)",
            "Resultados de testes estatísticos (KS, Chi-quadrado)",
        ],
        algorithms=[
            Algorithm(
                name="Population Stability Index (PSI)",
                summary="Mede o deslocamento entre distribuições categorizadas usando bins fixos.",
                when_to_use="Monitoramento recorrente com tolerância a ruídos e fácil interpretação por time de negócios.",
            ),
            Algorithm(
                name="Teste de Kolmogorov-Smirnov",
                summary="Testa diferença entre distribuições contínuas considerando a maior distância entre CDFs.",
                when_to_use="Features numéricas com histórico moderado de observações por janela.",
            ),
            Algorithm(
                name="Chi-quadrado",
                summary="Compara frequências esperadas e observadas em variáveis categóricas.",
                when_to_use="Features categóricas com cardinalidade baixa a moderada.",
            ),
        ],
        operational_tips=[
            "Definir janelas temporais alinhadas com o ritmo do negócio (diário, semanal, etc.)",
            "Armazenar os resultados para visualizar tendências e não apenas alertas isolados",
            "Usar múltiplas métricas para capturar diferentes tipos de desvios",
        ],
        related_problems=["Drift de dados", "Data quality"],
    ),
    Technique(
        name="Detecção de Drift de Conceito",
        objective="Descobrir mudanças na relação entre features e target que degradam a performance.",
        description=(
            "Observa o desempenho do modelo ou distribuições condicionais para sinalizar quando o conceito "
            "previsto mudou. Normalmente exige feedback rotulado ou proxies de performance."
        ),
        monitoring_signals=[
            "Métricas de performance ao longo do tempo",
            "Distribuição das previsões versus valores reais ou proxies",
            "Erros residuais agregados",
        ],
        algorithms=[
            Algorithm(
                name="Drift Detection Method (DDM)",
                summary="Monitora a taxa de erro e sua variância para identificar drifts súbitos.",
                when_to_use="Classificação online com feedback frequente e rápido.",
            ),
            Algorithm(
                name="ADaptive WINdowing (ADWIN)",
                summary="Mantém janelas dinâmicas e aplica testes de mudança na média para detectar drifts graduais.",
                when_to_use="Fluxos contínuos de dados com necessidade de adaptação automática.",
            ),
            Algorithm(
                name="Teste de hipótese em métricas de performance",
                summary="Aplica testes estatísticos (t-test, bootstrap) nas métricas para identificar quedas significativas.",
                when_to_use="Cenários batch com ciclos de avaliação periódica e dados rotulados atrasados.",
            ),
        ],
        operational_tips=[
            "Planejar mecanismos de coleta de rótulos (humano ou automatizado)",
            "Utilizar métricas proxy quando rótulos forem caros (ex.: taxa de reclamação)",
            "Documentar estratégias de fallback caso o drift seja confirmado",
        ],
        related_problems=["Drift de conceito", "Modelo defasado"],
    ),
    Technique(
        name="Monitoramento de Performance",
        objective="Acompanhar continuamente métricas de negócio e modelo para garantir aderência a SLAs.",
        description=(
            "Centraliza métricas como acurácia, ROC-AUC, precisão operacional e indicadores de custo/receita "
            "para detectar deteriorações relevantes."
        ),
        monitoring_signals=[
            "Métricas de performance clássicas (acurácia, RMSE, F1)",
            "Indicadores de negócio (NPS, aprovação de crédito, ROI)",
            "SLA de latência e throughput",
        ],
        algorithms=[
            Algorithm(
                name="Controle Estatístico de Processo (Shewhart, CUSUM)",
                summary="Define limites superiores/inferiores e detecta variações fora de controle.",
                when_to_use="Monitorar métricas contínuas com histórico suficiente para estimar limites.",
            ),
            Algorithm(
                name="Bootstrapping de métricas",
                summary="Reamostra os dados para criar intervalos de confiança para as métricas monitoradas.",
                when_to_use="Quando as distribuições das métricas são desconhecidas ou assimétricas.",
            ),
        ],
        operational_tips=[
            "Alinhar as métricas com stakeholders de negócio e tecnologia",
            "Definir limiares de alerta diferentes de limites de ação",
            "Registrar incidentes e aprendizados para calibrar limites futuros",
        ],
        related_problems=["Degradação de performance", "SLA violado"],
    ),
    Technique(
        name="Monitoramento de Qualidade de Dados",
        objective="Garantir que os dados ingeridos atendam padrões de completude, consistência e validade.",
        description=(
            "Aplica regras automáticas ou modelos de detecção de anomalia em features, integridade de schemas, "
            "faixas válidas, valores nulos e consistência entre sistemas."
        ),
        monitoring_signals=[
            "Percentual de valores faltantes",
            "Faixas e limites (mínimo, máximo, média)",
            "Relacionamentos e chaves entre tabelas",
        ],
        algorithms=[
            Algorithm(
                name="Regras declarativas (Great Expectations, Deequ)",
                summary="Permitem definir expectativas sobre estatísticas e valida-las automaticamente.",
                when_to_use="Pipeline batch ou streaming com regras bem definidas e audíveis.",
            ),
            Algorithm(
                name="Isolation Forest",
                summary="Detecta outliers ao isolar observações em árvores aleatórias.",
                when_to_use="Features contínuas com anomalias raras que fogem das regras tradicionais.",
            ),
            Algorithm(
                name="Autoencoders",
                summary="Modelos não supervisionados que aprendem representação e apontam reconstruções ruins como anomalias.",
                when_to_use="Datasets de alta dimensionalidade com correlações complexas entre features.",
            ),
        ],
        operational_tips=[
            "Integrar validações na esteira de dados para bloquear pipelines quebrados",
            "Criar dashboards que mostrem histórico e sazonalidade dos indicadores",
            "Combinar regras de negócio com métodos estatísticos para maior robustez",
        ],
        related_problems=["Data quality", "Pipeline quebrado"],
    ),
    Technique(
        name="Monitoramento de Fairness e Bias",
        objective="Identificar disparidades de tratamento entre grupos sensíveis e garantir conformidade ética.",
        description=(
            "Analisa métricas de equidade, taxas de aprovação/rejeição e impactos diferenciados para cada grupo "
            "protegido, com alertas quando limites são violados."
        ),
        monitoring_signals=[
            "Disparidade de impacto (impact ratio)",
            "Diferença de taxas de aprovação/rejeição",
            "Métricas de igualdade de oportunidade ou odds",
        ],
        algorithms=[
            Algorithm(
                name="Demographic Parity",
                summary="Compara a taxa de decisões positivas entre grupos.",
                when_to_use="Quando a política exige proporcionalidade independente do outcome.",
            ),
            Algorithm(
                name="Equalized Odds",
                summary="Analisa taxa de verdadeiros positivos e falsos positivos por grupo.",
                when_to_use="Aplicações com necessidade de equilíbrio em erros do tipo I e II.",
            ),
            Algorithm(
                name="Threshold Moving ou Reweighting",
                summary="Ajusta limiares ou pesos para reduzir disparidades detectadas.",
                when_to_use="Mitigação rápida enquanto soluções estruturais são implementadas.",
            ),
        ],
        operational_tips=[
            "Definir limites e políticas em conjunto com jurídico e compliance",
            "Monitorar a evolução após qualquer ajuste ou re-treinamento",
            "Registrar as justificativas das decisões em relatórios de governança",
        ],
        related_problems=["Viés algorítmico", "Problemas regulatórios"],
    ),
]


PRODUCTION_PROBLEMS: List[ProductionProblem] = [
    ProductionProblem(
        name="Drift de dados",
        symptoms=[
            "Queda gradual na performance sem mudanças no código",
            "Features com distribuições diferentes das observadas no treinamento",
            "Alertas frequentes de outliers em variáveis chave",
        ],
        causes=[
            "Mudança de comportamento dos usuários",
            "Atualização em sistemas upstream",
            "Entrada de novos segmentos ou produtos",
        ],
        detection_methods=[
            "PSI ou JS divergence acima de limites",
            "Testes estatísticos com p-valor abaixo do limiar",
            "Modelos de detecção de anomalias nas features",
        ],
        mitigation_actions=[
            "Rever a amostra de treinamento e considerar re-treinamento",
            "Criar modelos especializados por segmento",
            "Implementar filtros ou transformações adicionais nas features",
        ],
    ),
    ProductionProblem(
        name="Drift de conceito",
        symptoms=[
            "Queda brusca de métricas de performance",
            "Feedback humano indicando previsões inconsistentes",
            "Incremento de reclamações de clientes",
        ],
        causes=[
            "Mudança na dinâmica do mercado",
            "Alteração nas políticas internas de decisão",
            "Mudanças externas (regulação, pandemia)",
        ],
        detection_methods=[
            "Monitoramento de métricas com controle estatístico",
            "Testes de mudança em taxas de erro (DDM, ADWIN)",
            "Comparação de distribuições condicionais",
        ],
        mitigation_actions=[
            "Re-treinar ou ajustar hiperparâmetros",
            "Criar modelos adaptativos ou ensemble com pesos dinâmicos",
            "Rever features e incluir novas variáveis contextuais",
        ],
    ),
    ProductionProblem(
        name="Data quality",
        symptoms=[
            "Valores faltantes acima do normal",
            "Mudança inesperada em estatísticas básicas",
            "Falhas em validações de schema",
        ],
        causes=[
            "Pipelines upstream instáveis",
            "Falhas de integração entre sistemas",
            "Erro humano em cadastros ou ETLs",
        ],
        detection_methods=[
            "Regras de qualidade automatizadas",
            "Dashboards com limites aceitáveis",
            "Alarmes de anomalia em features críticas",
        ],
        mitigation_actions=[
            "Acionar times responsáveis pelos dados",
            "Criar processos de backfill ou correção",
            "Introduzir validações obrigatórias antes da inferência",
        ],
    ),
    ProductionProblem(
        name="Modelo defasado",
        symptoms=[
            "Métricas de negócio não batendo com projeções",
            "Comparação com modelos de benchmark mostra perda",
            "Equipe operacional relata decisões desatualizadas",
        ],
        causes=[
            "Modelo treinado com dados antigos",
            "Falta de agilidade no ciclo de re-treinamento",
            "Mudanças sazonais não capturadas",
        ],
        detection_methods=[
            "Monitoramento de performance com limites temporais",
            "Comparações A/B com versões atualizadas",
            "Avaliação offline periódica",
        ],
        mitigation_actions=[
            "Planejar calendário de re-treinamento",
            "Automatizar pipelines de dados e validação",
            "Adotar arquitetura champion/challenger",
        ],
    ),
    ProductionProblem(
        name="Viés algorítmico",
        symptoms=[
            "Diferença significativa em taxas de aprovação entre grupos",
            "Incidência desproporcional de falsos positivos/negativos",
            "Alertas de compliance ou auditoria",
        ],
        causes=[
            "Dados históricos enviesados",
            "Proxy de variáveis sensíveis",
            "Configuração de limiares sem análise de equidade",
        ],
        detection_methods=[
            "Cálculo periódico de métricas de fairness",
            "Dashboards segmentados por atributos sensíveis",
            "Testes contrafactuais",
        ],
        mitigation_actions=[
            "Ajustar limiares ou reponderar amostras",
            "Coletar dados adicionais para grupos sub-representados",
            "Aplicar técnicas de pós-processamento para equalizar erros",
        ],
    ),
]


USE_CASES: List[UseCase] = [
    UseCase(
        name="Concessão de crédito",
        context="Instituição financeira avaliando risco de crédito para novos clientes.",
        risks=[
            "Drift de dados devido a novos segmentos",
            "Aumento de inadimplência sem detecção",
            "Pressão regulatória sobre fairness",
        ],
        monitoring_focus=[
            "PSI por feature relevante",
            "Taxa de aprovação e inadimplência por grupo",
            "Acompanhamento de F1 e AUC semanal",
        ],
        example_kpis=[
            "Taxa de default",
            "Tempo médio de decisão",
            "Impact ratio entre grupos sensíveis",
        ],
    ),
    UseCase(
        name="Detecção de fraude",
        context="Empresa de pagamentos analisando transações em tempo real.",
        risks=[
            "Ataques coordenados gerando drifts súbitos",
            "Latência elevada comprometendo a experiência",
            "Atualização frequente de padrões de fraude",
        ],
        monitoring_focus=[
            "Taxa de falsos positivos e falsos negativos",
            "Latência de inferência e throughput",
            "Alertas de ADWIN ou DDM em taxa de erro",
        ],
        example_kpis=[
            "Custo evitado por bloqueio",
            "Tempo de resposta por decisão",
            "Taxa de investigação manual",
        ],
    ),
    UseCase(
        name="Manutenção preditiva",
        context="Indústria monitorando sensores para prever falhas em equipamentos.",
        risks=[
            "Sensores descalibrados gerando dados inválidos",
            "Mudança na operação com novos regimes",
            "Feedback rótulo atrasado",
        ],
        monitoring_focus=[
            "Integridade de dados de sensores",
            "Monitoramento de drift em variáveis de condição",
            "Avaliação pós-falha com controle estatístico",
        ],
        example_kpis=[
            "Tempo médio entre falhas",
            "Taxa de falsos alarmes",
            "Disponibilidade dos equipamentos",
        ],
    ),
    UseCase(
        name="Recomendação de conteúdo",
        context="Plataforma digital sugerindo conteúdos personalizados.",
        risks=[
            "Mudanças de comportamento de usuários",
            "Conteúdos novos sem histórico",
            "Efeito bolha ou viés em recomendações",
        ],
        monitoring_focus=[
            "Diversidade e novidade das recomendações",
            "Engajamento (CTR, tempo de sessão)",
            "Fairness para criadores ou grupos específicos",
        ],
        example_kpis=[
            "Click-through rate",
            "Tempo médio de consumo",
            "Distribuição de exposição por criador",
        ],
    ),
    UseCase(
        name="Previsão de demanda",
        context="Varejista prevendo vendas para otimizar estoque e logística.",
        risks=[
            "Sazonalidade extrema e eventos inesperados",
            "Dados de estoque incorretos ou atrasados",
            "Mudanças externas (clima, economia)",
        ],
        monitoring_focus=[
            "Erros de previsão por SKU e região",
            "Drift em variáveis macroeconômicas",
            "Integridade de dados de vendas",
        ],
        example_kpis=[
            "WAPE (Weighted Absolute Percentage Error)",
            "Cobertura de estoque",
            "Custo de ruptura",
        ],
    ),
]
