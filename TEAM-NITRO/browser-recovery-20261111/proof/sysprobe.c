/* sysprobe.c — probe which syscalls the container's seccomp filter permits.
 * Strategy: call each syscall with deliberately invalid args.
 *   ENOSYS  -> syscall not implemented / blocked at kernel level
 *   EFAULT/EINVAL/EBADF -> syscall IS implemented (filter allows it)
 *   EPERM   -> seccomp RET_ERRNO denial
 *   SIGSYS  -> seccomp RET_TRAP denial (caught by handler, reported)
 * Also tests prctl(PR_SET_SECCOMP) — browsers install their own BPF filters
 * at startup; if the outer filter blocks that, sandbox init fails.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <stddef.h>

static volatile int got_sigsys = 0;
static volatile int sigsys_nr = -1;
static void on_sigsys(int sig, siginfo_t *info, void *u) {
    got_sigsys = 1;
    sigsys_nr = info->si_syscall;
    /* return: the faulting syscall is skipped (kernel restarts? no — RET_TRAP
       delivers SIGSYS once; returning resumes after the syscall with -1/ENOSYS
       semantics in practice for this probe) */
}

struct probe { const char *name; long nr; long a1, a2, a3, a4, a5, a6; };

static struct probe probes[] = {
    {"clone3",        435, 0, 0, 0, 0, 0, 0},
    {"openat2",       437, -100, 0, 0, 0, 0, 0},
    {"io_uring_setup",425, 0, 0, 0, 0, 0, 0},
    {"pidfd_open",    434, -1, 0, 0, 0, 0, 0},
    {"membarrier",    324, 0, 0, 0, 0, 0, 0},
    {"rseq",          293, 0, 0, 0, 0, 0, 0},
    {"statx",         332, -100, 0, 0, 0, 0, 0},
    {"bpf",           321, 0, 0, 0, 0, 0, 0},
    {"keyctl",        250, 0, 0, 0, 0, 0, 0},
    {"mount",         165, 0, 0, 0, 0, 0, 0},
    {"perf_event_open",298,0, 0, -1, -1, 0, 0},
    {"clone(userns)", 56,  0x10000000 /*CLONE_NEWUSER*/ | 17 /*SIGCHLD*/, 0, 0, 0, 0, 0},
    {"getrandom",     318, 0, 0, 0, 0, 0, 0},
    {"futex",         202, 0, 0, 0, 0, 0, 0},
    {"prlimit64",     302, 0, 0, 0, 0, 0, 0},
    {NULL, 0, 0, 0, 0, 0, 0, 0}
};

int main(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_sigaction = on_sigsys;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSYS, &sa, NULL);

    printf("seccomp status: see /proc/self/status Seccomp (filter mode = 2)\n");
    for (int i = 0; probes[i].name; i++) {
        got_sigsys = 0; sigsys_nr = -1; errno = 0;
        long r = syscall(probes[i].nr, probes[i].a1, probes[i].a2, probes[i].a3,
                         probes[i].a4, probes[i].a5, probes[i].a6);
        int e = errno;
        if (got_sigsys)
            printf("%-16s -> SIGSYS trapped (syscall %d)\n", probes[i].name, sigsys_nr);
        else
            printf("%-16s -> ret=%ld errno=%d (%s)\n", probes[i].name, r, e, strerror(e));
        fflush(stdout);
    }

    /* Can we install our own seccomp filter (what browsers do at startup)? */
    struct sock_filter allow[] = {
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = { .len = 1, .filter = allow };
    errno = 0;
    /* need no_new_privs first */
    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    long r = prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
    printf("prctl(PR_SET_SECCOMP, FILTER, allow-all) -> ret=%ld errno=%d (%s)\n",
           r, errno, strerror(errno));
    return 0;
}
