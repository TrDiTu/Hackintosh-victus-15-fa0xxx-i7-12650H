DefinitionBlock ("", "SSDT", 2, "HACK", "GPI0", 0x00000000)
{
    External (_SB_.GPI0, DeviceObj)
    External (_SB_.GPI0.XSTA, MethodObj)

    Scope (\_SB_.GPI0)
    {
        Method (_STA, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                Return (0x0F)
            }
            Else
            {
                Return (\_SB_.GPI0.XSTA ())
            }
        }
    }
}
