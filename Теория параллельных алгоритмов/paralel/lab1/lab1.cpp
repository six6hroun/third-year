#include <iostream>
#include <omp.h>
#include <vector>
#include <iomanip>
#include <fstream>
#include <cmath>

using namespace std;
void sequentialMultiply(const vector<vector<double>>& A,
    const vector<vector<double>>& B,
    vector<vector<double>>& C) {
    int n = A.size();

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0;
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}


void parallelStriped(const vector<vector<double>>& A,
    const vector<vector<double>>& B,
    vector<vector<double>>& C,
    int num_threads) {
    int n = A.size();

    #pragma omp parallel num_threads(num_threads)
    {
        int thread_id = omp_get_thread_num();
        int total_threads = omp_get_num_threads();

        int rows_per_thread = n / total_threads;
        int start_row = thread_id * rows_per_thread;
        int end_row = (thread_id == total_threads - 1) ? n : start_row + rows_per_thread;

        for (int i = start_row; i < end_row; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = 0;
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
}

void parallelBlocked(const vector<vector<double>>& A,
    const vector<vector<double>>& B,
    vector<vector<double>>& C,
    int num_threads,
    int block_size = 32) {
    int n = A.size();

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            C[i][j] = 0;

    #pragma omp parallel num_threads(num_threads)
    {
        #pragma omp for collapse(2) schedule(dynamic)
        for (int ib = 0; ib < n; ib += block_size) {
            for (int jb = 0; jb < n; jb += block_size) {
                int i_end = min(ib + block_size, n);
                int j_end = min(jb + block_size, n);

                for (int kb = 0; kb < n; kb += block_size) {
                    int k_end = min(kb + block_size, n);

                    for (int i = ib; i < i_end; i++) {
                        for (int j = jb; j < j_end; j++) {
                            double sum = 0;
                            for (int k = kb; k < k_end; k++) {
                                sum += A[i][k] * B[k][j];
                            }
                            #pragma omp atomic
                            C[i][j] += sum;
                        }
                    }
                }
            }
        }
    }
}

int main() {
    setlocale(LC_ALL, "RU");

    vector<int> sizes = { 120, 250, 500, 800 };
    vector<int> threads = { 1, 2, 3, 4 };

    ofstream fout("results.csv");
    fout << "Size;Algorithm;Threads;Time(s)\n";

    cout << fixed << setprecision(6);
    cout << "Умножение матриц\n";

    for (int n : sizes) {
        cout << "\nРазмер матрицы: " << n << "\n";

        vector<vector<double>> A(n, vector<double>(n));
        vector<vector<double>> B(n, vector<double>(n));
        vector<vector<double>> C(n, vector<double>(n));

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = rand() % 10 + 1;
                B[i][j] = rand() % 10 + 1;
            }
        }

        double start, end;

        start = omp_get_wtime();
        sequentialMultiply(A, B, C);
        end = omp_get_wtime();
        double seq_time = end - start;
        cout << "Последовательный: " << seq_time << " с\n";
        fout << n << ";Sequential;1;" << seq_time << "\n";

        for (int t : threads) {
            cout << "  Потоков: " << t << "\n";

            start = omp_get_wtime();
            parallelStriped(A, B, C, t);
            end = omp_get_wtime();
            double striped_time = end - start;
            cout << "    Ленточный: " << striped_time << " с\n";
            fout << n << ";Striped;" << t << ";" << striped_time << "\n";

            start = omp_get_wtime();
            parallelBlocked(A, B, C, t, 32);
            end = omp_get_wtime();
            double blocked_time = end - start;
            cout << "    Блочный: " << blocked_time << " с\n";
            fout << n << ";Blocked;" << t << ";" << blocked_time << "\n";
        }

        fout.flush();
    }

    fout.close();
    return 0;
}