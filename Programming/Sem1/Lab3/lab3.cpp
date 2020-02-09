#include <iostream>

using namespace std;

/*
23. Реалізувати рекурсивну функцію для
обчислення найбільшого спільного дільника
двох натуральних чисел A та B, використовуючи
алгоритм Евкліда.
*/

typedef unsigned long long int N_num;

N_num nsd(N_num a, N_num b) {
    if (b == 0)
        return a;
    else if (a < b)
        nsd(b, a);
    else
        nsd(a % b, b);
}

int main()
{
    N_num num1, num2;

    cout << "Input first number: ";
    cin >> num1;

    cout << "Input second number: ";
    cin >> num2;

    cout << "NSD: " << nsd(num1, num2) << endl;
    return 0;
}
