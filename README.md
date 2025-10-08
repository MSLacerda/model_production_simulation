# Model Production Simulation Toolkit

Ferramenta educacional para apoiar aulas sobre monitoramento e operação de modelos de machine learning em produção. O projeto reúne técnicas, problemas recorrentes e casos de uso que podem ser consultados via linha de comando ou em um guia Markdown.

## Estrutura

- `monitoring_tool/`: pacote Python com a base de conhecimento estruturada e utilitários para geração de guias.
- `docs/monitoring_guide.md`: guia completo em Markdown gerado a partir do pacote.

## Como usar

### Pré-requisitos

- Python 3.10+ instalado no ambiente.

### Consultar pelo CLI

Execute os comandos abaixo a partir da raiz do repositório:

```bash
python -m monitoring_tool list         # Lista tudo que pode ser consultado
python -m monitoring_tool overview     # Mostra um panorama geral
python -m monitoring_tool technique "Detecção de Drift de Dados"
python -m monitoring_tool problem "Drift de conceito"
python -m monitoring_tool use-case "Concessão de crédito"
python -m monitoring_tool summary      # Gera o guia completo em Markdown
```

### Atualizar o guia em Markdown

O guia localizado em `docs/monitoring_guide.md` é gerado executando:

```bash
python -m monitoring_tool summary > docs/monitoring_guide.md
```

## Personalização sugerida

- Adicione novos algoritmos ou técnicas atualizando `monitoring_tool/data.py`.
- Crie exercícios pedindo para os alunos relacionarem problemas com técnicas apropriadas.
- Gere slides ou material de apoio exportando seções específicas com os comandos do CLI.
