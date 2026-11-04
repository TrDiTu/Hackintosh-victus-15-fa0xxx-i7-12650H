/*
 * SSDT-XOSI — macOS trả lời _OSI như Windows 10 (bản cao nhất DSDT kiểm: "Windows 2018.2" → OSYS = 0x07E2).
 * CẦN kèm ACPI/Patch đổi _OSI → XOSI, GIỚI HẠN TableSignature = "DSDT" (cả 16 chuỗi _OSI đều ở DSDT: 15 lời gọi
 * tại DSDT.dsl:27932–27998 và 30712, 1 CondRefOf(\_OSI); SSDT không có _OSI).
 * Mục đích chính: \_SB.PC00.I2C0.TPD0._CRS chỉ trả GpioInt/ngắt chuẩn khi OSYS >= 0x07DC (touchpad ELAN0788, VoodooI2C).
 * Danh sách chuỗi lấy ĐÚNG từ DSDT của máy, kể cả "Windows 2017.2 " có dấu cách cuối (DSDT.dsl:27988).
 * "Processor Aggregator Device" không có trong danh sách → trả theo _OSI gốc.
 */
DefinitionBlock ("", "SSDT", 2, "VICTUS", "XOSI", 0x00001000)
{
    Method (XOSI, 1, NotSerialized)
    {
        Local0 = Package ()
        {
            "Windows 2001",
            "Windows 2001 SP1",
            "Windows 2001 SP2",
            "Windows 2001.1",
            "Windows 2006",
            "Windows 2009",
            "Windows 2012",
            "Windows 2013",
            "Windows 2015",
            "Windows 2016",
            "Windows 2017",
            "Windows 2017.2 ",
            "Windows 2018",
            "Windows 2018.2"
        }
        If (_OSI ("Darwin"))
        {
            Return ((Match (Local0, MEQ, Arg0, MTR, Zero, Zero) != Ones))
        }
        Return (_OSI (Arg0))
    }
}
