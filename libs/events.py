# -*- coding: utf-8 -*-
# Created by zhangwei@baixing.net on 2015-02-03 14:52

from libs import fab
from configs import hosts
from libs.worker import worker_instance


class Events(object):
    """ PUSH事件

    粗略：记录当前版本号 -> 更新代码 -> 重启相关服务
    """
    def __init__(self, event, deliver_data=None, auto_run=True, *args, **kwargs):
        self.event = event
        self.deliver_data = deliver_data or {}
        if auto_run:
            self.thread_run(event)

    def thread_run(self, func, *args, **kwargs):
        if not callable(func):
            func = getattr(self, func)
        worker_instance.run(func, *args, **kwargs)

    def push(self):
        """ push事件

        deliver_data:
            - before: 之前版本
            - after:　更新后的版本号
            - pusher: 更新者
            - 其他见https://developer.github.com/v3/activity/events/types/#pushevent
        """
        for host in hosts:
            with fab.with_host(host):
                fab.upgrade()
                fab.service()

    def rollback(self, version):
        for host in hosts:
            with fab.with_host(host):
                fab.rollback(version)
