# Boas práticas para dados climáticos

## Preserve a entrada original

Nunca edite diretamente os dados brutos. Manter a entrada intacta permite auditar erros, reconstruir resultados e comparar versões do pipeline.

## Documente metadados

Dados climáticos dependem de contexto. Fonte, unidade, resolução temporal, cobertura espacial, regra de acumulação e horário de referência podem alterar a interpretação de uma variável.

## Padronize antes de combinar

Antes de juntar fontes, confirme nomes de colunas, tipos de dados, unidades e frequência temporal. Pequenas diferenças podem criar bases inconsistentes.

## Distinga grandezas instantâneas de acumuladas

Temperatura e umidade são medidas em um instante e podem ser interpoladas entre horários próximos. Precipitação é um acumulado em um intervalo: para mudar de resolução, some ou reparta o total, nunca interpole. No exemplo, interpolar o acumulado de 3 h do ERA5 para a grade horária triplicaria a chuva anual.

## Trate lacunas de forma explícita

Valores ausentes devem ser identificados e documentados. Preenchimentos automáticos sem registro dificultam a rastreabilidade. Uma hora sem registro de chuva não é uma hora seca.

Neste exemplo, as lacunas curtas de temperatura e umidade são interpoladas apenas para demonstrar o fluxo. Em um projeto real, a regra de preenchimento dependeria da variável, da duração da falha, da resolução temporal e do objetivo da análise.

## Separe pipeline de modelagem

Um modelo pode ser trocado sem alterar a preparação dos dados. Um pipeline bem documentado torna essa troca mais simples e reduz ambiguidades.
