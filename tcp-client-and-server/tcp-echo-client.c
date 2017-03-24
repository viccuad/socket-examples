#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>


#define BUFFSIZE 32
void die(char *mess) { perror(mess); exit(1); }

int main(int argc, char *argv[])
{
        int sock_fd;
        struct sockaddr_in echoserver; /* http://www.retran.com/beej/sockaddr_inman.html */
        char buffer[BUFFSIZE];
        unsigned int echolen;
        unsigned int received = 0;

        if (argc != 4) {
                fprintf(stderr, "Usage: TCPecho <server_ip> <word> <port>\n");
                exit(1);
        }

        /* Create the TCP socket */
        if ((sock_fd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
                die("failed to create socket");

        /* Construct the server sockaddr_in struct with information of where do
           we want to connect */
        memset(&echoserver, 0, sizeof(echoserver));        /* clear struct */
        echoserver.sin_family = AF_INET;                   /* IP protocol */
        echoserver.sin_addr.s_addr = inet_addr(argv[1]);   /* IP address */
        echoserver.sin_port = htons(atoi(argv[3]));        /* server port */

        /* Establish connection */
        if (connect(sock_fd, (struct sockaddr *) &echoserver,
                    sizeof(echoserver)) < 0)
                die("Failed to connect with server");

        /* Send the word to the server */
        echolen = strlen(argv[2]);
        if (send(sock_fd, argv[2], echolen, 0) != echolen)
                die("Mismatch in number of sent bytes");

        /* Receive the word back from the server */
        fprintf(stdout, "Received: ");
        while (received < echolen) {
                int bytes = 0;
                if ((bytes = recv(sock_fd, buffer, BUFFSIZE -1, 0)) < 1)
                        die("Failed to receive bytes from server");
                received += bytes;
                buffer[bytes] = '\0';
                fprintf(stdout, "%s", buffer);
        }

        return 0;
}
