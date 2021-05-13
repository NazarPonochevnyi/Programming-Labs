#include <tchar.h>
#include <windows.h>
#include <stdio.h>
#include <strsafe.h>

#define BUFSIZE 4096

HANDLE child1InRead = NULL;
HANDLE W11 = NULL;
HANDLE R11 = NULL;

HANDLE child2InRead = NULL;
HANDLE W21 = NULL;
HANDLE R21 = NULL;

void CreateChild1Process() {

    TCHAR chNewEnv[BUFSIZE];
    LPTSTR lpszCurrentVariable;
    DWORD dwFlags = 0;
    TCHAR applicationName[] = TEXT("\"D:\\Microsoft Visual Studio\\Workspace\\SysProga\\Lab3_1\\Debug\\Lab3_1.exe\" \"D:\\Microsoft Visual Studio\\Workspace\\SysProga\\files\" \"D:\\Microsoft Visual Studio\\Workspace\\SysProga\\Lab3\\Debug\\FILE21\\FILE22\\FILE23\"");
    PROCESS_INFORMATION pi;
    STARTUPINFO si;
    BOOL success = FALSE;

    // Change env vars and not inherit it from parent process

    lpszCurrentVariable = (LPTSTR)chNewEnv;
    StringCchCopy(lpszCurrentVariable, BUFSIZE, TEXT("Date=05-2021"));

    lpszCurrentVariable += lstrlen(lpszCurrentVariable) + 1;
    *lpszCurrentVariable = (TCHAR)0;

    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
    ZeroMemory(&si, sizeof(STARTUPINFO));

    si.cb = sizeof(STARTUPINFO);
    si.hStdError = W11;
    si.hStdOutput = W11;
    si.dwFlags |= STARTF_USESTDHANDLES;

#ifdef UNICODE
    dwFlags = CREATE_UNICODE_ENVIRONMENT | CREATE_NEW_CONSOLE;
#endif

    // Start process of files coping

    success = CreateProcess(NULL, applicationName, NULL, NULL, TRUE, dwFlags, (LPVOID)chNewEnv, NULL, &si, &pi);

    if (!success) {
        printf("Error creating child process \n");
        return;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

}

void CreateChild2Process() {

    TCHAR applicationName[] = TEXT("\"D:\\Microsoft Visual Studio\\Workspace\\SysProga\\Lab3_2\\Debug\\Lab3_2.exe\" \"D:\\Microsoft Visual Studio\\Workspace\\SysProga\\files\"");
    PROCESS_INFORMATION pi;
    STARTUPINFO si;
    BOOL success = FALSE;

    // Set env var with inheritence from parent process

    if (!SetEnvironmentVariable(TEXT("Path"), TEXT("Test")))
    {
        printf("SetEnvironmentVariable failed (%d)\n", GetLastError());
        return;
    }

    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
    ZeroMemory(&si, sizeof(STARTUPINFO));

    si.cb = sizeof(STARTUPINFO);
    si.hStdError = W21;
    si.hStdOutput = W21;
    si.dwFlags |= STARTF_USESTDHANDLES;

    // Create process of looking for files

    success = CreateProcess(NULL, applicationName, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);

    if (!success) {
        printf("Error creating child process \n");
        return;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

}

int main()
{
    DWORD MainProcessId = GetCurrentProcessId();
    printf("(%d) Parent process running.... \n", MainProcessId);

    // Create new directories

    if (!CreateDirectory(TEXT("FILE11"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }
    if (!CreateDirectory(TEXT("FILE11\\FILE12"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }
    if (!CreateDirectory(TEXT("FILE11\\FILE12\\FILE13"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }

    if (!CreateDirectory(TEXT("FILE21"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }
    if (!CreateDirectory(TEXT("FILE21\\FILE22"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }
    if (!CreateDirectory(TEXT("FILE21\\FILE22\\FILE23"), NULL))
    {
        printf("CreateDirectory failed (%d)\n", GetLastError());
        return 1;
    }
    printf("\n(%d) Directories created\n\n\n", MainProcessId);

    DWORD dRead, dWritten;
    CHAR chBuf[BUFSIZE] = "hello";
    BOOL bSuccess = FALSE;

    SECURITY_ATTRIBUTES secAttr;
    secAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
    secAttr.bInheritHandle = TRUE;
    secAttr.lpSecurityDescriptor = NULL;

    if (!CreatePipe(&R11, &W11, &secAttr, 0)) {
        printf("\nerror creating first pipe \n");
    }

    if (!SetHandleInformation(R11, HANDLE_FLAG_INHERIT, 0)) {
        printf("\nR1 SetHandleInformation \n");
    }

    if (!CreatePipe(&R21, &W21, &secAttr, 0)) {
        printf("\nerror creating second pipe \n");
    }

    if (!SetHandleInformation(R21, HANDLE_FLAG_INHERIT, 0)) {
        printf("\nR2 SetHandleInformation \n");
    }

    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);

    CreateChild1Process();
    CreateChild2Process();

    bSuccess = ReadFile(R11, chBuf, BUFSIZE, &dRead, NULL);
    if (!bSuccess) {
        printf("error reading \n");
        return 0;
    }

    bSuccess = WriteFile(hStdOut, chBuf, 619, &dWritten, NULL);
    if (!bSuccess) {
        printf("error reading \n");
        return 0;
    }

    bSuccess = ReadFile(R21, chBuf, BUFSIZE, &dRead, NULL);
    if (!bSuccess) {
        printf("error reading \n");
        return 0;
    }

    bSuccess = WriteFile(hStdOut, chBuf, 2100, &dWritten, NULL);
    if (!bSuccess) {
        printf("error reading \n");
        return 0;
    }

    return 0;

}
