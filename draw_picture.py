# coding:utf8

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class DrawPicture:
    def __init__(self, resolve_data_obj):
        self.RECTANGLE_START_X = 10
        self.RECTANGLE_START_Y = 350
        self.RECTANGLE_SIZE = 18
        self.RECTANGLE_SPACING = 2
        self.__resolve_data = resolve_data_obj
        self.__img = Image.open("./BG.png")
        self.__draw = ImageDraw.Draw(self.__img)

    def __draw__name(self):
        font = ImageFont.truetype("./STXINWEI.TTF", 40, encoding="unic")
        text1 = self.__resolve_data.name
        self.__draw.text([560, 320], text1, "black", font)

    def __draw_calender(self):
        for i in range(1, 56):
            x = self.RECTANGLE_START_X+self.RECTANGLE_SIZE*i+self.RECTANGLE_SPACING
            for j in range(1, 8):
                self.__draw.rectangle((x+self.RECTANGLE_SPACING,
                                       self.RECTANGLE_START_Y+self.RECTANGLE_SIZE*j+self.RECTANGLE_SPACING,
                                       x+self.RECTANGLE_SIZE,
                                       self.RECTANGLE_START_Y+self.RECTANGLE_SIZE*j+self.RECTANGLE_SIZE),
                                      self.__resolve_data.get_calendar_color_code(i-1, j-1))

    def __draw_text_calender(self):
        font = ImageFont.truetype("./STXINWEI.TTF", 40, encoding="unic")
        text1 = self.__resolve_data.get_calender_summary()
        text2 = self.__resolve_data.get_calender_description()
        self.__draw.text([330, 600], text1, "black", font)
        self.__draw.text([360, 700], text2, "black", font)

    def __draw_text_create_project(self):
        font = ImageFont.truetype("./STXINWEI.TTF", 40, encoding="unic")
        text1 = self.__resolve_data.get_create_project_description()
        self.__draw.text([150, 880], text1, "black", font)

    def __draw_text_contribution(self):
        font = ImageFont.truetype("./STXINWEI.TTF", 40, encoding="unic")
        text1 = self.__resolve_data.get_contribution_description()
        self.__draw.text([360, 1100], text1, "black", font)

    def __draw_text_most_contribution_date(self):
        font = ImageFont.truetype("./STXINWEI.TTF", 40, encoding="unic")
        text1 = self.__resolve_data.get_most_contribution_date_description()
        text2 = self.__resolve_data.get_most_contribution_date_summary()
        self.__draw.text([150, 1450], text1, "black", font)
        self.__draw.text([200, 1620], text2, "black", font)

    def start(self):
        print("开始画图...")
        self.__draw__name()
        self.__draw_calender()
        self.__draw_text_calender()
        self.__draw_text_create_project()
        self.__draw_text_contribution()
        self.__draw_text_most_contribution_date()
        # FIXME 正式上线时应该改成保存而非直接显示
        self.__img.show()
