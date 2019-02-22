# coding:utf8

import requests
from bs4 import BeautifulSoup
import json

from text_constant import TextConstant


class Util(TextConstant):
    def __init__(self):
        TextConstant.__init__(self)
        pass

    @staticmethod
    def request_data(url):
        print("正在发送请求：{}".format(url))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,  like Gecko)'
                          ' Chrome/63.0.3239.132 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=30).content
        return response


class GetContributionCalendar(Util):

    def __init__(self):
        Util.__init__(self)
        self.calendar_color_data = []
        """
        贡献日历的颜色代号

        注意：1.颜色代号从浅到深依次为：null,less,little,some,many,much

        2.使用二维List保存，第一层为一周，第二层为该周每一天，某些情况下可能一周数据不足7天且未用null填充
        """
        self.calendar_count_data = {}
        """
        每一天的贡献数量

        键为日期，值为当天的贡献数量
        """
        self.calendar_count_continuity = 0
        # TODO 尚未解析该数据
        """
        最长连续贡献时间
        """

    def start(self, name):
        """
        :param name: Gitee用户名
        :return:
        """
        print("开始获取贡献日历...")
        url = "https://gitee.com/" + name + "/contribution_calendar?year=" + self.YEAR
        self.__read_data(self.request_data(url))

    def __read_data(self, text):
        print("开始解析数据...")
        text = text.decode("utf8")
        text = text[text.find("html('") + 6:text.find("');")]
        text = text.replace('\\"', '"').replace('\\/', '/').replace("\\n", "\n")

        soup = BeautifulSoup(text, "lxml")

        columns = soup.findAll('div', class_='vertical')
        for column in columns:
            column_data = []
            boxs = column.findAll('div')
            for box in boxs:
                color = box.attrs['class']
                if len(color) <= 1:
                    column_data.append("null")
                else:
                    column_data.append(color[1])
                try:
                    count = box.attrs['data-content']
                    date = box.attrs['date']
                    count = count[:count.find(" 个贡献")]
                    self.calendar_count_data[date] = int(count)
                except KeyError:
                    pass
            self.calendar_color_data.append(column_data)


class GetContributionTimeline(Util):

    def __init__(self):
        Util.__init__(self)
        self.__name = ""
        self.__pager = 1
        self.timeline_datas = []
        """
        贡献时间轴数据
        
        数据采用数组嵌套字典组成，结构：
        [data1, data2, ...]
        
        data = {'action_type': '贡献类型', 'user_id': id, 'user_name': '用户名', 'user_nickname': '用户别名',
         'project_name': '/用户名/项目名', 'create_date': '日期时间'}
        """

        self.project = set()
        """
        活跃的所有项目（数据形如：/作者/项目名）
        """

        self.commits = []
        """
        提交记录（如果一次push多个commit则只能记录最新的两个）
        
        数据采用数组嵌套字典组成，结构：
        [data1, data2, ...]
        
        data = {"author_id": "作者id", "project": "/作者/项目名", "message": "提交说明", "date": "日期"}
        """

        self.created_project = set()
        """
        新建的项目（数据形如：/作者/项目名）
        """

        self.comments = []
        """
        评论数据（包括项目评论、ISSUE评论）
        
        数据采用数组嵌套字典组成，结构：
        [data1, data2, ...]
        
        data = {"author_id": "作者id", "content": "评论内容", "date": "日期", "project": "/作者/项目名"}
        """

        self.issues = []
        """
        ISSUE 数据，仅包含新建的 ISSUE ，更改状态等操作不保存
        
        数据采用数组嵌套字典组成，结构：
        [data1, data2, ...]
        
        data = {"date": "日期", "project": "/作者/项目名", "content": "内容", "title": "标题", "author_id": "作者id"}
        """

    def start(self, name):
        """
        :param name: Gitee用户名
        :return:
        """
        print("开始获取动态详情...")
        self.__name = name
        self.__get_data()

    def __get_data(self):
        url = "https://gitee.com/" + self.__name + "/contribution_timeline?&scope=my&year="\
              + self.YEAR + "&per_page=30&page=" + str(self.__pager)
        json_data = self.request_data(url).decode("utf8")
        self.__read_data(json_data)

    def __read_data(self, data):
        print("正在解析第 {} 页数据...".format(self.__pager))
        json_data = json.loads(data)
        try:
            if json_data["status"] == 404:
                return
        except KeyError:
            pass
        except TypeError:
            pass
        if len(json_data) == 0:
            return
        for contribution in json_data:
            created_date = contribution["created_at"]
            if created_date[:created_date.find("-")] != self.YEAR:
                return
            self.__read_normal_data(contribution)
            action_type = contribution["type"]
            if action_type == "push":
                self.__read_push_data(contribution)
            if action_type == "project":
                self.__read_create_data(contribution)
            if action_type == "note":
                self.__read_comment_data(contribution)
            if action_type == "issue":
                self.__read_issue_data(contribution)

        self.__pager += 1
        self.__get_data()

    def __read_normal_data(self, contribution):
        timeline_data = {}
        user_nickname = contribution["author"]["nickname"]
        user_name = contribution["author"]["username"]
        user_id = contribution["author"]["id"]
        project_name = contribution["project"]["path"]
        created_date = contribution["created_at"]
        action_type = contribution["type"]
        timeline_data["create_date"] = created_date
        timeline_data["action_name"] = action_type
        timeline_data["user_nickname"] = user_nickname
        timeline_data["user_name"] = user_name
        timeline_data["user_id"] = user_id
        timeline_data["project_name"] = project_name
        self.timeline_datas.append(timeline_data)
        self.project.add(project_name)

    def __read_push_data(self, data):
        commit_count = data["commit_count"]
        self.__read_commit_data(data, 0)
        if commit_count > 1:
            self.__read_commit_data(data, 1)

    def __read_commit_data(self, data, index):
        user_id = data["author"]["id"]
        commit_author_id = data["commits"][index]["author"]["id"]
        if user_id == commit_author_id:
            project_name = data["project"]["path"]
            date = data["created_at"]
            commit_message = data["commits"][index]["message"]
            commit = {"author_id": user_id, "project": project_name, "message": commit_message, "date": date}
            self.commits.append(commit)

    def __read_create_data(self, data):
        if data["action"] == "created":
            project = data["project"]["path"]
            self.created_project.add(project)

    def __read_comment_data(self, data):
        content = data["content"]
        date = data["created_at"]
        project = data["project"]["path"]
        author_id = data["author"]["id"]
        comment = {"author_id": author_id, "content": content, "date": date, "project": project}
        self.comments.append(comment)

    def __read_issue_data(self, data):
        action = data["action"]
        '''if action == "closed":
            pass
        if action == "changed_state":
            pass                     '''
        if action == "created":
            date = data["created_at"]
            project = data["project"]["path"]
            content = data["target"]["content"]
            title = data["target"]["title"]
            author_id = data["author"]["id"]
            issue = {"date": date, "project": project, "content": content, "title": title, "author_id": author_id}
            self.issues.append(issue)


class GetProjectLanguage(Util):
    def __init__(self):
        Util.__init__(self)
    # TODO 获取使用项目的语言构成
