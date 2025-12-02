# Reprodutibilidade e Ambiente de Testes

Execução da Tarefa C pelo aluno Gustavo Reginatto de IPPD

## 1. Hardware

-   **Processador (CPU):** Intel(R) Core(TM) i7-5500U @ 2.40GHz
-   **Arquitetura:** x86_64
-   **Núcleos Físicos:** 2
-   **Threads (Lógicos):** 4 (Hyper-Threading habilitado)
-   **Memória RAM:** 8 GB (DDR3/DDR4)
-   **Sistema Operacional:** Windows 10 (64 bits)
-   **Ambiente de Execução:** Windows Subsystem for Linux (WSL)

## 2. Software

### Compilador C

-   **GCC:** versão 9.4.0
-   **Suporte a OpenMP:** OpenMP 4.5

**Flags de compilação:**

    -std=c11 -O3 -Wall -fopenmp

**Flags de ligação:**

    -lm -fopenmp

### Ferramentas de Análise

-   **Python 3**
-   Bibliotecas utilizadas:
    -   pandas
    -   matplotlib
    -   seaborn
    -   numpy

## 3. Metodologia de Execução

### Compilação

O projeto utiliza compilação direta via GCC com otimização nível 3
(`-O3`).

### Parâmetros dos Testes

Os testes são automatizados pelo script `run.sh`, cobrindo:

-   **Tamanhos do vetor (N):**
    -   100.000
    -   500.000
    -   1.000.000
    -   10.000.000
-   **Número de threads (OpenMP):**
    -   1, 2, 4, 8, 16
-   **Repetições por configuração:** 5
-   **Métrica de avaliação:** tempo de execução em segundos 

### Coleta de Dados

Os resultados são armazenados no arquivo `results_tarefaC.csv`,
contendo:

  Campo                 Descrição
  --------------------- -----------------------------
  Execução              1 a 5
  Versão do algoritmo   (1=Seq, 2=SIMD, 3=Par+SIMD)
  Tamanho N             Tamanho do vetor
  Threads               Número de threads usadas
  Tempo                 Tempo de execução
  Checksum              Verificação da saída

## 4. Como Reproduzir os Resultados

### 1. Limpar artefatos anteriores (opcional)

    make clean

Ou manualmente:

    rm tarefaC
    rm results_tarefaC.csv
    rm -rf graficos/ graficos_criticos/

### 2. Compilar e executar todos os testes

    ./run.sh

**Comando interno utilizado pelo script:**

    gcc -std=c11 -O3 -Wall -fopenmp tarefaC.c -o tarefaC -lm

### 3. Gerar gráficos de análise básica

    python3 plot.py

### 4. Gerar gráficos de análise de vazão e eficiência

    python3 plot2.py


### 5. Conclusão

1. Sobre a Vetorização (SIMD): Basicamente, não mudou quase nada. Por quê? O seu compilador com a flag -O3 é inteligente. Ele percebeu sozinho que dava para otimizar a conta e já fez isso na versão normalmente.

2. Sobre a Velocidade com mais Threads: Muitas threads não foram necessárias para otimizar o problema visto que apenas uma daria conta do fluxo de entrada dos dados.

3. Sobre a Memória (Vazão): Os testes mostraram que a memória RAM tem um limite de velocidade real de 16 GB por segundo. O que isso significa? É o limite físico do seu notebook. Não importa o código os dados não conseguem trafegar entre a memória e o processador mais rápido que isso.

4. Sobre a Eficiência Com 16 threads: A eficiência foi de apenas 5%. Como a entrada de dados não era rapida o suficiente, muitas threads acabam ficando ociosas e apenas gastando recursos.

5. Quando usar muitas threads atrapalhou (Overhead): Em testes pequenos criar muitas threads demorava mais do que receber os proprios dados.
