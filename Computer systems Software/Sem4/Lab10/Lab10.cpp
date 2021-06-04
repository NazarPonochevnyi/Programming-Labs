#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("USAGE: ./Lab10 start\n");
        return 1;
    }

    string line;
    fstream file1, file2, file3;

    system("ls -la /proc/$$/fd");

    file1.open("file1.txt", ios::out);
    printf("\nOpened file for write: %s\n\n", "file1.txt");

    system("ls -la /proc/$$/fd");

    file2.open("file2.txt", ios::in);
    printf("\nOpened file for read: %s\n\n", "file2.txt");

    system("ls -la /proc/$$/fd");

    file3.open("file3.txt", ios::in);
    printf("\nOpened file for read: %s\n\n", "file3.txt");

    system("ls -la /proc/$$/fd");

    file3.close();
    file3.open("file3.txt", ios::out);
    printf("\nChanged file size to zero: %s\n\n", "file3.txt");

    system("ls -la /proc/$$/fd");

    while (getline(file2, line)) {
        file3 << line << '\n';
    }
    printf("\nCopied file2.txt to %s\n\n", "file3.txt");

    system("ls -la /proc/$$/fd");

    file1.close();
    file2.close();
    file3.close();

    printf("\nClose files and exit the program.\n");
    return 0;
}
