# Created by zhangwei@baixing.net on 2015-02-04 13:26


from libs.github import GitHub
from libs.dataobject import DataObject


def get_pulls():
    pulls_data = DataObject("pulls")
    if not pulls_data.all():
        github = GitHub()
        pulls_data.init(github.get_pull_requests("all"))
    return pulls_data.all()