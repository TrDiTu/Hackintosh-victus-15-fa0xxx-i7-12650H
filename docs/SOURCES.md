# SOURCES — Nguồn gốc và kiểm định mã băm (SHA256) các thành phần EFI

*Tài liệu này lưu vết toàn bộ binary kext, driver và công cụ được sử dụng trong dự án theo skill driver-vetting.*

| Thành phần | Phiên bản mục tiêu | URL release chính thức | Tên file lưu trữ | SHA256 | Ngày ghi nhận | Dùng trong EFI? |
|---|---|---|---|---|---|:---:|
| **OpenCorePkg** | 1.0.3 / mới nhất | https://github.com/acidanthera/OpenCorePkg/releases | OpenCore-1.0.3-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **ocvalidate** | 1.0.3 / đồng bộ OpenCore | https://github.com/acidanthera/OpenCorePkg/releases | ocvalidate.exe | CHỜ TẢI (Pha 3) | 2026-10-24 | Công cụ kiểm tra |
| **Lilu** | 1.7.0 / mới nhất | https://github.com/acidanthera/Lilu/releases | Lilu-1.7.0-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **VirtualSMC** | 1.3.5 / mới nhất | https://github.com/acidanthera/VirtualSMC/releases | VirtualSMC-1.3.5-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **WhateverGreen** | 1.6.9 / mới nhất | https://github.com/acidanthera/WhateverGreen/releases | WhateverGreen-1.6.9-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **AppleALC** | 1.9.3 / mới nhất | https://github.com/acidanthera/AppleALC/releases | AppleALC-1.9.3-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **itlwm** | 2.3.0 / mới nhất | https://github.com/OpenIntelWireless/itlwm/releases | itlwm_v2.3.0_stable.kext.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **HeliPort** | 1.4.1 / mới nhất | https://github.com/OpenIntelWireless/HeliPort/releases | HeliPort.dmg | CHỜ TẢI (Pha 3) | 2026-10-24 | App người dùng |
| **IntelBluetoothFirmware** | 2.5.0 / mới nhất | https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases | IntelBluetoothFirmware-2.5.0.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **BrcmPatchRAM (BlueToolFixup)** | 2.6.9 / mới nhất | https://github.com/acidanthera/BrcmPatchRAM/releases | BrcmPatchRAM-2.6.9-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **RealtekRTL8111** | 2.4.2 / mới nhất | https://github.com/Mieze/RTL8111_driver_for_OS_X/releases | RealtekRTL8111-V2.4.2.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **VoodooPS2** | 2.3.7 / mới nhất | https://github.com/acidanthera/VoodooPS2/releases | VoodooPS2Controller-2.3.7-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **VoodooI2C** | 2.8.1 / mới nhất | https://github.com/VoodooI2C/VoodooI2C/releases | VoodooI2C-2.8.1.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **ECEnabler** | 1.0.5 / mới nhất | https://github.com/1Revenger1/ECEnabler/releases | ECEnabler-1.0.5-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **NVMeFix** | 1.1.2 / mới nhất | https://github.com/acidanthera/NVMeFix/releases | NVMeFix-1.1.2-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **RealtekCardReader** | 0.9.7 / mới nhất | https://github.com/0xFireWolf/RealtekCardReader/releases | RealtekCardReader-0.9.7-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **RealtekCardReaderFriend** | 1.0.4 / mới nhất | https://github.com/0xFireWolf/RealtekCardReaderFriend/releases | RealtekCardReaderFriend-1.0.4-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **CpuTopologyRebuild** | 1.1.0 / mới nhất | https://github.com/b00t0x/CpuTopologyRebuild/releases | CpuTopologyRebuild-1.1.0-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **RestrictEvents** | 1.1.5 / mới nhất | https://github.com/acidanthera/RestrictEvents/releases | RestrictEvents-1.1.5-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **BrightnessKeys** | 1.0.3 / mới nhất | https://github.com/acidanthera/BrightnessKeys/releases | BrightnessKeys-1.0.3-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |
| **USBToolBox** | 1.1.1 / mới nhất | https://github.com/USBToolBox/kext/releases | USBToolBox-1.1.1-RELEASE.zip | CHỜ TẢI (Pha 3) | 2026-10-24 | Có |

*Ghi chú:* Toàn bộ binary sẽ được tải từ chính release chính thức của tác giả vào thư mục _cache/ và kiểm tra SHA256 trước khi giải nén vào EFI/OC/Kexts hoặc 	ools/ trong Pha 3.
