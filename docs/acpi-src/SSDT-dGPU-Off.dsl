/*
 * SSDT-dGPU-Off.dsl
 * Vô hiệu hoá nguồn điện NVIDIA GeForce RTX 3050 Ti Mobile [10DE:25A0] trên macOS.
 * Sử dụng dummy device RMD1 để tránh xung đột trùng lặp method _INI trong DSDT.
 *
 * Đường dẫn ACPI thật xác minh từ DSDT và SSDT4 của HP Victus 15-fa0xxx:
 * - Root PCI: \_SB.PC00
 * - Bridge: \_SB.PC00.PEG1 (PCI 00:01.0)
 * - Device dGPU: \_SB.PC00.PEG1.PEGP (PCI 01:00.0)
 * - Power Off Method: \_SB.PC00.PEG1.PEGP._OFF (xác minh tại SSDT4.aml)
 */

DefinitionBlock ("", "SSDT", 2, "HACK", "DGPUOFF", 0x00000000)
{
    External (_SB_.PC00.PEG1.PEGP._OFF, MethodObj)

    Device (RMD1)
    {
        Name (_HID, "RMD10000")

        Method (_INI, 0, NotSerialized)
        {
            If (CondRefOf (\_SB.PC00.PEG1.PEGP._OFF))
            {
                \_SB.PC00.PEG1.PEGP._OFF ()
            }
        }

        Method (_STA, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                Return (0x0F)
            }
            Else
            {
                Return (Zero)
            }
        }
    }
}
