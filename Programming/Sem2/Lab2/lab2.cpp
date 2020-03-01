#include <iostream>

using namespace std;

/*
10. Клас дробів
Базовий клас (правильний дріб, менший 1):
Конструктори: за замовчуванням, з параметрами та копіювання.
Деструктор.
Функції:
додавання;
віднімання;
множення;
виведення інформації на екран.
Похідний клас: довільний дріб (з цілю частиною).
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


class Any_Fraction : public Fraction
{
    public:
        Any_Fraction(int num, int den);
};

Any_Fraction::Any_Fraction(int num, int den) {
    if (den == 0) {
        cout << "Error: division by zero!\n";
        cout << 1/0;
    }
    numerator = num;
    denominator = den;
}


int main()
{
    Fraction f1 = Fraction(2, 3);
    Fraction f2 = Fraction(1, 3);
    cout << "f1: ";
    f1.print();
    cout << "\nf2: ";
    f2.print();

    f1.addition(f2);
    cout << "\nf1 + f2: ";
    f1.print();

    f1 = Fraction(2, 3);
    f2 = Fraction(1, 3);
    f1.subtraction(f2);
    cout << "\nf1 - f2: ";
    f1.print();

    f1 = Fraction(2, 3);
    f2 = Fraction(1, 3);
    f1.multiplication(f2);
    cout << "\nf1 * f2: ";
    f1.print();

    Any_Fraction f3 = Any_Fraction(4, 3);
    Any_Fraction f4 = Any_Fraction(3, 2);
    cout << "\n\nf3: ";
    f3.print();
    cout << "\nf4: ";
    f4.print();

    f3.addition(f4);
    cout << "\nf3 + f4: ";
    f3.print();
    cout << "\n";
    return 0;
}
