import pandas as pd
import pytest

from src.modelo import carregar_modelo, treinar_modelo


def casos(**colunas):
    """Monta uma tabela pequena de casos para os testes."""
    return pd.DataFrame(colunas)


def criar_csv(pasta, conteudo):
    caminho = pasta / "casos.csv"
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def test_treina_a_partir_de_um_csv(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes\nfalha_ram,1\nfalha_rede,0\n")

    modelo = treinar_modelo(caminho, caminho_saida=None)

    assert list(modelo.classes_) == ["falha_ram", "falha_rede"]


def test_treina_a_partir_de_um_dataframe():
    dados = casos(falha=["falha_ram", "falha_rede"], bipes=[1, 0])

    modelo = treinar_modelo(dados, caminho_saida=None)

    assert list(modelo.feature_names_in_) == ["bipes"]


def test_repassa_o_alpha():
    dados = casos(falha=["a", "b"], bipes=[1, 0])

    modelo = treinar_modelo(dados, alpha=0.5, caminho_saida=None)

    assert modelo.alpha == 0.5


def test_recusa_csv_sem_sintomas(tmp_path):
    caminho = criar_csv(tmp_path, "falha\nfalha_ram\n")

    with pytest.raises(ValueError, match="sintoma"):
        treinar_modelo(caminho, caminho_saida=None)


def test_recusa_dataframe_sem_sintomas():
    with pytest.raises(ValueError, match="sintoma"):
        treinar_modelo(casos(falha=["falha_ram"]), caminho_saida=None)


def test_recusa_vazio_no_treino():
    dados = casos(falha=["a", "b"], bipes=[1, None])

    with pytest.raises(ValueError, match="bipes"):
        treinar_modelo(dados, caminho_saida=None)


def test_recusa_coluna_totalmente_vazia(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes,conexao_cai\na,1,\nb,0,\n")

    with pytest.raises(ValueError, match="conexao_cai"):
        treinar_modelo(caminho, caminho_saida=None)


def test_junta_falhas_com_espacos_no_csv(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes\nx,1\nx ,0\ny,0\n")

    modelo = treinar_modelo(caminho, caminho_saida=None)

    assert list(modelo.classes_) == ["x", "y"]


def test_limpa_espacos_sem_alterar_o_dataframe_original():
    dados = casos(falha=["x", " x ", "y"], bipes=[1, 0, 0])

    modelo = treinar_modelo(dados, caminho_saida=None)

    assert list(modelo.classes_) == ["x", "y"]
    assert list(dados["falha"]) == ["x", " x ", "y"]


def test_salva_e_carrega_o_modelo(tmp_path):
    dados = casos(falha=["a", "b"], bipes=[1, 0], conexao_cai=[0, 1])
    destino = tmp_path / "models" / "modelo.joblib"

    treinar_modelo(dados, caminho_saida=destino)
    modelo = carregar_modelo(destino)

    assert list(modelo.classes_) == ["a", "b"]
    assert list(modelo.feature_names_in_) == ["bipes", "conexao_cai"]
