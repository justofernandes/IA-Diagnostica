# Agente de diagnóstico de computadores

Projeto da disciplina de Introdução à Inteligência Artificial (IMD3001). O objetivo é investigar falhas de hardware, sistema operacional e rede em uma entrevista interativa.

O agente fará uma pergunta por vez sobre um sintoma do computador. A cada resposta, o Bernoulli Naive Bayes atualizará as probabilidades das causas candidatas. A próxima pergunta será escolhida pelo ganho de informação esperado. Se a hipótese principal atingir o limiar de confiança e a margem mínima sobre a segunda, o agente apresentará essa hipótese. Ao atingir o limite de perguntas, exibirá as três causas mais prováveis. A interface será implementada em Streamlit.

## Estado do projeto

O repositório contém a estrutura, o dicionário de dados e uma amostra fictícia do CSV. A base de treinamento, o modelo e a interface serão desenvolvidos nas próximas etapas.

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `data/raw/` | Dados brutos e rascunhos da equipe. |
| `data/processed/` | Amostra do formato do CSV e futura base validada. |
| `notebooks/` | Análise exploratória e experimentos de avaliação. |
| `src/` | Preparação dos dados, treinamento e lógica da entrevista. |
| `app/` | Interface Streamlit. |
| `docs/` | Dicionário dos dados, documentação acadêmica e figuras. |
| `models/` | Artefatos gerados pelo treinamento. |

## Preparar o ambiente no Windows

Instale o Python 3.11 ou 3.12. No PowerShell, abra a pasta do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O [dicionário de dados](docs/dicionario_dados.md) descreve as colunas do [CSV de exemplo](data/processed/dataset_exemplo.csv).
