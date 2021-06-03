#include <iostream>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

using namespace std;

void cleanup_handler(void *arg) {
   cout << "Someone canceling me!" << endl;
}

void* func(void *arg) {
    pthread_cleanup_push(&cleanup_handler, NULL);
    cout << "Child thread started" << endl;
    for (int i = 1; i <= 25; i++) {
        usleep(500);
        cout << "(Child) Line number: " << i << endl;
    }
    pthread_cleanup_pop(1);
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
