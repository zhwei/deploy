# Created by zhangwei@baixing.net on 2015-02-04 09:59
# Deploy Script for CentOS 6.5

from fabric.api import *

env.hosts = ["root@test.zhangwei.netpupil.cn",]

def init():
    # run("yum install -y python-setuptools git vim tmux")
    # run("easy_install pip")
    # run("mkdir -p /webdata/")
    # with cd("/webdata/"):
    #     run("git clone https://github.com/zhwei/deploy.git")

    # with cd("/webdata/deploy"):
    #     run("pip install -r requirements.txt")

    pass