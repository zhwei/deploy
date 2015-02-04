# Created by zhangwei@baixing.net on 2015-02-03 17:59

from collections import defaultdict

class DataObject(object):

    __data = defaultdict(list)
    limit = 30

    def __init__(self, key):
        self.key = key

    def init(self, data_list):
        self.__data[self.key] = data_list[:30]

    def all(self):
        return self.__data[self.key]

    def push(self, data):
        self.__data[self.key].insert(0, data)
        if len(self.__data[self.key]) > self.limit:
            self.__data[self.key].pop()