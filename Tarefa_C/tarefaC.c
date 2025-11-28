#include <stdio.h>
#include <stdlib.h>
#include <string.h> // Memset
#include <omp.h>
#include <sys/time.h> // Função temporal 

double get_time(){
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec * 1e-6;
}

// V1: Função sequencial
void saxpy_v1_seq(long N, float a, float *x, float *y){
    for (long i = 0; i < N; i++){
        y[i] = a * x[i] + y[i];
    }
}

// V2: Sequencial + vetorial
void saxpy_v2_omp_simd(long N, float a, float *x, float *y){
    #pragma omp simd
    for (long i = 0; i < N; i ++){
        y[i] = a * x[i] + y[i];
    }
}

// V3: Paralelo + vetorial
void saxpy_v3_omp_parallel_for_simd(long N, float a, float *x, float *y){
    #pragma omp parallel for simd
    for (long i = 0; i < N; i++){
        y[i] = a * x[i] + y[i];
    }
}

// Inicializar vetores
void init_vectors
(long N, float *x, float *y){
    for(long i = 0; i < N; i++){
        x[i] = (float)i * 0.5f;
        y[i] = (float)i * 1.5f;
    }
}

// Soma de alguns elementos
float simple_check(long N, float *y){
    float sum = 0.0f;
    for (long i = 0; i < N; i+=N/10) {
        sum += y[i];
    } 
    return sum;
}

int main(int argc, char *argv[]){
    if (argc != 4) {
        fprintf(stderr, "Uso: %s <versao> <N> <num_threads>\n", argv[0]);
        fprintf(stderr, "versao: 1=seq, 2=smd, 3=par simd\n");
        return 1;       
    }

    int versao = atoi(argv[1]);
    long N = atol(argv[2]);
    int threads = atoi(argv[3]);

    if (N <= 0 || versao < 1 || versao > 3 || threads <= 0){
        printf("Argumento invalido");
        return 1;
    }

    if (versao == 3){
        omp_set_num_threads(threads); // Numero de threadh do OPENMP
    }

    float a = 2.0f;
    float *x, *y;
    
    x = (float *)malloc(N * sizeof(float));
    y = (float *)malloc(N * sizeof(float));

    if (!x || !y){
        printf("Erro de alocacao \n");
        free(x);
        free(y);
        return 1;
    }

    init_vectors(N, x, y);
    double start_time, end_time, kernel_time;
    float check_sum = 0.0f;

    start_time = get_time();

    switch(versao){
        case 1: // Seq
            saxpy_v1_seq(N, a, x, y);
            break;
        case 2: // SIMD
            saxpy_v2_omp_simd(N, a, x, y);
            break;
        case 3:  // la ele SIMD
            saxpy_v3_omp_parallel_for_simd(N, a, x, y);
            break;
    }

    end_time = get_time();
    kernel_time = end_time - start_time;
    check_sum = simple_check(N, y);

    printf("%d, %ld, %d, %.6f, %.2f\n", versao, N, threads, kernel_time, check_sum);

    free(x);
    free(y);

    return 0;
}