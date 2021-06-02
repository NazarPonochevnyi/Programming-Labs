#include <tchar.h>
#include <windows.h>
#include <stdio.h>
#include <strsafe.h>
#include <atlstr.h>
#include <vector>
#include <string>
#include <sstream>
#include <stdlib.h>

using namespace std;

#define BUFSIZE 4096
#define MAX_ADMINS 5
#define MAX_THREADS 50
#define MAX_ROOMS 15

typedef long long int mInt;

struct Request {
    string clientName = "";
    mInt desiredPrice = 0;
    mInt vacStart = 0;
    mInt vacDuration = 1;
};
struct Response {
    string adminName = "";
    mInt status = -1;
    mInt rNumber = 0;
    mInt rPrice = 0;
};

class Room {
public:
    Room(mInt num = 0, mInt fare = 10, string strSch = "");
    ~Room();
    bool isFree(mInt start, mInt duration = 1);
    void book(mInt start, mInt duration = 1);
    mInt number;
    mInt price;
protected:
    vector<mInt> sheet;
    mInt sheetLen = 0;
    HANDLE ghRoomMutex;
};
Room::Room(mInt num, mInt fare, string strSch) {
    ghRoomMutex = CreateMutex(
        NULL,
        FALSE,
        NULL);
    if (ghRoomMutex == NULL)
    {
        printf("CreateMutex error: %d\n", GetLastError());
    }
    number = num;
    price = fare;
    if (strSch.size() > 0) {
        string buf;
        stringstream ss(strSch);
        vector<string> strs;
        while (ss >> buf)
            strs.push_back(buf);
        if (strs.size() > 0) {
            sheetLen = stoi(strs[0]);
            mInt strs_len = sheetLen * 2;
            strs.erase(strs.begin());
            for (mInt i = 0; i < strs_len; i++) {
                sheet.push_back(stoi(strs[i]));
            }
        }
    }
}
Room::~Room() {
    CloseHandle(ghRoomMutex);
}
bool Room::isFree(mInt start, mInt duration) {
    DWORD dwWaitResult = WaitForSingleObject(
        ghRoomMutex,
        INFINITE);
    if (sheetLen > 0) {
        mInt loopLen = sheetLen * 2;
        for (mInt i = 0; i < loopLen; i += 2) {
            if (start + duration > sheet[i] && start < sheet[i] + sheet[i + 1])
                return FALSE;
        }
    }
    return TRUE;
    ReleaseMutex(ghRoomMutex);
}
void Room::book(mInt start, mInt duration) {
    DWORD dwWaitResult = WaitForSingleObject(
        ghRoomMutex,
        INFINITE);
    sheetLen++;
    sheet.push_back(start);
    sheet.push_back(duration);
    ReleaseMutex(ghRoomMutex);
}

Room rooms[MAX_ROOMS];

class Admin {
public:
    string name;
    Admin(string n);
    Response check(Request req);
    bool book(string clientName, mInt number, mInt start, mInt duration = 1);
};
Admin::Admin(string n) {
    name = n;
}
Response Admin::check(Request req) {
    Response res;
    printf("[Admin %s -> Client %s] Searching room for %lld price from %lld during %lld period... \n", name.c_str(), req.clientName.c_str(), req.desiredPrice, req.vacStart, req.vacDuration);
    for (mInt i = 0; i < MAX_ROOMS; i++) {
        Sleep(500);
        Room& room = rooms[i];
        if (room.isFree(req.vacStart, req.vacDuration)) {
            if (room.price > req.desiredPrice) {
                printf("[Admin %s -> Client %s] Room %lld is free, but has greater price: %lld. Are you agree? \n", name.c_str(), req.clientName.c_str(), room.number, room.price);
                res = { name, 0, room.number, room.price };
                return res;
            }
            printf("[Admin %s -> Client %s] Room %lld is free and has affortable price: %lld. Are you agree? \n", name.c_str(), req.clientName.c_str(), room.number, room.price);
            res = { name, 1, room.number, room.price };
            return res;
        }
        printf("Room %lld is already occupied for this period. \n", room.number);
    }
    res.adminName = name;
    res.status = -1;
    return res;
}
bool Admin::book(string clientName, mInt number, mInt start, mInt duration) {
    for (mInt i = 0; i < MAX_ROOMS; i++) {
        Sleep(500);
        Room& room = rooms[i];
        if (room.number == number) {
            if (room.isFree(start, duration)) {
                room.book(start, duration);
                printf("[Admin %s -> Client %s] Room %lld is successfully booked from %lld during %lld period. \n", name.c_str(), clientName.c_str(), room.number, start, duration);
                return TRUE;
            }
            printf("Room %lld is already occupied for this period. \n", room.number);
            return FALSE;
        }
    }
    printf("Room %lld not found. \n", number);
    return FALSE;
}

