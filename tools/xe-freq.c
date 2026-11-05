// xe-freq.c — measure the real CPU clock without powermetrics (which panics the TGL framebuffer on this stack).
// RUN ON MACHINE B (macOS). User space only: no kernel, no IOReport, no graphics driver involved.
//
// Method: a chain of dependent integer ADDs costs exactly 1 cycle each on Golden Cove (P) and Gracemont (E) cores,
// so ADDs per second = core clock. Each thread runs the chain for a short window and reports MHz. macOS decides
// which core a thread lands on (no pinning): P-core threads show the higher numbers.
//
// Build:  clang -O2 -o xe-freq xe-freq.c -lpthread
// Use:    ./xe-freq            one thread, 10 samples   (single-core turbo)
//         ./xe-freq 16         16 threads at once        (all-core clock under full load)
//         ./xe-freq 1 30       one thread, 30 samples
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ADDS_PER_ITER 100

static uint64_t now_ns(void) {
	struct timespec t;
	clock_gettime(CLOCK_MONOTONIC_RAW, &t);
	return (uint64_t)t.tv_sec * 1000000000ull + (uint64_t)t.tv_nsec;
}

// 100 dependent adds per call; the compiler cannot reorder or drop them (asm volatile, register dependency).
static inline void chain(uint64_t *x) {
	__asm__ volatile(
#define A "add $1, %0\n\t"
#define A10 A A A A A A A A A A
		A10 A10 A10 A10 A10 A10 A10 A10 A10 A10
#undef A10
#undef A
		: "+r"(*x));
}

static double measure_mhz(uint64_t iters) {
	uint64_t x = 0;
	for (uint64_t i = 0; i < iters / 10; i++) chain(&x);  // warm-up: let the core ramp its clock
	uint64_t t0 = now_ns();
	for (uint64_t i = 0; i < iters; i++) chain(&x);
	uint64_t t1 = now_ns();
	if (x == 42) puts("");  // keep x live
	return (double)iters * ADDS_PER_ITER / ((double)(t1 - t0) / 1e3);  // adds per microsecond = MHz
}

typedef struct { int id, samples; double *out; } job_t;

static void *worker(void *p) {
	job_t *j = p;
	for (int s = 0; s < j->samples; s++) j->out[s] = measure_mhz(2000000);  // ~0.05 s per sample at 4 GHz
	return NULL;
}

int main(int argc, char **argv) {
	int threads = argc > 1 ? atoi(argv[1]) : 1;
	int samples = argc > 2 ? atoi(argv[2]) : 10;
	if (threads < 1 || threads > 64 || samples < 1) { fprintf(stderr, "usage: %s [threads 1-64] [samples]\n", argv[0]); return 1; }
	pthread_t th[64];
	job_t jobs[64];
	double *res = calloc((size_t)threads * samples, sizeof(double));
	for (int i = 0; i < threads; i++) {
		jobs[i] = (job_t){i, samples, res + (size_t)i * samples};
		pthread_create(&th[i], NULL, worker, &jobs[i]);
	}
	for (int i = 0; i < threads; i++) pthread_join(th[i], NULL);
	for (int i = 0; i < threads; i++) {
		double mn = 1e9, mx = 0, sum = 0;
		for (int s = 0; s < samples; s++) { double v = jobs[i].out[s]; mn = v < mn ? v : mn; mx = v > mx ? v : mx; sum += v; }
		printf("thread %2d: min %5.0f  avg %5.0f  max %5.0f MHz\n", i, mn, sum / samples, mx);
	}
	free(res);
	return 0;
}
