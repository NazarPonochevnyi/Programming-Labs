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
Node<T> create_list() {
    Node<T> L;
    L.prev = NULL;
    L.data = NULL;
    L.next = NULL;
    return L;
}

template <typename T>
void append_item(Node<T> &L, T item) {
    if (L.data == NULL) {
        L.prev = NULL;
        L.data = item;
        L.next = NULL;
    } else {
        Node<T> *L_tail = &L;
        while ((*L_tail).next != NULL)
            L_tail = (*L_tail).next;
        Node<T> *L_next = new Node<T>;
        L_next->prev = L_tail;
        L_next->data = item;
        L_next->next = NULL;
        (*L_tail).next = L_next;
    }
}

template <typename T>
bool in_list(Node<T> &L, T item) {
    if (L.data == item)
        return true;
    if (L.next == NULL)
        return false;
    return in_list(*L.next, item);
}

template <typename T>
unsigned int count_item(Node<T> &L, T item, unsigned int amount = 0) {
    if (L.data == item)
        amount += 1;
    if (L.next == NULL)
        return amount;
    return count_item(*L.next, item, amount);
}

template <typename T>
T max_item(Node<T> &L) {
    T result = L.data;
    Node<T> *L_tail = &L;
    while ((*L_tail).next != NULL)
        L_tail = (*L_tail).next;
        if ((*L_tail).data > result)
            result = (*L_tail).data;
    return result;
}

template <typename T1, typename T2>
void replace_item(Node<T1> &L, T1 item1, T2 item2) {
    if (L.data == item1)
        L.data = item2;
    if (L.next != NULL)
        replace_item(*L.next, item1, item2);
}

template <typename T>
void write_to_file(Node<T> &L, string filename, string result = "") {
    if (L.next == NULL) {
        ofstream file;
        file.open(filename);
        result = result + to_string(L.data) + " ";
        file << result << endl;
        file.close();
    } else {
        write_to_file(*L.next, filename, result + to_string(L.data) + " ");
    }
}

template <typename T>
void show_list(Node<T> &L, string result = "") {
    if (L.next == NULL) {
        result = result + to_string(L.data) + " ";
        cout << "List: " << result << endl;
    } else {
        show_list(*L.next, result + to_string(L.data) + " ");
    }
}

int main() {
    typedef long long int ListType;
    Node<ListType> L = create_list<ListType>();

    append_item<ListType>(L, 1);
    append_item<ListType>(L, 2);
    append_item<ListType>(L, 2);
    append_item<ListType>(L, 3);
    append_item<ListType>(L, 3);
    append_item<ListType>(L, 3);
    append_item<ListType>(L, 4);
    show_list<ListType>(L);

    cout << "\n2 in list: " << in_list<ListType>(L, 2) << endl;
    cout << "10 in list: " << in_list<ListType>(L, 10) << endl;

    cout << "\nAmount of 3 in list: " << count_item<ListType>(L, 3) << endl;

    cout << "\nMax item in list: " << max_item<ListType>(L) << endl;

    cout << "\nReplace 3 by 4:" << endl;
    replace_item<ListType, ListType>(L, 3, 4);
    show_list<ListType>(L);

    cout << "\nList writed in List.txt" << endl;
    write_to_file<ListType>(L, "List.txt");

    return 0;
}
