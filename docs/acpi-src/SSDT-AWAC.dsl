/*
 * SSDT-AWAC — bật RTC cổ điển, tắt AWAC khi chạy macOS.
 * Dựa trên mẫu chính thức OpenCore 1.0.8 SSDT-AWAC-DISABLE.dsl (BSD-3-Clause).
 * Bằng chứng DSDT (F.34): STAS là trường NVS (DSDT.dsl:2592); \_SB.AWAC._STA trả 0x0F khi STAS==0 (DSDT.dsl:8477);
 * \_SB.PC00.LPCB.RTC._STA trả 0x0F khi STAS==1 (DSDT.dsl:87084). Linux: AWAC status 15, RTC_ status 0.
 */
DefinitionBlock ("", "SSDT", 2, "VICTUS", "RTCAWAC", 0x00000000)
{
    External (STAS, FieldUnitObj)

    Scope (\)
    {
        Method (_INI, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                STAS = One
            }
        }
    }
}
