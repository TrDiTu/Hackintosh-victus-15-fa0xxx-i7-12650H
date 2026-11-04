/*
 * SSDT-DGPU-OFF — tắt nguồn RTX 3050 Ti (10DE:25A0) khi chạy macOS (không có driver).
 * Bằng chứng (BIOS F.34): dGPU = \_SB.PC00.PEG1.PEGP (DSDT.dsl:6285, _ADR 0);
 * \_SB.PC00.PEG1.PEGP._OFF ở SSDT14.dsl:584 (Scope dòng 174), lưu VGA ctx rồi gọi \_SB.PC00.PEG1.PXP._OFF;
 * PowerResource \_SB.PC00.PEG1.PXP ở SSDT4.dsl:3615 (_STA/_ON/_OFF), PEG1._PR0/_PR3 = {PXP} (SSDT4.dsl:3952–3966).
 * PEGP chưa có _INI ở bất kỳ bảng nào (PEG1 có _INI riêng ở SSDT16.dsl:584 — không đụng tới).
 * Dự phòng nếu không tắt được: WhateverGreen `disable-gpu` / `-wegnoegpu` (ghi ở config).
 */
DefinitionBlock ("", "SSDT", 2, "VICTUS", "DGPUOFF", 0x00000000)
{
    External (_SB_.PC00.PEG1.PEGP, DeviceObj)
    External (_SB_.PC00.PEG1.PEGP._OFF, MethodObj)

    Scope (\_SB.PC00.PEG1.PEGP)
    {
        Method (_INI, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                If (CondRefOf (\_SB.PC00.PEG1.PEGP._OFF))
                {
                    \_SB.PC00.PEG1.PEGP._OFF ()
                }
            }
        }
    }
}
