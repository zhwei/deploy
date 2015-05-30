# Created by zhangwei@baixing.net on 2015-02-04 09:59
# Deploy Script for CentOS 6.5

from fabric.api import env, local, run, roles

# env.hosts = ["zhwei@jp1.rpvhost.net",]
actions = ['init', 'a']
env.roledefs = {
    'test': ["zhwei@jp1.rpvhost.net",]
}

@roles('test')
def init():
    # run("yum install -y python-setuptools git vim tmux")
    # run("easy_install pip")
    # run("mkdir -p /webdata/")
    # with cd("/webdata/"):
    #     run("git clone https://github.com/zhwei/deploy.git")

    # with cd("/webdata/deploy"):
    #     run("pip install -r requirements.txt")
    # run('ls')
    import time
    start = time.time()
    while start < time.time() + 1000:
        print(start)
        start += 1
        time.sleep(1)

def a():
    local('pwd')
