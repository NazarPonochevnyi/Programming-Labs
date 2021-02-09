#include <iostream>
#include <chrono>
#include <vector>
#include <list>

using namespace std;

/*
4. Надрукувати всі слова, які відрізняються від першого слова.
Перед друком подвоїти першу літеру, якщо в слові парна кількість літер,
та видалити останню літеру, якщо в слові непарна кількість літер.
Якщо слів менше, ніж два, видати повідомлення.
*/


template <typename T>
void show_array(T L) {
    for (auto n : L)
        cout << n;
    cout << endl;
}

template <typename T>
void task(T &arrayString) {
    vector<T> arrayWords;
    T arrayWord;
    for (auto data : arrayString) {
        if (data != ' ' && data != '.')
            arrayWord.push_back(data);
        else {
            arrayWords.push_back(arrayWord);
            arrayWord = {};
        }
    }
    arrayWord.clear();

    T first_array_word = arrayWords.front();
    unsigned int index = 0;
    for (auto i = arrayWords.begin(); i != arrayWords.end(); ++i) {
        if (first_array_word == arrayWords[index]) {
            arrayWords[index].clear();
            arrayWords.erase(i);
            i--;
        }
        else
            index++;
    }
    first_array_word.clear();

    unsigned int words_count = arrayWords.size();

    if (words_count == 0)
        cout << "No words to print" << endl;
    else if (words_count == 1)
        show_array<T>(arrayWords[0]);
    else {
        for (auto i = arrayWords.begin(); i != arrayWords.end(); ++i) {
            if (arrayWords[0].size() % 2 == 0)
                arrayWords[0].insert(arrayWords[0].begin(), arrayWords[0].front());
            else
                arrayWords[0].pop_back();
            show_array<T>(arrayWords[0]);
            arrayWords[0].clear();
            arrayWords.erase(i);
            i--;
        }
    }
    cout << endl;
}


int main() {
    char line, symbol;

    // Create array and list
    vector<char> arrayString;
    list<char> listString;

    // Read input
    cout << "Input string:" << endl;
    while (true) {
        cin.get(line);
        symbol = line;
        if ((symbol >= 'a' && symbol <= 'z') || symbol == ' ' || symbol == '.') {
            if (symbol != ' ' || (symbol == ' ' && listString.back() != ' '))
                listString.push_back(symbol);
                arrayString.push_back(symbol);
            if (symbol == '.')
                break;
        }
        else
            cout << "Wrong value: '" << symbol << "'" << endl;
    }


    unsigned int num_repeat = 1000;

    // Perform task with array
    auto array_start = chrono::steady_clock::now();

    for (unsigned int i = 0; i < num_repeat; i++)
        task<vector<char>>(arrayString);

    auto array_stop = chrono::steady_clock::now();
    auto array_diff = array_stop - array_start;


    // Perform task with list
    auto list_start = chrono::steady_clock::now();

    for (unsigned int i = 0; i < num_repeat; i++)
        task<list<char>>(listString);

    auto list_stop = chrono::steady_clock::now();
    auto list_diff = list_stop - list_start;


    // Show parsed input, size of array and list, and execution times
    cout << "Parsed words: ";
    show_array<list<char>>(listString);
    cout << "(array) Size in bytes: " << sizeof(vector<char>) + (sizeof(char) * arrayString.size()) << endl;
    cout << "(list) Size in bytes: " << listString.size() * sizeof(char*) << endl;
    cout << "(array) Execution time: " << chrono::duration<double, milli> (array_diff).count() << " ms" << endl;
    cout << "(list) Execution time: " << chrono::duration<double, milli> (list_diff).count() << " ms" << endl;

    arrayString.clear();
    listString.clear();
    cout << "All memory cleared after " << num_repeat << " repeats." << endl;

    return 0;
}
