#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

/*
14. Дано натуральне число n.
Написати програму, яка виводить число,
записане цифрами числа n в зворотному
порядку.
*/

int main()
{
    unsigned long long int n;
    cout << "Input number: ";
    cin >> n;

    string s_n;
    s_n = to_string(n);

    reverse(s_n.begin(), s_n.end());

    n = stoi(s_n);
    cout << "Output number: " << n << endl;
    return 0;
}
