#include <iostream>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

using namespace std;

pthread_t tid[2];

void* func(void *arg) {
    cout << "\nChild thread started" << endl;
    for (int i = 1; i <= 10; i++) {
        usleep(500);
        cout << "(Child) Line number: " << i << endl;
    }
}

int main(void) {
    cout << "\nParent thread started" << endl;
    tid[0] = pthread_self();

    pthread_create(&(tid[1]), NULL, &func, NULL);

    for (int i = 1; i <= 10; i++) {
        usleep(500);
        cout << "(Parent) Line number: " << i << endl;
    }

    return 0;
}
