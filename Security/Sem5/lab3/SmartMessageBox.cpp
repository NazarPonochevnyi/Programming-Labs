#include "framework.h"
#include "SmartMessageBox.h"

#define CPUID_H
#ifdef _WIN32
#include <limits.h>
#include <intrin.h>
typedef unsigned __int32  uint32_t;
#else
#include <stdint.h>
#endif

HINSTANCE hInst;

bool IsVM() {
    int cpuInfo[4] = {};
    __cpuid(cpuInfo, 1);
    if (!(cpuInfo[2] & (1 << 31)))
        return false;
    const auto queryVendorIdMagic = 0x40000000;
    __cpuid(cpuInfo, queryVendorIdMagic);
    const int vendorIdLength = 13;
    using VendorIdStr = char[vendorIdLength];
    VendorIdStr hyperVendorId = {};
    memcpy(hyperVendorId + 0, &cpuInfo[1], 4);
    memcpy(hyperVendorId + 4, &cpuInfo[2], 4);
    memcpy(hyperVendorId + 8, &cpuInfo[3], 4);
    hyperVendorId[12] = '\0';
    static const VendorIdStr vendors[]{
    "KVMKVMKVM\0\0\0", // KVM 
    "Microsoft Hv",    // Microsoft Hyper-V or Windows Virtual PC */
    "VMwareVMware",    // VMware 
    "XenVMMXenVMM",    // Xen 
    "prl hyperv  ",    // Parallels
    "VBoxVBoxVBox"     // VirtualBox 
    };
    for (const auto& vendor : vendors) {
        if (!memcmp(vendor, hyperVendorId, vendorIdLength))
            return true;
    }
    return false;
}

int DisplayMessageBox() {
    int msgboxID = MessageBox(
        NULL,
        (LPCWSTR)L"Hello kitty!",
        (LPCWSTR)L"Payload",
        NULL
    );
    return msgboxID;
}

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow) {
    if (!IsVM())
        DisplayMessageBox();
    return 0;
}
