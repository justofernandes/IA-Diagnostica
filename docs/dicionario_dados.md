# Dicionário de dados

Cada linha do CSV representa um caso de diagnóstico. O arquivo tem cabeçalho, usa vírgulas como separador e é salvo em UTF-8. A coluna `falha` registra o rótulo do caso. Cada coluna de sintoma corresponde a uma pergunta que o agente pode fazer ao usuário.

## Campos do CSV de exemplo

| Coluna | Valores de exemplo | Significado |
| --- | --- | --- |
| `falha` | `superaquecimento`, `falha_ram`, `falha_rede` | Falha associada ao caso. É a coluna-alvo do modelo. |
| `desliga_em_tarefa_pesada` | `0` ou `1` | O computador costuma desligar durante jogos ou outras tarefas pesadas? |
| `bipes_ao_ligar` | `0` ou `1` | O computador emite bipes incomuns ao ligar? |
| `conexao_cai` | `0` ou `1` | A conexão com a rede cai repetidamente durante o uso? |

As classes e perguntas acima são ilustrativas. O [CSV de exemplo](../data/processed/dataset_exemplo.csv) contém seis casos fictícios. A lista de classes e sintomas da base de treino será definida após a análise piloto.

## Conversão de relatos e valores desconhecidos

| Registro na conversão | Significado | Resposta equivalente na entrevista |
| --- | --- | --- |
| `1` | Há evidência de que o sintoma está presente. | **Sim** |
| `0` | Há evidência de que o sintoma está ausente. | **Não** |
| Campo vazio | O relato deixou o sintoma em aberto. | **Não sei** |

Por exemplo, se o relato diz apenas que o computador desliga durante jogos, `desliga_em_tarefa_pesada` recebe `1` e `bipes_ao_ligar` fica vazio. Na amostra piloto, a equipe registrará quantas respostas são conhecidas para cada pergunta, a origem dos relatos e como os rótulos de origem foram associados às falhas do projeto.

Os campos vazios podem aparecer nas tabelas intermediárias. Antes do primeiro treino com `BernoulliNB`, a equipe definirá e documentará quais registros e colunas entram no conjunto binário de treinamento e como os casos incompletos foram tratados. Durante uma entrevista, **Não sei** fica registrado no histórico, e o motor deixa aquele sintoma fora do cálculo das probabilidades.
