#include <tchar.h>
#include <windows.h>

const wchar_t* procPath = L"D:\\Microsoft Visual Studio\\Workspace\\Test\\Debug\\Test.exe";
wchar_t* cmdPath = const_cast<wchar_t*>(L"D:\\Microsoft Visual Studio\\Workspace\\Test\\Debug\\Test.exe");

bool bLeftClicked = false;
bool bRightClicked = false;

const wchar_t* g_szClassName = _T("windowClass");

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
    case WM_LBUTTONDOWN:
        bLeftClicked = true;
        if (bLeftClicked && bRightClicked) {
            STARTUPINFO info = { sizeof(info) };
            PROCESS_INFORMATION processInfo;
            CreateProcess(procPath, cmdPath, NULL, NULL, FALSE, 0, NULL, NULL,
                &info, &processInfo);
        }
        break;
    case WM_LBUTTONUP:
        bLeftClicked = false;
        break;
    case WM_RBUTTONDOWN:
        bRightClicked = true;
        if (bLeftClicked && bRightClicked) {
            STARTUPINFO info = { sizeof(info) };
            PROCESS_INFORMATION processInfo;
            CreateProcess(procPath, cmdPath, NULL, NULL, FALSE, 0, NULL, NULL,
                &info, &processInfo);
        }
        break;
    case WM_RBUTTONUP:
        bRightClicked = false;
        break;
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;

    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = g_szClassName;
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc))
    {
        MessageBox(NULL, _T("Window Registration Failed!"), _T("Error!"),
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        g_szClassName,
        _T("Title"),
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 240, 120,
        NULL, NULL, hInstance, NULL);

    if (hwnd == NULL)
    {
        MessageBox(NULL, _T("Window Creation Failed!"), _T("Error!"),
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&Msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}
