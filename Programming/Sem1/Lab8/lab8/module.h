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

struct Node {
    Node* prev;
    double data;
    Node* next;
};

Node create_list();
void append_item(Node &L, double item);
bool in_list(Node &L, double item);
unsigned int count_item(Node &L, double item, unsigned int amount = 0);
double max_item(Node &L);
void replace_item(Node &L, double item1, double item2);
void write_to_file(Node &L, string filename, string result = "");
void show_list(Node &L, string result = "");
