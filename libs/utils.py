# Created by zhangwei@baixing.net on 2015-02-04 13:26

import os

from libs.github import GitHub
from libs.dataobject import DataObject


def get_pulls():
    pulls_data = DataObject("pulls")
    if not pulls_data.all():
        github = GitHub()
        pulls_data.init(github.get_pull_requests("all"))
    return pulls_data.all()


def flash_msg(type, msg):
    data = DataObject("msgs")
    return data.push((type, msg))


class Lock(object):

    def __init__(self, key):
        self.lock_file = "/tmp/deploy-{}.lock".format(key)

    def lock(self):
        if os.path.isfile(self.lock_file):
            return False
        with open(self.lock_file, "w") as fi:
            fi.write("deploy lock")
        return True

    def unlock(self):
        if os.path.isfile(self.lock_file):
            os.remove(self.lock_file)