#include <iostream>

using namespace std;

/*
4. Ввести три числа a, b, c.
Подвоїти кожне з них, якщо  a>=b>=c,
інакше поміняти значення a  та b.
*/

int main()
{
    int a, b, c;

    cout << "Input number a: ";
    cin >> a;

    cout << "Input number b: ";
    cin >> b;

    cout << "Input number c: ";
    cin >> c;

    if (a >= b && b >= c) {
        a *= 2;
        b *= 2;
        c *= 2;
    }
    else {
        int temp = a;
        a = b;
        b = temp;
    }

    cout << "a:\t" << a << endl;
    cout << "b:\t" << b << endl;
    cout << "c:\t" << c << endl;
    return 0;
}
