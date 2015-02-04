# -*- coding: utf-8 -*-
# Created by zhangwei@baixing.net on 2015-02-03 15:13

from fabric.api import run, settings, cd, env, roles, with_settings

from configs import project_root, hosts

env.hosts = hosts


def wrap_configs(func):
    def inner(*args, **kwargs):
        for host in hosts:
            with settings(host_string=host):
                func(*args, **kwargs)
    return inner


@wrap_configs
def deploy():
    with cd(project_root):
        run("git reset --hard && git clean -f")
        run("git pull origin master")