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
    Node L = create_list();

    append_item(L, 1.0);
    append_item(L, 2.0);
    append_item(L, 2.0);
    append_item(L, 3.0);
    append_item(L, 3.0);
    append_item(L, 3.0);
    append_item(L, 4.0);
    show_list(L);

    cout << "\n2 in list: " << in_list(L, 2.0) << endl;
    cout << "10 in list: " << in_list(L, 10.0) << endl;

    cout << "\nAmount of 3 in list: " << count_item(L, 3.0) << endl;

    cout << "\nMax item in list: " << max_item(L) << endl;

    cout << "\nReplace 3 by 4:" << endl;
    replace_item(L, 3.0, 4.0);
    show_list(L);

    cout << "\nList writed in List.txt" << endl;
    write_to_file(L, "List.txt");

    return 0;
}
