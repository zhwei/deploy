# Created by zhangwei@baixing.net on 2015-02-04 13:26


import os
import sys
import time

import tailer


TMP_PATH = '/tmp/FabricWebWorker/'
if not os.path.isdir(TMP_PATH):
    os.makedirs(TMP_PATH)


class Logger(object):

    bak_file_count = {}

    def __init__(self, item, level='out'):
        self.terminal = sys.stdout
        self.path = Logger._log_path(item)
        self.level = level

    def open_file(self):
        return open(self.path, 'a' if os.path.isfile(self.path) else 'w')

    def cur_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def write(self, message):
        self.terminal.write(message)
        message = message.strip('\n')
        if not message:
            return
        with self.open_file() as fi:
            fi.write('[{}]{}: {}\n'.format(self.cur_time(), self.level, message))

    def flush(self):
        pass

    log = write

    def clear(self):
        os.unlink(self.path)

    @staticmethod
    def _log_path(item):
        path = TMP_PATH + 'logs/'
        if not os.path.isdir(path):
            os.makedirs(path)

        return path + item.unit_name

    @staticmethod
    def redirect_to_file(item):
        sys.stdout = Logger(item)
        sys.stderr = Logger(item, 'err')

    @staticmethod
    def tail_log_file(item, lines=1000):
        path = Logger._log_path(item)

        if not os.path.isfile(path):
            return 'No Log'

        with open(path) as fi:
            return '\n'.join(tailer.tail(fi, lines))


class Lock(object):
    """ file lock """

    _dir = TMP_PATH + 'lock/'
    if not os.path.isdir(_dir):
        os.makedirs(_dir)

    def __init__(self, item):
        self.name = item.unit_name
        self.lock_file = self._dir + str(self.name)

    def lock(self, msg='lock'):
        if os.path.isfile(self.lock_file):
            raise Exception('locked before, please unlock')

        with open(self.lock_file, "w") as fi:
            fi.write(str(msg))
        return True

    def unlock(self):
        if not os.path.isfile(self.lock_file):
            return False
        os.remove(self.lock_file)
        return True

    def status(self):
        if not os.path.isfile(self.lock_file):
            return False
        with open(self.lock_file) as fi:
            return fi.read()
