import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CSV_EXEMPLO = RAIZ / "data" / "processed" / "dataset_exemplo.csv"

sys.path.append(str(RAIZ))

from src.dados import carregar_csv


def analisar(caminho):
    dados = carregar_csv(caminho)

    print("\n--- RESUMO DO DATASET ---")
    print(f"Casos: {len(dados)}")
    print(f"Sintomas: {len(dados.columns) - 1}")
    print(f"Classes: {dados['falha'].nunique()}")

    print("\n--- CASOS POR FALHA ---")
    print(dados["falha"].value_counts())

    sintomas = dados.drop(columns="falha")

    print("\n--- FREQUÊNCIA DOS SINTOMAS ---")

    for coluna in sintomas.columns:
        positivos = sintomas[coluna].eq(1).sum()
        negativos = sintomas[coluna].eq(0).sum()
        desconhecidos = sintomas[coluna].isna().sum()

        print(
            f"{coluna}: "
            f"Sim={positivos} | "
            f"Não={negativos} | "
            f"Desconhecidos={desconhecidos}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume um CSV de casos e sintomas.")
    parser.add_argument(
        "caminho",
        nargs="?",
        default=CSV_EXEMPLO,
        help="CSV a analisar (padrão: o CSV de exemplo)",
    )
    analisar(parser.parse_args().caminho)
