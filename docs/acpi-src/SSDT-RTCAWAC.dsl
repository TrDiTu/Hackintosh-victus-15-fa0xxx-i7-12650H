DefinitionBlock ("", "SSDT", 2, "HACK", "RTCAWAC", 0x00000000)
{
    External (STAS, IntObj)

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
