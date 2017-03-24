#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define BUFFSIZE 255

void die(char *mess) {perror(mess); exit(1); }

int main(int argc, char *argv[])
{
        int sockfd;
        struct sockaddr_in echoserver;
        struct sockaddr_in echoclient;
        char buffer[BUFFSIZE];
        unsigned int echolen, clientlen, serverlen;
        int received = 0;

        if (argc != 2) {
                fprintf(stderr, "Usage: %s <port>\n", argv[0]);
                exit(1);
        }

        // create UDP socket
        if ((sockfd = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
                die("Failed to create socket");

        // construct the server sockaddr_in struct
        memset(&echoserver, 0, sizeof(echoserver));
        echoserver.sin_port = htons(atoi(argv[1]));      // server port
        echoserver.sin_family = AF_INET;                 // internet ip
        echoserver.sin_addr.s_addr = htonl(INADDR_ANY);  // any ip address

        // bind the socket
        serverlen = sizeof(echoserver);
        if (bind(sockfd, (struct sockaddr *) &echoserver, serverlen) < 0)
                die("Failed to bind server socket");

        while (1) {
                // receive a message from the client
                clientlen = sizeof(echoclient);
                if ( (received = recvfrom(sockfd, buffer, BUFFSIZE, 0,
                                          (struct sockaddr *) &echoclient,
                                          &clientlen)) < 0 )
                        die("Failed to receive message");

                fprintf(stderr, "Client connected: %s\n",
                        inet_ntoa(echoclient.sin_addr));

                // send the message back to the client
                if (sendto(sockfd, buffer, BUFFSIZE, 0, (struct sockaddr *)
                           &echoclient, sizeof(echoclient)) != received )
                        die("Mismatch in number of echo'd bytes");
        }
        // never reached
}
