# A Python ssh tunnel 
This program allows an ssh tunnel to be created from the local machine to an SSH server. It was primarily written to allow ssh port forwarding on Windows machines that did not have openssh installed. It supports both forward and reverse ssh port forwarding.

# Building
To build the ssh_tunnel program run build.bat as shown below after ensuring python (3.12 or greater) and poetry are installed.

```
C:\git_repos\ssh_tunnel>build.bat

C:\git_repos\ssh_tunnel>python -m poetry lock
Updating dependencies
Resolving dependencies... (0.9s)

C:\git_repos\ssh_tunnel>python -m poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: ssh-tunnel (0.1.0)

C:\git_repos\ssh_tunnel>python -m poetry run pyflakes ssh_tunnel/ssh_tunnel.py

C:\git_repos\ssh_tunnel>python -m poetry -vvv build
Using virtualenv: C:\Users\pja\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\Local\pypoetry\Cache\virtualenvs\ssh-tunnel-OU_n7vJ3-py3.12
Building ssh-tunnel (0.1.0)
  - Building sdist
Ignoring:
  - Adding: C:\git_repos\ssh_tunnel\ssh_tunnel\__init__.py
  - Adding: C:\git_repos\ssh_tunnel\ssh_tunnel\ssh_tunnel.py
  - Adding: pyproject.toml
  - Adding: README.md
  - Built ssh_tunnel-0.1.0.tar.gz
  - Building wheel
Ignoring:
  - Adding: C:\git_repos\ssh_tunnel\ssh_tunnel\__init__.py
  - Adding: C:\git_repos\ssh_tunnel\ssh_tunnel\ssh_tunnel.py
  - Built ssh_tunnel-0.1.0-py3-none-any.whl

C:\git_repos\ssh_tunnel>
```

This creates the *.whl file in the dist folder which can be installed using pipx.

# Installation
To install the ssh_tunnel program run the following commands after installing python (3.12 or greater) and pipx.

```
python -m pipx ensurepath
python -m pipx install dist/ssh_tunnel-0.1.0-py3-none-any.whl
```

Once installed you must close the terminal (Linux) cmd or powershell window (Windows).

# Usage
Command line help for the ssh_tunnel command is available as shown below.

```C:\Users\auser>ssh_tunnel -h
usage: ssh_tunnel [-h] [-d] [-s SSH_SERVER_ADDRESS] [-p PORT] [-u USERNAME] [-f FORWARD] [-r REVERSE] [-t DEST_HOST]
                  [-k]

Allows the user to create a forward (local -> ssh server) or reverse (ssh server - > local) connection tunnelled down an ssh connection.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debugging.
  -s SSH_SERVER_ADDRESS, --ssh_server_address SSH_SERVER_ADDRESS
                        The SSH server address.
  -p PORT, --port PORT  The TCP port of the SSH server (default=22).
  -u USERNAME, --username USERNAME
                        The username to log into the SSH server with.
  -f FORWARD, --forward FORWARD
                        The local TCP port followed by the remote (ssh server) TCP port to connect to (comma
                        separated). E.G 8080,80 = When a TCP connect is made to the local TCP port 8080 it is
                        connected to the remote (ssh server) port 80.
  -r REVERSE, --reverse REVERSE
                        The remote (ssh server) TCP port followed by the local TCP port to connect to (comma
                        separated). E.G 80,8080 = When a TCP connect is made to the the ssh server port 8080 it is
                        connected to the local port 80.
  -t DEST_HOST, --dest_host DEST_HOST
                        The destination host address (default = localhost)
  -k, --public_key      Show the local ssh public key that will be used to login to the ssh server.

C:\Users\auser>

```