import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

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
    analisar(sys.argv[1])
