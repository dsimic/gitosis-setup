from fabric.api import env, run, sudo, put

env.use_ssh_config = True


env.gitosis_src_dir = '~/src/gitosis'


def install_deps():
    sudo('apt-get install -y python-setuptools')


def install_gitosis():
    run('mkdir -p %s' % env.gitosis_src_dir)
    run('cd %s; python setup.py install' % env.gitosis_src_dir)
    # create git user
    sudo('adduser --system ' +
         '--shell /bin/sh ' +
         '--gecos ' +
         '--group ' +
         '--disabled-password ' +
         '--home /home/git ' +
         'git'
         )
    # ensure gitosis post-update hook executable
    sudo('chmod 755 /home/git/repositories/gitosis-admin.git/hooks/post-update')


def add_git_pubkey(pubkey_name):
    """
    Call as:
        fab -H host1:user1, host2:user2 add_git_pubkey:pubkey_name
    """
    # add pub key
    put('~/.ssh/%s.pub' % pubkey_name, '/tmp/%s.pub' % pubkey_name)
    sudo('-H -u git gitosis-init < /tmp/%s.pub' % pubkey_name)
