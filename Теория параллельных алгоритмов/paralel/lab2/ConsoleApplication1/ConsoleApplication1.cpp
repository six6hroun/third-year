#include <iostream>
#include <omp.h>
#include <vector>
#include <iomanip>
#include <cmath>

using namespace std;

void sequentialJacobi(const vector<vector<double>>& A,
    const vector<double>& b,
    vector<double>& x,
    double tolerance,
    int maxIterations) {
    int n = A.size();
    vector<double> x_new(n, 0.0);

    for (int iter = 0; iter < maxIterations; iter++) {
        double maxDiff = 0.0;

        for (int i = 0; i < n; i++) {
            double sum = 0.0;
            for (int j = 0; j < n; j++) {
                if (j != i) {
                    sum += A[i][j] * x[j];
                }
            }
            x_new[i] = (b[i] - sum) / A[i][i];

            double diff = fabs(x_new[i] - x[i]);
            if (diff > maxDiff) maxDiff = diff;
        }

        x = x_new;

        if (maxDiff < tolerance) {
            break;
        }
    }
}

void parallelJacobi(const vector<vector<double>>& A,
    const vector<double>& b,
    vector<double>& x,
    double tolerance,
    int maxIterations,
    int num_threads) {
    int n = A.size();
    vector<double> x_new(n, 0.0);

    for (int iter = 0; iter < maxIterations; iter++) {
        double maxDiff = 0.0;

#pragma omp parallel num_threads(num_threads)
        {
            double local_maxDiff = 0.0;

#pragma omp for
            for (int i = 0; i < n; i++) {
                double sum = 0.0;
                for (int j = 0; j < n; j++) {
                    if (j != i) {
                        sum += A[i][j] * x[j];
                    }
                }
                x_new[i] = (b[i] - sum) / A[i][i];

                double diff = fabs(x_new[i] - x[i]);
                if (diff > local_maxDiff) local_maxDiff = diff;
            }

#pragma omp critical
            {
                if (local_maxDiff > maxDiff) maxDiff = local_maxDiff;
            }
        }

        x = x_new;

        if (maxDiff < tolerance) {
            break;
        }
    }
}

void generateDiagonallyDominantMatrix(vector<vector<double>>& A, int n) {
    for (int i = 0; i < n; i++) {
        double sum = 0.0;
        for (int j = 0; j < n; j++) {
            if (i != j) {
                A[i][j] = (rand() % 10) / 10.0 + 0.1;
                sum += fabs(A[i][j]);
            }
        }
        A[i][i] = sum + (rand() % 5 + 1);
    }
}

void generateB(const vector<vector<double>>& A,
    const vector<double>& x_true,
    vector<double>& b) {
    int n = A.size();
    for (int i = 0; i < n; i++) {
        b[i] = 0;
        for (int j = 0; j < n; j++) {
            b[i] += A[i][j] * x_true[j];
        }
    }
}

int main() {
    setlocale(LC_ALL, "RU");

    vector<int> sizes = { 120, 250, 500, 800 };
    vector<int> threads = { 1, 2, 3, 4 };

    double tolerance = 1e-6;
    int maxIterations = 1000;

    cout << fixed << setprecision(6);
    cout << "МЕТОД ЯКОБИ\n";

    for (int n : sizes) {
        cout << "\n--- Размер системы: " << n << " ---\n";

        vector<vector<double>> A(n, vector<double>(n));
        vector<double> b(n);
        vector<double> x_true(n);
        vector<double> x(n, 0.0);

        for (int i = 0; i < n; i++) {
            x_true[i] = rand() % 10 + 1;
        }

        generateDiagonallyDominantMatrix(A, n);
        generateB(A, x_true, b);

        double start, end;

        for (int t : threads) {
            x.assign(n, 0.0);

            if (t == 1) {
                start = omp_get_wtime();
                sequentialJacobi(A, b, x, tolerance, maxIterations);
                end = omp_get_wtime();
            }
            else {
                start = omp_get_wtime();
                parallelJacobi(A, b, x, tolerance, maxIterations, t);
                end = omp_get_wtime();
            }

            double time = end - start;

            if (t == 1) {
                cout << "Последовательный (1 поток): " << time << " с\n";
            }
            else {
                cout << "  Потоков " << t << ": " << time << " с\n";
            }
        }
    }


    return 0;
}