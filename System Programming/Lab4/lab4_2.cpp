#include <tchar.h>
#include <windows.h>
#include <stdio.h>
#include <strsafe.h>
#include <string>
#include <atlstr.h>

#define BUFSIZE 4096
#define MAX_THREADS 2

DWORD Child2ProcessId = GetCurrentProcessId();
int iMatrix[3][3];
TCHAR sTargetFilePath[MAX_PATH];

HANDLE ghWriteEvent;
DWORD WINAPI FirstThreadFunction(LPVOID lpParam);
DWORD WINAPI SecondThreadFunction(LPVOID lpParam);

HANDLE hPipe;
TCHAR  chBuf[BUFSIZE];
BOOL   fSuccess = FALSE;
DWORD  cbRead, cbToWrite, cbWritten, dwMode;
LPCTSTR lpszPipename = TEXT("\\\\.\\pipe\\mynamedpipe");

int _tmain(int argc, TCHAR* argv[])
{
    if (argc != 2)
    {
        _tprintf(TEXT("Usage: %s <target file>\n"), argv[0]);
        return 1;
    }

    StringCchCopy(sTargetFilePath, MAX_PATH, argv[1]);

    printf("(%d) Child2 process running.... \n", Child2ProcessId);

    printf("(%d) Sleep for 10 secs... \n", Child2ProcessId);
    Sleep(10000);

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

    // Create an Event.
    ghWriteEvent = CreateEvent(
        NULL,
        TRUE,
        FALSE,
        TEXT("WriteEvent")
    );

    if (ghWriteEvent == NULL)
    {
        printf("CreateEvent failed (%d)\n", GetLastError());
        return 1;
    }

    // Create Threads.
    DWORD   dwThreadIdArray[MAX_THREADS];
    HANDLE  hThreadArray[MAX_THREADS];

    hThreadArray[0] = CreateThread(
        NULL,
        0,
        FirstThreadFunction,
        0,
        0,
        &dwThreadIdArray[0]);

    hThreadArray[1] = CreateThread(
        NULL,
        0,
        SecondThreadFunction,
        0,
        0,
        &dwThreadIdArray[1]);

    if (hThreadArray[0] == NULL || hThreadArray[1] == NULL)
    {
        _tprintf(TEXT("CreateThread Error"));
        ExitProcess(3);
    }

    WaitForMultipleObjects(MAX_THREADS, hThreadArray, TRUE, INFINITE);

    // Close all thread handles and free memory allocations.
    CloseHandle(ghWriteEvent);
    CloseHandle(hThreadArray[0]);
    CloseHandle(hThreadArray[1]);

    // Close Pipe.
    CloseHandle(hPipe);

    return 0;
}

DWORD WINAPI FirstThreadFunction(LPVOID lpParam)
{
    HANDLE hFile;
    DWORD  dwBytesRead;
    BYTE   buff[BUFSIZE];
    BOOL   bSuccess;

    DWORD Child1ThreadId = GetCurrentThreadId();
    printf("\n(%d - %d) First thread creating matrix...\n", Child2ProcessId, Child1ThreadId);


    hFile = CreateFile(sTargetFilePath,
        GENERIC_READ,
        0,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL);

    if (hFile == INVALID_HANDLE_VALUE)
    {
        printf("Could not open Two.txt \n");
        return 1;
    }

    bSuccess = ReadFile(hFile, buff, BUFSIZE, &dwBytesRead, NULL);
    if (!bSuccess) {
        printf("Error reading \n");
        return 1;
    }

    buff[dwBytesRead] = '\0';

    int i = 0, a = 0, b = 0;
    char digits[10] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
    BOOL wfinished = FALSE;
    while (!wfinished)
    {
        if (buff[i] == '\0')
        {
            wfinished = TRUE;
            break;
        }
        for (int j = 0; j < 10; j++)
        {
            if (buff[i] == digits[j])
            {
                iMatrix[a][b] = j;
                b++;
                if (b > 2)
                {
                    b = 0;
                    a++;
                }
                if (a > 3)
                    wfinished = TRUE;
                break;
            }
        }
        i++;
    }

    // Add sleep to show sync.
    Sleep(3000);

    _tprintf(TEXT("(%d - %d) Matrix filled by numbers from file\n"), Child2ProcessId, Child1ThreadId);

    CloseHandle(hFile);

    // Set ghWriteEvent to signaled.

    if (!SetEvent(ghWriteEvent))
    {
        printf("SetEvent failed (%d)\n", GetLastError());
        return 1;
    }

    return 0;
}

DWORD WINAPI SecondThreadFunction(LPVOID lpParam)
{
    std::string sMatrix;
    std::string sMatrixMul;
    TCHAR szMatrixMul[MAX_PATH];
    DWORD dwWaitResult;
    int iMmul = 1;

    DWORD Child2ThreadId = GetCurrentThreadId();
    printf("(%d - %d) Second thread waiting for write event...\n", Child2ProcessId, Child2ThreadId);

    dwWaitResult = WaitForSingleObject(
        ghWriteEvent,
        INFINITE);

    switch (dwWaitResult)
    {
    case WAIT_OBJECT_0:
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                iMmul *= iMatrix[i][j];
                sMatrix += std::to_string(iMatrix[i][j]) + " ";
            }
            sMatrixMul += std::to_string(iMmul) + " ";
            iMmul = 1;
            sMatrix += "\n";
        }
        sMatrixMul.pop_back();
        printf("(%d - %d) Matrix:\n%s", Child2ProcessId, Child2ThreadId, sMatrix.c_str());

        // Send a message to the pipe server.

        TCHAR lpvMessage[MAX_PATH];
        _tcscpy_s(szMatrixMul, CA2T(sMatrixMul.c_str()));
        StringCchPrintf(lpvMessage, MAX_PATH, TEXT("(%d - %d) Matrix multiplications: %s"), Child2ProcessId, Child2ThreadId, szMatrixMul);

        cbToWrite = (lstrlen(lpvMessage) + 1) * sizeof(TCHAR);

        fSuccess = WriteFile(
            hPipe,
            lpvMessage,
            cbToWrite,
            &cbWritten,
            NULL);

        if (!fSuccess)
        {
            _tprintf(TEXT("(%d) WriteFile to pipe failed. GLE=%d\n"), Child2ProcessId, GetLastError());
            return -1;
        }

        break;

    default:
        printf("Wait error (%d)\n", GetLastError());
        return 1;
    }

    return 0;
}
