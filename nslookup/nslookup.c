/* Bare nslookup utility with minimal error checking */


#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>       /* hostent struct, gethostbyname() */
#include <netinet/in.h>  /* in_addr structure */
#include <arpa/inet.h>   /* in_addr structure */


int main(int argc, char **argv)
{
        struct hostent *host;    /* host information */
        struct in_addr h_addr;   /* internet address */
        if (argc != 2) {
                fprintf(stderr, "Usage: nslookup <inet_address>\n");
                exit(1);
        }
        if ((host = gethostbyname(argv[1])) == NULL) {
                fprintf(stderr, "nslookup failed on '%s'\n", argv[1]);
                exit(1);
        }
        h_addr.s_addr = *((unsigned long *) host->h_addr_list[0]);
        fprintf(stdout, "%s\n", inet_ntoa(h_addr));
        exit(0);
}
