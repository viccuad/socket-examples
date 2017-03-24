#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>


#define MAXPENDING 5 /* Max connection requests */
#define BUFFSIZE 32
void die(char *mess) { perror(mess); exit(1); }

void handle_client(int sock_fd) {
        char buffer[BUFFSIZE];
        int received = -1;

        /* Receive message */
        if ((received = recv(sock_fd, buffer, BUFFSIZE, 0)) < 0 )
                die("Failed to receive initial bytes from client");

        /* Send bytes and check for more incoming data in loop */
        while (received > 0) {
                /* Send back received data */
                if (send(sock_fd, buffer, received, 0) != received)
                        die("Failed to send bytes to client");
                /* Check for more data */
                if ((received = recv(sock_fd, buffer, BUFFSIZE, 0)) < 0)
                        die("Failed to receive additional bytes from client");
        }
        close(sock_fd);
}


int main(int argc, char *argv[])
{
        int serversock;
        struct sockaddr_in echoserver, echoclient;

        if (argc != 2) {
                fprintf(stderr, "Usage: echoserver <port>\n");
                exit(1);
        }

        /* Create the TCP socket */
        if ( (serversock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0 )
                die("Failed to create socket");

        /* Construct the server sockaddr_in structure */
        memset(&echoserver, 0, sizeof(echoserver));      /* Clear struct */
        echoserver.sin_family = AF_INET;                 /* ip protocol */
        echoserver.sin_addr.s_addr = htonl(INADDR_ANY);  /* incomming addr */
        echoserver.sin_port = htons(atoi(argv[1]));      /* server port */

        /* Bind the server socket */
        if (bind(serversock, (struct sockaddr *) &echoserver, sizeof(echoserver)) < 0)
            die("Failed to bind the server socket");

        /* Listen on the server socket */
        if (listen(serversock, MAXPENDING) < 0)
                die("Failed to listen on server socket");

        /* Run until cancelled */
        while (1) {
                unsigned int clientlen = sizeof(echoclient);
                int clientsock;
                /* Wait for client connection */
                        /* accept() returns a socket pointer for the new socket, and populates the */
                        /* sockadd_in struct pointed to echclient */
                if ((clientsock =
                     accept(serversock, (struct sockaddr *) &echoclient, &clientlen)) < 0)
                        die("Failed to accept client connection");
                fprintf(stdout, "Client connected: %s\n", inet_ntoa(echoclient.sin_addr));
                handle_client(clientsock);
        }
}
