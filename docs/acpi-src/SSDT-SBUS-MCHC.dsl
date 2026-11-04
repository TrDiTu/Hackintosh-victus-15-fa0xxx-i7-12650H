/*
 * SSDT-SBUS-MCHC — thêm MCHC và BUS0 cho SMBus (8086:51A3) để AppleSMBus nạp.
 * Dựa trên mẫu chính thức OpenCore 1.0.8 SSDT-SBUS-MCHC.dsl (BSD-3-Clause), đổi PCI0 → PC00 theo DSDT thật.
 * Bằng chứng: \_SB.PC00.SBUS có (DSDT.dsl:10058); không có Device (MCHC) / Device (BUS0) (đã grep 2026-11-02).
 * Bỏ thiết bị DVL0 (diagsvault) tuỳ chọn của mẫu.
 */
DefinitionBlock ("", "SSDT", 2, "VICTUS", "MCHCSBUS", 0x00000000)
{
    External (_SB_.PC00, DeviceObj)
    External (_SB_.PC00.SBUS, DeviceObj)

    Scope (\_SB.PC00)
    {
        Device (MCHC)
        {
            Name (_ADR, Zero)
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin")) { Return (0x0F) }
                Return (Zero)
            }
        }
    }

    Scope (\_SB.PC00.SBUS)
    {
        Device (BUS0)
        {
            Name (_CID, "smbus")
            Name (_ADR, Zero)
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin")) { Return (0x0F) }
                Return (Zero)
            }
        }
    }
}
