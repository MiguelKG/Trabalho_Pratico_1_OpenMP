#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

int main() {

    double total_start = omp_get_wtime();

    int n_values[] = {100000, 500000, 1000000};
    int n_total = 3;

    int threads_values[] = {1, 2, 4, 8, 16};
    int threads_total = 5;

    int loop_size = 5;
    int test_num = 1;

    int n_max = 0;
    for (int i = 0; i < n_total; i++) {
        if (n_values[i] > n_max) {
            n_max = n_values[i];
        }
    }

    FILE *csv = fopen("resultados_d.csv", "w");
    if (!csv) {
        printf("Erro ao criar CSV\n");
        return 1;
    }
    fprintf(csv,
        "n,threads,media_ingenua,media_arrumada,"
        "variancia_ingenua,variancia_arrumada,"
        "desvio_ingenua,desvio_arrumada\n"
    );

    int *v1 = malloc(n_max * sizeof(int));
    int *v2 = malloc(n_max * sizeof(int));

    printf("\nTarefa D - Organização De Região Paralela\n");
    for (int ni = 0; ni < n_total; ni++) {

        int n = n_values[ni];

        for (int ti = 0; ti < threads_total; ti++) {

            int t = threads_values[ti];
            omp_set_num_threads(t);

            printf("\n--- Teste %d ---\n", test_num);
            printf("%d elementos e %d thread(s)\n\n", n, t);

            double sum_1 = 0.0, sum_2 = 0.0;

            double loop_values_1[5];
            double loop_values_2[5];

            for (int r = 0; r < loop_size; r++) {

                double t_start_1 = omp_get_wtime();

                #pragma omp parallel for
                for (int i = 0; i < n; i++) {
                    v1[i] = i;
                }

                #pragma omp parallel for
                for (int i = 0; i < n; i++) {
                    v2[i] = 2 * i;
                }

                double t_end_1 = omp_get_wtime();
                double time_1 = t_end_1 - t_start_1;

                double t_start_2 = omp_get_wtime();

                #pragma omp parallel
                {
                    #pragma omp for
                    for (int i = 0; i < n; i++) {
                        v1[i] = i;
                    }

                    #pragma omp for
                    for (int i = 0; i < n; i++) {
                        v2[i] = 2 * i;
                    }
                }

                double t_end_2 = omp_get_wtime();
                double time_2 = t_end_2 - t_start_2;

                sum_1 += time_1;
                sum_2 += time_2;

                loop_values_1[r] = time_1;
                loop_values_2[r] = time_2;

                printf("Ciclo %d: Ingenua = %.6f s | Arrumada = %.6f s\n", r + 1, time_1, time_2);
            }

            double average_1 = sum_1 / loop_size;
            double average_2 = sum_2 / loop_size;

            double variance_1 = 0.0, variance_2 = 0.0;

            for (int i = 0; i < loop_size; i++) {
                variance_1 += (loop_values_1[i] - average_1) * (loop_values_1[i] - average_1);
                variance_2 += (loop_values_2[i] - average_2) * (loop_values_2[i] - average_2);
            }

            variance_1 /= loop_size;
            variance_2 /= loop_size;

            double deviation_1 = sqrt(variance_1);
            double deviation_2 = sqrt(variance_2);

            printf("\n");
            printf("Média Ingenua  = %.6f s | Variância = %.6f | Desvio = %.6f\n",
                average_1, variance_1, deviation_1);

            printf("Média Arrumada = %.6f s | Variância = %.6f | Desvio = %.6f\n",
                average_2, variance_2, deviation_2);
            printf("----------------\n");

            fprintf(csv, "%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                n, t,
                average_1, average_2,
                variance_1, variance_2,
                deviation_1, deviation_2
            );

            test_num++;
        }
    }

    free(v1);
    free(v2);
    fclose(csv);
    
    double total_end = omp_get_wtime();
    double total_time = total_end - total_start;

    printf("\nTempo total de execução: %.6f s\n", total_time);

    return 0;
}