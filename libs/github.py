# Created by zhangwei@baixing.net on 2015-02-03 16:14

import json

import requests

from configs import github_token
from libs.dataobject import DataObject


URL_BASE = "https://api.github.com/repos/baixing/che/"


class GitHub(object):

    def _get(self, api, *args):
        url = URL_BASE + api
        url = "{}{}access_token={}".format(
            url, "?" if "?" not in url else "&", github_token)
        return json.loads(requests.get(url).text)

    def get_pull_requests(self, status="open"):
        return self._get("pulls?state={}".format(status))
