<h1>Resultados</h1>

<p align="justify">
Analisando os resultados obtidos nos gráficos, faz-se claro que a "versão arrumada" do código foi mais rápida que a ingênua, visto que ela cria a
região paralela apenas uma vez. Na ingênua, cada <i>parallel for</i> abre e fecha sua própria região paralela, fazendo com que as <i>threads</i>
sejam criadas, sincronizadas e destruídas duas vezes, um custo que se soma no tempo total. Já na versão arrumada, as <i>threads</i> são criadas uma
única vez e permanecem ativas dentro da mesma região, executando os dois <i>for</i> em sequência sem precisar repetir todo o processo de gerenciamento.
</p>

<p align="justify">
Além disso, observando os desvios-padrão exibidos nos gráficos, nota-se que a versão ingênua apresenta flutuações
significativamente maiores que a arrumada. Isso ocorre porque no processo de criar e finalizar duas vezes as regiões paralelas, aumenta-se
consideravelmente a variabilidade entre execuções devido às diferenças no custo de gerenciamento de threads. Já a versão arrumada, ao manter uma
única região ativa, tende a produzir tempos mais estáveis e previsíveis, o que reforça sua vantagem não apenas em desempenho médio, mas também em
consistência.
</p>

<p align="justify">
Também foi possível notar ganho de desempenho ao aumentar o número de <i>threads</i> de 1 para 2 e depois para 4 (o processador utilizado contém 4
<i>threads</i> lógicas). Porém, ao ultrapassar esse valor, usando 8 ou 16 <i>threads</i>, o tempo piorou devido à competição pelas mesmas unidades
de hardware, causando mais disputas e trocas de contexto do que paralelização real. 
</p>

<p align="justify">
Assim, a versão arrumada se mostrou mais eficiente e o ganho com mais <i>threads</i> só aconteceu até o ponto suportado pelo <i>hardware</i>.
</p>
