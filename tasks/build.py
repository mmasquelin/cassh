from invoke import task


# == Helpers
#
def docker_build(ctx, name):
    """
    Build
    """
    ctx.run("""
        FAIL="\033[0;31m"
        SUCCESS="\033[0;32m"
        COLOR_NONE="\033[0m"

        docker-compose -f src/tests/docker-compose.yml build {name}

        if [[ $? -eq 0 ]]; then
            echo "${{SUCCESS}}---> SUCCESS${{COLOR_NONE}}"
        else
            echo "${{FAIL}}---> FAILURE${{COLOR_NONE}}"
            exit 2
        fi
        """.format(name=name))


# == Build
#
@task
def cassh(ctx):
    """
    Build cassh CLI
    """
    docker_build(ctx=ctx, name='cassh-cli')


@task
def cassh_server(ctx):
    """
    Build cassh-server
    """
    docker_build(ctx=ctx, name='cassh-server')


@task(post=[cassh, cassh_server])
def all(ctx):
    """
    Build cassh & cassh-server docker images
    """
    print("Building all images")