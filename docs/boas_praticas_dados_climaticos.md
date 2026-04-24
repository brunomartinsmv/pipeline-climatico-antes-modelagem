# Boas praticas para dados climaticos

## Preserve a entrada original

Nunca edite diretamente os dados brutos. Manter a entrada intacta permite auditar erros, reconstruir resultados e comparar versoes do pipeline.

## Documente metadados

Dados climaticos dependem de contexto. Fonte, unidade, resolucao temporal, cobertura espacial, regra de acumulacao e horario de referencia podem alterar a interpretacao de uma variavel.

## Padronize antes de combinar

Antes de juntar fontes, confirme nomes de colunas, tipos de dados, unidades e frequencia temporal. Pequenas diferencas podem criar bases inconsistentes.

## Trate lacunas de forma explicita

Valores ausentes devem ser identificados e documentados. Preenchimentos automaticos sem registro dificultam a rastreabilidade.

Neste exemplo, as lacunas do INMET ficticio sao preenchidas apenas para demonstrar o fluxo. Em um projeto real, a regra de preenchimento dependeria da variavel, da duracao da falha, da resolucao temporal e do objetivo da analise.

## Separe pipeline de modelagem

Um modelo pode ser trocado sem alterar a preparacao dos dados. Um pipeline bem documentado torna essa troca mais simples e reduz ambiguidades.
