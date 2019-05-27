# Contrib files

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Systemd](#systemd)
  - [Cassh-server](#cassh-server)
  - [Cassh-cli (sign)](#cassh-cli-sign)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



## Systemd

### Cassh-server

* `cassh-server.service`

SystemD unit files to run `cassh-server` as a service


### Cassh-cli (sign)

Autosign your key everyday with SystemD timers

Files:
* [`cassh_docker.sh`](systemd/cassh_docker.sh): Shell script using `cassh` client dockerized version and sign your key.
* [`cassh_sign.service`](systemd/cassh_sign.service): SystemD unit that is triggered by the SystemD timer.
* [`cassh_sign.timer`](systemd/cassh_sign.timer): SystemD timer.

> 
> Instructions how to install the systemd unit files are in the files header.
>


Screenshots

![Passoword prompt](systemd/imgs/prompt.png)
![Success message](systemd/imgs/success.png)
![Error message](systemd/imgs/error.png)
