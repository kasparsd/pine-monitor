# AutoSSH Tunnel for Raspberry Pi

Creates an SSH tunnel to a remote server that maps remote port 6622 to local port 22.

## Requirements

	sudo apt-get install autossh

## Setup

1. Symlink `tunnel.service` to `/etc/systemd/system/tunnel.service`:

        ln -s "$PWD/tunnel.service" /etc/systemd/system/tunnel.service

2. Register the service:

        systemctl enable tunnel.service
        systemctl daemon-reload


