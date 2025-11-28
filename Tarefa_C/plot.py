import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

CSV_FILE = "results_tarefaC.csv"
OUTPUT_DIR = "graficos"

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Erro: Arquivo '{CSV_FILE}' não encontrado. Execute ./run.sh primeiro.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(CSV_FILE)
    
    df_avg = df.groupby(['versao', 'N', 'threads'])['tempo_kernel'].mean().reset_index()
    
    # Criação dos Gráficos
    plot_simd_gain(df_avg)
    plot_scalability(df_avg)

    print(f"Gráficos gerados com sucesso em: {OUTPUT_DIR}/")

def plot_simd_gain(df):
    """
    Gráfico 1: Comparação V1 (Seq) vs V2 (SIMD) para diferentes tamanhos N.
    """
    plt.figure(figsize=(10, 6))
    
    # Filtra apenas V1 e V2
    subset = df[df['versao'].isin([1, 2])]
    
    # Pivot para ter versões como colunas e facilitar o cálculo do speedup
    pivot = subset.pivot(index='N', columns='versao', values='tempo_kernel')
    
    if 1 not in pivot.columns or 2 not in pivot.columns:
        print("Aviso: Dados para V1 ou V2 ausentes. Pulando gráfico de SIMD.")
        return

    # Calcula Speedup (Tempo Seq / Tempo SIMD)
    pivot['speedup'] = pivot[1] / pivot[2]
    
    # Plota o Speedup
    ax = pivot['speedup'].plot(kind='bar', color='skyblue', edgecolor='black')
    
    plt.title("Ganho de Vetorização (SIMD)\nSpeedup da V2 sobre V1")
    plt.xlabel("Tamanho do Vetor (N)")
    plt.ylabel("Speedup (x vezes mais rápido)")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adiciona os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}x', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/ganho_simd.png")
    plt.close()

def plot_scalability(df):
    """
    Gráfico 2: Escalabilidade da V3 (Parallel For SIMD) variando threads.
    Focamos no maior N para ver o comportamento assintótico melhor.
    """
    max_n = df['N'].max()
    
    subset = df[(df['versao'] == 3) & (df['N'] == max_n)].copy()
    
    time_seq = df[(df['versao'] == 1) & (df['N'] == max_n)]['tempo_kernel'].values
    
    if len(subset) == 0 or len(time_seq) == 0:
        print("Aviso: Dados insuficientes para gráfico de escalabilidade.")
        return
        
    base_time = time_seq[0]
    
    # Calcula Speedup
    subset['speedup'] = base_time / subset['tempo_kernel']
    
    plt.figure(figsize=(10, 6))
    
    # Linha do Speedup Real
    sns.lineplot(data=subset, x='threads', y='speedup', marker='o', label='Real (V3 vs V1)')
    
    # Linha do Speedup Ideal (Linear)
    plt.plot([1, subset['threads'].max()], [1, subset['threads'].max()], 
             '--', color='gray', label='Ideal (Linear)')
    
    plt.title(f"Escalabilidade OpenMP (V3) - N={max_n}")
    plt.xlabel("Número de Threads")
    plt.ylabel("Speedup")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Garante que o eixo X mostre apenas as threads testadas
    plt.xticks(subset['threads'].unique())
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/escalabilidade_v3.png")
    plt.close()

if __name__ == "__main__":
    main()