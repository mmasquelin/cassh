"""
Invoke tasks definition for CASSH project
"""
from invoke import task

CONF = {
    'client': {
        'image_dir': 'utils/pylint/client',
        'image_name': 'leboncoin/cassh-pylint',
        'src_dir': 'src/client/cassh'
    },
    'server': {
        'image_dir': 'utils/pylint/server',
        'image_name': 'leboncoin/cassh-server-pylint',
        'src_dir': 'src/server'
    }
}

# == Helpers
#
def lint(ctx, image_name, image_dir, src_dir):
    """
    Run pylint with project's image
    """
    ctx.run("""
        RED="\033[0;31m"
        GREEN="\033[0;32m"
        YELLOW="\033[0;33m"
        COLOR_NONE="\033[0m"

        if [[ -z "$(docker images -q {image_name} 2> /dev/null)" ]]; then
            echo ""
            echo "${{YELLOW}}Image {image_name} not found !${{COLOR_NONE}}"
            echo "${{YELLOW}}Building image${{COLOR_NONE}}"
            echo ""

            docker build -t {image_name} {image_dir}
            if [[ $? -eq 0 ]]; then
                echo "${{YELLOW}}Done${{COLOR_NONE}}"
            else
                echo "${{RED}}FAILED${{COLOR_NONE}}"
                exit 2
            fi
        fi

        echo "${{GREEN}}===> Running PyLint${{COLOR_NONE}}"
        docker run --rm -it \
                    --volume=${{PWD}}:${{PWD}} \
                    --workdir=${{PWD}} \
                    {image_name} \
                    "pylint {src_dir}"
        if [[ $? -eq 0 ]]; then
            echo "${{YELLOW}}Done${{COLOR_NONE}}"
        else
            echo "${{RED}}FAILED${{COLOR_NONE}}"
            exit 2
        fi
        """.format(image_name=image_name, image_dir=image_dir, src_dir=src_dir),
            pty=True)


# == Tasks
#
@task
def lint_client(ctx):
    """
    pylint cassh
    """
    lint(ctx=ctx,
         image_name=CONF['client']['image_name'],
         image_dir=CONF['client']['image_dir'],
         src_dir=CONF['client']['src_dir'])

@task
def lint_server(ctx):
    """
    pylint cassh-server
    """
    lint(ctx=ctx,
         image_name=CONF['server']['image_name'],
         image_dir=CONF['server']['image_dir'],
         src_dir=CONF['server']['src_dir'])

@task
def e2e(ctx):
    """
    End to End tests of CASSH-server and CASSH cli
    """
    ctx.run("""
    src/tests/tests.sh
    """, pty=True)
