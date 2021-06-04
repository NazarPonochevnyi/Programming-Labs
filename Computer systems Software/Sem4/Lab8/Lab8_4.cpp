#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <pthread.h>
#include <unistd.h>
#include <string>

#define RAND_DIVISOR 100000000

using namespace std;

int rNum;
string forkStatus = "ОOOOO";
struct timeval nowTime;
double msNowTime;
pthread_t philosopher[5];
pthread_mutex_t forks[5];

void* func(void *arg) {
    int n = *((int *) arg);
    while (1) {
        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d is thinking\n", msNowTime, n);

        rNum = rand() / RAND_DIVISOR;
        usleep(5000);

        pthread_mutex_lock(&forks[n]);
        forkStatus[n] = 'X';
        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d takes fork %d (left). Fork status %s\n", msNowTime, n, n, forkStatus.c_str());

        pthread_mutex_lock(&forks[(n + 1) % 5]);
        forkStatus[(n + 1) % 5] = 'X';
        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d takes fork %d (right). Fork status %s\n", msNowTime, n, (n + 1) % 5, forkStatus.c_str());

        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d is eating\n", msNowTime, n);

        rNum = rand() / RAND_DIVISOR;
        usleep(10000);

        pthread_mutex_unlock(&forks[n]);
        forkStatus[n] = 'O';
        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d leave fork %d (left). Fork status %s\n", msNowTime, n, n, forkStatus.c_str());

        pthread_mutex_unlock(&forks[(n + 1) % 5]);
        forkStatus[(n + 1) % 5] = 'O';
        gettimeofday(&nowTime, NULL);
        msNowTime = (nowTime.tv_sec) * 1000 + (nowTime.tv_usec) / 1000;
        printf("[%f] Philosopher %d leave fork %d (right). Fork status %s\n", msNowTime, n, (n + 1) % 5, forkStatus.c_str());

        printf("Philosopher %d finished eating\n", n);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("USAGE: ./Lab8_4 start\n");
        return 1;
    }

    unsigned int i;
    srand(time(NULL));
    int ids[] = {0, 1, 2, 3, 4};

    for (i = 0; i < 5; i++)
        pthread_mutex_init(&forks[i], NULL);
    for (i = 0; i < 5; i++) {
        pthread_create(&philosopher[i], NULL, func, &ids[i]);
    }

    for (i = 0; i < 5; i++)
        pthread_join(philosopher[i], NULL);
    for (i = 0; i < 5; i++)
        pthread_mutex_destroy(&forks[i]);

    printf("Exit the program\n");
    return 0;
}
