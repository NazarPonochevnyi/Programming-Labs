#include "module.h"

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

Node create_list() {
    Node L;
    L.prev = nullptr;
    L.data = NULL;
    L.next = nullptr;
    return L;
}

void append_item(Node &L, double item) {
    if (L.data == NULL) {
        L.prev = nullptr;
        L.data = item;
        L.next = nullptr;
    } else {
        Node *L_tail = &L;
        while ((*L_tail).next != nullptr)
            L_tail = (*L_tail).next;
        Node *L_next = new Node;
        L_next->prev = L_tail;
        L_next->data = item;
        L_next->next = nullptr;
        (*L_tail).next = L_next;
    }
}

bool in_list(Node &L, double item) {
    if (L.data == item)
        return true;
    if (L.next == nullptr)
        return false;
    return in_list(*L.next, item);
}

unsigned int count_item(Node &L, double item, unsigned int amount) {
    if (L.data == item)
        amount += 1;
    if (L.next == nullptr)
        return amount;
    return count_item(*L.next, item, amount);
}

double max_item(Node &L) {
    double result = L.data;
    Node *L_tail = &L;
    while ((*L_tail).next != nullptr)
        L_tail = (*L_tail).next;
        if ((*L_tail).data > result)
            result = (*L_tail).data;
    return result;
}

void replace_item(Node &L, double item1, double item2) {
    if (L.data == item1)
        L.data = item2;
    if (L.next != nullptr)
        replace_item(*L.next, item1, item2);
}

void write_to_file(Node &L, string filename, string result) {
    if (L.next == nullptr) {
        ofstream file;
        file.open(filename);
        result = result + to_string(L.data) + " ";
        file << result << endl;
        file.close();
    } else {
        write_to_file(*L.next, filename, result + to_string(L.data) + " ");
    }
}

void show_list(Node &L, string result) {
    if (L.next == nullptr) {
        result = result + to_string(L.data) + " ";
        cout << "List: " << result << endl;
    } else {
        show_list(*L.next, result + to_string(L.data) + " ");
    }
}
