#include <iostream>
#include <omp.h>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <algorithm>

using namespace std;

void sequentialBubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

void parallelBubbleSort(vector<int>& arr, int num_threads) {
    int n = arr.size();

    for (int i = 0; i < n - 1; i++) {
        if (i % 2 == 0) {
            #pragma omp parallel for num_threads(num_threads)
            for (int j = 0; j < n - 1; j += 2) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr[j], arr[j + 1]);
                }
            }
        }
        else {
            #pragma omp parallel for num_threads(num_threads)
            for (int j = 1; j < n - 1; j += 2) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr[j], arr[j + 1]);
                }
            }
        }
    }
}

void sequentialShellSort(vector<int>& arr) {
    int n = arr.size();
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                arr[j] = arr[j - gap];
            }
            arr[j] = temp;
        }
    }
}

void parallelShellSort(vector<int>& arr, int num_threads) {
    int n = arr.size();

    for (int gap = n / 2; gap > 0; gap /= 2) {
        #pragma omp parallel for num_threads(num_threads)
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                arr[j] = arr[j - gap];
            }
            arr[j] = temp;
        }
    }
}

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void sequentialQuickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        sequentialQuickSort(arr, low, pi - 1);
        sequentialQuickSort(arr, pi + 1, high);
    }
}

void parallelQuickSort(vector<int>& arr, int low, int high, int num_threads, int depth = 0) {
    if (low < high) {
        int pi = partition(arr, low, high);

        if (depth < 2) {
            #pragma omp parallel sections num_threads(2)
            {
                #pragma omp section
                {
                    parallelQuickSort(arr, low, pi - 1, num_threads, depth + 1);
                }
                #pragma omp section
                {
                    parallelQuickSort(arr, pi + 1, high, num_threads, depth + 1);
                }
            }
        }
        else {
            sequentialQuickSort(arr, low, pi - 1);
            sequentialQuickSort(arr, pi + 1, high);
        }
    }
}

void generateArray(vector<int>& arr, int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 10000;
    }
}

void copyArray(const vector<int>& src, vector<int>& dst) {
    for (int i = 0; i < src.size(); i++) {
        dst[i] = src[i];
    }
}

bool isSorted(const vector<int>& arr) {
    for (int i = 1; i < arr.size(); i++) {
        if (arr[i] < arr[i - 1]) return false;
    }
    return true;
}

int main() {
    setlocale(LC_ALL, "RU");

    vector<int> sizes = { 1000, 5000, 10000, 50000 };
    vector<int> threads = { 1, 2, 4 };

    cout << fixed << setprecision(6);
    cout << "СРАВНЕНИЕ АЛГОРИТМОВ СОРТИРОВКИ\n";

    for (int n : sizes) {
        cout << "\n========== РАЗМЕР МАССИВА: " << n << " ==========\n";

        vector<int> original(n);
        vector<int> arr(n);
        generateArray(original, n);

        cout << "\n--- СОРТИРОВКА ПУЗЫРЬКОМ ---\n";
        for (int t : threads) {
            copyArray(original, arr);
            double start, end;

            if (t == 1) {
                start = omp_get_wtime();
                sequentialBubbleSort(arr);
                end = omp_get_wtime();
            }
            else {
                start = omp_get_wtime();
                parallelBubbleSort(arr, t);
                end = omp_get_wtime();
            }

            if (t == 1)
                cout << "  Последовательный (1 поток): " << (end - start) << " с\n";
            else
                cout << "  Потоков " << t << ": " << (end - start) << " с\n";
        }

        cout << "\n--- СОРТИРОВКА ШЕЛЛА ---\n";
        for (int t : threads) {
            copyArray(original, arr);
            double start, end;

            if (t == 1) {
                start = omp_get_wtime();
                sequentialShellSort(arr);
                end = omp_get_wtime();
            }
            else {
                start = omp_get_wtime();
                parallelShellSort(arr, t);
                end = omp_get_wtime();
            }

            if (t == 1)
                cout << "  Последовательный (1 поток): " << (end - start) << " с\n";
            else
                cout << "  Потоков " << t << ": " << (end - start) << " с\n";
        }

        cout << "\n--- БЫСТРАЯ СОРТИРОВКА ---\n";
        for (int t : threads) {
            copyArray(original, arr);
            double start, end;

            if (t == 1) {
                start = omp_get_wtime();
                sequentialQuickSort(arr, 0, n - 1);
                end = omp_get_wtime();
            }
            else {
                start = omp_get_wtime();
                parallelQuickSort(arr, 0, n - 1, t);
                end = omp_get_wtime();
            }

            if (t == 1)
                cout << "  Последовательный (1 поток): " << (end - start) << " с\n";
            else
                cout << "  Потоков " << t << ": " << (end - start) << " с\n";
        }
    }

    cout << "\n========================================================\n";

    return 0;
}