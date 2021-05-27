#include <tchar.h>
#include <windows.h>
#include <stdio.h>
#include <strsafe.h>

#define BUFSIZE 4096

DWORD Child1ProcessId = GetCurrentProcessId();

int _tmain(int argc, TCHAR* argv[])
{
    HANDLE hFile;
    HANDLE hAppend;
    DWORD  dwBytesRead, dwBytesWritten, dwPos;
    BYTE   buff[BUFSIZE];

    if (argc != 3)
    {
        _tprintf(TEXT("Usage: %s <data file> <copy file>\n"), argv[0]);
        return 1;
    }

    printf("(%d) Child1 process running.... \n", Child1ProcessId);

    printf("(%d) Sleep for 5 secs... \n", Child1ProcessId);
    Sleep(5000);

    // Connect to Named Pipe.
    HANDLE hPipe;
    TCHAR  chBuf[BUFSIZE];
    BOOL   fSuccess = FALSE;
    DWORD  cbRead, cbToWrite, cbWritten, dwMode;
    LPCTSTR lpszPipename = TEXT("\\\\.\\pipe\\mynamedpipe");

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
            _tprintf(TEXT("(%d) Could not open pipe. GLE=%d\n"), Child1ProcessId, GetLastError());
            return -1;
        }

        if (!WaitNamedPipe(lpszPipename, 20000))
        {
            printf("(%d) Could not open pipe: 20 second wait timed out.", Child1ProcessId);
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

    // Open the existing file.

    hFile = CreateFile(argv[1],
        GENERIC_READ,
        0,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL);

    if (hFile == INVALID_HANDLE_VALUE)
    {
        printf("Could not open One.txt.");
        return 1;
    }

    // Create a new file.

    hAppend = CreateFile(argv[2],
        FILE_WRITE_DATA,
        FILE_SHARE_READ,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        NULL);

    if (hAppend == INVALID_HANDLE_VALUE)
    {
        printf("Could not open Two.txt.");
        return 1;
    }

    while (ReadFile(hFile, buff, sizeof(buff), &dwBytesRead, NULL)
        && dwBytesRead > 0)
    {
        dwPos = SetFilePointer(hAppend, 0, NULL, FILE_END);
        LockFile(hAppend, dwPos, 0, dwBytesRead, 0);
        WriteFile(hAppend, buff, dwBytesRead, &dwBytesWritten, NULL);
        UnlockFile(hAppend, dwPos, 0, dwBytesRead, 0);
    }

    // Close both files.

    CloseHandle(hFile);
    CloseHandle(hAppend);

    // Send a message to the pipe server.

    TCHAR lpvMessage[MAX_PATH];
    StringCchPrintf(lpvMessage, MAX_PATH, TEXT("(%d) Created file %s"), Child1ProcessId, argv[2]);

    cbToWrite = (lstrlen(lpvMessage) + 1) * sizeof(TCHAR);

    fSuccess = WriteFile(
        hPipe,
        lpvMessage,
        cbToWrite,
        &cbWritten,
        NULL);

    if (!fSuccess)
    {
        _tprintf(TEXT("(%d) WriteFile to pipe failed. GLE=%d\n"), Child1ProcessId, GetLastError());
        return -1;
    }

    // Close Pipe.
    CloseHandle(hPipe);

	return 0;
}
