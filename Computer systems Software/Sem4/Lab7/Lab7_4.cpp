#include <iostream>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

using namespace std;

void* func(void *arg) {
    cout << "Child thread started" << endl;
    for (int i = 1; i <= 25; i++) {
        usleep(500);
        cout << "(Child) Line number: " << i << endl;
    }
    pthread_exit(NULL);
}

int main(void) {
    cout << "Parent thread started" << endl;

    pthread_t thread;
    pthread_create(&thread, NULL, &func, NULL);

    usleep(5000);
    pthread_cancel(thread);
    cout << "Child thread canceled by parent" << endl;

    return 0;
}
