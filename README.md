# Agente de diagnóstico de computadores

Projeto da disciplina de Introdução à Inteligência Artificial (IMD3001). O agente investiga falhas de hardware, sistema operacional e rede em computadores por meio de uma entrevista. Ele faz uma pergunta por vez, atualiza as probabilidades das falhas candidatas e usa as respostas para decidir o que perguntar em seguida.

O projeto usará Python, `BernoulliNB` do scikit-learn para treinar o modelo e Streamlit para a entrevista. O motor de diagnóstico será compartilhado pela interface e pelos scripts de avaliação. O repositório já contém a estrutura inicial, o dicionário de dados e um CSV fictício para demonstrar o formato.

## Como a entrevista funciona

1. O motor começa com as probabilidades iniciais das falhas que o modelo conhece.
2. Entre as perguntas disponíveis, escolhe a de maior ganho de informação esperado, ou seja, a que tende a reduzir mais a incerteza sobre a falha.
3. O usuário responde **Sim**, **Não** ou **Não sei**. As duas primeiras respostas indicam presença ou ausência do sintoma. A terceira fica registrada no histórico e o sintoma é omitido do cálculo.
4. O motor apresenta a hipótese líder quando ela atinge o limiar de confiança e abre a margem mínima sobre a segunda hipótese. Se atingir o limite de perguntas antes disso, mostra até três hipóteses, em ordem de probabilidade. O limiar, a margem e o limite serão configuráveis.

### Painel de trajetória

Em cada rodada, o motor registra a pergunta escolhida, os ganhos de informação esperados das perguntas candidatas, a resposta e as probabilidades das falhas antes e depois da resposta. Ao encerrar a entrevista, também registra o motivo da parada.

O painel **Como o agente chegou a esse resultado?** lê esse histórico da sessão no Streamlit. Ele mostra quais perguntas teriam ajudado a reduzir a incerteza, como cada resposta mudou as hipóteses e qual regra encerrou o atendimento. Os scripts de avaliação também usam esse histórico para contar perguntas e analisar as decisões do agente em simulações.

## Dados e treinamento

O [FACTO Dataset](https://github.com/malu-maia/FACTO) é uma fonte candidata de relatos sobre falhas em PCs. A equipe fará uma amostra piloto para verificar quais rótulos se encaixam no escopo e quantas perguntas podem ser respondidas a partir dos relatos. A cobertura da amostra orientará a escolha entre adaptar os casos disponíveis, complementar a base ou usar os relatos como referência para definir sintomas.

- `data/raw/` reúne os dados de origem e a preparação intermediária, com o registro da procedência dos casos.
- `data/processed/` reúne a base em CSV, com uma linha por caso, a coluna-alvo `falha` e uma coluna por sintoma. Para o primeiro treino, as colunas de sintomas usadas pelo modelo terão valores `0` ou `1`, conforme os critérios de preparação registrados pela equipe.

O [dicionário de dados](docs/dicionario_dados.md) define o formato e o tratamento de sintomas desconhecidos. O [CSV de exemplo](data/processed/dataset_exemplo.csv) serve para testar a leitura e demonstrar o primeiro treino. A medição de desempenho será feita com a base preparada para o projeto.

## Gráficos e avaliação

Os gráficos serão produzidos por scripts Python. As figuras do relatório serão exportadas para `docs/figuras/`. A interface leva o histórico da sessão ao painel, e os scripts de avaliação chamam o mesmo motor para reproduzir os resultados em casos rotulados.

| Análise | Dados usados | Saídas previstas |
| --- | --- | --- |
| **Análise da base** | CSV de casos e sintomas | Barras de casos por falha, frequência de sintomas por classe, percentual de desconhecidos, gráfico de especificidade (`log₂`) e mapa de calor dos sintomas que aparecem juntos. |
| **Avaliação do classificador** | Casos rotulados de teste, com os sintomas usados pelo modelo | Matriz de confusão, precisão, revocação e F1 por falha. Comparação com um `DummyClassifier` que prevê a classe mais frequente do treino. |
| **Avaliação da entrevista** | Simulações com falha conhecida, incluindo cenários com respostas **Não sei** | Acurácia, taxa de acerto no top 3, média de perguntas e curva de acurácia × média de perguntas para diferentes limiares. |
| **Trajetória da sessão** | Histórico de perguntas, respostas e hipóteses | Evolução das probabilidades, ganho de informação esperado e motivo da parada. |

Na frequência e na especificidade, as proporções são calculadas entre os casos com resposta conhecida para o sintoma. A figura ou tabela de apoio informa quantos casos puderam ser avaliados. Para escolher parâmetros do modelo e da entrevista, a equipe usa treino e validação e reserva o conjunto de teste para a medição final.

Na apresentação, o grupo pode demonstrar uma entrevista e abrir o painel para explicar as decisões do agente. A matriz de confusão e a curva de acurácia × número de perguntas dão suporte à discussão de resultados e limitações.

## Organização da equipe

| Frente | Primeira entrega |
| --- | --- |
| **Modelo e aplicação** | Ler e validar o CSV, fazer o primeiro treino com `BernoulliNB` e combinar o formato do histórico da entrevista com a pessoa da visualização. |
| **Dados** | Avaliar a amostra do FACTO, propor classes e perguntas e atualizar o dicionário com os critérios de conversão. |
| **Documentação** | Redigir o escopo, a modelagem PEAS e a arquitetura. Registrar fontes, decisões e, à medida que os testes forem feitos, métricas, resultados e limitações. |
| **Visualização e avaliação** | Preparar os primeiros gráficos da base e esboçar o painel com uma sessão de exemplo. Integrar a avaliação ao modelo quando o código e os casos de teste estiverem disponíveis. |

Para começar em paralelo, a equipe combina duas coisas logo no início: **as colunas do CSV** entre dados e modelo e **os campos do histórico da sessão** entre motor e visualização. O primeiro marco é carregar a amostra, treinar o modelo e gerar um gráfico da base. Depois, a equipe integra a entrevista e o painel e mede o desempenho em sessões simuladas.

## Estrutura do repositório

| Pasta | Responsabilidade prevista |
| --- | --- |
| `data/raw/` e `data/processed/` | Dados de origem e tabelas preparadas. |
| `src/` | Leitura do CSV, treinamento e motor da entrevista. |
| `app/` | Interface Streamlit e painel da sessão. |
| `scripts/` | Pasta prevista para gerar gráficos, avaliar o classificador e simular entrevistas. |
| `docs/` | Dicionário, documentação acadêmica e figuras exportadas. |
| `models/` | Artefatos gerados pelo treinamento. |

## Preparar o ambiente no Windows

Instale o Python 3.11 ou 3.12. Abra o PowerShell na pasta do projeto e execute os comandos abaixo para criar o ambiente e instalar as dependências.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
