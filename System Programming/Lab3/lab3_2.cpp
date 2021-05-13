#include <tchar.h>
#include <windows.h>
#include <stdio.h>
#include <strsafe.h>

int _tmain(int argc, TCHAR* argv[])
{

    TCHAR           szSearchDir[MAX_PATH];
    WIN32_FIND_DATA FileData;
    HANDLE          hSearch;
    BOOL            fFinished;
    TCHAR           szPath[MAX_PATH];

    LPTSTR lpszVariable;
    LPTCH lpvEnv;

    lpvEnv = GetEnvironmentStrings();

    if (lpvEnv == NULL)
    {
        printf("GetEnvironmentStrings failed (%d)\n", GetLastError());
        return 1;
    }

    if (argc != 2)
    {
        _tprintf(TEXT("Usage: %s <search dir>\n"), argv[0]);
        return 1;
    }

    DWORD Child2ProcessId = GetCurrentProcessId();
    printf("(%d) Child2 process running.... \n\n", Child2ProcessId);

    // Search "*.txt" files in directory

    StringCchCopy(szSearchDir, MAX_PATH, argv[1]);
    StringCchCat(szSearchDir, MAX_PATH, TEXT("\\*.txt"));

    hSearch = FindFirstFile(szSearchDir, &FileData);
    if (hSearch == INVALID_HANDLE_VALUE)
    {
        printf("No *.txt files found.\n");
        return 1;
    }

    fFinished = FALSE;
    while (!fFinished)
    {
        StringCchPrintf(szPath, sizeof(szPath) / sizeof(szPath[0]), TEXT("%s\\%s"), argv[1], FileData.cFileName);
        _tprintf(TEXT("(%d) Found: %s\n"), Child2ProcessId, szPath);

        if (!FindNextFile(hSearch, &FileData))
        {
            if (GetLastError() == ERROR_NO_MORE_FILES)
                fFinished = TRUE;
            else
            {
                printf("Could not find next file.\n");
                return 1;
            }
        }
    }

    FindClose(hSearch);

    lpszVariable = (LPTSTR)lpvEnv;

    _tprintf(TEXT("\n(%d) EnvVars:\n"), Child2ProcessId);
    while (*lpszVariable)
    {
        _tprintf(TEXT("%s\n"), lpszVariable);
        lpszVariable += lstrlen(lpszVariable) + 1;
    }
    FreeEnvironmentStrings(lpvEnv);

    return 0;

}
