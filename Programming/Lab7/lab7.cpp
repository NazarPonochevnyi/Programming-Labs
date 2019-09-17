#include <iostream>
#include <cassert>
#include <string>

using namespace std;

/*
Реалізувати варіанти завдань з лабораторного практикуму № 1

4. Ввести три числа a, b, c.
Подвоїти кожне з них, якщо  a>=b>=c,
інакше поміняти значення a  та b.

з урахуванням наступних додаткових вимог.

7.5.1. Математичний вираз повинен обчислюватись у
окремій користувацькій функції.
7.5.2. Коректність вхідних даних повинна перевірятись
за допомогою механізма перехвату виключень мови С++.
7.5.3. При виконанні завдання забезпечити дворівневу
перевірку двома способами: – за допомогою
вкладених блоків try; – шляхом перехвату виключень
у основній програмі та у функції, що викликається.

2. За допомогою механізму обробки стандартних
виключень та макросу assert забезпечити перевірку
коректності введених даних.
*/

bool is_number(const std::string& s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it)) ++it;
    return !s.empty() && it == s.end();
}

void my_func(int &a, int &b, int &c) {
    assert(a > 0 && b > 0 && c > 0);
    if (a >= b && b >= c)
        a *= 2, b *= 2, c *= 2;
    else
        swap(a, b);
}

int main()
{
    int a = 0, b = 0, c = 0;
    string s_a = "", s_b = "", s_c = "";

    try {
        cout << "Input number a: ";
        getline(cin, s_a);

        cout << "Input number b: ";
        getline(cin, s_b);

        cout << "Input number c: ";
        getline(cin, s_c);

        if (is_number(s_a) && is_number(s_b) && is_number(s_c))
            a = stoi(s_a), b = stoi(s_b), c = stoi(s_c);
        else
            //cout << "error" << endl;
            throw exception();
    }
    catch(...) {
        cout << "\n[ERROR] You entered data in the wrong format! [Numbers expected]\n" << endl;
        return 1;
    }

    my_func(a, b, c);

    cout << "a:\t" << a << endl;
    cout << "b:\t" << b << endl;
    cout << "c:\t" << c << endl;
    return 0;
}
