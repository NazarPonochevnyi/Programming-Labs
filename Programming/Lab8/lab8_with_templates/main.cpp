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
