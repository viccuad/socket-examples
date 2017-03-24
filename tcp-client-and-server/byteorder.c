#include <stdio.h>
#include <stdlib.h>

/* See: */
/* https://www.tutorialspoint.com/unix_sockets/network_byte_orders.htm */

int main() {
        union {
                short s;
                char c[sizeof(short)];
        }un;

        un.s = 0x0102;

        if (sizeof(short) == 2) {
                if (un.c[0] == 1 && un.c[1] == 2)
                        printf("big-endian\n");

                else if (un.c[0] == 2 && un.c[1] == 1)
                        printf("little-endian\n");

                else
                        printf("unknown\n");
        }
        else {
                printf("sizeof(short) = %d\n", sizeof(short));
        }

        exit(0);
}