class Client {
public:
    string name;
    Client(string n);
    bool request(Admin& admin);
    void showInfo();
protected:
    mInt vdesiredPrice = 0;
    mInt vMoney = 0;
    mInt vStart = 0;
    mInt vDuration = 0;
    mInt vBookedRoom = 0;
};
Client::Client(string n) {
    name = n;
    vMoney = rand() % 1100;
    vdesiredPrice = rand() % vMoney;
    vStart = rand() % 90 + 1;
    vDuration = rand() % 20 + 1;
}
bool Client::request(Admin& admin) {
    Request req = { name, vdesiredPrice, vStart, vDuration };
    printf("\n[Client %s -> Admin %s] Requesting room for %lld price from %lld during %lld period... \n", name.c_str(), admin.name.c_str(), req.desiredPrice, req.vacStart, req.vacDuration);
    Response res = admin.check(req);
    if (res.status == 1) {
        vMoney -= res.rPrice;
        vBookedRoom = res.rNumber;
        printf("[Client %s -> Admin %s] Yes, awesome\n", name.c_str(), res.adminName.c_str());
        return admin.book(name, res.rNumber, vStart, vDuration);
    }
    if (res.status == 0 && res.rPrice <= vMoney) {
        vMoney -= res.rPrice;
        vBookedRoom = res.rNumber;
        printf("[Client %s -> Admin %s] Okay, fortunatly, I have enough money\n", name.c_str(), res.adminName.c_str());
        return admin.book(name, res.rNumber, vStart, vDuration);
    }
    printf("[Client %s -> Admin %s] No, it is too expensive for me. I leaving your hotel!\n", name.c_str(), res.adminName.c_str());
    return FALSE;
}
void Client::showInfo() {
    printf("Client %s: %lld for room, %lld at all, start %lld, duration %lld, room %lld \n", name.c_str(), vdesiredPrice, vMoney, vStart, vDuration, vBookedRoom);
}

DWORD Child2ProcessId = GetCurrentProcessId();
TCHAR sTargetFilePath[MAX_PATH];

HANDLE ghWriteEvent;
DWORD WINAPI AdminThreadFunction(LPVOID lpParam);
DWORD WINAPI ClientThreadFunction(LPVOID lpParam);

struct AdminThreadParams {
    Admin admin = Admin("");
    HANDLE ghAdminMutex;
};

struct ClientThreadParams {
    Client client = Client("");
    mInt threadSleepTime = 0;
    mInt adminId = 0;
};

AdminThreadParams   threadAdmins[MAX_ADMINS];

HANDLE hPipe;
TCHAR  chBuf[BUFSIZE];
BOOL   fSuccess = FALSE;
DWORD  cbRead, cbToWrite, cbWritten, dwMode;
LPCTSTR lpszPipename = TEXT("\\\\.\\pipe\\mynamedpipe");

DWORD WINAPI ClientThreadFunction(LPVOID lpParam)
{
    ClientThreadParams* params = (ClientThreadParams*)lpParam;
    Client& client = params->client;
    mInt& threadSleepTime = params->threadSleepTime;
    mInt& adminId = params->adminId;
    Admin& admin = threadAdmins[adminId].admin;
    HANDLE& ghAdminMutex = threadAdmins[adminId].ghAdminMutex;

    BOOL rSuccess;
    DWORD ClientThreadId = GetCurrentThreadId();
    printf("(%d - %d) Client thread created and waiting for %lld ms...\n", Child2ProcessId, ClientThreadId, threadSleepTime);
    Sleep(threadSleepTime);

    DWORD dwWaitResult = WaitForSingleObject(
        ghAdminMutex,
        INFINITE);
    rSuccess = client.request(admin);
    ReleaseMutex(ghAdminMutex);

    if (rSuccess)
    {
        _tprintf(TEXT("(%d - %d) Room successfully booked\n"), Child2ProcessId, ClientThreadId);
    }
    else
        _tprintf(TEXT("(%d - %d) Room cannot be booked\n"), Child2ProcessId, ClientThreadId);

    return 0;
}

