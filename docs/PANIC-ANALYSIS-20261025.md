# Panic analysis — 2026-10-25

## Evidence

All five `logs/Kernel-2026-10-24-*.panic` reports contain:

- `IOGMD: not wired for the IODMACommand @IOMemoryDescriptor.cpp:3537`.
- Panicked task: `UVCAssistant`.
- Stack: `IntelBTPatcher::newHostDeviceRequest` -> `IOMemoryDescriptor::readBytes` -> `getPhysicalSegment` -> `dmaCommandOperation` -> panic.
- IntelBTPatcher 2.4, IOUSBHostFamily 1.2, Darwin 25.6.0, OS build 25G241 (as reported, not independently verified).

071850 and 084753 use amfi=0x80 without -igfxvesa. 101831 adds -igfxvesa. 104828 and 105723 use amfi_get_out_of_my_way=0x1 with -igfxvesa. None has the exact boot-args of deployed build-07. Report timestamps are October 24; do not assume they are the latest boot merely because they were copied now.

## Assessment

High confidence: these panics occur on the IntelBTPatcher USB request interception path during a UVCAssistant request. The official v2.4.0 source routes IOUSBHostDevice::deviceRequest and calls descriptor->readBytes in newHostDeviceRequest, matching the stack.

Source: https://github.com/OpenIntelWireless/IntelBluetoothFirmware/blob/v2.4.0/IntelBTPatcher/IntelBTPatcher.cpp

This identifies a concrete suspect for the recorded panics. It does not prove that all preceding GUI stalls or AppleKeyStore messages have the same cause, or that the camera hardware is defective. Both graphics boot-arg variants panic on the same path.

## Controlled test

Disable only Kernel/Add/IntelBTPatcher.kext (Enabled=false) in the workspace. Retain the file for rollback; leave firmware, BlueToolFixup, graphics properties and boot-args unchanged from build-07. No new driver is introduced.

Bluetooth may fail to initialize or connect without its patcher. The purpose is to test whether this panic disappears and whether boot reaches Recovery/Desktop. Success requires testing on machine B; static validation cannot establish it. If panic recurs, obtain a newly generated report and verify its Boot args and backtrace.

Rollback: restore this entry to Enabled=true through the validation/deployment workflow. USB is not modified by this analysis.
