from pathlib import Path

import pandas as pd


def carregar_csv(caminho: str | Path) -> pd.DataFrame:
    """Lê os casos de diagnóstico e preserva os campos em branco como valores desconhecidos."""
    dados = pd.read_csv(
        caminho, encoding="utf-8", keep_default_na=False, na_values=[""]
    )
    validar_dados(dados)
    return normalizar_falhas(dados)


def validar_dados(dados: pd.DataFrame) -> None:
    """Verifica se os casos têm diagnóstico e se os sintomas são binários ou desconhecidos."""
    if "falha" not in dados.columns:
        raise ValueError("O CSV precisa conter a coluna 'falha'.")

    if dados.empty:
        raise ValueError("O CSV precisa conter pelo menos um caso de diagnóstico.")

    if dados.drop(columns="falha").shape[1] == 0:
        raise ValueError("O CSV precisa ter sintomas")

    falhas = dados["falha"].astype("string").fillna("").str.strip()
    if falhas.eq("").any():
        raise ValueError("Todos os casos precisam ter a coluna 'falha' preenchida.")

    for coluna, sintomas in dados.drop(columns="falha").items():
        invalidos = sintomas.notna() & ~sintomas.isin([0, 1, "0", "1"])
        if invalidos.any():
            valor = sintomas[invalidos].iloc[0]
            raise ValueError(
                f"A coluna '{coluna}' contém o valor inválido '{valor}'. "
                "Use 0, 1 ou deixe o campo em branco."
            )


def normalizar_falhas(dados: pd.DataFrame) -> pd.DataFrame:
    """Devolve uma cópia sem espaços sobrando nos nomes das falhas."""
    copia = dados.copy()
    copia["falha"] = copia["falha"].astype(str).str.strip()
    return copia


def separar_sintomas_e_falhas(dados: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separa os sintomas (X) dos diagnósticos conhecidos (y) de uma tabela validada.

    O diagnóstico é o que o modelo vai aprender a prever. Mantê-lo fora de X
    evita entregar a resposta ao modelo junto com os sintomas.
    """
    X = dados.drop(columns="falha")
    y = dados["falha"]
    return X, y
