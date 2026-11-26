# Formato do histórico da sessão

**Versão 1 (proposta, aguardando revisão do motor, do painel e da avaliação)**

O histórico é o acordo entre o motor, que o escreve, e o painel e a avaliação, que só o leem. O exemplo completo está em [`sessao_exemplo.json`](../data/processed/sessao_exemplo.json). Ele usa o CSV fictício, com `alpha = 1`.

No código, o histórico é um dicionário Python com esta mesma estrutura, que pode ser salvo em JSON.

## Campos principais

Todos são obrigatórios.

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `versao` | inteiro | Versão do formato. Hoje, `1`. |
| `parametros` | objeto | `tau` (número de 0 a 1), `delta` (número de 0 a 1) e `n_max` (inteiro, no mínimo 1) usados na sessão. |
| `rodadas` | lista | Uma entrada por pergunta **respondida**, em ordem. Começa vazia. |
| `parada` | texto ou `null` | Motivo do encerramento. `null` enquanto a entrevista está em andamento. |
| `hipoteses` | lista | Pares `[falha, probabilidade]` com **todas** as falhas, da mais provável para a menos provável. |

## Campos de cada rodada

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `n` | inteiro | Número da rodada, começando em 1. |
| `sintoma` | texto | Pergunta feita, com o nome da coluna no CSV. |
| `ganhos` | objeto | Ganho de informação esperado, em bits, de cada pergunta ainda não feita no momento da escolha. Inclui a escolhida. |
| `resposta` | texto | `sim`, `nao` ou `nao_sei`. |
| `antes` | objeto | Probabilidade de cada falha antes da resposta. |
| `depois` | objeto | Probabilidade de cada falha depois da resposta. |

## Regras

### Perguntas

- A pergunta escolhida é a de maior ganho. No empate, vale a ordem das colunas do CSV.
- Uma pergunta nunca se repete, mesmo que a resposta tenha sido `nao_sei`.
- Com `nao_sei`, `depois` é igual a `antes`.
- `nao_sei` conta para o limite `n_max`.
- Ganhos negativos muito pequenos, causados por arredondamento do computador, são gravados como `0`.

### Probabilidades

- `antes`, `depois` e `hipoteses` trazem todas as falhas, com valores de 0 a 1 que somam 1.
- O `antes` da rodada 1 são as probabilidades iniciais. Nas demais, é igual ao `depois` da rodada anterior.
- `hipoteses` corresponde ao último `depois`. Sem rodadas, às probabilidades iniciais. No empate, vale a ordem de `classes_` do modelo.
- O motor grava os valores sem arredondar. Quem exibe é que arredonda. O arquivo de exemplo usa 6 casas decimais só para facilitar a leitura, então compare com tolerância de `0.00001`.

### Parada

O motor verifica as condições depois de cada resposta, nesta ordem. A primeira verdadeira define o valor.

| Valor | Condição | O que a interface mostra |
| --- | --- | --- |
| `confianca` | 1ª hipótese >= `tau` **e** diferença para a 2ª >= `delta` | A hipótese líder |
| `limite_perguntas` | Número de rodadas igual a `n_max` | Até 3 hipóteses |
| `sem_perguntas` | Não há pergunta ainda não feita | Até 3 hipóteses |

Se não houver nenhuma pergunta já no início, `rodadas` fica vazia e `parada` é `sem_perguntas`.

## Uso por cada parte

- **Motor:** converte os tipos do NumPy para tipos do Python (`str`, `float`, `int`), para o histórico poder ser salvo em JSON.
- **Painel:** só lê o histórico, sem recalcular probabilidades. O texto de cada pergunta vem de `perguntas.csv`, buscado pelo nome do sintoma. Enquanto esse arquivo não existir, mostra o próprio nome.
- **Avaliação:** o número de perguntas é o tamanho de `rodadas`. O acerto usa o primeiro item de `hipoteses`, e o top 3 usa os três primeiros. A falha verdadeira do caso simulado fica com o simulador, fora do histórico.

## Como mudar o formato

Abra um pull request que atualize este documento e o arquivo de exemplo, com revisão de quem cuida do motor, do painel e da avaliação. Depois que o código estiver usando o formato, toda mudança incompatível aumenta `versao`.
