# coding:utf8

import calendar
from collections import Counter

from get_contribution import GetContributionCalendar, GetContributionTimeline
from text_constant import TextConstant


class ResolveData(TextConstant):
    def __init__(self, name):
        TextConstant.__init__(self)
        self.calendar = GetContributionCalendar()
        self.timeline = GetContributionTimeline()
        self.calendar.start(name)
        self.timeline.start(name)
        self.name = name
        self.color_describe_sort = []

    def get_calendar_color_code(self, x, y):
        color_code = {"null": "#fff", "less": "#eee", "little": "#d6e685", "some": "#8cc665", "many": "#44a3340",
                      "much": "1e6823"}
        try:
            color = self.calendar.calendar_color_data[x][y]
        except IndexError:
            color = "null"
        return color_code[color]

    def get_calender_summary(self):
        print("获取贡献总结...")
        result = {}
        for item in self.calendar.calendar_color_data:
            nums = Counter(item)
            result = dict(Counter(result) + nums)
        if result["less"] < 251/3:
            # 一年的工作日大概有251天，假设每3天提交一次
            result["less"] /= 1.5
            # 留点面子吧
        result = sorted(result.items(), key=lambda item:item[1], reverse=True)
        self.color_describe_sort = result
        return self.CALENDER_SUMMARY[self.color_describe_sort[0][0]]

    def get_calender_description(self):
        print("获取贡献日历描述...")
        month_range = calendar.monthrange(int(self.YEAR), 2)
        year_of_day = "365" if month_range[1] == 28 else "366"
        if self.color_describe_sort[0][0] == "less":
            day_action = self.color_describe_sort[0][1]
            action = "摸鱼"
        else:
            day_action = 0
            for item in self.color_describe_sort:
                if item[0] != "less" or item[0] != "null":
                    day_action += item[1]
            action = "努力coding"

        parameter = {"YEAR": self.YEAR, "DAY_ALL": year_of_day,
                     "DAY_ACTION": day_action, "ACTION": action,
                     "DAY_CONTINUITY": self.calendar.calendar_count_continuity, "RATIO": "0"}
        return self.CALENDER_DESCRIPTION.format(**parameter)

    def get_contribution_description(self):
        # TODO
        print("获取贡献描述...")
        return '● 2018年你最关注的项目是：\n    “绅士图下载器”\n    你通过\n    提交10086个issue的方式\n' \
               '    积极为开源世界贡献自己的力量\n    你在issue中提到最多的词是 \n    “求番号”'

    def get_create_project_description(self):
        # TODO
        print("获取新建项目情况...")
        return '●2018年，你又开了一个叫\n    “快速下载图片” 的新坑\n    2018，你似乎乐于挖坑却不会填，\n' \
               '    新项目只提交了0次'

    def get_most_contribution_date_description(self):
        # TODO
        print("获取最多贡献描述...")
        return '● 2018年02月04日这天\n    你很兴奋，半夜4点了还在活跃\n    提交了 88 个issue\n    fork了20个项目'

    def get_most_contribution_date_summary(self):
        # TODO
        print("获取最多贡献日期描述...")
        return '● 那天是情人节，别人有女朋友，你有代码'
