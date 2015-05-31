# Created by zhangwei@baixing.net on 2015-02-04 10:36
# Create Deploy Log

import os
import sys
import time

import tailer

import configs


def get_log_path(project, function):
    log_path = configs.TEMP_PATH + 'logs/'
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    return log_path + '{}.{}'.format(project, function)


class Logger(object):

    bak_file_count = {}

    def __init__(self, project, function):
        self.terminal = sys.stdout
        self.mark = '{}.{}'.format(project, function)
        self.path = get_log_path(project, function)

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
            fi.write('[{}] {}\n'.format(self.cur_time(), message))

    def flush(self):
        with self.open_file() as fi:
            fi.write('Flush at {}\n'.format(self.cur_time()))

    log = write



def redirect_stdout_to_file(project, function):
    sys.stdout = Logger(project, function)


def tail_log_file(project, function, lines=1000):
    path = get_log_path(project, function)

    if not os.path.isfile(path):
        return None

    with open(path) as fi:
        return '\n'.join(tailer.tail(fi, lines))
