# Boas práticas para dados climáticos

## Preserve a entrada original

Nunca edite diretamente os dados brutos. Manter a entrada intacta permite auditar erros, reconstruir resultados e comparar versões do pipeline.

## Documente metadados

Dados climáticos dependem de contexto. Fonte, unidade, resolução temporal, cobertura espacial, regra de acumulação e horário de referência podem alterar a interpretação de uma variável. Um CSV com `t2m` e `tp` não diz que um está em kelvin e o outro em metros acumulados.

## Distinga grandezas instantâneas de acumuladas

Temperatura e ponto de orvalho são medidos em um instante e podem ser interpolados entre horários próximos. Precipitação é um acumulado em um intervalo: para mudar de resolução, some ou reparta o total, nunca interpole. No exemplo, interpolar o acumulado de 3 h para a grade horária triplicaria a chuva anual.

## Confira a convenção de tempo dos acumulados

No ERA5, o acumulado rotulado em um horário cobre o período que **termina** nesse horário. Outras fontes rotulam pelo início. Errar a convenção desloca toda a chuva no tempo, e a primeira e a última hora do período passam a depender de dados fora dele.

O tamanho da janela também varia dentro de uma mesma fonte. No ERA5 horário, `tp` cobre 1 hora; nos produtos de 3 h, como os membros do ensemble, cobre 3 horas. Confira as duas coisas na documentação do produto baixado.

Ao somar por dia ou por mês, rotule cada valor pelo período a que ele pertence. Se a chuva das 23h às 00h ficar no rótulo das 00h, ela vai parar no dia seguinte, e a última hora de cada mês, no mês seguinte.

## Trate lacunas de forma explícita

Valores ausentes devem ser identificados e documentados. Preenchimentos automáticos sem registro dificultam a rastreabilidade. Um passo sem registro de chuva não é um passo seco.

Neste exemplo, lacunas curtas de temperatura e orvalho são interpoladas apenas para demonstrar o fluxo. Em um projeto real, a regra de preenchimento dependeria da variável, da duração da falha, da resolução temporal e do objetivo da análise.

## Variáveis derivadas herdam as falhas

A umidade relativa do exemplo é calculada de `t2m` e `d2m`. Onde uma delas falta, a umidade também falta; onde uma foi interpolada, a umidade depende dessa interpolação.

## Separe pipeline de modelagem

Um modelo pode ser trocado sem alterar a preparação dos dados. Um pipeline bem documentado torna essa troca mais simples e reduz ambiguidades.
