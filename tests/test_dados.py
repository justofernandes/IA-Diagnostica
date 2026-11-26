import pytest

from src.dados import carregar_csv, separar_sintomas_e_falhas


def criar_csv(pasta, conteudo):
    caminho = pasta / "casos.csv"
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def test_carrega_csv_valido(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes,conexao_cai\nfalha_ram,1,0\nfalha_rede,0,1\n")

    dados = carregar_csv(caminho)
    sintomas, falhas = separar_sintomas_e_falhas(dados)

    assert list(sintomas.columns) == ["bipes", "conexao_cai"]
    assert list(falhas) == ["falha_ram", "falha_rede"]


def test_recusa_csv_sem_coluna_falha(tmp_path):
    caminho = criar_csv(tmp_path, "bipes,conexao_cai\n1,0\n")

    with pytest.raises(ValueError, match="coluna 'falha'"):
        carregar_csv(caminho)


def test_recusa_valor_invalido(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes\nfalha_ram,2\n")

    with pytest.raises(ValueError, match="valor inválido"):
        carregar_csv(caminho)


def test_campo_vazio_fica_desconhecido(tmp_path):
    caminho = criar_csv(tmp_path, "falha,bipes,conexao_cai\nfalha_ram,1,\n")

    dados = carregar_csv(caminho)

    assert dados["conexao_cai"].isna().all()
