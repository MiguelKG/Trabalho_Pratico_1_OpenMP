Reprodutibilidade e Ambiente de Testes

Este documento descreve o hardware, software e configurações utilizados para obter os resultados aqui apresentados.

1. Caracterização do Hardware

Os experimentos foram executados em uma máquina pessoal com as seguintes especificações (baseadas no host):

Processador (CPU): Intel(R) Core(TM) i7-5500U CPU @ 2.40GHz

Arquitetura: x86_64

Frequência Base: 2.40 GHz

Núcleos Físicos: 2

Threads (Lógicos): 4 (Hyper-Threading habilitado)

Memória RAM: 8.00 GB (DDR3/DDR4)

Sistema Operacional (Host): Windows 10/11 (64 bits)

Ambiente de Execução: Subsistema Windows para Linux (WSL) / Linux Nativo

Nota: O código foi compilado e executado em ambiente Linux conforme exigido.

2. Caracterização do Software

Compilador e Bibliotecas

Compilador C: GCC (GNU Compiler Collection)

Versão: 9.4

Suporte OpenMP: OpenMP 4.5 ou superior (Flags -fopenmp)

Flags de Compilação:

-std=c11 -O3 -Wall -fopenmp


Flags de Ligação (Linker):

-lm -fopenmp


Ferramentas de Análise

Python: Versão 3.x

Bibliotecas: pandas, matplotlib, seaborn (utilizadas para geração dos gráficos).

3. Metodologia de Execução

Compilação

O projeto utiliza um Makefile para garantir a compilação consistente com otimizações de nível 3 (-O3).
Comando utilizado:

make omp


Parâmetros dos Testes

Os testes foram automatizados pelo script run.sh, cobrindo o seguinte espaço de parâmetros:

Tamanhos de Vetor (N): 100.000, 500.000, 1.000.000, 10.000.000

Número de Threads (OpenMP): 1, 2, 4, 8, 16

Repetições: Cada configuração foi executada 5 vezes.

Métrica: Tempo de execução do kernel (excluindo alocação e inicialização), reportado em segundos.

Coleta de Dados

Os dados brutos foram salvos automaticamente em formato CSV (results_tarefaC.csv) contendo:

Número da execução (1 a 5)

Versão do algoritmo (1=Seq, 2=SIMD, 3=Par+SIMD)

Tamanho N

Número de Threads

Tempo de execução

Checksum (para validação de corretude)

4. Como Reproduzir os Resultados

Para reproduzir exatamente os mesmos testes neste ambiente:

Limpe os artefatos anteriores:

make clean


Compile o código:

make omp


Execute a bateria de testes:

./run.sh


Gere os gráficos de análise:

python3 plot.py
