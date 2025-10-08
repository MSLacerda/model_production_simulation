"""Utilities for building textual guides from the monitoring knowledge base."""

from __future__ import annotations

from textwrap import indent

from .data import MONITORING_TECHNIQUES, PRODUCTION_PROBLEMS, USE_CASES


def _format_list(items: list[str], bullet: str = "- ") -> str:
    return "\n".join(f"{bullet}{item}" for item in items)


def build_summary() -> str:
    """Build a rich Markdown summary covering techniques, problems and use cases."""

    sections: list[str] = []

    technique_lines = ["## Técnicas de monitoramento", ""]
    for technique in MONITORING_TECHNIQUES:
        technique_lines.extend(
            [
                f"### {technique.name}",
                f"**Objetivo:** {technique.objective}",
                technique.description,
                "",
                "**Sinais acompanhados:**",
                _format_list(technique.monitoring_signals),
                "",
                "**Algoritmos ou testes relevantes:**",
                _format_list(
                    [
                        f"{algorithm.name} — {algorithm.summary} (Uso indicado: {algorithm.when_to_use})"
                        for algorithm in technique.algorithms
                    ]
                ),
                "",
                "**Boas práticas operacionais:**",
                _format_list(technique.operational_tips),
                "",
                f"**Problemas relacionados:** {', '.join(technique.related_problems)}",
                "",
            ]
        )
    sections.append("\n".join(technique_lines))

    problem_lines = ["## Problemas recorrentes em produção", ""]
    for problem in PRODUCTION_PROBLEMS:
        problem_lines.extend(
            [
                f"### {problem.name}",
                "**Sintomas:**",
                _format_list(problem.symptoms),
                "",
                "**Causas comuns:**",
                _format_list(problem.causes),
                "",
                "**Como detectar:**",
                _format_list(problem.detection_methods),
                "",
                "**Ações de mitigação:**",
                _format_list(problem.mitigation_actions),
                "",
            ]
        )
    sections.append("\n".join(problem_lines))

    use_case_lines = ["## Casos de uso", ""]
    for use_case in USE_CASES:
        use_case_lines.extend(
            [
                f"### {use_case.name}",
                use_case.context,
                "",
                "**Riscos de produção:**",
                _format_list(use_case.risks),
                "",
                "**Foco de monitoramento:**",
                _format_list(use_case.monitoring_focus),
                "",
                "**KPIs recomendados:**",
                _format_list(use_case.example_kpis),
                "",
            ]
        )
    sections.append("\n".join(use_case_lines))

    header = [
        "# Guia rápido de monitoramento de modelos",
        "Ferramenta educacional para apoiar aulas sobre operação de modelos de machine learning em produção.",
        "",
    ]
    header.append("\n\n".join(sections))
    return "\n".join(header)


def build_cli_overview() -> str:
    """Generate a plain-text overview for use in CLI outputs."""

    summary_parts: list[str] = []
    summary_parts.append("Técnicas disponíveis: " + ", ".join(t.name for t in MONITORING_TECHNIQUES))
    summary_parts.append("Problemas monitorados: " + ", ".join(p.name for p in PRODUCTION_PROBLEMS))
    summary_parts.append("Casos de uso mapeados: " + ", ".join(u.name for u in USE_CASES))
    return "\n".join(summary_parts)


def format_technique(name: str) -> str:
    """Return a detailed description for a given technique."""

    technique = next((t for t in MONITORING_TECHNIQUES if t.name.lower() == name.lower()), None)
    if technique is None:
        available = ", ".join(t.name for t in MONITORING_TECHNIQUES)
        raise ValueError(f"Técnica '{name}' não encontrada. Opções: {available}")

    lines = [technique.name, "=" * len(technique.name), ""]
    lines.append(f"Objetivo: {technique.objective}")
    lines.append(technique.description)
    lines.append("")
    lines.append("Sinais acompanhados:")
    lines.append(indent(_format_list(technique.monitoring_signals, "* "), "  "))
    lines.append("")
    lines.append("Algoritmos/testes:")
    lines.append(
        indent(
            _format_list(
                [
                    f"{algorithm.name}: {algorithm.summary} (Uso: {algorithm.when_to_use})"
                    for algorithm in technique.algorithms
                ],
                "* ",
            ),
            "  ",
        )
    )
    lines.append("")
    lines.append("Boas práticas:")
    lines.append(indent(_format_list(technique.operational_tips, "* "), "  "))
    lines.append("")
    lines.append("Problemas relacionados: " + ", ".join(technique.related_problems))
    return "\n".join(lines)


def format_problem(name: str) -> str:
    """Return details for a production problem."""

    problem = next((p for p in PRODUCTION_PROBLEMS if p.name.lower() == name.lower()), None)
    if problem is None:
        available = ", ".join(p.name for p in PRODUCTION_PROBLEMS)
        raise ValueError(f"Problema '{name}' não encontrado. Opções: {available}")

    lines = [problem.name, "=" * len(problem.name), ""]
    lines.append("Sintomas:")
    lines.append(indent(_format_list(problem.symptoms, "* "), "  "))
    lines.append("")
    lines.append("Causas comuns:")
    lines.append(indent(_format_list(problem.causes, "* "), "  "))
    lines.append("")
    lines.append("Como detectar:")
    lines.append(indent(_format_list(problem.detection_methods, "* "), "  "))
    lines.append("")
    lines.append("Ações de mitigação:")
    lines.append(indent(_format_list(problem.mitigation_actions, "* "), "  "))
    return "\n".join(lines)


def format_use_case(name: str) -> str:
    """Return a scenario description for a given use case."""

    use_case = next((u for u in USE_CASES if u.name.lower() == name.lower()), None)
    if use_case is None:
        available = ", ".join(u.name for u in USE_CASES)
        raise ValueError(f"Caso de uso '{name}' não encontrado. Opções: {available}")

    lines = [use_case.name, "=" * len(use_case.name), ""]
    lines.append(use_case.context)
    lines.append("")
    lines.append("Riscos de produção:")
    lines.append(indent(_format_list(use_case.risks, "* "), "  "))
    lines.append("")
    lines.append("Foco de monitoramento:")
    lines.append(indent(_format_list(use_case.monitoring_focus, "* "), "  "))
    lines.append("")
    lines.append("KPIs recomendados:")
    lines.append(indent(_format_list(use_case.example_kpis, "* "), "  "))
    return "\n".join(lines)
