from fabric.contrib.files import exists
from fabric.api import env, run, sudo, put

env.use_ssh_config = True
env['sudo_prefix'] += '-H '
env.gitosis_src_dir = './src/gitosis'


def install_deps():
    sudo('apt-get install -y python-setuptools')


def install_gitosis():
    if not exists(env.gitosis_src_dir):
        run('cd; mkdir -p %s' % env.gitosis_src_dir)
        run('cd; cd %s/../; git clone https://github.com/tv42/gitosis.git' %
            env.gitosis_src_dir)
        sudo('cd; cd %s; python setup.py install --record files.txt' %
             env.gitosis_src_dir)
    # create git user
    if not exists('/home/git'):
        sudo('adduser --system ' +
             '--shell /bin/sh ' +
             '--gecos ' +
             '--group ' +
             '--disabled-password ' +
             '--home /home/git ' +
             'git'
             )


def pubkey(pubkey_name):
    """
    Call as:
        fab -H host1:user1, host2:user2 add_git_pubkey:pubkey_name
    """
    # add pub key
    put('~/.ssh/%s.pub' % pubkey_name, '/tmp/%s.pub' % pubkey_name)
    sudo('gitosis-init < /tmp/%s.pub' % pubkey_name, user="git")
    # ensure gitosis post-update hook executable
    sudo('chmod 755 /home/git/repositories/gitosis-admin.git/hooks/post-update')


def teardown():
    pass


def deploy():
    install_deps()
    install_gitosis()
