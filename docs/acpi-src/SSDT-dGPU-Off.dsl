DefinitionBlock ("", "SSDT", 2, "HACK", "DGPUOFF", 0x00000000)
{
    External (_SB_.PC00.PEG1.PEGP, DeviceObj)
    External (_SB_.PC00.PEG1.PEGP._OFF, MethodObj)

    Scope (\_SB_.PC00.PEG1.PEGP)
    {
        Method (_INI, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                If (CondRefOf (\_SB_.PC00.PEG1.PEGP._OFF))
                {
                    \_SB_.PC00.PEG1.PEGP._OFF ()
                }
            }
        }
    }
}
