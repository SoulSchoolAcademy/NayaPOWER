/* mmapprobe.c — is MAP_SHARED mmap denied by the container?
 * Tests each mapping kind and prints the errno. Run 3x to check consistency.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

static void t(const char *name, void *r) {
    if (r == MAP_FAILED)
        printf("%-42s -> FAIL errno=%d (%s)\n", name, errno, strerror(errno));
    else {
        printf("%-42s -> OK %p\n", name, r);
        munmap(r, 4096);
    }
    fflush(stdout);
}

int main(void) {
    int mfd = memfd_create("probe", MFD_CLOEXEC | MFD_ALLOW_SEALING);
    printf("memfd_create -> %d errno=%d\n", mfd, errno);
    if (mfd >= 0) { ftruncate(mfd, 4096); }
    t("memfd MAP_SHARED PROT_READ|WRITE", mfd >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, mfd, 0) : MAP_FAILED);
    t("memfd MAP_PRIVATE PROT_READ|WRITE", mfd >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE, mfd, 0) : MAP_FAILED);
    t("anon MAP_SHARED", mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0));
    t("anon MAP_PRIVATE", mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0));
    int f1 = open("/tmp/mmapprobe.bin", O_RDWR|O_CREAT|O_TRUNC, 0600);
    if (f1 >= 0) { ftruncate(f1, 4096); }
    t("/tmp file MAP_SHARED", f1 >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, f1, 0) : MAP_FAILED);
    t("/tmp file MAP_PRIVATE", f1 >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE, f1, 0) : MAP_FAILED);
    int f2 = open("/dev/shm/mmapprobe.bin", O_RDWR|O_CREAT|O_TRUNC, 0600);
    if (f2 >= 0) { ftruncate(f2, 4096); }
    t("/dev/shm file MAP_SHARED", f2 >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, f2, 0) : MAP_FAILED);
    t("/dev/shm file MAP_PRIVATE", f2 >= 0 ? mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE, f2, 0) : MAP_FAILED);
    if (f1 >= 0) close(f1);
    if (f2 >= 0) close(f2);
    if (mfd >= 0) close(mfd);
    return 0;
}
