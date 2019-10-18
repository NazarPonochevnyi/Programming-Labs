#include <iostream>
#include <fstream>
#include <string>

using namespace std;

/*
14. Використовувати (лінійні) односпрямовані списки без заголовної
ланки (мал. а) або з заголовною ланкою (мал. б) при наступному їхньому
описі
Параметр L позначає список, а параметри Е, Е1 — дані типу ТЕ, до яких
можна застосовувати операції присвоювання і перевірки на рівність. {ТЕ =
double}
Визначити рекурсивні функції, що:
а) визначає, чи входить елемент Е в список L;
б) підраховує число входжень елемента Е в список L;
в) знаходить максимальний елемент непорожнього списку L;
г) заміняє в списку L всі входження E1 на E2;
д) виводить список у файл.
*/

template <typename T>
struct Node {
    Node<T>* prev;
    T data;
    Node<T>* next;
};

template <typename T>
Node<T> create_list();

template <typename T>
void append_item(Node<T> &L, T item);

template <typename T>
bool in_list(Node<T> &L, T item);

template <typename T>
unsigned int count_item(Node<T> &L, T item, unsigned int amount = 0);

template <typename T>
T max_item(Node<T> &L);

template <typename T1, typename T2>
void replace_item(Node<T1> &L, T1 item1, T2 item2);

template <typename T>
void write_to_file(Node<T> &L, string filename, string result = "");

template <typename T>
void show_list(Node<T> &L, string result = "");
