# coding:utf8
from draw_picture import DrawPicture
from resolve_data import ResolveData
from save_database import Save2Database

print("Please enter user name:")
name = input()

resolve_data = ResolveData(name)

save_database = Save2Database(resolve_data)

drawer = DrawPicture(resolve_data)
drawer.start()
