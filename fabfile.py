# Created by zhangwei@baixing.net on 2015-02-04 09:59

from fabric.api import *


def init():
    run("yum install -y python-setuptools")
    run("easy-install2.6 pip")

    run("mkdir -p /webdata/")
    with cd("/webdata/"):
        run("git clone ")

    run("pip install ")