#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

extern void work_init(); // Provided by the workload library
extern void work_run();  // Provided by the workload library

#define PAGE_SIZE_2MB (2 * 1024 * 1024)  // 2MB size for large pages
#define NUM_PAGES 8  // Number of large pages to allocate

// Addresses to allocate for the large pages
unsigned long large_page_addresses[NUM_PAGES] = {
    536870912,
    538968064,
    541065216,
    543162368,
    545259520,
    547356672,
    549453824,
    551550976
};

// Function to allocate large pages at specific addresses
void allocate_large_pages(int num_pages) {
    // Allocate a contiguous block of memory for the large pages
    void *addr = mmap((void *)large_page_addresses[0], num_pages * PAGE_SIZE_2MB, PROT_READ | PROT_WRITE,
                      MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (addr == MAP_FAILED) {
        perror("Error allocating memory");
        exit(1);
    }

    printf("Allocated %d large pages at addresses:\n", num_pages);
    for (int i = 0; i < num_pages; i++) {
        printf("Address: 0x%lx\n", large_page_addresses[i]);
    }
}

int main(void) {
    printf("Initializing workload...\n");
    work_init();

    // Allocate large pages at specified addresses
    printf("Allocating large pages...\n");
    allocate_large_pages(NUM_PAGES);

    printf("Running workload...\n");
    work_run();

    return 0;
}


