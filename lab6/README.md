# Lab 6:
## Implementation of PKI-Based Authentication

This lab implements the public key registration of a server with a Certificate athourity, and the a clients verification of that server using the RSA signature from the CA.

The ca, client, and server are implemented in the files `ca.py`, `client.py`, and `server.py`.
This folder also includes files for each of the temporary DES keys, and the session key, as they are hard coded, however, it would be easy to generate them at runtime.
The RSA keys for the CA and server are, however, generated at runtime, and the public key for the CA is written to a file giving access to both the server and client.

Validation occurs at three points in the protocol, when the server provides the certificate to the client, the client can then validate that message using the public knowledge of the ids of the server and CA, as well as the publicly avaliable CA public key.
Then, when data is requested and recieved by the client, both the server and client use the lifetime established for the session key to validate their messages.

## Running

This projects are implemented using Python3, and the DES and RSA packages provided in external python libraries.
They make it very simple to generate, encrypt, decrypt, sign, and validate each of the messages.

These scripts must be run in a specific order to work properly

First, run the CA script, which waits for connection from the server and must be provided a port to wait on:

`python3 ca.py [ca port]`

Then, run the server to connect to the CA.
It must be provided a port to acccess the CA, as well as a port to listen on itself.

`python3 server.py [server port] [ca port]`

After running, the server will recieve a certificate from the CA, and the CA program will exit after writing its public key to a file
The server continues to wait for connection from the client.
The client should be provided the port for the server.

`python3 client.py [server port]`

An example print out screen is provided in this folder.
