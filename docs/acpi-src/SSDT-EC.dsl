DefinitionBlock ("", "SSDT", 2, "HACK", "EC", 0x00000000)
{
    External (_SB_.PC00.LPCB, DeviceObj)

    Scope (\_SB_.PC00.LPCB)
    {
        Device (EC)
        {
            Name (_HID, "ACID0001")
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
}
