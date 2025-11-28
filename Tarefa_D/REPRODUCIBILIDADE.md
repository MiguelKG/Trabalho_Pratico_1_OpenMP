Reprodutibilidade e Ambiente de Testes

Este documento descreve o hardware, software e configurações utilizados para obter os resultados aqui apresentados.

1. Caracterização do Hardware

Os experimentos foram executados em uma máquina pessoal com as seguintes especificações:

Processador (CPU): Intel(R) Core(TM) i3-6006U CPU @ 2.00GHz

Arquitetura: x86_64

Frequência Base: 2.00 GHz

Núcleos Físicos: 2

Threads (Lógicos): 4 (Hyper-Threading habilitado)

Memória RAM: 8.00 GB (DDR4)

Sistema Operacional (Host): Windows 10 (64 bits)

Ambiente de Execução: Subsistema Windows para Linux (WSL)

Nota: O código foi compilado e executado em ambiente Linux conforme exigido.

2. Caracterização do Software

Compilador e Bibliotecas

Compilador C: GCC (GNU Compiler Collection)

Versão: 11.4.0

Suporte OpenMP: OpenMP 4.5 ou superior (Flags -fopenmp)

Flags:

-lm -fopenmp

Ferramentas de Análise

Python: Versão 3.10.12

Bibliotecas: matplotlib.

3. Metodologia de Execução

Parâmetros dos Testes

Os testes foram automatizados pelo script run.sh, cobrindo o seguinte espaço de parâmetros:

Tamanhos de Vetor (N): 100.000, 500.000, 1.000.000

Número de Threads (OpenMP): 1, 2, 4, 8, 16

Repetições: Cada configuração foi executada 5 vezes.

Métrica: Tempo de execução reportado em segundos.

Coleta de Dados

Os dados brutos foram salvos automaticamente em formato CSV (resultados_d.csv) contendo:

Tamanho de N

Número de Threads

Média Ingênua e Arrumada das 5 repetições para cada configuração

Variância Ingênua e Arrumada das 5 repetições para cada configuração

Desvio Padrão Ingênuo e Arrumado das 5 repetições para cada configuração

4. Como Reproduzir os Resultados

Para reproduzir os testes desta tarefa basta executar o script:

./run.sh

Os gráficos com os resultados serão gerados dentro da pasta plots.

Caso desejar, é possível também executar os scripts de geração de csv e construção dos gráficos
manualmente com:

gcc tarefa_d.c -o tarefa_d -fopenmp -lm
./tarefa_d
python3 grafico_d.py

Obs: certas informações da execução são somente exibidas na saída do script "tarefa_d", enquanto os gráficos dão maior enfoque nos dados mais relevantas.