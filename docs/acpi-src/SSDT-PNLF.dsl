/*
 * SSDT-PNLF — backlight device for macOS (HP Victus 15-fa0xxx, iGPU 46A3 spoofed 9A49, NootedGreen).
 *
 * Why: firmware (BIOS F.34) has no PNLF / APP0002 device (ioreg IODeviceTree on machine B, 2026-11-05),
 * so macOS attaches AppleDisplay instead of AppleBacklightDisplay and shows no brightness slider.
 *
 * Minimal form (no _INI, no PWM register writes): NootedGreen XE-BLR owns the PWM registers
 * (0xC8254 period / 0xC8258 duty). _UID 0x13 = WhateverGreen "CoffeeLake and later" profile.
 * Same structure as JulioNectar's SSDT-PNLF (TGL laptop); written here, not copied.
 *
 * iGPU path \_SB.PC00.GFX0: confirmed on machine B (ioreg acpi-path IOACPIPlane:/_SB/PC00@0/GFX0@20000, 2026-11-05).
 */
DefinitionBlock ("", "SSDT", 2, "HACK", "PNLF", 0x00000000)
{
    External (_SB_.PC00.GFX0, DeviceObj)

    Device (\_SB.PC00.GFX0.PNLF)
    {
        Name (_HID, EisaId ("APP0002"))
        Name (_CID, "backlight")
        Name (_UID, 0x13)

        Method (_STA, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                Return (0x0B)
            }

            Return (Zero)
        }
    }
}
