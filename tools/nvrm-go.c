// nvrm-go: start the NullMoth NVRM driver by hand when it was booted with -nvrmnogo.
// Same call as `nvrmctl go <pass>` in the NullMoth README: NVRMUserClient selector 0 (sGo), one scalar = pass.
// Pass 1 = RM initialised + GSP firmware requested, pass 2 = adapter up (GSP-RM running); NVRM refuses a new pass
// unless the caller is root. Build and run on machine B (macOS):
//   clang -Wall -o nvrm-go nvrm-go.c -framework IOKit
//   sudo ./nvrm-go 1      then      sudo ./nvrm-go 2
#include <IOKit/IOKitLib.h>
#include <mach/mach.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	if (argc != 2) { fprintf(stderr, "usage: sudo %s <pass 1|2>\n", argv[0]); return 2; }
	uint64_t pass = strtoull(argv[1], NULL, 10);
	if (pass < 1 || pass > 2) { fprintf(stderr, "pass must be 1 or 2\n"); return 2; }
	io_service_t svc = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("NVRM"));
	if (!svc) { fprintf(stderr, "no NVRM service (driver not loaded?)\n"); return 1; }
	io_connect_t conn = 0;
	kern_return_t kr = IOServiceOpen(svc, mach_task_self(), 0, &conn);
	IOObjectRelease(svc);
	if (kr != KERN_SUCCESS) { fprintf(stderr, "IOServiceOpen failed: 0x%x\n", kr); return 1; }
	printf("go(%llu) ...\n", (unsigned long long)pass);
	fflush(stdout);
	kr = IOConnectCallScalarMethod(conn, 0, &pass, 1, NULL, NULL);
	printf("go(%llu) -> 0x%x\n", (unsigned long long)pass, kr);
	IOServiceClose(conn);
	return kr == KERN_SUCCESS ? 0 : 1;
}
