#include <iostream>

using namespace std;

/*
10. Перевантажити оператори потокового введення-виведення (>>,<<).
*/

class Fraction
{
    protected:
        int numerator, denominator;
        int nod(int a, int b);
        int nok(int a, int b);
    public:
        Fraction();
        Fraction(int num, int den);
        Fraction(const Fraction& f);
        void addition(const Fraction& f);
        void subtraction(const Fraction& f);
        void multiplication(const Fraction& f);
        void print();
        ~Fraction();
        friend Fraction operator +(const Fraction& a, const Fraction& b);
        Fraction& operator =(const Fraction& d);
        friend istream& operator >>(istream& s, Fraction& f);
        friend ostream& operator <<(ostream& s, const Fraction& f);
};

Fraction::Fraction() {
    numerator = 1;
    denominator = 2;
}

Fraction::Fraction(int num, int den) {
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

Fraction::Fraction(const Fraction& f) {
    numerator = f.numerator;
    denominator = f.denominator;
}

int Fraction::nod(int a, int b) {
    while (a != 0 && b != 0) {
        if (a > b) {
            a = a % b;
        }
        else b = b % a;
    }
    return a + b;
}

int Fraction::nok(int a, int b) {
    return a * b / Fraction::nod(a, b);
}

void Fraction::addition(const Fraction& f) {
    int cd = nok(denominator, f.denominator);
    numerator = (numerator * (cd / denominator)) + (f.numerator * (cd / f.denominator));
    denominator = cd;
}

void Fraction::subtraction(const Fraction& f) {
    Fraction f1 = Fraction(f);
    f1.numerator *= -1;
    Fraction::addition(f1);
}

void Fraction::multiplication(const Fraction& f) {
    numerator *= f.numerator;
    denominator *= f.denominator;
}

void Fraction::print() {
    cout << numerator << "/" << denominator;
}

Fraction::~Fraction() {
    numerator = 0;
    denominator = 0;
}

Fraction operator +(const Fraction& a, const Fraction& b) {
    Fraction c = Fraction(a);
    c.addition(b);
    return c;
}

Fraction& Fraction::operator =(const Fraction& f) {
    numerator = f.numerator;
    denominator = f.denominator;
    return *this;
}

istream& operator >>(istream& s, Fraction& f) {
    cout << "Enter fraction:\n";
    s >> f.numerator;
    cout << "--\n";
    s >> f.denominator;
    return s;
}

ostream& operator <<(ostream& s, const Fraction& f) {
    s << f.numerator << "/" << f.denominator;
    return s;
}


class Any_Fraction : public Fraction
{
    public:
        Any_Fraction();
        Any_Fraction(int num, int den);
        Any_Fraction(const Any_Fraction& f);
};

Any_Fraction::Any_Fraction() {
    numerator = 1;
    denominator = 2;
}

Any_Fraction::Any_Fraction(int num, int den) {
    if (den == 0) {
        cout << "Error: division by zero!\n";
        cout << 1/0;
    }
    numerator = num;
    denominator = den;
}

Any_Fraction::Any_Fraction(const Any_Fraction& f) {
    numerator = f.numerator;
    denominator = f.denominator;
}


int main()
{
    Fraction f1, f2, f3;
    cin >> f1;
    cin >> f2;

    f3 = f1 + f2;
    cout << "f1 + f2: " << f3;

    return 0;
}
