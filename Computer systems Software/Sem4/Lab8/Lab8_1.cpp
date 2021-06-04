#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

typedef unsigned long int buffer_item;
#define BUFFER_SIZE 5
#define RAND_DIVISOR 100000000

sem_t lock, full, empty;
buffer_item buffer[BUFFER_SIZE];
int counter;

void *producer(void *param);
void *consumer(void *param);

void initializeData() {
    sem_init(&lock, 0, 1);
    sem_init(&full, 0, 0);
    sem_init(&empty, 0, BUFFER_SIZE);
    counter = 0;
    srand(time(NULL));
}

int insert_item(buffer_item item) {
   if (counter < BUFFER_SIZE) {
      buffer[counter] = item;
      counter++;
      return 0;
   }
   return -1;
}

int remove_item(buffer_item *item) {
   if (counter > 0) {
      *item = buffer[(counter-1)];
      counter--;
      return 0;
   }
   return -1;
}

void *producer(void *param) {
    buffer_item item;
    pthread_t tid = pthread_self();

    while (1) {
        int rNum = rand() / RAND_DIVISOR;
        usleep(rNum);

        item = rand() % 100000 + 1000;

        sem_wait(&empty);
        sem_wait(&lock);

        if (insert_item(item))
            printf("(%d) Producer report error condition\n", tid);
        else
            printf("(%d) producer produced %d\n", tid, item);

        sem_post(&lock);
        sem_post(&full);
    }
}

void *consumer(void *param) {
    buffer_item item;
    pthread_t tid = pthread_self();

    while (1) {
        int rNum = rand() / RAND_DIVISOR;
        usleep(rNum);

        sem_wait(&full);
        sem_wait(&lock);

        if (remove_item(&item))
            printf("(%d) Consumer report error condition\n", tid);
        else
            printf("(%d) consumer consumed %d\n", tid, item);

        sem_post(&lock);
        sem_post(&empty);
    }
}

int main(int argc, char *argv[]) {
    unsigned int i;

    if (argc != 4) {
        printf("USAGE: ./Lab8_1 <mainSleepTime> <numProd> <numCons>\n");
        return 1;
    }

    int mainSleepTime = atoi(argv[1]);
    int numProd = atoi(argv[2]);
    int numCons = atoi(argv[3]);

    pthread_t producerThreads[numProd];
    pthread_t consumerThreads[numCons];
    initializeData();

    for (i = 0; i < numProd; i++)
        pthread_create(&producerThreads[i], NULL, producer, NULL);
    for (i = 0; i < numCons; i++)
        pthread_create(&consumerThreads[i], NULL, consumer, NULL);

    usleep(mainSleepTime);

    for (i = 0; i < numProd; i++)
        pthread_cancel(producerThreads[i]);
    for (i = 0; i < numCons; i++)
        pthread_cancel(consumerThreads[i]);

    printf("Exit the program\n");
    return 0;
}
