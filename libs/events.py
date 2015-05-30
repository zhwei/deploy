# -*- coding: utf-8 -*-
# Created by zhangwei@baixing.net on 2015-02-03 14:52

import threading


from libs import fab
from configs import hosts
from libs.utils import Lock, flash_msg
from libs.deploylog import deploy_log


def run_in_thread(func, args, kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()


def with_lock(func):

    def inner(*args, **kwargs):
        lock = Lock("deploy")
        lock.lock()
        func()
        lock.unlock()

    return inner


class Events(object):
    """ PUSH事件

    粗略：记录当前版本号 -> 更新代码 -> 重启相关服务
    """
    def __init__(self, event, deliver_data=None, auto_run=True, *args, **kwargs):
        self.event = event
        self.deliver_data = deliver_data or {}
        if auto_run:
            if not callable(event):
                event = getattr(self, event)
            run_in_thread(event, args=args, kwargs=kwargs)

    @with_lock
    def push(self):
        """ push事件

        deliver_data:
            - before: 之前版本
            - after:　更新后的版本号
            - pusher: 更新者
            - 其他见https://developer.github.com/v3/activity/events/types/#pushevent
        """
        for host in hosts:
            deploy_log("开始更新 {}".format(host))
            with fab.with_host(host):
                fab.upgrade()
                fab.service()
            deploy_log("{} 更新完成.".format(host))
            deploy_log("*"*10)

    @with_lock
    def rollback(self, version):
        for host in hosts:
            deploy_log("开始回滚 {}".format(host))
            with fab.with_host(host):
                fab.rollback(version)
            deploy_log("{} 回滚完成.".format(host))
            deploy_log("*"*10)
