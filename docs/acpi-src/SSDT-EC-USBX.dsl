/*
 * SSDT-EC-USBX — HP Victus 15-fa0xxx (8A4F), BIOS F.34
 * Dựa trên mẫu chính thức OpenCore 1.0.8 Docs/AcpiSamples/Source/SSDT-EC-USBX.dsl (BSD-3-Clause),
 * đổi đường dẫn theo DSDT thật: LPC = \_SB.PC00.LPCB, EC thật = \_SB.PC00.LPCB.EC0_ (PNP0C09, acpi-devices.csv).
 * Laptop: KHÔNG tắt EC0_ thật (pin/quạt cần nó); chỉ thêm thiết bị EC giả cho macOS + USBX cấp điện USB.
 * DSDT không có sẵn Device (EC) hay Device (USBX) (đã grep 2026-11-02).
 */
DefinitionBlock ("", "SSDT", 2, "VICTUS", "SsdtEC", 0x00001000)
{
    External (_SB_.PC00.LPCB, DeviceObj)

    Scope (\_SB)
    {
        Device (USBX)
        {
            Name (_ADR, Zero)
            Method (_DSM, 4, NotSerialized)
            {
                If ((Arg2 == Zero))
                {
                    Return (Buffer (One) { 0x03 })
                }
                Return (Package (0x08)
                {
                    "kUSBSleepPowerSupply", 0x13EC,
                    "kUSBSleepPortCurrentLimit", 0x0834,
                    "kUSBWakePowerSupply", 0x13EC,
                    "kUSBWakePortCurrentLimit", 0x0834
                })
            }
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin")) { Return (0x0F) }
                Return (Zero)
            }
        }
    }

    Scope (\_SB.PC00.LPCB)
    {
        Device (EC)
        {
            Name (_HID, "ACID0001")
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin")) { Return (0x0F) }
                Return (Zero)
            }
        }
    }
}
