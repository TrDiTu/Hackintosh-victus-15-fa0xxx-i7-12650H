// xe-freq.c — measure the real CPU clock without powermetrics (which panics the TGL framebuffer on this stack).
// RUN ON MACHINE B (macOS). User space only: no kernel, no IOReport, no graphics driver involved.
//
// Method: a chain of dependent integer ADDs costs exactly 1 cycle each on Golden Cove (P) and Gracemont (E) cores,
// so ADDs per second = core clock. Each thread runs the chain for a short window and reports MHz. macOS decides
// which core a thread lands on (no pinning): P-core threads show the higher numbers. Two threads on one P-core
// (Hyper-Threading) share it, so with 16 threads some threads read about half the core clock.
//
// Build:  clang -O2 -o xe-freq xe-freq.c -lpthread
// Use:    ./xe-freq            one thread, 10 samples (~10 s, single-core turbo)
//         ./xe-freq 16         16 threads at once        (all-core clock under full load)
//         ./xe-freq 1 30       one thread, 30 samples (each sample ~1 s)
//         XEFREQ_SAMPLES=1 ./xe-freq 1 30   also print every sample (shows drops/migration over time)
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#ifdef __APPLE__
#include <mach/mach_time.h>
#endif

#define ADDS_PER_ITER 100

// mach_absolute_time on macOS: CLOCK_MONOTONIC_RAW stepped in ~8 ms increments on the Victus (first version gave 8-24 GHz).
static uint64_t now_ns(void) {
#ifdef __APPLE__
	static mach_timebase_info_data_t tb;
	if (!tb.denom) mach_timebase_info(&tb);
	return mach_absolute_time() * tb.numer / tb.denom;
#else
	struct timespec t;
	clock_gettime(CLOCK_MONOTONIC_RAW, &t);
	return (uint64_t)t.tv_sec * 1000000000ull + (uint64_t)t.tv_nsec;
#endif
}

// Smallest observable step of now_ns(), to show the timer is fine enough for the sample length.
static uint64_t timer_step_ns(void) {
	uint64_t best = UINT64_MAX;
	for (int i = 0; i < 50; i++) {
		uint64_t a = now_ns(), b;
		while ((b = now_ns()) == a) {}
		if (b - a < best) best = b - a;
	}
	return best;
}

// 100 dependent register-register adds per call. NOT "add $imm": Golden Cove (ADL P-core) folds add-immediate chains
// in the renamer and retires several per cycle (gave 20 GHz). The addend comes from memory at run time, so it cannot
// be folded; reg-reg ADD latency is 1 cycle on Golden Cove and Gracemont.
static volatile uint64_t g_one = 1;
static inline void chain(uint64_t *x, uint64_t y) {
	__asm__ volatile(
#define A "add %1, %0\n\t"
#define A10 A A A A A A A A A A
		A10 A10 A10 A10 A10 A10 A10 A10 A10 A10
#undef A10
#undef A
		: "+r"(*x)
		: "r"(y));
}

// Where is this thread running? CPUID 0x1A EAX[31:24]: 0x40 = Core (P), 0x20 = Atom (E). CPUID 0x0B EDX = x2APIC id.
// User-space instructions: safe on macOS, no driver involved.
static void where(unsigned *type, unsigned *apic) {
	unsigned a, b, c, d;
	__asm__ volatile("cpuid" : "=a"(a), "=b"(b), "=c"(c), "=d"(d) : "a"(0x1A), "c"(0));
	*type = a >> 24;
	__asm__ volatile("cpuid" : "=a"(a), "=b"(b), "=c"(c), "=d"(d) : "a"(0x0B), "c"(0));
	*apic = d;
}

typedef struct { double mhz, epct; int cores; } sample_t;

#define CHECKS 200  // core checks per sample (~every 5 ms)
static sample_t measure(uint64_t iters) {
	uint64_t x = 0, y = g_one, chunk = iters / CHECKS;
	for (uint64_t i = 0; i < iters / 10; i++) chain(&x, y);  // warm-up: let the core ramp its clock
	int ecount = 0;
	uint64_t seen[4] = {0};  // bitmap of x2APIC ids 0-255
	uint64_t t0 = now_ns();
	for (int c = 0; c < CHECKS; c++) {
		for (uint64_t i = 0; i < chunk; i++) chain(&x, y);
		unsigned type, apic;
		where(&type, &apic);
		if (type == 0x20) ecount++;
		seen[(apic & 255) >> 6] |= 1ull << (apic & 63);
	}
	uint64_t t1 = now_ns();
	if (x == 42) puts("");  // keep x live
	int cores = 0;
	for (int i = 0; i < 4; i++) cores += __builtin_popcountll(seen[i]);
	sample_t r = {(double)chunk * CHECKS * ADDS_PER_ITER / ((double)(t1 - t0) / 1e3), 100.0 * ecount / CHECKS, cores};
	return r;  // adds per microsecond = MHz
}

typedef struct { int id, samples; sample_t *out; } job_t;

static void *worker(void *p) {
	job_t *j = p;
	for (int s = 0; s < j->samples; s++) j->out[s] = measure(40000000);  // ~1 s per sample at 4 GHz
	return NULL;
}

int main(int argc, char **argv) {
	int threads = argc > 1 ? atoi(argv[1]) : 1;
	int samples = argc > 2 ? atoi(argv[2]) : 10;
	if (threads < 1 || threads > 64 || samples < 1) { fprintf(stderr, "usage: %s [threads 1-64] [samples]\n", argv[0]); return 1; }
	printf("timer step: %llu ns (must be far below the ~1 s sample)\n", (unsigned long long)timer_step_ns());
	pthread_t th[64];
	job_t jobs[64];
	sample_t *res = calloc((size_t)threads * samples, sizeof(sample_t));
	for (int i = 0; i < threads; i++) {
		jobs[i] = (job_t){i, samples, res + (size_t)i * samples};
		pthread_create(&th[i], NULL, worker, &jobs[i]);
	}
	for (int i = 0; i < threads; i++) pthread_join(th[i], NULL);
	if (getenv("XEFREQ_SAMPLES")) {  // XEFREQ_SAMPLES=1 ./xe-freq 1 30 : one line per ~1 s sample, to see the pattern
		printf("per sample: MHz  E-core%%  distinct-cores\n");
		for (int s = 0; s < samples; s++) {
			printf("sample %2d:", s);
			for (int i = 0; i < threads; i++) printf("  %5.0f %3.0f%% %2d", jobs[i].out[s].mhz, jobs[i].out[s].epct, jobs[i].out[s].cores);
			printf("\n");
		}
	}
	for (int i = 0; i < threads; i++) {
		double mn = 1e9, mx = 0, sum = 0;
		double ep = 0;
		for (int s = 0; s < samples; s++) ep += jobs[i].out[s].epct;
		for (int s = 0; s < samples; s++) { double v = jobs[i].out[s].mhz; mn = v < mn ? v : mn; mx = v > mx ? v : mx; sum += v; }
		printf("thread %2d: min %5.0f  avg %5.0f  max %5.0f MHz  E-core %3.0f%%\n", i, mn, sum / samples, mx, ep / samples);
	}
	free(res);
	return 0;
}
