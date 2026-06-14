#include <iostream>
#include <omp.h>
#include <vector>
#include <iomanip>
#include <cstdlib>

using namespace std;

const int INF = 1e9;

void sequentialFloydWarshall(vector<vector<int>>& dist, int n) {
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] < INF && dist[k][j] < INF) {
                    if (dist[i][j] > dist[i][k] + dist[k][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }
    }
}

void parallelFloydWarshall(vector<vector<int>>& dist, int n, int num_threads) {
    for (int k = 0; k < n; k++) {
#pragma omp parallel for num_threads(num_threads)
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] < INF && dist[k][j] < INF) {
                    if (dist[i][j] > dist[i][k] + dist[k][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }
    }
}

void generateGraph(vector<vector<int>>& dist, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                dist[i][j] = 0;
            }
            else {
                int r = rand() % 100;
                if (r < 30) { 
                    dist[i][j] = rand() % 10 + 1;
                }
                else {
                    dist[i][j] = INF;
                }
            }
        }
    }
}

void copyMatrix(const vector<vector<int>>& src, vector<vector<int>>& dst) {
    int n = src.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            dst[i][j] = src[i][j];
        }
    }
}

int main() {
    setlocale(LC_ALL, "RU");

    vector<int> sizes = { 100, 500,700, 900 };
    vector<int> threads = { 1, 2, 4 };

    cout << fixed << setprecision(6);
    cout << "ФЛОЙД-УОРШЕЛЛ\n";

    cout << "Размер | 1 поток | 2 потока | 4 потока\n";
    cout << "---------------------------------------\n";

    for (int n : sizes) {
        vector<vector<int>> original(n, vector<int>(n));
        vector<vector<int>> matrix(n, vector<int>(n));

        generateGraph(original, n);

        cout << setw(6) << n << " |";

        for (int t : threads) {
            copyMatrix(original, matrix);

            double start = omp_get_wtime();

            if (t == 1) {
                sequentialFloydWarshall(matrix, n);
            }
            else {
                parallelFloydWarshall(matrix, n, t);
            }

            double end = omp_get_wtime();

            cout << " " << setw(8) << (end - start) << " |";
        }
        cout << "\n";
    }

    cout << "========================================================\n";

    return 0;
}