#include <iostream>

using namespace std;

/* Char Dynamic Array */


class DynamicArray {
    public:
        DynamicArray();
        ~DynamicArray();
        unsigned int length();
        bool is_empty();
        void resize();
        void append_left(char);
        void append(char);
        void insert(unsigned int, char);
        char pop_left();
        char pop();
        char delete_item(unsigned int);
        bool search(char);
        void show();

    protected:
        size_t size;
        size_t capacity;
        char* array;
};

DynamicArray::DynamicArray() {
    size = 0;
    capacity = 1;
    array = new char[capacity];
    for (unsigned int i = 0; i < capacity; i++)
        array[i] = 0;
}

DynamicArray::~DynamicArray() {
    delete[] array;
}

unsigned int DynamicArray::length() {
    return size;
}

bool DynamicArray::is_empty() {
    if (size <= 0)
        return true;
    return false;
}

void DynamicArray::resize() {
    capacity *= 2;
    char* new_array = new char[capacity];
    for (unsigned int i = 0; i < size; i++)
        new_array[i] = array[i];
    delete[] array;
    array = new_array;
}

void DynamicArray::append_left(char value) {
    if (capacity <= size + 1)
        resize();
    for (int i = size - 1; i >= 0; i--)
        array[i + 1] = array[i];
    array[0] = value;
    size++;
}

void DynamicArray::append(char value) {
    if (capacity <= size + 1)
        resize();
    array[size] = value;
    size++;
}

void DynamicArray::insert(unsigned int index, char value) {
    if (0 <= index <= size) {
        if (capacity <= size + 1)
            resize();
        for (int i = size - 1; i >= index; i--)
            array[i + 1] = array[i];
        array[index] = value;
        size++;
    }
    else
        cout << "Index out of range" << endl;
}

char DynamicArray::pop_left() {
    if (!is_empty()) {
        char delValue = array[0];
        for (unsigned int i = 1; i < size; i++)
            array[i - 1] = array[i];
        size--;
        array[size] = 0;
        return delValue;
    }
    else
        cout << "Dynamic Array is empty" << endl;
    return 0;
}

char DynamicArray::pop() {
    if (!is_empty()) {
        size--;
        char delValue = array[size];
        array[size] = 0;
        return delValue;
    }
    else
        cout << "Dynamic Array is empty" << endl;
    return 0;
}

char DynamicArray::delete_item(unsigned int index) {
    if (!is_empty()) {
        if (0 <= index <= size - 1) {
            char delValue = array[index];
            for (unsigned int i = index + 1; i < size; i++)
                array[i - 1] = array[i];
            size--;
            array[size] = 0;
            return delValue;
        }
        else
            cout << "Index out of range" << endl;
    }
    else
        cout << "Dynamic Array is empty" << endl;
    return 0;
}

bool DynamicArray::search(char value) {
    if (!is_empty()) {
        for (unsigned int i = 0; i < size; i++) {
            if (array[i] == value)
                return true;
        }
        return false;
    }
    cout << "Dynamic Array is empty" << endl;
    return false;
}

void DynamicArray::show() {
    if (!is_empty()) {
        cout << "Dynamic Array: [";
        for (unsigned int i = 0; i < size - 1; i++)
            cout << array[i] << ", ";
        cout << array[size - 1] << "]" << endl;
    }
    else
        cout << "Dynamic Array: NULL" << endl;
}


int main()
{
    DynamicArray* arr = new DynamicArray();
    arr->show();
    cout << "Length: " << arr->length() << endl;
    cout << "Empty: " << arr->is_empty() << endl;
    arr->pop();

    cout << "\nAppend 'b'" << endl;
    arr->append('b');
    cout << "Append 'd'" << endl;
    arr->append('d');
    cout << "Append 'e'" << endl;
    arr->append('e');
    cout << "Append left 'a'" << endl;
    arr->append_left('a');
    cout << "Insert in 2 index 'c'" << endl;
    arr->insert(2, 'c');
    arr->show();

    cout << "\n'e' in array: " << arr->search('e') << endl;
    cout << "'z' in array: " << arr->search('z') << endl;
    cout << "Length: " << arr->length() << endl;
    cout << "Empty: " << arr->is_empty() << endl;

    cout << "\nDelete item: " << arr->pop() << endl;
    cout << "Delete item: " << arr->pop_left() << endl;
    cout << "Delete item: " << arr->delete_item(1) << endl;
    arr->show();

    cout << "\nDelete item: " << arr->pop() << endl;
    cout << "Delete item: " << arr->pop() << endl;
    arr->show();

    delete arr;
    cout << "\nDynamic Array cleared from memory" << endl;

    return 0;
}
