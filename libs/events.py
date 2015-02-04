# -*- coding: utf-8 -*-
# Created by zhangwei@baixing.net on 2015-02-03 14:52


from libs import fabfile


class Events(object):
    """ PUSH事件

    粗略：记录当前版本号 -> 更新代码 -> 重启相关服务
    """

    def __init__(self, event, deliver_data):
        self.event = event

        self.deliver_data = deliver_data

    def push(self):
        """ push事件

        deliver_data:
            - before: 之前版本
            - after:　更新后的版本号
            - pusher: 更新者
            - 其他见https://developer.github.com/v3/activity/events/types/#pushevent
        """
        fabfile.deploy()
