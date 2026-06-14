#include <iostream>
#include <omp.h>
#include <vector>
#include <iomanip>
#include <cmath>

using namespace std;

double f(double x) {
    return sin(x);
}

double sequentialSimpson(double a, double b, int n) {
    double h = (b - a) / n;
    double sum = f(a) + f(b);

    for (int i = 1; i < n; i++) {
        double x = a + i * h;
        if (i % 2 == 0) {
            sum += 2 * f(x);
        }
        else {
            sum += 4 * f(x);
        }
    }

    return sum * h / 3.0;
}

double parallelSimpson(double a, double b, int n, int num_threads) {
    double h = (b - a) / n;
    double sum = f(a) + f(b);

    #pragma omp parallel num_threads(num_threads)
    {
        double local_sum = 0.0;

        #pragma omp for
        for (int i = 1; i < n; i++) {
            double x = a + i * h;
            if (i % 2 == 0) {
                local_sum += 2 * f(x);
            }
            else {
                local_sum += 4 * f(x);
            }
        }

        #pragma omp atomic
        sum += local_sum;
    }

    return sum * h / 3.0;
}

int main() {
    setlocale(LC_ALL, "RU");

    double a = 0.0;
    double b = 3.14159265358979323846;
    vector<int> intervals = { 1000, 2700, 5000, 8000 };
    vector<int> threads = { 1, 2, 3, 4 };

    cout << fixed << setprecision(6);
    cout << "МЕТОД СИМПСОНА\n";
    cout << "Интеграл: sin(x) на [0, pi]\n";

    cout << "Разбиений | 1 поток | 2 потока | 3 потока | 4 потока\n";
    cout << "--------------------------------------------------------\n";

    for (int n : intervals) {
        if (n % 2 != 0) n++;

        cout << setw(9) << n << " |";

        for (int t : threads) {
            double start, end, result;

            if (t == 1) {
                start = omp_get_wtime();
                result = sequentialSimpson(a, b, n);
                end = omp_get_wtime();
            }
            else {
                start = omp_get_wtime();
                result = parallelSimpson(a, b, n, t);
                end = omp_get_wtime();
            }

            cout << " " << setw(8) << (end - start) << " |";
        }
        cout << "\n";
    }

    cout << "========================================================\n";

    return 0;
}