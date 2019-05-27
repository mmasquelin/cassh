# E2E Tests

End-to-end tests to validate `cassh-server` and `cassh` cli behaviors.


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview](#overview)
- [Details](#details)
  - [docker-compose](#docker-compose)
    - [Services](#services)
    - [Code](#code)
    - [Config](#config)
  - [BATS tests](#bats-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Overview

End-to-end tests are "simple" `curl` requests sent to a `cassh-server` to validate some scenario that a user / admin would have using Cassh.

Tools:
* [docker-compose](https://docs.docker.com/compose/): to run the needed services (server, db, client, ...) from the docker images that will be published to the Docker Hub.
* [bats](https://github.com/sstephenson/bats): Automated Testing System to write and process `curl` commands and outputs.



## Details

### docker-compose

#### Services

Mentioned in [docker-compose.yml](./docker-compose.yml)

Server:
- `cassh-server` 
- and its `db`

"Runners":
- `cassh-cli`: A container configured to mimic `cassh` cli client as setup on workstation
- `test-runner`: A specific image built to run the BATS tests


These late services are designed to be run through:
```
docker-compose run SERVICE_NAME COMMAND
```


#### Code

For local testing, the source code is "shared" in the containers as binded volumes.


#### Config

The configurations shared in the containers are located in [`src/tests/conf`](conf)



### BATS tests

Files:
- `tests.sh`: The main test file that "orchestrate" the tests
- `tests_*.bats`: Various scenario
- `helpers.bash`: Bash file for shared testing code (functions, variables, ...) See Bats documentation for its usage.


Other helpers:
- [`wait-for-it.sh`](https://github.com/vishnubob/wait-for-it): Pure bash script to test and wait on the availability of a TCP host and port. This script is used to wait for needed services to be up before firing the tests requests :)


Using the BATS syntax, a test statement looks like: 

```
@test "DEPRECATED status URL with username" {
    RESP=$(curl -s -X GET -d 'username=test_user' ${CASSH_URL}/client)
    [ "${RESP}" == 'Error: DEPRECATED option. Update your CASSH >= 1.5.0' ]
}
```

Which results in:

```
---> Run tests
     * Test server
Starting tests_db_1 ... done
Starting tests_cassh-server_1 ... done
wait-for-it.sh: waiting 10 seconds for cassh-server:8080
wait-for-it.sh: cassh-server:8080 is available after 0 seconds
 ✓ SERVER: /ping
 ✓ SERVER: /health
 ✓ DEPRECATED status URL without username
 ✓ DEPRECATED admin status URL without username
 ✓ DEPRECATED status URL with username
 ✓ DEPRECATED status URL with username
 ✓ CLIENT: Status unknown user
 ✓ CLIENT: Add user without username
 ✓ CLIENT: Add user with bad username
 ✓ CLIENT: Add user without realname
 ✓ CLIENT: Add user with no pubkey
 ✓ CLIENT: Add user with bad pubkey
 ✓ CLIENT: Add user
 ✓ CLIENT: Add user named 'all' (should fail)
 ✓ CLIENT: Add user with same username (should fail)
 ✓ CLIENT: Add user with same realname (which is possible)
 ✓ CLIENT: Status pending user
 ✓ CLIENT: Updating user
 ✓ CLIENT: Signing key without username
 ✓ CLIENT: Signing key without realname
 ✓ CLIENT: Signing key with no pubkey
 ✓ CLIENT: Signing key with bad pubkey
 ✓ CLIENT: Signing key when wrong public key
 ✓ CLIENT: Signing key when PENDING status
 ✓ ADMIN: Revoke 'toto'
 ✓ ADMIN: Verify 'toto' status
 ✓ CLIENT: Signing key when revoked
 ✓ ADMIN: Delete 'toto'
 ✓ ADMIN: Active unknown user
 ✓ ADMIN: Verify 'testuser' status
 ✓ ADMIN: Active 'testuser'
 ✓ ADMIN: Re-active testuser
 ✓ CLIENT: Signing key for reactivated testuser
 ✓ ADMIN: Delete 'testuser'

34 tests, 0 failures
```

