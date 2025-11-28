#!/bin/bash

# Nome do executável
EXE=./tarefaC
# Nome do arquivo de código fonte
SRC=tarefaC.c
# Nome do arquivo de saída
CSV_FILE=results_tarefaC.csv

echo "--- 1. Compilando $SRC ---"
# Compilação manual direta
gcc -std=c11 -O3 -Wall -fopenmp $SRC -o tarefaC -lm

# Verifica se compilou com sucesso
if [ $? -ne 0 ]; then
    echo "Erro na compilação!"
    exit 1
fi

echo "--- 2. Iniciando os testes ---"

# Garante que números usem ponto (.) e não vírgula (,)
export LC_NUMERIC=C

# Cria o cabeçalho do CSV
echo "run,versao,N,threads,tempo_kernel,check_sum" > $CSV_FILE

# Parâmetros de teste (Mantendo os seus originais)
N_VALUES="100000 500000 1000000 10000000"
THREAD_VALUES="1 2 4 8 16"
RUNS=5

for N in $N_VALUES; do
    echo "Testando N = $N"

    # --- V1: Sequencial ---
    for R in $(seq 1 $RUNS); do
        output=$(OMP_NUM_THREADS=1 $EXE 1 $N 1)
        echo "$R,$output" >> $CSV_FILE
    done

    # --- V2: SIMD ---
    for R in $(seq 1 $RUNS); do
        output=$(OMP_NUM_THREADS=1 $EXE 2 $N 1)
        echo "$R,$output" >> $CSV_FILE
    done

    # --- V3: Paralelo + SIMD ---
    for T in $THREAD_VALUES; do
        for R in $(seq 1 $RUNS); do
            output=$(OMP_NUM_THREADS=$T $EXE 3 $N $T)
            echo "$R,$output" >> $CSV_FILE
        done
    done
done

echo "--- 3. Concluído! ---"
echo "Arquivo gerado: $CSV_FILE"