DWORD WINAPI AdminThreadFunction(LPVOID lpParam)
{
    AdminThreadParams* params = (AdminThreadParams*)lpParam;
    Admin& admin = params->admin;

    Request req;
    Response res;
    DWORD AdminThreadId = GetCurrentThreadId();
    printf("(%d - %d) Admin thread created and waiting for requests...\n", Child2ProcessId, AdminThreadId);

    while (TRUE) {
        // Start block
        res = admin.check(req);
        if (res.status) {
            admin.book();
            _tprintf(TEXT("(%d - %d) Room successfully booked\n"), Child2ProcessId, AdminThreadId);
        }
        else
            _tprintf(TEXT("(%d - %d) Room cannot be booked\n"), Child2ProcessId, AdminThreadId);
        // End block
    };
    return 0;
}

int _tmain(int argc, TCHAR* argv[])
{
    if (argc != 2)
    {
        _tprintf(TEXT("Usage: %s <target file>\n"), argv[0]);
        return 1;
    }

    StringCchCopy(sTargetFilePath, MAX_PATH, argv[1]);

    printf("(%d) Child2 process running.... \n", Child2ProcessId);

    // Open an Event.
    ghWriteEvent = OpenEvent(
        EVENT_ALL_ACCESS,
        TRUE,
        TEXT("WriteEvent")
    );

    if (ghWriteEvent == NULL)
    {
        printf("OpenEvent failed (%d)\n", GetLastError());
        return 1;
    }

    printf("(%d) Waiting for event from Child1 process... \n", Child2ProcessId);
    WaitForSingleObject(ghWriteEvent, 10000);

    // Connect to Named Pipe.
    while (1)
    {
        hPipe = CreateFile(
            lpszPipename,
            GENERIC_READ |
            GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            0,
            NULL);

        if (hPipe != INVALID_HANDLE_VALUE)
            break;

        if (GetLastError() != ERROR_PIPE_BUSY)
        {
            _tprintf(TEXT("(%d) Could not open pipe. GLE=%d\n"), Child2ProcessId, GetLastError());
            return -1;
        }

        if (!WaitNamedPipe(lpszPipename, 20000))
        {
            printf("(%d) Could not open pipe: 20 second wait timed out.", Child2ProcessId);
            return -1;
        }
    }

    dwMode = PIPE_READMODE_MESSAGE;
    fSuccess = SetNamedPipeHandleState(
        hPipe,
        &dwMode,
        NULL,
        NULL);

    if (!fSuccess)
    {
        _tprintf(TEXT("SetNamedPipeHandleState failed. GLE=%d\n"), GetLastError());
        return -1;
    }

    // Create Admin Threads.
    DWORD               dwAdmThreadIdArray[MAX_ADMINS];
    HANDLE              hAdmThreadArray[MAX_ADMINS];

    for (mInt i = 0; i < MAX_ADMINS; i++) {
        threadAdmins[i] = { Admin(to_string(i + 1)), CreateMutex(NULL, FALSE, NULL) };
        hAdmThreadArray[i] = CreateThread(
            NULL,
            0,
            AdminThreadFunction,
            &threadAdmins[i],
            0,
            &dwAdmThreadIdArray[i]);
        if (hAdmThreadArray[i] == NULL)
        {
            _tprintf(TEXT("Admin CreateThread Error"));
            ExitProcess(3);
        }
    }

    // Create Client Threads.
    DWORD               dwThreadIdArray[MAX_THREADS];
    HANDLE              hThreadArray[MAX_THREADS];
    ClientThreadParams  threadClients[MAX_THREADS];

    for (mInt i = 0; i < MAX_THREADS; i++) {
        threadClients[i] = { Client(to_string(i + 1)), rand() % 10000 + 1000, rand() % MAX_ADMINS };
        hThreadArray[i] = CreateThread(
            NULL,
            0,
            ClientThreadFunction,
            &threadClients[i],
            0,
            &dwThreadIdArray[i]);
        if (hThreadArray[i] == NULL)
        {
            _tprintf(TEXT("CreateThread Error"));
            ExitProcess(3);
        }
    }

    WaitForMultipleObjects(MAX_THREADS, hThreadArray, TRUE, INFINITE);
    WaitForMultipleObjects(MAX_ADMINS, hAdmThreadArray, TRUE, INFINITE);

    // Close all thread handles and free memory allocations.
    CloseHandle(ghWriteEvent);
    for (mInt i = 0; i < MAX_ADMINS; i++)
        CloseHandle(threadAdmins[i].ghAdminMutex);
    for (mInt i = 0; i < MAX_THREADS; i++)
        CloseHandle(hThreadArray[i]);
    for (mInt i = 0; i < MAX_ADMINS; i++)
        CloseHandle(hAdmThreadArray[i]);

    // Close Pipe.
    CloseHandle(hPipe);

    return 0;
}
