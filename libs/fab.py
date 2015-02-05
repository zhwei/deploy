# -*- coding: utf-8 -*-
# Created by zhangwei@baixing.net on 2015-02-03 15:13

from fabric.contrib import files
from fabric.api import run, settings, cd, env, roles, with_settings

from configs import project_root, hosts
from libs.deploylog import get_logger

deploy_log = get_logger("Deploy")


def with_host(host_string):
    return settings(host_string=host_string)


def git(*args):
    run("git {}".format(" ".join(args)))

def upgrade():
    deploy_log("开始更新代码")

    with cd(project_root):
        git("reset", "--hard")
        git("clean", "-f")
        git("pull", "origin", "master")

    deploy_log("更新完成.")


def service(control="start"):
    deploy_log("开始【】【】服务".format(control, "xxx"))
    pass
    deploy_log("【】【】服务完成".format(control, "xxx"))


def checkout(version):
    git("reset", version, "--hard")

def rollback(version):
    service("stop")
    with cd(project_root):
        checkout(version)
    service("start")


def stop():
    run("killall git")
    service("restart")
    # run("...")
