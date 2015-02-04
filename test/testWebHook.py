# Created by zhangwei@baixing.net on 2015-02-03 14:03

import json
import unittest

import requests

from deploy import app
from test import test_data

build_url = lambda x: "http://127.0.0.1:5000{}".format(x)

class TestWebHook(object):

    def testHello(self):

        res = requests.post(
            build_url("/github/webhook"),
            data=json.dumps(test_data.push_data),
            headers=test_data.headers
        )

        print(res.content)
        print(res.text)

if __name__ == '__main__':
    # unittest.main()
    test = TestWebHook()
    test.testHello()