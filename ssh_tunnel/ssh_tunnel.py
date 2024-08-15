#!/usr/bin/env python3

import argparse

from   time import sleep
from   p3lib.uio import UIO
from   p3lib.helper import logTraceBack
from   p3lib.ssh import SSH, SSHTunnelManager

class SSHForwarder(object):

    def __init__(self, uio, options):
        """@brief Constructor
           @param uio A UIO instance handling user input and output (E.G stdin/stdout or a GUI)
           @param options An instance of the OptionParser command line options."""
        self._uio = uio
        self._options = options

    def info(self, msg):
        """"@brief Display an info level message.
            @param msg The message to be displayed."""
        if self._uio:
            self._uio.info(msg)

    def _getPorts(self, portStr):
        """@brief Extract two TCP port from the comma separated string.
           @param portStr The comma separated port string."""
        port0 = None
        port1 = None
        elems = portStr.split(',')
        if len(elems) == 2:
            try:
                port0 = int(elems[0])
                port1 = int(elems[1])
            except ValueError:
                pass
        
        if port0 is None or port1 is None:
            raise Exception(f"Unable to extract TCP port numbers from {portStr}")
        
        return (port0, port1)

    def _waitForCtrlC(self):
        """@brief Wait for the user to press CTRL C."""
        self.info("Press Ctrl C to close ssh tunnel.")
        while True:
            sleep(0.2)

    def connect(self):
        """@brief Connect to the SSH server."""
        ssh = None
        sshTunnelManager = None
        try:
            ssh = SSH(self._options.ssh_server_address,
                      self._options.username,
                      port = self._options.port,
                      uio = self._uio)
            ssh.connect()
            self.info(f"Connected to {self._options.username}@{self._options.ssh_server_address}:{self._options.port}")
            sshTunnelManager = SSHTunnelManager(self._uio, ssh, True)
            if self._options.forward:
                localPort, remotePort = self._getPorts(self._options.forward)
                sshTunnelManager.startFwdSSHTunnel(localPort, self._options.dest_host, remotePort)
                self._waitForCtrlC()

            elif self._options.reverse:
                remotePort, localPort = self._getPorts(self._options.reverse)
                sshTunnelManager.startRevSSHTunnel(localPort, self._options.dest_host, remotePort)
                self._waitForCtrlC()

            else:
                raise Exception("Either the -f/--forward or -r/--reverse command line arguments must be used.")


        finally:
            if ssh:
                ssh.close()
                self.info("Disconnected SSH connection.")
                ssh = None

    def showPublicKey(self):
        """@brief Show the users public key file and contents."""
        publicKeyFileList = SSH.GetPublicKeyFileList()
        lines = None
        publicKey = None
        for publicKeyFile in publicKeyFileList:
            self.info(f"Public Key File: {publicKeyFile}")
            
            with open(publicKeyFile, 'r') as fd:
                lines = fd.readlines()
        if lines and len(lines) > 0:        
            publicKey = lines[0]
            publicKey = publicKey.strip('\n')
            publicKey = publicKey.strip('\r')
            publicKey = publicKey.strip()
        if not publicKey:
            self._uio.error("No public key data found.")
        else:
            self.info(f"Public Key:      {publicKey}")


def main():
    """@brief Program entry point"""
    uio = UIO()

    try:
        parser = argparse.ArgumentParser(description="Allows the user to create a forward (local -> ssh server) or reverse (ssh server - > local) connection tunnelled down an ssh connection.", formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--debug",                action='store_true', help="Enable debugging.")
        parser.add_argument("-s", "--ssh_server_address",   help="The SSH server address.", default=None)
        parser.add_argument("-p", "--port",                 type=int, help="The TCP port of the SSH server (default=22).", default=22)
        parser.add_argument("-u", "--username",             help="The username to log into the SSH server with.", default=None)
        parser.add_argument("-f", "--forward",              help="The local TCP port followed by the remote (ssh server) TCP port to connect to (comma separated). E.G 8080,80 = When a TCP connect is made to the local TCP port 8080 it is connected to the remote (ssh server) port 80.", default=None)
        parser.add_argument("-r", "--reverse",              help="The remote (ssh server) TCP port followed by the local TCP port to connect to (comma separated). E.G 8080,80 = When a TCP connect is made to the the ssh server port 8080 it is connected to the local port 80.", default=None)
        parser.add_argument("-t", "--dest_host",            help="The destination host address (default = localhost)", default='localhost')
        parser.add_argument("-k", "--public_key",           action='store_true', help="Show the local ssh public key that will be used to login to the ssh server.")

        options = parser.parse_args()

        uio.enableDebug(options.debug)
        sshForwarder = SSHForwarder(uio, options)

        if options.public_key:
            sshForwarder.showPublicKey()

        else:
            sshForwarder.connect()

    #If the program throws a system exit exception
    except SystemExit:
        pass
    #Don't print error information if CTRL C pressed
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        logTraceBack(uio)

        if options.debug:
            raise
        else:
            uio.error(str(ex))

if __name__== '__main__':
    main()
