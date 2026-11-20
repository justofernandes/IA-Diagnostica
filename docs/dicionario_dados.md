# Dicionário de dados

Cada linha do CSV representa um caso de diagnóstico. O arquivo tem cabeçalho, usa vírgulas como separador e é salvo em UTF-8.

| Coluna | Valores | Significado |
| --- | --- | --- |
| `falha` | `superaquecimento`, `falha_ram`, `falha_rede` | Causa conhecida do caso. Esta é a coluna-alvo. |
| `desliga_em_tarefa_pesada` | `0` ou `1` | O computador costuma desligar durante jogos ou outras tarefas pesadas? |
| `bipes_ao_ligar` | `0` ou `1` | O computador emite bipes incomuns ao ligar? |
| `conexao_cai` | `0` ou `1` | A conexão com a rede cai repetidamente durante o uso? |

Nas colunas de sintomas, `0` indica ausência e `1` indica presença. Na futura entrevista, a resposta **Não sei** deixará o sintoma fora do cálculo daquele atendimento.

As classes e perguntas desta versão são ilustrativas. A equipe vai definir o conjunto completo de classes e sintomas antes de montar a base de treinamento. O arquivo `dataset_exemplo.csv` contém casos fictícios para demonstrar o formato.
