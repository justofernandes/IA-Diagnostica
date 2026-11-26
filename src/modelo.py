from pathlib import Path

import joblib
import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline

from src.dados import (
    carregar_csv,
    normalizar_falhas,
    separar_sintomas_e_falhas,
    validar_dados,
)

CAMINHO_MODELO_PADRAO = Path("models/modelo_diagnostico.joblib")


def treinar_modelo(
    origem: str | Path | pd.DataFrame,
    alpha: float = 1.0,
    caminho_saida: str | Path | None = CAMINHO_MODELO_PADRAO,
) -> Pipeline:
    """Treina o classificador BernoulliNB a partir do CSV processado."""
    if isinstance(origem, pd.DataFrame):
        validar_dados(origem)
        dados = normalizar_falhas(origem)
    else:
        dados = carregar_csv(origem)

    x, y = separar_sintomas_e_falhas(dados)

    vazios = x.columns[x.isna().any()].tolist()
    if vazios:
        raise ValueError(
            f"Há campos vazios nas colunas: {', '.join(vazios)}. "
            "O treino aceita apenas 0 ou 1."
        )

    modelo = BernoulliNB(alpha=alpha)
    modelo.fit(x, y)

    if caminho_saida is not None:
        salvar_modelo(modelo, caminho_saida)

    return modelo


def salvar_modelo(
    modelo: Pipeline, caminho_saida: str | Path = CAMINHO_MODELO_PADRAO
) -> Path:
    """Serializa o pipeline treinado em disco."""
    destino = Path(caminho_saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, destino)
    return destino


def carregar_modelo(caminho_modelo: str | Path = CAMINHO_MODELO_PADRAO) -> Pipeline:
    """Carrega um modelo treinado a partir do arquivo .joblib."""
    return joblib.load(caminho_modelo)


def prever_completo(
    modelo: Pipeline, sintomas: dict[str, int | float | None]
) -> list[tuple[str, float]]:
    """
    Calcula probabilidades para um vetor completo de sintomas (uso em testes/batch).
    Nota: para inferência interativa ignorando 'Não sei', usar o motor de crenças.
    """
    entrada = pd.DataFrame([sintomas]).reindex(columns=modelo.feature_names_in_)
    probabilidades = modelo.predict_proba(entrada)[0]

    return sorted(
        zip(modelo.classes_, probabilidades),
        key=lambda item: item[1],
        reverse=True,
    )


if __name__ == "__main__":
    caminho = Path("data/processed/dataset_exemplo.csv")

    modelo = treinar_modelo(caminho)
    print("Modelo treinado!")
    print(f"Classes: {list(modelo.classes_)}")
    print(f"Modelo salvo em: {CAMINHO_MODELO_PADRAO}")

    exemplo = {coluna: 0 for coluna in modelo.feature_names_in_}
    resultado = prever_completo(modelo, exemplo)

    print("\n--- DIAGNÓSTICOS ---")
    for falha, probabilidade in resultado:
        print(f"{falha}: {probabilidade:.2%}")
