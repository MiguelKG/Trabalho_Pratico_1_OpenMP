set -e

gcc tarefa_d.c -fopenmp -lm -o tarefa_d

# descarta stdout
./tarefa_d > /dev/null

mkdir -p plots
python3 grafico_d.py
mv plot_*.png plots/

echo "Concluído."