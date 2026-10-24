import os, subprocess

src_dir = 'docs/acpi-src'
os.makedirs(src_dir, exist_ok=True)

ssdts = {
    'SSDT-dGPU-Off.dsl': """DefinitionBlock ("", "SSDT", 2, "HACK", "DGPUOFF", 0x00000000)
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
""",
    'SSDT-RTCAWAC.dsl': """DefinitionBlock ("", "SSDT", 2, "HACK", "RTCAWAC", 0x00000000)
{
    External (STAS, IntObj)

    Scope (\\)
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
""",
    'SSDT-EC.dsl': """DefinitionBlock ("", "SSDT", 2, "HACK", "EC", 0x00000000)
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
""",
    'SSDT-USBX.dsl': """DefinitionBlock ("", "SSDT", 2, "HACK", "USBX", 0x00000000)
{
    Scope (\_SB)
    {
        Device (USBX)
        {
            Name (_ADR, Zero)
            Method (_DSM, 4, NotSerialized)
            {
                If (!Arg2)
                {
                    Return (Buffer (One)
                    {
                         0x03
                    })
                }

                Return (Package (0x04)
                {
                    "kUSBSleepPortCurrentLimit", 
                    0x0BB8, 
                    "kUSBWakePortCurrentLimit", 
                    0x0BB8
                })
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
}
""",
    'SSDT-GPI0.dsl': """DefinitionBlock ("", "SSDT", 2, "HACK", "GPI0", 0x00000000)
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
"""
}

iasl = os.path.abspath('tools/iasl/iasl.exe')

for name, content in ssdts.items():
    dsl_path = os.path.join(src_dir, name)
    aml_path = dsl_path[:-4] + '.aml'
    with open(dsl_path, 'w', encoding='ascii') as f:
        f.write(content.replace('\r\n', '\n'))
    
    cmd = [iasl, '-ve', dsl_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(aml_path):
        sz = os.path.getsize(aml_path)
        print(f'SUCCESS: {name} -> {os.path.basename(aml_path)} ({sz} bytes)')
    else:
        print(f'FAILED: {name}')
        print(res.stdout)
        print(res.stderr)
