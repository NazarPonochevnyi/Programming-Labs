#include <iostream>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <vector>
#include <cstdlib>

using namespace std;

void* func(void *arg) {
    string str = *reinterpret_cast<string*>(arg);
    for (int i = 1; i <= 2; i++) {
        usleep(500);
        cout << str << " and " << i << endl;
    }
    pthread_exit(NULL);
}

int main(void) {
    cout << "Parent thread started" << endl;

    pthread_t tid[4];
    vector<string> text {
        "Amazing first text",
        "Second line here",
        "Why we need third text?",
        "Ohh! That is the last 4 string"
    };

    for (int i = 0; i < 4; i++) {
        pthread_create(&(tid[i]), NULL, &func, &text[i]);
    }
    for (int i = 0; i < 4; i++) {
        pthread_join(tid[i], NULL);
    }

    return 0;
}
