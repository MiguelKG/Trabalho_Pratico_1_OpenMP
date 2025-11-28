import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Configurações
CSV_FILE = "results_tarefaC.csv"
OUTPUT_DIR = "graficos_criticos"

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Erro: {CSV_FILE} não encontrado. Execute ./run.sh primeiro.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    # Carregar Dados
    df = pd.read_csv(CSV_FILE)
    
    # Calcular Vazão (GB/s): (12 Bytes * N) / (Tempo * 10^9)
    # SAXPY lê 2 vetores e escreve 1 (4 bytes cada float = 12 bytes/elem)
    df['bandwidth_gbs'] = (12 * df['N']) / (df['tempo_kernel'] * 1e9)
    
    # Calcular Estatísticas Agrupadas
    df_agg = df.groupby(['versao', 'N', 'threads']).agg(
        tempo_medio=('tempo_kernel', 'mean'),
        tempo_std=('tempo_kernel', 'std'),
        bandwidth_medio=('bandwidth_gbs', 'mean')
    ).reset_index()

    print(f"Gerando gráficos críticos em '{OUTPUT_DIR}'...")
    plot_bandwidth(df_agg)
    plot_efficiency(df_agg)
    plot_stability(df)
    print("Concluído.")

def plot_bandwidth(df):
    plt.figure(figsize=(10, 6))
    subset = df[df['versao'].isin([2, 3])] # Comparar SIMD vs Paralelo
    
    sns.lineplot(data=subset, x='N', y='bandwidth_medio', hue='threads', style='versao', markers=True, palette="viridis")
    
    plt.xscale('log')
    plt.title("Vazão de Memória (Throughput)")
    plt.xlabel("Tamanho do Vetor (N)")
    plt.ylabel("Vazão Efetiva (GB/s)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/1_bandwidth.png")
    plt.close()

def plot_efficiency(df_agg):
    # Analisa eficiência apenas no maior N
    max_n = df_agg['N'].max()
    subset = df_agg[(df_agg['versao'] == 3) & (df_agg['N'] == max_n)].copy()
    
    if not subset.empty:
        # Pega tempo base da V1 (Sequencial) para o mesmo N
        t_base = df_agg[(df_agg['versao'] == 1) & (df_agg['N'] == max_n)]['tempo_medio'].values[0]
        
        subset['speedup'] = t_base / subset['tempo_medio']
        subset['efficiency'] = subset['speedup'] / subset['threads']
        
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=subset, x='threads', y='efficiency', palette="rocket")
        plt.axhline(0.5, color='r', ls='--', label='50% Eficiência')
        plt.axhline(1.0, color='g', ls='--', label='Ideal')
        plt.legend()
        plt.title(f"Eficiência Paralela (N={max_n})")
        plt.ylabel("Eficiência (Speedup / Threads)")
        plt.ylim(0, 1.2)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height*100:.1f}%', (p.get_x() + p.get_width() / 2., height), 
                        ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/2_eficiencia.png")
        plt.close()

def plot_stability(df):
    plt.figure(figsize=(10, 6))
    # Foca na V3 para ver variação entre threads
    subset = df[df['versao'] == 3]
    
    # Gráfico com barras de erro (intervalo de confiança 95%)
    sns.lineplot(data=subset, x='N', y='tempo_kernel', hue='threads', marker='o', errorbar=('ci', 95))
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Estabilidade: Tempo x N (Log-Log)")
    plt.xlabel("N")
    plt.ylabel("Tempo (s)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/3_estabilidade.png")
    plt.close()

if __name__ == "__main__":
    main()