#include <string>
#include <iostream>

using namespace std;


class Car
{
    private:
        string model, color, engine_type;
        int power = 0, mileage = 0;
    public:
        void setData();
        void getData();
};

void Car::setData()
{
    cout << "\n--- Car creating ---\n";
    cout << "Enter model:" << endl;
    cin >> model;
    cout << "\nEnter color:" << endl;
    cin >> color;
    cout << "\nEnter engine type:" << endl;
    cin >> engine_type;
    cout << "\nCar created!" << endl;
}

void Car::getData()
{
    cout << "\n--- Car parameters ---\n";
    cout << "Model: " << model << endl;
    cout << "Color: " << color << endl;
    cout << "Engine: " << engine_type << endl;
    cout << "Power: " << power << endl;
    cout << "Mileage: " << mileage << endl;
}


int main()
{
    Car Tesla;
    Car* BMW;

    Tesla.setData();
    Tesla.getData();

    BMW = new Car;
    BMW->setData();
    BMW->getData();

    return 0;
}
