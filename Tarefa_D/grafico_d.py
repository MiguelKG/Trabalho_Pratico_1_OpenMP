import csv
import matplotlib.pyplot as plt

csv_file = "resultados_d.csv"

csv_n = []
csv_threads = []
csv_naive_avg = []
csv_naive_std = []
csv_fixed_avg = []
csv_fixed_std = []

with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_n.append(int(row['n']))
        csv_threads.append(int(row['threads']))
        csv_naive_avg.append(float(row['media_ingenua']))
        csv_naive_std.append(float(row['desvio_ingenua']))
        csv_fixed_avg.append(float(row['media_arrumada']))
        csv_fixed_std.append(float(row['desvio_arrumada']))

unique_n = sorted(set(csv_n))
for n in unique_n:

    t_vals = []
    naive_vals = []
    naive_std = []
    fixed_vals = []
    fixed_std = []

    for i in range(len(csv_n)):
        if csv_n[i] == n:
            t_vals.append(csv_threads[i])
            naive_vals.append(csv_naive_avg[i])
            naive_std.append(csv_naive_std[i])
            fixed_vals.append(csv_fixed_avg[i])
            fixed_std.append(csv_fixed_std[i])

    plt.figure(figsize=(8,5))
    plt.errorbar(t_vals, naive_vals, yerr=naive_std, fmt='-o', label='Ingênua', capsize=5, capthick=2)
    plt.errorbar(t_vals, fixed_vals, yerr=fixed_std, fmt='-o', label='Arrumada', capsize=5, capthick=2)

    plt.title(f'Tarefa D - Organização de Região Paralela (N={n})')
    plt.xlabel('Número de Threads')
    plt.ylabel('Tempo médio de execução (s)')
    plt.xticks(t_vals)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f'plot_N{n}.png')