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
    TCHAR           szNewPath[MAX_PATH];
    TCHAR           sTargetFileDirectory[MAX_PATH];

    LPTSTR lpszVariable;
    LPTCH lpvEnv;

    lpvEnv = GetEnvironmentStrings();

    if (lpvEnv == NULL)
    {
        printf("GetEnvironmentStrings failed (%d)\n", GetLastError());
        return 1;
    }

    if (argc != 3)
    {
        _tprintf(TEXT("Usage: %s <search dir> <copy dir>\n"), argv[0]);
        return 1;
    }

    StringCchCopy(sTargetFileDirectory, MAX_PATH, argv[2]);

    DWORD Child1ProcessId = GetCurrentProcessId();
    printf("(%d) Child1 process running.... \n", Child1ProcessId);

    // Copy "*.txt" and "*.exe" files to FILE23 folder

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
        StringCchPrintf(szNewPath, sizeof(szNewPath) / sizeof(szNewPath[0]), TEXT("%s\\%s"), sTargetFileDirectory, FileData.cFileName);

        if (!CopyFile(szPath, szNewPath, FALSE))
        {
            _tprintf(TEXT("Could not copy file %s to %s\n"), szPath, szNewPath);
            return 1;
        }

        if (!FindNextFile(hSearch, &FileData))
        {
            if (GetLastError() == ERROR_NO_MORE_FILES)
            {
                _tprintf(TEXT("\n(%d) Copied %s to %s\n"), Child1ProcessId, szSearchDir, sTargetFileDirectory);
                fFinished = TRUE;
            }
            else
            {
                printf("Could not find next file.\n");
                return 1;
            }
        }
    }

    FindClose(hSearch);

    StringCchCopy(szSearchDir, MAX_PATH, argv[1]);
    StringCchCat(szSearchDir, MAX_PATH, TEXT("\\*.exe"));

    hSearch = FindFirstFile(szSearchDir, &FileData);
    if (hSearch == INVALID_HANDLE_VALUE)
    {
        printf("No *.exe files found.\n");
        return 1;
    }

    fFinished = FALSE;
    while (!fFinished)
    {
        StringCchPrintf(szPath, sizeof(szPath) / sizeof(szPath[0]), TEXT("%s\\%s"), argv[1], FileData.cFileName);
        StringCchPrintf(szNewPath, sizeof(szNewPath) / sizeof(szNewPath[0]), TEXT("%s\\%s"), sTargetFileDirectory, FileData.cFileName);

        if (!CopyFile(szPath, szNewPath, FALSE))
        {
            _tprintf(TEXT("Could not copy file %s to %s\n"), szPath, szNewPath);
            return 1;
        }

        if (!FindNextFile(hSearch, &FileData))
        {
            if (GetLastError() == ERROR_NO_MORE_FILES)
            {
                _tprintf(TEXT("(%d) Copied %s to %s\n"), Child1ProcessId, szSearchDir, sTargetFileDirectory);
                fFinished = TRUE;
            }
            else
            {
                printf("Could not find next file.\n");
                return 1;
            }
        }
    }

    FindClose(hSearch);

    lpszVariable = (LPTSTR)lpvEnv;

    _tprintf(TEXT("\n(%d) EnvVars:\n"), Child1ProcessId);
    while (*lpszVariable)
    {
        _tprintf(TEXT("%s\n"), lpszVariable);
        lpszVariable += lstrlen(lpszVariable) + 1;
    }
    FreeEnvironmentStrings(lpvEnv);

    return 0;

}
