"""Command line interface for the monitoring toolkit."""

from __future__ import annotations

import argparse
import sys

from . import MONITORING_TECHNIQUES, PRODUCTION_PROBLEMS, USE_CASES
from .guide import (
    build_cli_overview,
    build_summary,
    format_problem,
    format_technique,
    format_use_case,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Ferramenta educativa para explorar técnicas de monitoramento de modelos em produção."
        )
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("overview", help="Mostra um resumo com técnicas, problemas e casos de uso.")

    subparsers.add_parser(
        "summary", help="Gera um guia completo em Markdown com todas as informações.")

    technique_parser = subparsers.add_parser(
        "technique",
        help="Mostra detalhes de uma técnica de monitoramento específica.",
    )
    technique_parser.add_argument("name", help="Nome da técnica exatamente como listado.")

    problem_parser = subparsers.add_parser(
        "problem", help="Explora sintomas, causas e mitigação de um problema de produção.")
    problem_parser.add_argument("name", help="Nome do problema.")

    use_case_parser = subparsers.add_parser("use-case", help="Mostra detalhes de um caso de uso.")
    use_case_parser.add_argument("name", help="Nome do caso de uso.")

    subparsers.add_parser(
        "list",
        help="Lista técnicas, problemas e casos disponíveis para consulta.",
    )

    return parser


def _print(text: str) -> None:
    sys.stdout.write(text + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "overview":
            _print(build_cli_overview())
        elif args.command == "summary":
            _print(build_summary())
        elif args.command == "technique":
            _print(format_technique(args.name))
        elif args.command == "problem":
            _print(format_problem(args.name))
        elif args.command == "use-case":
            _print(format_use_case(args.name))
        elif args.command == "list":
            lines = [
                "Técnicas:",
                *[f"  - {technique.name}" for technique in MONITORING_TECHNIQUES],
                "",
                "Problemas:",
                *[f"  - {problem.name}" for problem in PRODUCTION_PROBLEMS],
                "",
                "Casos de uso:",
                *[f"  - {use_case.name}" for use_case in USE_CASES],
            ]
            _print("\n".join(lines))
        else:
            parser.error("Comando não suportado.")
    except ValueError as exc:  # pragma: no cover - defensive branch
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
