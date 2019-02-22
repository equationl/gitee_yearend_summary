# coding:utf8


class TextConstant:
    # TODO 尚未写完
    """
    该类用于储存字符常量
    """
    def __init__(self):
        self.YEAR = "2018"
        """
        
        """
        self.CALENDER_SUMMARY = {"less": self.YEAR+"年是不是又摸鱼了？全是白的！",
                                 "little": self.YEAR+"，又是本本分分的一年哦~",
                                 "some": self.YEAR+"，工作压力有点大了吧？",
                                 "many": "今天，你还有头发吗？",
                                 "much": "IT狂魔！恐怖如斯！膜拜！膜拜！"}

        self.CALENDER_DESCRIPTION = "● {YEAR}年有{DAY_ALL}天，\n    你有{DAY_ACTION}天在{ACTION}，" \
                                    "\n    最长连续{DAY_CONTINUITY}天提交代码，\n    你成功超越了{RATIO}%的人"
