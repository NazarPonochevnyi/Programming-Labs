#include <iostream>

using namespace std;

/* Char Doubled Linked List */


struct Node {
    Node* prev;
    char data;
    Node* next;
    Node(char);
};

Node::Node(char value) {
    data = value;
    next = prev = NULL;
}


class DoublyLinkedList {
    public:
        DoublyLinkedList();
        ~DoublyLinkedList();
        unsigned int length();
        bool is_empty();
        void append_left(char);
        void append(char);
        void insert(unsigned int, char);
        char pop_left();
        char pop();
        char delete_item(unsigned int);
        bool search(char);
        void show();

    protected:
        Node* head;
        Node* tail;
        unsigned int size;
};

DoublyLinkedList::DoublyLinkedList() {
    head = tail = NULL;
    size = 0;
}

DoublyLinkedList::~DoublyLinkedList() {
    while (!is_empty())
        pop();
}

unsigned int DoublyLinkedList::length() {
    return size;
}

bool DoublyLinkedList::is_empty() {
    if (size <= 0)
        return true;
    return false;
}

void DoublyLinkedList::append_left(char value) {
    Node* node = new Node(value);

    if (head == NULL)
        head = tail = node;
    else {
        head->prev = node;
        node->next = head;
        head = node;
    }
    size++;
}

void DoublyLinkedList::append(char value) {
    Node* node = new Node(value);

    if (tail == NULL)
        head = tail = node;
    else {
        tail->next = node;
        node->prev = tail;
        tail = node;
    }
    size++;
}

void DoublyLinkedList::insert(unsigned int index, char value) {
    if (index == 0)
        append_left(value);
    else if (index >= size)
        append(value);
    else {
        Node* node = new Node(value);

        Node* temp = head;
        unsigned int i = 0;
        while (temp) {
            if (i == index) {
                node->prev = temp->prev;
                node->next = temp;
                temp->prev->next = node;
                temp->prev = node;
                break;
            }
            temp = temp->next;
            i++;
        }
        size++;
    }
}

char DoublyLinkedList::pop_left() {
    if (!is_empty()) {
        Node* temp = head;
        char delValue = temp->data;
        if (head == tail) {
            tail = NULL;
            head = NULL;
        }
        else {
            head = head->next;
            head->prev = NULL;
        }
        delete temp;
        size--;
        return delValue;
    }
    else
        cout << "Doubly Linked List is empty" << endl;
    return 0;
}

char DoublyLinkedList::pop() {
    if (!is_empty()) {
        Node* temp = tail;
        char delValue = temp->data;
        if (head == tail) {
            head = NULL;
            tail = NULL;
        }
        else {
            tail = tail->prev;
            tail->next = NULL;
        }
        delete temp;
        size--;
        return delValue;
    }
    else
        cout << "Doubly Linked List is empty" << endl;
    return 0;
}

char DoublyLinkedList::delete_item(unsigned int index) {
    if (!is_empty()) {
        if (index == 0)
            return pop_left();
        else if (index == size - 1)
            return pop();
        else {
            Node* temp = head;

            unsigned int i = 0;
            while (temp) {
                if (i == index) {
                    char delValue = temp->data;
                    temp->prev->next = temp->next;
                    temp->next->prev = temp->prev;
                    delete temp;
                    size--;
                    return delValue;
                }
                temp = temp->next;
                i++;
            }
            cout << "Index out of range" << endl;
        }
    }
    else
        cout << "Doubly Linked List is empty" << endl;
    return 0;
}

bool DoublyLinkedList::search(char value) {
    if (!is_empty()) {
        Node* temp = head;
        while (temp) {
            if (temp->data == value)
                return true;
            temp = temp->next;
        }
        return false;
    }
    cout << "Doubly Linked List is empty" << endl;
    return false;
}

void DoublyLinkedList::show() {
    cout << "Doubly Linked List: ";
    if (!is_empty()) {
        Node* temp = head;

        cout << "NULL <- " << temp->data;
        while (temp->next != NULL) {
            temp = temp->next;
            cout << " <-> " << temp->data;
        }
        cout << " -> NULL" << endl;
    }
    else
        cout << "NULL" << endl;
}


int main()
{
    DoublyLinkedList* L = new DoublyLinkedList();
    L->show();
    cout << "Length: " << L->length() << endl;
    cout << "Empty: " << L->is_empty() << endl;
    L->pop();

    cout << "\nAppend 'b'" << endl;
    L->append('b');
    cout << "Append 'd'" << endl;
    L->append('d');
    cout << "Append 'e'" << endl;
    L->append('e');
    cout << "Append left 'a'" << endl;
    L->append_left('a');
    cout << "Insert in 2 index 'c'" << endl;
    L->insert(2, 'c');
    L->show();

    cout << "\n'e' in list: " << L->search('e') << endl;
    cout << "'z' in list: " << L->search('z') << endl;
    cout << "Length: " << L->length() << endl;
    cout << "Empty: " << L->is_empty() << endl;

    cout << "\nDelete item: " << L->pop() << endl;
    cout << "Delete item: " << L->pop_left() << endl;
    cout << "Delete item: " << L->delete_item(1) << endl;
    L->show();

    cout << "\nDelete item: " << L->pop() << endl;
    cout << "Delete item: " << L->pop() << endl;
    L->show();

    delete L;
    cout << "\nDoubly Linked List cleared from memory" << endl;

    return 0;
}
