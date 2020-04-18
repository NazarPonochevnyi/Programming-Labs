#include <iostream>

using namespace std;

/*
Спроектувати шаблон для класу, створити відповідні структури
простих (наприклад, список чисел або рядків) і складних даних (наприклад,
список об’єктів іншого класу) і продемонструвати роботу з ними.
*/

template <class T>
class Fraction
{
    protected:
        T numerator, denominator;
        T nod(T a, T b);
        T nok(T a, T b);
    public:
        Fraction();
        Fraction(T num, T den);
        Fraction(const Fraction<T>& f);
        void addition(const Fraction<T>& f);
        void subtraction(const Fraction<T>& f);
        void multiplication(const Fraction<T>& f);
        void print();
        ~Fraction();
        friend Fraction<T> operator +(const Fraction<T>& a, const Fraction<T>& b);
        Fraction<T>& operator =(const Fraction<T>& d);
        friend istream& operator >>(istream& s, Fraction<T>& f);
        friend ostream& operator <<(ostream& s, const Fraction<T>& f);
};

template <class T>
Fraction<T>::Fraction() {
    numerator = 1;
    denominator = 2;
}

template <class T>
Fraction<T>::Fraction(T num, T den) {
    if (den == 0) {
        cout << "Error: division by zero!\n";
        cout << 1/0;
    }
    if (num >= den) {
        cout << "Error: fraction must be < 1! Use Any_Fraction fraction.\n";
        cout << 1/0;
    }
    numerator = num;
    denominator = den;
}

template <class T>
Fraction<T>::Fraction(const Fraction<T>& f) {
    numerator = f.numerator;
    denominator = f.denominator;
}

template <class T>
T Fraction<T>::nod(T a, T b) {
    while (a != 0 && b != 0) {
        if (a > b) {
            a = a % b;
        }
        else b = b % a;
    }
    return a + b;
}

template <class T>
T Fraction<T>::nok(T a, T b) {
    return a * b / Fraction<T>::nod(a, b);
}

template <class T>
void Fraction<T>::addition(const Fraction<T>& f) {
    T cd = nok(denominator, f.denominator);
    numerator = (numerator * (cd / denominator)) + (f.numerator * (cd / f.denominator));
    denominator = cd;
}

template <class T>
void Fraction<T>::subtraction(const Fraction<T>& f) {
    Fraction<T> f1 = Fraction(f);
    f1.numerator *= -1;
    Fraction<T>::addition(f1);
}

template <class T>
void Fraction<T>::multiplication(const Fraction<T>& f) {
    numerator *= f.numerator;
    denominator *= f.denominator;
}

template <class T>
void Fraction<T>::print() {
    cout << numerator << "/" << denominator;
}

template <class T>
Fraction<T>::~Fraction() {
    numerator = 0;
    denominator = 0;
}

template <class T>
Fraction<T> operator +(const Fraction<T>& a, const Fraction<T>& b) {
    Fraction<T> c = Fraction<T>(a);
    c.addition(b);
    return c;
}

template <class T>
Fraction<T>& Fraction<T>::operator =(const Fraction<T>& f) {
    numerator = f.numerator;
    denominator = f.denominator;
    return *this;
}

template <class T>
istream& operator >>(istream& s, Fraction<T>& f) {
    cout << "Enter fraction:\n";
    s >> f.numerator;
    cout << "--\n";
    s >> f.denominator;
    return s;
}

template <class T>
ostream& operator <<(ostream& s, const Fraction<T>& f) {
    s << f.numerator << "/" << f.denominator;
    return s;
}


template <class T>
class Any_Fraction : public Fraction<T>
{
    public:
        Any_Fraction();
        Any_Fraction(T num, T den);
        Any_Fraction(const Any_Fraction<T>& f);
};

template <class T>
Any_Fraction<T>::Any_Fraction() {
    this->numerator = 1;
    this->denominator = 2;
}

template <class T>
Any_Fraction<T>::Any_Fraction(T num, T den) {
    if (den == 0) {
        cout << "Error: division by zero!\n";
        cout << 1/0;
    }
    this->numerator = num;
    this->denominator = den;
}

template <class T>
Any_Fraction<T>::Any_Fraction(const Any_Fraction<T>& f) {
    this->numerator = f.numerator;
    this->denominator = f.denominator;
}


int main()
{
    int a, b, c, d;
    cout << "Input f1 fraction: ";
    cin >> a >> b;
    Fraction<int> f1(a, b);
    cout << "Input f2 fraction: ";
    cin >> c >> d;
    Fraction<int> f2(c, d);

    f1.addition(f2);
    cout << "f1 + f2: ";
    f1.print();

    return 0;
}
